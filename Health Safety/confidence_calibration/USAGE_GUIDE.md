# Usage Guide

## Quick Start

### Installation

```bash
cd "Health Safety/confidence_calibration"
pip install -r requirements.txt
```

### Run Demo

```bash
chmod +x run_demo.sh
./run_demo.sh
```

Or manually:

```bash
python examples/demo.py
```

## Core Usage

### 1. Basic Calibration Evaluation

```python
from confidence_calibration import CalibrationAnalyzer

# Your model predictions
y_true = [0, 1, 1, 0, 1]  # Ground truth
y_pred = [0, 1, 0, 0, 1]  # Predictions
confidences = [0.6, 0.9, 0.7, 0.4, 0.95]  # Confidence scores

# Create analyzer
analyzer = CalibrationAnalyzer(n_bins=10)

# Evaluate calibration
result = analyzer.evaluate(y_true, y_pred, confidences, model_name="My Model")

# View metrics
print(f"ECE: {result['metrics']['ece']:.4f}")
print(f"MCE: {result['metrics']['mce']:.4f}")
print(f"Status: {result['assessment']['status']}")
```

### 2. Calculate Individual Metrics

```python
from confidence_calibration.core.metrics import (
    expected_calibration_error,
    maximum_calibration_error,
    calculate_all_metrics
)

# Calculate specific metric
ece = expected_calibration_error(y_true, y_pred, confidences)

# Or get all metrics at once
all_metrics = calculate_all_metrics(y_true, y_pred, confidences)
```

### 3. Apply Calibration Methods

#### Temperature Scaling

```python
import numpy as np

# You need raw logits (before softmax/sigmoid)
logits = np.array([[-0.5], [2.0], [0.3], [-1.0], [2.5]])

# Apply temperature scaling
calibrated_conf = analyzer.calibrate(
    confidences,
    y_true=y_true,
    logits=logits,
    method='temperature_scaling'
)

print(f"Temperature: {analyzer.temperature_scaler.temperature}")
```

#### Isotonic Regression

```python
# Apply isotonic regression (only needs confidences)
calibrated_conf = analyzer.calibrate(
    confidences,
    y_true=y_true,
    method='isotonic'
)
```

### 4. Compare Methods

```python
# Compare all calibration methods
comparison = analyzer.compare_calibration_methods(
    y_true, y_pred, confidences, logits
)

for method, metrics in comparison.items():
    print(f"{method}: ECE={metrics['ece']:.4f}")
```

### 5. Visualization

```python
from confidence_calibration.visualization.plots import (
    plot_reliability_diagram,
    plot_confidence_histogram,
    plot_eu_ai_act_dashboard
)

# Reliability diagram
plot_reliability_diagram(y_true, y_pred, confidences, 
                        title="Model Calibration",
                        save_path="reliability.png")

# Confidence distribution
plot_confidence_histogram(confidences, y_true, y_pred,
                         save_path="confidence_dist.png")

# EU AI Act dashboard
evaluation = analyzer.evaluate(y_true, y_pred, confidences)
plot_eu_ai_act_dashboard(evaluation, save_path="compliance.png")
```

### 6. EU AI Act Compliance Report

```python
# Generate compliance report
evaluation = analyzer.evaluate(y_true, y_pred, confidences)
report = analyzer.generate_eu_ai_act_report(evaluation)

# Check compliance status
for req_id, req_data in report['compliance_requirements'].items():
    print(f"{req_id}: {req_data['status']}")

# Overall summary
print(report['summary'])
```

## API Usage

### Start Server

```bash
python -m confidence_calibration.api.app
```

Server runs on `http://localhost:8000`

View interactive docs: `http://localhost:8000/docs`

### API Endpoints

#### 1. Health Check

```bash
curl http://localhost:8000/health
```

#### 2. Evaluate Calibration

```bash
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "y_true": [0, 1, 1, 0, 1],
    "y_pred": [0, 1, 0, 0, 1],
    "confidences": [0.6, 0.9, 0.7, 0.4, 0.95],
    "n_bins": 10,
    "model_name": "Test Model"
  }'
```

