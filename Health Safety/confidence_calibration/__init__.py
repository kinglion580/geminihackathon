"""
Confidence Calibration System

A comprehensive toolkit for measuring and improving ML model confidence calibration.
"""

__version__ = "1.0.0"

from .core.metrics import (
    expected_calibration_error,
    maximum_calibration_error,
    average_calibration_error,
    calculate_all_metrics,
)

from .core.calibration import (
    TemperatureScaling,
    IsotonicCalibrator,
    CalibrationAnalyzer,
)

__all__ = [
    "expected_calibration_error",
    "maximum_calibration_error",
    "average_calibration_error",
    "calculate_all_metrics",
    "TemperatureScaling",
    "IsotonicCalibrator",
    "CalibrationAnalyzer",
]
