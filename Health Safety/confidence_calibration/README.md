# Confidence Calibration System

## 置信度校准系统

A comprehensive Python toolbox for measuring and improving ML model confidence calibration, ensuring predictions are reliable and trustworthy.

## Features

### 📊 Calibration Metrics
- **ECE (Expected Calibration Error)**: Average calibration error across all bins
- **MCE (Maximum Calibration Error)**: Maximum calibration error in any bin
- **ACE (Average Calibration Error)**: Mean absolute calibration error

### 🔧 Recalibration Methods
- **Temperature Scaling**: Post-hoc calibration using temperature parameter
- **Isotonic Regression**: Non-parametric calibration method

### 📈 Visualization
- **Reliability Diagrams**: Visual assessment of calibration quality
- **Calibration Curves**: Predicted vs actual probability curves
- **Confidence Histograms**: Distribution of prediction confidence

### 🌐 API Service
- REST API for real-time calibration monitoring
- Batch processing support
- Model performance tracking

## EU AI Act Compliance

This system addresses the following EU AI Act requirements:

- **tech-004**: Technical documentation and transparency
- **safety-001**: Safety monitoring and risk assessment
- **safety-002**: Post-market monitoring
- **trust-001**: Trustworthiness and reliability metrics

## Architecture

```
confidence_calibration/
├── core/
│   ├── metrics.py          # Calibration metrics (ECE, MCE, ACE)
│   ├── calibration.py      # Recalibration methods
│   └── validators.py       # Input validation
├── visualization/
│   ├── plots.py            # Plotting functions
│   └── dashboard.py        # Interactive dashboard
├── api/
│   ├── app.py              # FastAPI application
│   └── models.py           # API data models
├── examples/
│   └── demo.py             # Usage examples
└── tests/
    └── test_calibration.py # Unit tests
```

## Quick Start

```python
from confidence_calibration import CalibrationAnalyzer

# Initialize analyzer
analyzer = CalibrationAnalyzer()

# Calculate calibration metrics
metrics = analyzer.evaluate(y_true, y_pred, y_confidence)
print(f"ECE: {metrics['ece']:.4f}")
print(f"MCE: {metrics['mce']:.4f}")

# Apply temperature scaling
calibrated_conf = analyzer.calibrate(y_confidence, method='temperature_scaling')

# Visualize calibration
analyzer.plot_reliability_diagram(y_true, y_pred, y_confidence)
```

## Installation

```bash
pip install -r requirements.txt
```

## API Usage

```bash
# Start API server
python -m confidence_calibration.api.app

# Evaluate calibration
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{"predictions": [...], "confidences": [...], "labels": [...]}'
```

## References

- [Uncertainty Toolbox](https://github.com/uncertainty-toolbox/uncertainty-toolbox)
- Guo et al. (2017): "On Calibration of Modern Neural Networks"
- Kuleshov et al. (2018): "Accurate Uncertainties for Deep Learning"

## License

MIT License
