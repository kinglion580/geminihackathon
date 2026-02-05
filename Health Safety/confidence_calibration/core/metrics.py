"""
Calibration Metrics

Implements ECE, MCE, ACE and other calibration quality metrics.
"""

import numpy as np
from typing import Dict, Optional, Tuple


def _create_bins(confidences: np.ndarray, n_bins: int = 10) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create bins for calibration calculation.
    
    Args:
        confidences: Predicted confidence scores [0, 1]
        n_bins: Number of bins to use
        
    Returns:
        bin_boundaries: Bin boundary values
        bin_indices: Bin index for each prediction
    """
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_indices = np.digitize(confidences, bin_boundaries[1:-1])
    return bin_boundaries, bin_indices


def expected_calibration_error(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    n_bins: int = 10
) -> float:
    """
    Calculate Expected Calibration Error (ECE).
    
    ECE measures the difference between predicted confidence and actual accuracy,
    weighted by the number of samples in each bin.
    
    Args:
        y_true: Ground truth labels (binary or class indices)
        y_pred: Predicted classes
        confidences: Predicted confidence scores [0, 1]
        n_bins: Number of bins for calibration
        
    Returns:
        ECE value (lower is better)
        
    Reference:
        Guo et al. (2017): "On Calibration of Modern Neural Networks"
    """
    _, bin_indices = _create_bins(confidences, n_bins)
    
    ece = 0.0
    total_samples = len(y_true)
    
    for bin_idx in range(n_bins):
        bin_mask = bin_indices == bin_idx
        bin_count = np.sum(bin_mask)
        
        if bin_count > 0:
            # Accuracy in this bin
            bin_accuracy = np.mean(y_true[bin_mask] == y_pred[bin_mask])
            # Average confidence in this bin
            bin_confidence = np.mean(confidences[bin_mask])
            # Weighted absolute difference
            ece += (bin_count / total_samples) * np.abs(bin_accuracy - bin_confidence)
    
    return ece


def maximum_calibration_error(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    n_bins: int = 10
) -> float:
    """
    Calculate Maximum Calibration Error (MCE).
    
    MCE is the maximum difference between predicted confidence and actual accuracy
    across all bins. It represents the worst-case calibration error.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted classes
        confidences: Predicted confidence scores [0, 1]
        n_bins: Number of bins
        
    Returns:
        MCE value (lower is better)
    """
    _, bin_indices = _create_bins(confidences, n_bins)
    
    max_error = 0.0
    
    for bin_idx in range(n_bins):
        bin_mask = bin_indices == bin_idx
        bin_count = np.sum(bin_mask)
        
        if bin_count > 0:
            bin_accuracy = np.mean(y_true[bin_mask] == y_pred[bin_mask])
            bin_confidence = np.mean(confidences[bin_mask])
            error = np.abs(bin_accuracy - bin_confidence)
            max_error = max(max_error, error)
    
    return max_error


def average_calibration_error(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    n_bins: int = 10
) -> float:
    """
    Calculate Average Calibration Error (ACE).
    
    ACE is the average of absolute differences between confidence and accuracy
    across all bins (unweighted).
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted classes
        confidences: Predicted confidence scores [0, 1]
        n_bins: Number of bins
        
    Returns:
        ACE value (lower is better)
    """
    _, bin_indices = _create_bins(confidences, n_bins)
    
    errors = []
    
    for bin_idx in range(n_bins):
        bin_mask = bin_indices == bin_idx
        bin_count = np.sum(bin_mask)
        
        if bin_count > 0:
            bin_accuracy = np.mean(y_true[bin_mask] == y_pred[bin_mask])
            bin_confidence = np.mean(confidences[bin_mask])
            errors.append(np.abs(bin_accuracy - bin_confidence))
    
    return np.mean(errors) if errors else 0.0


def brier_score(y_true: np.ndarray, confidences: np.ndarray) -> float:
    """
    Calculate Brier Score for probabilistic predictions.
    
    Args:
        y_true: Ground truth binary labels (0 or 1)
        confidences: Predicted probabilities [0, 1]
        
    Returns:
        Brier score (lower is better)
    """
    return np.mean((confidences - y_true) ** 2)


def negative_log_likelihood(y_true: np.ndarray, confidences: np.ndarray) -> float:
    """
    Calculate Negative Log-Likelihood.
    
    Args:
        y_true: Ground truth binary labels (0 or 1)
        confidences: Predicted probabilities [0, 1]
        
    Returns:
        NLL value (lower is better)
    """
    eps = 1e-15
    confidences = np.clip(confidences, eps, 1 - eps)
    return -np.mean(y_true * np.log(confidences) + (1 - y_true) * np.log(1 - confidences))


def get_calibration_bins_data(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    n_bins: int = 10
) -> Dict[str, np.ndarray]:
    """
    Get detailed data for each calibration bin (for visualization).
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted classes
        confidences: Predicted confidence scores
        n_bins: Number of bins
        
    Returns:
        Dictionary with bin_confidences, bin_accuracies, bin_counts
    """
    bin_boundaries, bin_indices = _create_bins(confidences, n_bins)
    
    bin_confidences = []
    bin_accuracies = []
    bin_counts = []
    
    for bin_idx in range(n_bins):
        bin_mask = bin_indices == bin_idx
        bin_count = np.sum(bin_mask)
        
        if bin_count > 0:
            bin_accuracy = np.mean(y_true[bin_mask] == y_pred[bin_mask])
            bin_confidence = np.mean(confidences[bin_mask])
        else:
            bin_accuracy = 0.0
            bin_confidence = (bin_boundaries[bin_idx] + bin_boundaries[bin_idx + 1]) / 2
        
        bin_confidences.append(bin_confidence)
        bin_accuracies.append(bin_accuracy)
        bin_counts.append(bin_count)
    
    return {
        "bin_confidences": np.array(bin_confidences),
        "bin_accuracies": np.array(bin_accuracies),
        "bin_counts": np.array(bin_counts),
        "bin_boundaries": bin_boundaries,
    }


def calculate_all_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    n_bins: int = 10
) -> Dict[str, float]:
    """
    Calculate all calibration metrics at once.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted classes
        confidences: Predicted confidence scores [0, 1]
        n_bins: Number of bins
        
    Returns:
        Dictionary containing all calibration metrics
    """
    # Ensure inputs are numpy arrays
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    confidences = np.asarray(confidences)
    
    # Calculate metrics
    ece = expected_calibration_error(y_true, y_pred, confidences, n_bins)
    mce = maximum_calibration_error(y_true, y_pred, confidences, n_bins)
    ace = average_calibration_error(y_true, y_pred, confidences, n_bins)
    
    # Calculate accuracy
    accuracy = np.mean(y_true == y_pred)
    
    # Calculate Brier score (for binary classification)
    if len(np.unique(y_true)) == 2:
        brier = brier_score(y_true, confidences)
        nll = negative_log_likelihood(y_true, confidences)
    else:
        brier = None
        nll = None
    
    metrics = {
        "ece": float(ece),
        "mce": float(mce),
        "ace": float(ace),
        "accuracy": float(accuracy),
        "num_samples": len(y_true),
        "num_bins": n_bins,
    }
    
    if brier is not None:
        metrics["brier_score"] = float(brier)
    if nll is not None:
        metrics["negative_log_likelihood"] = float(nll)
    
    return metrics


def is_well_calibrated(
    ece: float,
    mce: float,
    ece_threshold: float = 0.05,
    mce_threshold: float = 0.10
) -> Dict[str, any]:
    """
    Determine if model is well-calibrated based on thresholds.
    
    Args:
        ece: Expected Calibration Error
        mce: Maximum Calibration Error
        ece_threshold: ECE threshold for good calibration
        mce_threshold: MCE threshold for good calibration
        
    Returns:
        Dictionary with calibration status and recommendations
    """
    well_calibrated = ece <= ece_threshold and mce <= mce_threshold
    
    if well_calibrated:
        status = "well_calibrated"
        recommendation = "Model is well-calibrated. No recalibration needed."
    elif ece > ece_threshold:
        status = "poorly_calibrated"
        recommendation = "ECE is high. Consider applying temperature scaling or isotonic regression."
    else:
        status = "moderately_calibrated"
        recommendation = "MCE is high. Some bins have poor calibration. Consider isotonic regression."
    
    return {
        "well_calibrated": well_calibrated,
        "status": status,
        "ece": ece,
        "mce": mce,
        "ece_threshold": ece_threshold,
        "mce_threshold": mce_threshold,
        "recommendation": recommendation,
    }
