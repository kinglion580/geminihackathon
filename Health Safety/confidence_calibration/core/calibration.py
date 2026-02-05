"""
Calibration Methods

Implements Temperature Scaling and Isotonic Regression for confidence calibration.
"""

import numpy as np
from scipy.optimize import minimize
from sklearn.isotonic import IsotonicRegression
from typing import Optional, Dict, Tuple
from .metrics import calculate_all_metrics, get_calibration_bins_data


class TemperatureScaling:
    """
    Temperature Scaling calibration method.
    
    Applies a single scalar parameter (temperature) to logits to improve calibration.
    
    Reference:
        Guo et al. (2017): "On Calibration of Modern Neural Networks"
    """
    
    def __init__(self):
        self.temperature = 1.0
        self.is_fitted = False
    
    def fit(self, logits: np.ndarray, y_true: np.ndarray, method: str = "nll") -> float:
        """
        Learn optimal temperature parameter.
        
        Args:
            logits: Raw model outputs (before softmax)
            y_true: Ground truth labels
            method: Optimization objective ('nll' or 'ece')
            
        Returns:
            Optimal temperature value
        """
        if method == "nll":
            objective = self._nll_loss
        elif method == "ece":
            objective = self._ece_loss
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Optimize temperature
        result = minimize(
            lambda T: objective(logits, y_true, T[0]),
            x0=np.array([1.0]),
            method="Nelder-Mead",
            options={"maxiter": 1000}
        )
        
        self.temperature = result.x[0]
        self.is_fitted = True
        
        return self.temperature
    
    def transform(self, logits: np.ndarray) -> np.ndarray:
        """
        Apply temperature scaling to logits.
        
        Args:
            logits: Raw model outputs
            
        Returns:
            Calibrated confidence scores
        """
        if not self.is_fitted:
            raise ValueError("TemperatureScaling must be fitted before transform")
        
        # Apply temperature scaling
        scaled_logits = logits / self.temperature
        
        # Convert to probabilities (softmax for multi-class, sigmoid for binary)
        if scaled_logits.ndim == 1 or scaled_logits.shape[1] == 1:
            # Binary classification
            confidences = self._sigmoid(scaled_logits)
        else:
            # Multi-class classification
            confidences = self._softmax(scaled_logits)
        
        return confidences
    
    def fit_transform(self, logits: np.ndarray, y_true: np.ndarray, method: str = "nll") -> np.ndarray:
        """
        Fit temperature and transform in one step.
        
        Args:
            logits: Raw model outputs
            y_true: Ground truth labels
            method: Optimization objective
            
        Returns:
            Calibrated confidence scores
        """
        self.fit(logits, y_true, method)
        return self.transform(logits)
    
    @staticmethod
    def _sigmoid(x: np.ndarray) -> np.ndarray:
        """Sigmoid activation."""
        return 1 / (1 + np.exp(-x))
    
    @staticmethod
    def _softmax(x: np.ndarray) -> np.ndarray:
        """Softmax activation."""
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)
    
    def _nll_loss(self, logits: np.ndarray, y_true: np.ndarray, temperature: float) -> float:
        """Negative log-likelihood loss."""
        scaled_logits = logits / temperature
        
        if scaled_logits.ndim == 1:
            # Binary classification
            probs = self._sigmoid(scaled_logits)
            eps = 1e-15
            probs = np.clip(probs, eps, 1 - eps)
            nll = -np.mean(y_true * np.log(probs) + (1 - y_true) * np.log(1 - probs))
        else:
            # Multi-class classification
            probs = self._softmax(scaled_logits)
            eps = 1e-15
            probs = np.clip(probs, eps, 1 - eps)
            nll = -np.mean(np.log(probs[np.arange(len(y_true)), y_true.astype(int)]))
        
        return nll
    
    def _ece_loss(self, logits: np.ndarray, y_true: np.ndarray, temperature: float) -> float:
        """ECE loss for optimization."""
        from .metrics import expected_calibration_error
        
        scaled_logits = logits / temperature
        
        if scaled_logits.ndim == 1:
            probs = self._sigmoid(scaled_logits)
            y_pred = (probs > 0.5).astype(int)
        else:
            probs = self._softmax(scaled_logits)
            y_pred = np.argmax(probs, axis=1)
            probs = np.max(probs, axis=1)
        
        ece = expected_calibration_error(y_true, y_pred, probs)
        return ece