#### 3. Apply Recalibration

```bash
curl -X POST http://localhost:8000/recalibrate \
  -H "Content-Type: application/json" \
  -d '{
    "confidences": [0.6, 0.9, 0.7, 0.4, 0.95],
    "y_true": [0, 1, 1, 0, 1],
    "method": "isotonic"
  }'
```

#### 4. Compare Methods

```bash
curl -X POST http://localhost:8000/compare \
  -H "Content-Type: application/json" \
  -d '{
    "y_true": [0, 1, 1, 0, 1],
    "y_pred": [0, 1, 0, 0, 1],
    "confidences": [0.6, 0.9, 0.7, 0.4, 0.95],
    "logits": [[-0.5], [2.0], [0.3], [-1.0], [2.5]]
  }'
```

#### 5. EU AI Act Report

```bash
curl -X POST http://localhost:8000/eu-ai-act-report \
  -H "Content-Type: application/json" \
  -d '{
    "y_true": [0, 1, 1, 0, 1],
    "y_pred": [0, 1, 0, 0, 1],
    "confidences": [0.6, 0.9, 0.7, 0.4, 0.95],
    "model_name": "Healthcare Model"
  }'
```

#### 6. Generate Visualization

```bash
curl -X POST http://localhost:8000/visualize/reliability-diagram \
  -H "Content-Type: application/json" \
  -d '{
    "y_true": [0, 1, 1, 0, 1],
    "y_pred": [0, 1, 0, 0, 1],
    "confidences": [0.6, 0.9, 0.7, 0.4, 0.95]
  }' \
  --output reliability_diagram.png
```

#### 7. View History

```bash
curl http://localhost:8000/history
```

## Integration Examples

### Integration with Scikit-learn

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
import numpy as np

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Get predictions
y_pred = model.predict(X_test)
confidences = model.predict_proba(X_test)[:, 1]  # Probability of positive class

# Evaluate calibration
from confidence_calibration import CalibrationAnalyzer
analyzer = CalibrationAnalyzer()
result = analyzer.evaluate(y_test, y_pred, confidences)

# If poorly calibrated, apply recalibration
if not result['assessment']['well_calibrated']:
    # Get raw scores (decision function)
    logits = model.predict_log_proba(X_test)
    calibrated_conf = analyzer.calibrate(
        confidences, y_true=y_test, logits=logits,
        method='temperature_scaling'
    )
```

### Integration with PyTorch

```python
import torch
import torch.nn as nn
from confidence_calibration import CalibrationAnalyzer

# Your PyTorch model
model = MyNeuralNetwork()
model.eval()

# Get predictions
with torch.no_grad():
    logits = model(X_test_tensor)
    probs = torch.softmax(logits, dim=1)
    confidences, y_pred = torch.max(probs, dim=1)

# Convert to numpy
y_pred_np = y_pred.cpu().numpy()
confidences_np = confidences.cpu().numpy()
logits_np = logits.cpu().numpy()

# Evaluate calibration
analyzer = CalibrationAnalyzer()
result = analyzer.evaluate(y_test, y_pred_np, confidences_np)

# Apply temperature scaling
calibrated_conf = analyzer.calibrate(
    confidences_np,
    y_true=y_test,
    logits=logits_np,
    method='temperature_scaling'
)
```

### Integration with TensorFlow/Keras

```python
import tensorflow as tf
from confidence_calibration import CalibrationAnalyzer

# Your Keras model
model = tf.keras.models.load_model('my_model.h5')

# Get predictions
logits = model(X_test)
probs = tf.nn.softmax(logits, axis=1).numpy()
y_pred = probs.argmax(axis=1)
confidences = probs.max(axis=1)

# Evaluate calibration
analyzer = CalibrationAnalyzer()
result = analyzer.evaluate(y_test, y_pred, confidences)
```

### Production Monitoring Pipeline

```python
from confidence_calibration.api.models import CalibrationRequest
import requests

