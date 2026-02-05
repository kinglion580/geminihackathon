"""
Input Validation

Validates inputs for calibration functions to ensure data quality and safety.
"""

import numpy as np
from typing import Tuple, Optional


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_arrays_shape(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray
) -> None:
    """
    Validate that all arrays have compatible shapes.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted classes
        confidences: Confidence scores
        
    Raises:
        ValidationError: If shapes are incompatible
    """
    if len(y_true) != len(y_pred):
        raise ValidationError(
            f"y_true and y_pred must have same length. "
            f"Got {len(y_true)} and {len(y_pred)}"
        )
    
    if len(y_true) != len(confidences):
        raise ValidationError(
            f"y_true and confidences must have same length. "
            f"Got {len(y_true)} and {len(confidences)}"
        )
    
    if len(y_true) == 0:
        raise ValidationError("Input arrays cannot be empty")


def validate_confidence_range(confidences: np.ndarray) -> None:
    """
    Validate that confidence scores are in valid range [0, 1].
    
    Args:
        confidences: Confidence scores
        
    Raises:
        ValidationError: If confidences are outside [0, 1]
    """
    if np.any(confidences < 0) or np.any(confidences > 1):
        min_val = np.min(confidences)
        max_val = np.max(confidences)
        raise ValidationError(
            f"Confidences must be in range [0, 1]. "
            f"Got range [{min_val:.4f}, {max_val:.4f}]"
        )


def validate_labels(y_true: np.ndarray, y_pred: np.ndarray) -> None:
    """
    Validate label arrays.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted labels
        
    Raises:
        ValidationError: If labels are invalid
    """
    # Check for NaN or infinite values
    if np.any(np.isnan(y_true)) or np.any(np.isnan(y_pred)):
        raise ValidationError("Labels cannot contain NaN values")
    
    if np.any(np.isinf(y_true)) or np.any(np.isinf(y_pred)):
        raise ValidationError("Labels cannot contain infinite values")
    
    # Check that labels are non-negative integers
    if not np.all(y_true >= 0) or not np.all(y_pred >= 0):
        raise ValidationError("Labels must be non-negative")
    
    # Check that y_pred classes are subset of y_true classes
    true_classes = set(np.unique(y_true))
    pred_classes = set(np.unique(y_pred))
    
    if not pred_classes.issubset(true_classes):
        extra_classes = pred_classes - true_classes
        raise ValidationError(
            f"y_pred contains classes not in y_true: {extra_classes}"
        )


def validate_n_bins(n_bins: int, n_samples: int) -> None:
    """
    Validate number of bins for calibration.
    
    Args:
        n_bins: Number of bins
        n_samples: Number of samples
        
    Raises:
        ValidationError: If n_bins is invalid
    """
    if n_bins < 2:
        raise ValidationError(f"n_bins must be at least 2. Got {n_bins}")
    
    if n_bins > n_samples:
        raise ValidationError(
            f"n_bins ({n_bins}) cannot exceed number of samples ({n_samples})"
        )
    
    if n_bins > n_samples / 2:
        import warnings
        warnings.warn(
            f"n_bins ({n_bins}) is large relative to sample size ({n_samples}). "
            f"This may lead to unreliable calibration metrics.",
            UserWarning
        )


def validate_calibration_input(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    n_bins: int = 10
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Comprehensive validation of calibration inputs.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted classes
        confidences: Confidence scores
        n_bins: Number of bins
        
    Returns:
        Validated and converted arrays
        
    Raises:
        ValidationError: If any validation fails
    """
    # Convert to numpy arrays
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    confidences = np.asarray(confidences)
    
    # Validate shapes
    validate_arrays_shape(y_true, y_pred, confidences)
    
    # Validate confidence range
    validate_confidence_range(confidences)
    
    # Validate labels
    validate_labels(y_true, y_pred)
    
    # Validate n_bins
    validate_n_bins(n_bins, len(y_true))
    
    return y_true, y_pred, confidences


def validate_logits(logits: np.ndarray, y_true: np.ndarray) -> None:
    """
    Validate logits for temperature scaling.
    
    Args:
        logits: Raw model outputs
        y_true: Ground truth labels
        
    Raises:
        ValidationError: If logits are invalid
    """
    if len(logits) != len(y_true):
        raise ValidationError(
            f"logits and y_true must have same length. "
            f"Got {len(logits)} and {len(y_true)}"
        )
    
    if np.any(np.isnan(logits)) or np.any(np.isinf(logits)):
        raise ValidationError("Logits cannot contain NaN or infinite values")
    
    # Check logits shape for multi-class
    if logits.ndim == 2:
        n_classes = logits.shape[1]
        max_label = np.max(y_true)
        if max_label >= n_classes:
            raise ValidationError(
                f"Logits shape {logits.shape} incompatible with max label {max_label}"
            )


def sanitize_confidences(confidences: np.ndarray, eps: float = 1e-10) -> np.ndarray:
    """
    Sanitize confidence scores to avoid numerical issues.
    
    Args:
        confidences: Confidence scores
        eps: Small epsilon for clipping
        
    Returns:
        Sanitized confidences in range [eps, 1-eps]
    """
    return np.clip(confidences, eps, 1 - eps)


def check_minimum_samples_per_class(
    y_true: np.ndarray,
    min_samples: int = 10,
    warn_only: bool = True
) -> bool:
    """
    Check if each class has minimum number of samples.
    
    Args:
        y_true: Ground truth labels
        min_samples: Minimum samples required per class
        warn_only: If True, only warn; if False, raise error
        
    Returns:
        True if all classes have enough samples
        
    Raises:
        ValidationError: If warn_only=False and check fails
    """
    unique, counts = np.unique(y_true, return_counts=True)
    insufficient = counts < min_samples
    
    if np.any(insufficient):
        problem_classes = unique[insufficient]
        problem_counts = counts[insufficient]
        
        message = (
            f"Some classes have fewer than {min_samples} samples: "
            f"{dict(zip(problem_classes, problem_counts))}"
        )
        
        if warn_only:
            import warnings
            warnings.warn(message, UserWarning)
            return False
        else:
            raise ValidationError(message)
    
    return True