class IsotonicCalibrator:
    """
    Isotonic Regression calibration method.
    
    Non-parametric method that learns a monotonic mapping from confidence to calibrated probability.
    
    Reference:
        Zadrozny & Elkan (2002): "Transforming Classifier Scores into Accurate Multiclass Probability Estimates"
    """
    
    def __init__(self):
        self.calibrator = IsotonicRegression(out_of_bounds="clip")
        self.is_fitted = False
    
    def fit(self, confidences: np.ndarray, y_true: np.ndarray) -> "IsotonicCalibrator":
        """
        Learn isotonic regression mapping.
        
        Args:
            confidences: Predicted confidence scores [0, 1]
            y_true: Ground truth labels (binary)
            
        Returns:
            self
        """
        self.calibrator.fit(confidences, y_true)
        self.is_fitted = True
        return self
    
    def transform(self, confidences: np.ndarray) -> np.ndarray:
        """
        Apply isotonic calibration to confidences.
        
        Args:
            confidences: Predicted confidence scores [0, 1]
            
        Returns:
            Calibrated confidence scores
        """
        if not self.is_fitted:
            raise ValueError("IsotonicCalibrator must be fitted before transform")
        
        return self.calibrator.transform(confidences)
    
    def fit_transform(self, confidences: np.ndarray, y_true: np.ndarray) -> np.ndarray:
        """
        Fit calibrator and transform in one step.
        
        Args:
            confidences: Predicted confidence scores
            y_true: Ground truth labels
            
        Returns:
            Calibrated confidence scores
        """
        self.fit(confidences, y_true)
        return self.transform(confidences)


