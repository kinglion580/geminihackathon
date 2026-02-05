"""
Unit Tests for Confidence Calibration

Tests for metrics, calibration methods, and validators.
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from confidence_calibration.core.metrics import (
    expected_calibration_error,
    maximum_calibration_error,
    average_calibration_error,
    calculate_all_metrics,
    is_well_calibrated,
)

from confidence_calibration.core.calibration import (
    TemperatureScaling,
    IsotonicCalibrator,
    CalibrationAnalyzer,
)

from confidence_calibration.core.validators import (
    validate_arrays_shape,
    validate_confidence_range,
    validate_calibration_input,
    ValidationError,
)


class TestCalibrationMetrics(unittest.TestCase):
    """Test calibration metrics calculation."""
    
    def setUp(self):
        """Set up test data."""
        np.random.seed(42)
        self.n_samples = 100
        self.y_true = np.random.randint(0, 2, self.n_samples)
        self.y_pred = np.random.randint(0, 2, self.n_samples)
        self.confidences = np.random.uniform(0.5, 1.0, self.n_samples)
    
    def test_ece_calculation(self):
        """Test ECE calculation."""
        ece = expected_calibration_error(
            self.y_true, self.y_pred, self.confidences, n_bins=10
        )
        self.assertIsInstance(ece, float)
        self.assertGreaterEqual(ece, 0.0)
        self.assertLessEqual(ece, 1.0)
    
    def test_mce_calculation(self):
        """Test MCE calculation."""
        mce = maximum_calibration_error(
            self.y_true, self.y_pred, self.confidences, n_bins=10
        )
        self.assertIsInstance(mce, float)
        self.assertGreaterEqual(mce, 0.0)
        self.assertLessEqual(mce, 1.0)
    
    def test_ace_calculation(self):
        """Test ACE calculation."""
        ace = average_calibration_error(
            self.y_true, self.y_pred, self.confidences, n_bins=10
        )
        self.assertIsInstance(ace, float)
        self.assertGreaterEqual(ace, 0.0)
        self.assertLessEqual(ace, 1.0)
    
    def test_perfect_calibration(self):
        """Test metrics for perfectly calibrated model."""
        # Create perfectly calibrated data
        y_true = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
        y_pred = y_true.copy()
        confidences = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.9, 0.9, 0.9, 0.9, 0.9])
        
        ece = expected_calibration_error(y_true, y_pred, confidences, n_bins=5)
        
        # ECE should be very small for perfect calibration
        self.assertLess(ece, 0.1)
    
    def test_calculate_all_metrics(self):
        """Test comprehensive metrics calculation."""
        metrics = calculate_all_metrics(
            self.y_true, self.y_pred, self.confidences, n_bins=10
        )
        
        # Check all required metrics are present
        self.assertIn("ece", metrics)
        self.assertIn("mce", metrics)
        self.assertIn("ace", metrics)
        self.assertIn("accuracy", metrics)
        self.assertIn("num_samples", metrics)
        self.assertIn("num_bins", metrics)
        
        # Check value ranges
        self.assertGreaterEqual(metrics["ece"], 0.0)
        self.assertGreaterEqual(metrics["mce"], 0.0)
        self.assertGreaterEqual(metrics["ace"], 0.0)
        self.assertGreaterEqual(metrics["accuracy"], 0.0)
        self.assertLessEqual(metrics["accuracy"], 1.0)
    
    def test_is_well_calibrated(self):
        """Test calibration quality assessment."""
        # Well calibrated
        result = is_well_calibrated(ece=0.02, mce=0.05)
        self.assertTrue(result["well_calibrated"])
        self.assertEqual(result["status"], "well_calibrated")
        
        # Poorly calibrated
        result = is_well_calibrated(ece=0.15, mce=0.25)
        self.assertFalse(result["well_calibrated"])
        self.assertEqual(result["status"], "poorly_calibrated")


class TestTemperatureScaling(unittest.TestCase):
    """Test temperature scaling calibration."""
    
    def setUp(self):
        """Set up test data."""
        np.random.seed(42)
        self.n_samples = 100
        self.y_true = np.random.randint(0, 2, self.n_samples)
        self.logits = np.random.randn(self.n_samples, 1)
        self.scaler = TemperatureScaling()
    
    def test_fit(self):
        """Test temperature fitting."""
        temperature = self.scaler.fit(self.logits, self.y_true, method="nll")
        
        self.assertIsInstance(temperature, (float, np.floating))
        self.assertGreater(temperature, 0.0)
        self.assertTrue(self.scaler.is_fitted)
    
    def test_transform(self):
        """Test temperature transformation."""
        self.scaler.fit(self.logits, self.y_true)
        calibrated = self.scaler.transform(self.logits)
        
        self.assertEqual(len(calibrated), len(self.logits))
        self.assertTrue(np.all(calibrated >= 0))
        self.assertTrue(np.all(calibrated <= 1))
    
    def test_fit_transform(self):
        """Test combined fit and transform."""
        calibrated = self.scaler.fit_transform(self.logits, self.y_true)
        
        self.assertEqual(len(calibrated), len(self.logits))
        self.assertTrue(np.all(calibrated >= 0))
        self.assertTrue(np.all(calibrated <= 1))
        self.assertTrue(self.scaler.is_fitted)
    
    def test_transform_before_fit_raises_error(self):
        """Test that transform before fit raises error."""
        with self.assertRaises(ValueError):
            self.scaler.transform(self.logits)


class TestIsotonicCalibrator(unittest.TestCase):
    """Test isotonic regression calibration."""
    
    def setUp(self):
        """Set up test data."""
        np.random.seed(42)
        self.n_samples = 100
        self.y_true = np.random.randint(0, 2, self.n_samples)
        self.confidences = np.random.uniform(0.0, 1.0, self.n_samples)
        self.calibrator = IsotonicCalibrator()
    
    def test_fit(self):
        """Test isotonic fitting."""
        result = self.calibrator.fit(self.confidences, self.y_true)
        
        self.assertEqual(result, self.calibrator)
        self.assertTrue(self.calibrator.is_fitted)
    
    def test_transform(self):
        """Test isotonic transformation."""
        self.calibrator.fit(self.confidences, self.y_true)
        calibrated = self.calibrator.transform(self.confidences)
        
        self.assertEqual(len(calibrated), len(self.confidences))
        self.assertTrue(np.all(calibrated >= 0))
        self.assertTrue(np.all(calibrated <= 1))
    
    def test_fit_transform(self):
        """Test combined fit and transform."""
        calibrated = self.calibrator.fit_transform(self.confidences, self.y_true)
        
        self.assertEqual(len(calibrated), len(self.confidences))
        self.assertTrue(np.all(calibrated >= 0))
        self.assertTrue(np.all(calibrated <= 1))
    
    def test_monotonicity(self):
        """Test that isotonic calibration preserves monotonicity."""
        sorted_conf = np.sort(self.confidences)
        self.calibrator.fit(self.confidences, self.y_true)
        calibrated = self.calibrator.transform(sorted_conf)
        
        # Check monotonicity
        diffs = np.diff(calibrated)
        self.assertTrue(np.all(diffs >= -1e-10))  # Allow small numerical errors


class TestCalibrationAnalyzer(unittest.TestCase):
    """Test high-level calibration analyzer."""
    
    def setUp(self):
        """Set up test data."""
        np.random.seed(42)
        self.n_samples = 100
        self.y_true = np.random.randint(0, 2, self.n_samples)
        self.y_pred = np.random.randint(0, 2, self.n_samples)
        self.confidences = np.random.uniform(0.5, 1.0, self.n_samples)
        self.logits = np.random.randn(self.n_samples, 1)
        self.analyzer = CalibrationAnalyzer(n_bins=10)
    
    def test_evaluate(self):
        """Test calibration evaluation."""
        result = self.analyzer.evaluate(
            self.y_true, self.y_pred, self.confidences,
            model_name="Test Model"
        )
        
        self.assertIn("model_name", result)
        self.assertIn("metrics", result)
        self.assertIn("assessment", result)
        self.assertIn("bin_data", result)
        self.assertEqual(result["model_name"], "Test Model")
    
    def test_calibrate_temperature(self):
        """Test temperature scaling calibration."""
        calibrated = self.analyzer.calibrate(
            self.confidences,
            y_true=self.y_true,
            logits=self.logits,
            method="temperature_scaling"
        )
        
        self.assertEqual(len(calibrated), len(self.confidences))
        self.assertTrue(np.all(calibrated >= 0))
        self.assertTrue(np.all(calibrated <= 1))
    
    def test_calibrate_isotonic(self):
        """Test isotonic calibration."""
        calibrated = self.analyzer.calibrate(
            self.confidences,
            y_true=self.y_true,
            method="isotonic"
        )
        
        self.assertEqual(len(calibrated), len(self.confidences))
        self.assertTrue(np.all(calibrated >= 0))
        self.assertTrue(np.all(calibrated <= 1))
    
    def test_compare_methods(self):
        """Test comparison of calibration methods."""
        results = self.analyzer.compare_calibration_methods(
            self.y_true, self.y_pred, self.confidences, self.logits
        )
        
        self.assertIn("original", results)
        self.assertIn("temperature_scaling", results)
        self.assertIn("isotonic", results)
        
        # Check all methods have metrics
        for method in results.values():
            if "error" not in method:
                self.assertIn("ece", method)
    
    def test_eu_ai_act_report(self):
        """Test EU AI Act report generation."""
        evaluation = self.analyzer.evaluate(
            self.y_true, self.y_pred, self.confidences
        )
        report = self.analyzer.generate_eu_ai_act_report(evaluation)
        
        self.assertIn("compliance_requirements", report)
        self.assertIn("summary", report)
        
        # Check all required sections
        reqs = report["compliance_requirements"]
        self.assertIn("tech-004", reqs)
        self.assertIn("safety-001", reqs)
        self.assertIn("safety-002", reqs)
        self.assertIn("trust-001", reqs)
    
    def test_history(self):
        """Test evaluation history tracking."""
        # Perform multiple evaluations
        for i in range(3):
            self.analyzer.evaluate(
                self.y_true, self.y_pred, self.confidences,
                model_name=f"Model_{i}"
            )
        
        history = self.analyzer.get_history()
        self.assertEqual(len(history), 3)


class TestValidators(unittest.TestCase):
    """Test input validation."""
    
    def test_validate_arrays_shape(self):
        """Test array shape validation."""
        y_true = np.array([0, 1, 0])
        y_pred = np.array([0, 1, 1])
        confidences = np.array([0.6, 0.8, 0.7])
        
        # Should not raise
        validate_arrays_shape(y_true, y_pred, confidences)
        
        # Should raise for mismatched lengths
        with self.assertRaises(ValidationError):
            validate_arrays_shape(y_true, np.array([0, 1]), confidences)
    
    def test_validate_confidence_range(self):
        """Test confidence range validation."""
        valid_conf = np.array([0.1, 0.5, 0.9])
        validate_confidence_range(valid_conf)
        
        # Should raise for out-of-range values
        with self.assertRaises(ValidationError):
            validate_confidence_range(np.array([0.5, 1.5, 0.3]))
        
        with self.assertRaises(ValidationError):
            validate_confidence_range(np.array([-0.1, 0.5, 0.8]))
    
    def test_validate_calibration_input(self):
        """Test comprehensive input validation."""
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0, 1, 1, 1])
        confidences = np.array([0.6, 0.8, 0.7, 0.9])
        
        # Should return validated arrays
        y_t, y_p, conf = validate_calibration_input(
            y_true, y_pred, confidences, n_bins=2
        )
        
        self.assertIsInstance(y_t, np.ndarray)
        self.assertIsInstance(y_p, np.ndarray)
        self.assertIsInstance(conf, np.ndarray)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCalibrationMetrics))
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureScaling))
    suite.addTests(loader.loadTestsFromTestCase(TestIsotonicCalibrator))
    suite.addTests(loader.loadTestsFromTestCase(TestCalibrationAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestValidators))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
