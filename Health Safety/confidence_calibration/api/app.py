"""
FastAPI Application for Confidence Calibration

REST API for real-time calibration monitoring and analysis.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import numpy as np
from datetime import datetime
import tempfile
import os
from typing import Dict

from .models import (
    CalibrationRequest,
    CalibrationResponse,
    RecalibrationRequest,
    RecalibrationResponse,
    ComparisonRequest,
    ComparisonResponse,
    EUAIActReportRequest,
    EUAIActReportResponse,
    HealthCheckResponse,
)

from ..core.calibration import CalibrationAnalyzer
from ..core.validators import validate_calibration_input, ValidationError
from ..visualization.plots import (
    plot_reliability_diagram,
    plot_eu_ai_act_dashboard,
)

# Create FastAPI app
app = FastAPI(
    title="Confidence Calibration API",
    description="REST API for ML model confidence calibration and EU AI Act compliance",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global analyzer instance
analyzer = CalibrationAnalyzer(n_bins=10)


@app.get("/", response_model=HealthCheckResponse)
async def root():
    """Health check endpoint."""
    return HealthCheckResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Detailed health check."""
    return HealthCheckResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )


@app.post("/evaluate", response_model=CalibrationResponse)
async def evaluate_calibration(request: CalibrationRequest):
    """
    Evaluate model calibration and calculate metrics.
    
    Returns ECE, MCE, ACE and calibration assessment.
    """
    try:
        # Convert to numpy arrays
        y_true = np.array(request.y_true)
        y_pred = np.array(request.y_pred)
        confidences = np.array(request.confidences)
        
        # Validate inputs
        validate_calibration_input(y_true, y_pred, confidences, request.n_bins)
        
        # Update analyzer bins if needed
        if analyzer.n_bins != request.n_bins:
            analyzer.n_bins = request.n_bins
        
        # Evaluate
        result = analyzer.evaluate(y_true, y_pred, confidences, request.model_name)
        
        # Convert numpy arrays to lists for JSON serialization
        bin_data_serializable = {
            k: v.tolist() if isinstance(v, np.ndarray) else v
            for k, v in result["bin_data"].items()
        }
        
        return CalibrationResponse(
            model_name=result["model_name"],
            metrics=result["metrics"],
            assessment=result["assessment"],
            bin_data=bin_data_serializable,
            success=True,
            message="Calibration evaluated successfully"
        )
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/recalibrate", response_model=RecalibrationResponse)
async def recalibrate(request: RecalibrationRequest):
    """
    Apply recalibration method to confidence scores.
    
    Supports temperature scaling and isotonic regression.
    """
    try:
        confidences = np.array(request.confidences)
        
        if request.y_true is None:
            raise HTTPException(
                status_code=400,
                detail="y_true is required for calibration"
            )
        
        y_true = np.array(request.y_true)
        
        if request.method == "temperature_scaling":
            if request.logits is None:
                raise HTTPException(
                    status_code=400,
                    detail="logits are required for temperature scaling"
                )
            logits = np.array(request.logits)
            calibrated = analyzer.calibrate(
                confidences, y_true=y_true, logits=logits, method="temperature_scaling"
            )
            parameters = {"temperature": float(analyzer.temperature_scaler.temperature)}
        
        elif request.method == "isotonic":
            calibrated = analyzer.calibrate(
                confidences, y_true=y_true, method="isotonic"
            )
            parameters = {"method": "isotonic_regression"}
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown method: {request.method}"
            )
        
        return RecalibrationResponse(
            calibrated_confidences=calibrated.tolist(),
            method=request.method,
            parameters=parameters,
            success=True,
            message="Recalibration applied successfully"
        )
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/compare", response_model=ComparisonResponse)
async def compare_methods(request: ComparisonRequest):
    """
    Compare calibration across multiple methods.
    
    Returns metrics for original, temperature scaling, and isotonic regression.
    """
    try:
        y_true = np.array(request.y_true)
        y_pred = np.array(request.y_pred)
        confidences = np.array(request.confidences)
        logits = np.array(request.logits) if request.logits else None
        
        # Validate
        validate_calibration_input(y_true, y_pred, confidences, request.n_bins)
        
        # Update analyzer bins
        if analyzer.n_bins != request.n_bins:
            analyzer.n_bins = request.n_bins
        
        # Compare methods
        results = analyzer.compare_calibration_methods(
            y_true, y_pred, confidences, logits
        )
        
        # Determine best method
        valid_methods = {
            k: v for k, v in results.items()
            if "error" not in v
        }
        
        best_method = min(
            valid_methods.keys(),
            key=lambda k: valid_methods[k]["ece"]
        )
        
        # Calculate improvement
        original_ece = results["original"]["ece"]
        improvement = {
            method: {
                "ece_reduction": float(original_ece - metrics["ece"]),
                "ece_reduction_pct": float((original_ece - metrics["ece"]) / original_ece * 100)
            }
            for method, metrics in valid_methods.items()
            if method != "original"
        }
        
        return ComparisonResponse(
            results=results,
            best_method=best_method,
            improvement=improvement,
            success=True,
            message="Comparison completed successfully"
        )
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/eu-ai-act-report", response_model=EUAIActReportResponse)
async def generate_eu_ai_act_report(request: EUAIActReportRequest):
    """
    Generate EU AI Act compliance report.
    
    Addresses tech-004, safety-001, safety-002, trust-001 requirements.
    """
    try:
        y_true = np.array(request.y_true)
        y_pred = np.array(request.y_pred)
        confidences = np.array(request.confidences)
        
        # Validate
        validate_calibration_input(y_true, y_pred, confidences, request.n_bins)
        
        # Update analyzer bins
        if analyzer.n_bins != request.n_bins:
            analyzer.n_bins = request.n_bins
        
        # Evaluate
        evaluation = analyzer.evaluate(y_true, y_pred, confidences, request.model_name)
        
        # Generate report
        report = analyzer.generate_eu_ai_act_report(evaluation)
        
        return EUAIActReportResponse(
            compliance_requirements=report["compliance_requirements"],
            summary=report["summary"],
            success=True,
            message="EU AI Act report generated successfully"
        )
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/visualize/reliability-diagram")
async def create_reliability_diagram(request: CalibrationRequest):
    """
    Generate reliability diagram visualization.
    
    Returns PNG image file.
    """
    try:
        y_true = np.array(request.y_true)
        y_pred = np.array(request.y_pred)
        confidences = np.array(request.confidences)
        
        # Validate
        validate_calibration_input(y_true, y_pred, confidences, request.n_bins)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            plot_reliability_diagram(
                y_true, y_pred, confidences,
                n_bins=request.n_bins,
                title=f"Reliability Diagram - {request.model_name or 'Model'}",
                save_path=tmp.name,
                show=False
            )
            
            return FileResponse(
                tmp.name,
                media_type="image/png",
                filename="reliability_diagram.png"
            )
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/visualize/eu-ai-act-dashboard")
async def create_eu_ai_act_dashboard(request: EUAIActReportRequest):
    """
    Generate EU AI Act compliance dashboard visualization.
    
    Returns PNG image file.
    """
    try:
        y_true = np.array(request.y_true)
        y_pred = np.array(request.y_pred)
        confidences = np.array(request.confidences)
        
        # Validate
        validate_calibration_input(y_true, y_pred, confidences, request.n_bins)
        
        # Update analyzer bins
        if analyzer.n_bins != request.n_bins:
            analyzer.n_bins = request.n_bins
        
        # Evaluate
        evaluation = analyzer.evaluate(y_true, y_pred, confidences, request.model_name)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            plot_eu_ai_act_dashboard(
                evaluation,
                save_path=tmp.name,
                show=False
            )
            
            return FileResponse(
                tmp.name,
                media_type="image/png",
                filename="eu_ai_act_dashboard.png"
            )
    
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/history")
async def get_evaluation_history():
    """
    Get history of calibration evaluations.
    
    Returns list of past evaluations for monitoring.
    """
    history = analyzer.get_history()
    
    # Convert numpy arrays to lists for JSON serialization
    serializable_history = []
    for record in history:
        serializable_record = {
            "model_name": record["model_name"],
            "metrics": record["metrics"],
            "assessment": record["assessment"],
        }
        serializable_history.append(serializable_record)
    
    return {
        "success": True,
        "count": len(serializable_history),
        "history": serializable_history
    }


@app.delete("/history")
async def clear_history():
    """Clear evaluation history."""
    analyzer.calibration_history.clear()
    return {
        "success": True,
        "message": "History cleared successfully"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