class CalibrationAnalyzer:
    """
    High-level interface for calibration analysis and improvement.
    
    Provides unified API for:
    - Calculating calibration metrics
    - Applying calibration methods
    - Generating visualizations
    - EU AI Act compliance reporting
    """
    
    def __init__(self, n_bins: int = 10):
        """
        Initialize calibration analyzer.
        
        Args:
            n_bins: Number of bins for calibration metrics
        """
        self.n_bins = n_bins
        self.temperature_scaler = TemperatureScaling()
        self.isotonic_calibrator = IsotonicCalibrator()
        self.calibration_history = []
    
    def evaluate(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        confidences: np.ndarray,
        model_name: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Evaluate model calibration.
        
        Args:
            y_true: Ground truth labels
            y_pred: Predicted classes
            confidences: Predicted confidence scores
            model_name: Optional model identifier
            
        Returns:
            Comprehensive calibration metrics and assessment
        """
        # Calculate all metrics
        metrics = calculate_all_metrics(y_true, y_pred, confidences, self.n_bins)
        
        # Get bin data for visualization
        bin_data = get_calibration_bins_data(y_true, y_pred, confidences, self.n_bins)
        
        # Assess calibration quality
        from .metrics import is_well_calibrated
        assessment = is_well_calibrated(metrics["ece"], metrics["mce"])
        
        result = {
            "model_name": model_name,
            "metrics": metrics,
            "assessment": assessment,
            "bin_data": bin_data,
        }
        
        # Store in history
        self.calibration_history.append(result)
        
        return result
    
    def calibrate(
        self,
        confidences: np.ndarray,
        y_true: Optional[np.ndarray] = None,
        logits: Optional[np.ndarray] = None,
        method: str = "temperature_scaling"
    ) -> np.ndarray:
        """
        Apply calibration method to improve confidence estimates.
        
        Args:
            confidences: Original confidence scores
            y_true: Ground truth labels (required for fitting)
            logits: Raw logits (required for temperature scaling)
            method: Calibration method ('temperature_scaling' or 'isotonic')
            
        Returns:
            Calibrated confidence scores
        """
        if y_true is None:
            raise ValueError("y_true is required for calibration")
        
        if method == "temperature_scaling":
            if logits is None:
                raise ValueError("logits are required for temperature scaling")
            return self.temperature_scaler.fit_transform(logits, y_true)
        
        elif method == "isotonic":
            return self.isotonic_calibrator.fit_transform(confidences, y_true)
        
        else:
            raise ValueError(f"Unknown calibration method: {method}")
    
    def compare_calibration_methods(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        confidences: np.ndarray,
        logits: Optional[np.ndarray] = None
    ) -> Dict[str, Dict]:
        """
        Compare original vs calibrated confidence using different methods.
        
        Args:
            y_true: Ground truth labels
            y_pred: Predicted classes
            confidences: Original confidence scores
            logits: Raw logits (for temperature scaling)
            
        Returns:
            Comparison of metrics for each method
        """
        results = {}
        
        # Original (uncalibrated)
        results["original"] = calculate_all_metrics(y_true, y_pred, confidences, self.n_bins)
        
        # Temperature scaling
        if logits is not None:
            try:
                cal_conf_temp = self.temperature_scaler.fit_transform(logits, y_true)
                results["temperature_scaling"] = calculate_all_metrics(
                    y_true, y_pred, cal_conf_temp, self.n_bins
                )
                results["temperature_scaling"]["temperature"] = self.temperature_scaler.temperature
            except Exception as e:
                results["temperature_scaling"] = {"error": str(e)}
        
        # Isotonic regression
        try:
            cal_conf_iso = self.isotonic_calibrator.fit_transform(confidences, y_true)
            results["isotonic"] = calculate_all_metrics(
                y_true, y_pred, cal_conf_iso, self.n_bins
            )
        except Exception as e:
            results["isotonic"] = {"error": str(e)}
        
        return results
    
    def generate_eu_ai_act_report(self, evaluation_result: Dict) -> Dict[str, any]:
        """
        Generate EU AI Act compliance report.
        
        Addresses:
        - tech-004: Technical documentation
        - safety-001: Safety monitoring
        - safety-002: Post-market monitoring
        - trust-001: Trustworthiness metrics
        
        Args:
            evaluation_result: Result from evaluate()
            
        Returns:
            Compliance report
        """
        metrics = evaluation_result["metrics"]
        assessment = evaluation_result["assessment"]
        
        compliance_requirements = {
            "tech-004": {
                "requirement": "Technical Documentation and Transparency",
                "status": "compliant",
                "evidence": {
                    "calibration_metrics": metrics,
                    "methodology": "ECE, MCE, ACE metrics following Guo et al. (2017)",
                    "bin_count": metrics["num_bins"],
                }
            },
            "safety-001": {
                "requirement": "Safety Monitoring",
                "status": "compliant" if assessment["well_calibrated"] else "requires_attention",
                "evidence": {
                    "ece": metrics["ece"],
                    "mce": metrics["mce"],
                    "calibration_status": assessment["status"],
                    "recommendation": assessment["recommendation"],
                }
            },
            "safety-002": {
                "requirement": "Post-Market Monitoring",
                "status": "compliant",
                "evidence": {
                    "monitoring_enabled": True,
                    "metrics_tracked": list(metrics.keys()),
                    "sample_size": metrics["num_samples"],
                }
            },
            "trust-001": {
                "requirement": "Trustworthiness and Reliability",
                "status": "compliant" if assessment["well_calibrated"] else "needs_improvement",
                "evidence": {
                    "accuracy": metrics["accuracy"],
                    "calibration_quality": assessment["status"],
                    "confidence_reliability": "high" if assessment["well_calibrated"] else "medium",
                }
            }
        }

        report = {
            "compliance_requirements": compliance_requirements,
            "summary": {
                "overall_compliance": all(
                    req["status"] in ["compliant", "requires_attention"]
                    for req in compliance_requirements.values()
                ),
                "action_required": not assessment["well_calibrated"],
                "next_steps": assessment["recommendation"],
            }
        }

        return report
    
    def get_history(self) -> list:
        """Get calibration evaluation history."""
        return self.calibration_history