class ModelMonitor:
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url
        self.alert_threshold = 0.10
    
    def evaluate_batch(self, y_true, y_pred, confidences, model_name):
        """Evaluate a batch of predictions."""
        response = requests.post(
            f"{self.api_url}/evaluate",
            json={
                "y_true": y_true.tolist(),
                "y_pred": y_pred.tolist(),
                "confidences": confidences.tolist(),
                "model_name": model_name
            }
        )
        
        result = response.json()
        ece = result['metrics']['ece']
        
        # Alert if calibration degrades
        if ece > self.alert_threshold:
            self.send_alert(model_name, ece)
        
        return result
    
    def send_alert(self, model_name, ece):
        """Send alert for poor calibration."""
        print(f"⚠️  ALERT: {model_name} calibration degraded (ECE={ece:.4f})")
        # Add your alerting logic here (email, Slack, etc.)

# Usage
monitor = ModelMonitor()

# Monitor production predictions
for batch in production_batches:
    result = monitor.evaluate_batch(
        batch.y_true,
        batch.y_pred,
        batch.confidences,
        model_name="Production Model v1.2"
    )
```

## Advanced Usage

### Custom Bin Configuration

```python
# Use more bins for larger datasets
analyzer = CalibrationAnalyzer(n_bins=20)

# Or fewer bins for small datasets
analyzer = CalibrationAnalyzer(n_bins=5)
```

### Batch Processing

```python
# Process multiple models
models = ['model_v1', 'model_v2', 'model_v3']
results = {}

for model_name in models:
    # Load predictions for this model
    y_true, y_pred, confidences = load_predictions(model_name)
    
    # Evaluate
    result = analyzer.evaluate(y_true, y_pred, confidences, model_name)
    results[model_name] = result

# Compare models
for name, result in results.items():
    print(f"{name}: ECE={result['metrics']['ece']:.4f}")
```

### Custom Thresholds

```python
from confidence_calibration.core.metrics import is_well_calibrated

# Custom calibration thresholds for your application
assessment = is_well_calibrated(
    ece=metrics['ece'],
    mce=metrics['mce'],
    ece_threshold=0.03,  # Stricter for medical applications
    mce_threshold=0.08
)
```

## Testing

```bash
# Run all tests
python tests/test_calibration.py

# Run with verbose output
python tests/test_calibration.py -v

# Run specific test
python -m unittest tests.test_calibration.TestCalibrationMetrics
```

## Troubleshooting

### Issue: High ECE values

**Solution**: Apply temperature scaling or isotonic regression

```python
calibrated_conf = analyzer.calibrate(confidences, y_true, logits, method='temperature_scaling')
```

### Issue: NaN or Inf values

**Solution**: Check input data ranges and apply sanitization

```python
from confidence_calibration.core.validators import sanitize_confidences

confidences = sanitize_confidences(confidences, eps=1e-10)
```

### Issue: Few samples in some bins

**Solution**: Reduce number of bins

```python
analyzer = CalibrationAnalyzer(n_bins=5)
```

### Issue: Logits not available for temperature scaling

**Solution**: Use isotonic regression instead

```python
calibrated_conf = analyzer.calibrate(confidences, y_true, method='isotonic')
```

## Best Practices

1. **Always evaluate on validation set** before deploying
2. **Use n_bins=10** for most applications (adjust based on sample size)
3. **Monitor calibration continuously** in production
4. **Recalibrate periodically** if model or data changes
5. **Document calibration status** for compliance
6. **Set up alerts** for calibration degradation (ECE > 0.10)
7. **Generate reports regularly** for audit trail

## Performance Tips

- For large datasets (>100k samples), consider sampling for initial evaluation
- Use API for production to avoid loading models repeatedly
- Cache calibration models (temperature, isotonic) after fitting
- Batch predictions for API calls to reduce overhead

## Support

- Issues: Create issue on GitHub
- Documentation: See `README.md` and `EU_AI_ACT_COMPLIANCE.md`
- Examples: Check `examples/demo.py`
- API Docs: Visit `/docs` when server is running
