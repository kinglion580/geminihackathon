"""
API Data Models

Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
import numpy as np


class CalibrationRequest(BaseModel):
    """Request model for calibration evaluation."""
    
    y_true: List[int] = Field(..., description="Ground truth labels")
    y_pred: List[int] = Field(..., description="Predicted classes")
    confidences: List[float] = Field(..., description="Confidence scores [0, 1]")
    n_bins: int = Field(10, ge=2, le=50, description="Number of bins for calibration")
    model_name: Optional[str] = Field(None, description="Model identifier")
    
    @validator('confidences')
    def validate_confidences(cls, v):
        """Validate confidence scores are in [0, 1]."""
        if any(c < 0 or c > 1 for c in v):
            raise ValueError("All confidence scores must be in range [0, 1]")
        return v
    
    @validator('y_pred')
    def validate_same_length(cls, v, values):
        """Validate arrays have same length."""
        if 'y_true' in values and len(v) != len(values['y_true']):
            raise ValueError("y_true and y_pred must have same length")
        if 'confidences' in values and len(v) != len(values['confidences']):
            raise ValueError("y_pred and confidences must have same length")
        return v


class CalibrationResponse(BaseModel):
    """Response model for calibration evaluation."""
    
    model_name: Optional[str]
    metrics: Dict[str, float]
    assessment: Dict[str, any]
    bin_data: Dict[str, List[float]]
    success: bool = True
    message: Optional[str] = None


class RecalibrationRequest(BaseModel):
    """Request model for applying recalibration."""
    
    confidences: List[float] = Field(..., description="Confidence scores to calibrate")
    y_true: Optional[List[int]] = Field(None, description="Ground truth (for fitting)")
    logits: Optional[List[List[float]]] = Field(None, description="Raw logits (for temperature scaling)")
    method: str = Field("isotonic", description="Calibration method: 'temperature_scaling' or 'isotonic'")
    
    @validator('method')
    def validate_method(cls, v):
        """Validate calibration method."""
        if v not in ['temperature_scaling', 'isotonic']:
            raise ValueError("method must be 'temperature_scaling' or 'isotonic'")
        return v


class RecalibrationResponse(BaseModel):
    """Response model for recalibration."""
    
    calibrated_confidences: List[float]
    method: str
    parameters: Optional[Dict[str, any]] = None
    success: bool = True
    message: Optional[str] = None


class ComparisonRequest(BaseModel):
    """Request model for comparing calibration methods."""
    
    y_true: List[int]
    y_pred: List[int]
    confidences: List[float]
    logits: Optional[List[List[float]]] = None
    n_bins: int = Field(10, ge=2, le=50)


class ComparisonResponse(BaseModel):
    """Response model for method comparison."""
    
    results: Dict[str, Dict]
    best_method: str
    improvement: Dict[str, float]
    success: bool = True
    message: Optional[str] = None


class EUAIActReportRequest(BaseModel):
    """Request model for EU AI Act report."""
    
    y_true: List[int]
    y_pred: List[int]
    confidences: List[float]
    n_bins: int = Field(10, ge=2, le=50)
    model_name: Optional[str] = None


class EUAIActReportResponse(BaseModel):
    """Response model for EU AI Act compliance report."""
    
    compliance_requirements: Dict[str, Dict]
    summary: Dict[str, any]
    success: bool = True
    message: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Health check response."""
    
    status: str
    version: str
    timestamp: str
