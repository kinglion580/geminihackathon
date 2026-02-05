"""
Demo Script for Confidence Calibration

Demonstrates the usage of the calibration system with synthetic data.
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from confidence_calibration.core.calibration import CalibrationAnalyzer
from confidence_calibration.core.metrics import calculate_all_metrics
from confidence_calibration.visualization.plots import (
    plot_reliability_diagram,
    plot_confidence_histogram,
    plot_calibration_comparison,
    plot_eu_ai_act_dashboard,
)


def generate_synthetic_data(
    n_samples: int = 1000,
    calibration_quality: str = "poor"
) -> tuple:
    """
    Generate synthetic classification data with controllable calibration.
    
    Args:
        n_samples: Number of samples
        calibration_quality: 'good', 'medium', or 'poor'
        
    Returns:
        y_true, y_pred, confidences, logits
    """
    np.random.seed(42)
    
    # Generate true labels (binary classification)
    y_true = np.random.randint(0, 2, n_samples)
    
    # Generate model scores
    # Well-calibrated model: confidences match actual probabilities
    # Poorly-calibrated: confidences are overconfident
    
    if calibration_quality == "good":
        # Well-calibrated predictions
        true_probs = np.where(y_true == 1, 0.7, 0.3)
        noise = np.random.normal(0, 0.1, n_samples)
        confidences = np.clip(true_probs + noise, 0.01, 0.99)
    
    elif calibration_quality == "medium":
        # Moderately calibrated
        true_probs = np.where(y_true == 1, 0.6, 0.4)
        noise = np.random.normal(0, 0.15, n_samples)
        confidences = np.clip(true_probs + noise + 0.1, 0.01, 0.99)
    
    else:  # poor
        # Poorly calibrated (overconfident)
        true_probs = np.where(y_true == 1, 0.5, 0.5)
        noise = np.random.normal(0, 0.2, n_samples)
        # Make predictions overconfident
        raw_conf = true_probs + noise
        confidences = np.clip(np.where(raw_conf > 0.5, raw_conf + 0.3, raw_conf - 0.3), 0.01, 0.99)
    
    # Generate predictions from confidences
    y_pred = (confidences > 0.5).astype(int)
    
    # Generate logits (inverse sigmoid of confidences)
    logits = np.log(confidences / (1 - confidences))
    
    return y_true, y_pred, confidences, logits


def demo_basic_evaluation():
    """Demonstrate basic calibration evaluation."""
    print("=" * 80)
    print("DEMO 1: Basic Calibration Evaluation")
    print("=" * 80)
    
    # Generate poorly calibrated data
    y_true, y_pred, confidences, logits = generate_synthetic_data(
        n_samples=1000,
        calibration_quality="poor"
    )
    
    # Create analyzer
    analyzer = CalibrationAnalyzer(n_bins=10)
    
    # Evaluate calibration
    result = analyzer.evaluate(y_true, y_pred, confidences, model_name="Demo Model")
    
    # Print results
    print("\nCalibration Metrics:")
    print("-" * 40)
    for metric, value in result["metrics"].items():
        print(f"  {metric}: {value}")
    
    print("\nCalibration Assessment:")
    print("-" * 40)
    assessment = result["assessment"]
    print(f"  Status: {assessment['status']}")
    print(f"  Well Calibrated: {assessment['well_calibrated']}")
    print(f"  Recommendation: {assessment['recommendation']}")
    
    # Visualize
    print("\nGenerating reliability diagram...")
    plot_reliability_diagram(
        y_true, y_pred, confidences,
        title="Demo Model - Reliability Diagram",
        save_path="demo_reliability_diagram.png",
        show=False
    )
    print("  Saved: demo_reliability_diagram.png")
    
    plot_confidence_histogram(
        confidences, y_true, y_pred,
        title="Demo Model - Confidence Distribution",
        save_path="demo_confidence_histogram.png",
        show=False
    )
    print("  Saved: demo_confidence_histogram.png")


def demo_calibration_methods():
    """Demonstrate calibration improvement methods."""
    print("\n" + "=" * 80)
    print("DEMO 2: Calibration Methods Comparison")
    print("=" * 80)
    
    # Generate poorly calibrated data
    y_true, y_pred, confidences, logits = generate_synthetic_data(
        n_samples=1000,
        calibration_quality="poor"
    )
    
    # Create analyzer
    analyzer = CalibrationAnalyzer(n_bins=10)
    
    # Compare calibration methods
    print("\nComparing calibration methods...")
    comparison = analyzer.compare_calibration_methods(
        y_true, y_pred, confidences, logits
    )
    
    print("\nResults:")
    print("-" * 60)
    for method, metrics in comparison.items():
        if "error" in metrics:
            print(f"\n{method.upper()}: Error - {metrics['error']}")
        else:
            print(f"\n{method.upper()}:")
            print(f"  ECE: {metrics['ece']:.4f}")
            print(f"  MCE: {metrics['mce']:.4f}")
            print(f"  Accuracy: {metrics['accuracy']:.4f}")
            if "temperature" in metrics:
                print(f"  Temperature: {metrics['temperature']:.4f}")
    
    # Visualize comparison
    print("\nGenerating comparison plot...")
    
    # Prepare confidence dictionaries
    confidences_dict = {"Original": confidences}
    
    if "temperature_scaling" in comparison and "error" not in comparison["temperature_scaling"]:
        cal_temp = analyzer.temperature_scaler.transform(logits.reshape(-1, 1))
        confidences_dict["Temperature Scaling"] = cal_temp.flatten()
    
    if "isotonic" in comparison and "error" not in comparison["isotonic"]:
        cal_iso = analyzer.isotonic_calibrator.transform(confidences)
        confidences_dict["Isotonic Regression"] = cal_iso
    
    plot_calibration_comparison(
        y_true, y_pred, confidences_dict,
        title="Calibration Methods Comparison",
        save_path="demo_calibration_comparison.png",
        show=False
    )
    print("  Saved: demo_calibration_comparison.png")


def demo_eu_ai_act_compliance():
    """Demonstrate EU AI Act compliance reporting."""
    print("\n" + "=" * 80)
    print("DEMO 3: EU AI Act Compliance Report")
    print("=" * 80)
    
    # Generate data
    y_true, y_pred, confidences, logits = generate_synthetic_data(
        n_samples=1000,
        calibration_quality="medium"
    )
    
    # Create analyzer
    analyzer = CalibrationAnalyzer(n_bins=10)
    
    # Evaluate
    evaluation = analyzer.evaluate(y_true, y_pred, confidences, model_name="Healthcare Model")
    
    # Generate EU AI Act report
    print("\nGenerating EU AI Act compliance report...")
    report = analyzer.generate_eu_ai_act_report(evaluation)
    
    print("\nCompliance Requirements:")
    print("-" * 60)
    for req_id, req_data in report["compliance_requirements"].items():
        print(f"\n{req_id}: {req_data['requirement']}")
        print(f"  Status: {req_data['status']}")
        print(f"  Evidence: {req_data['evidence']}")
    
    print("\nSummary:")
    print("-" * 60)
    summary = report["summary"]
    print(f"  Overall Compliance: {summary['overall_compliance']}")
    print(f"  Action Required: {summary['action_required']}")
    print(f"  Next Steps: {summary['next_steps']}")
    
    # Generate dashboard
    print("\nGenerating EU AI Act dashboard...")
    plot_eu_ai_act_dashboard(
        evaluation,
        save_path="demo_eu_ai_act_dashboard.png",
        show=False
    )
    print("  Saved: demo_eu_ai_act_dashboard.png")


def demo_post_market_monitoring():
    """Demonstrate post-market monitoring scenario."""
    print("\n" + "=" * 80)
    print("DEMO 4: Post-Market Monitoring (safety-002)")
    print("=" * 80)
    
    analyzer = CalibrationAnalyzer(n_bins=10)
    
    print("\nSimulating model predictions over time...")
    
    # Simulate 5 batches of predictions
    for batch_num in range(1, 6):
        # Simulate gradual calibration degradation
        quality = "good" if batch_num < 3 else "medium" if batch_num < 5 else "poor"
        
        y_true, y_pred, confidences, logits = generate_synthetic_data(
            n_samples=200,
            calibration_quality=quality
        )
        
        result = analyzer.evaluate(
            y_true, y_pred, confidences,
            model_name=f"Batch_{batch_num}"
        )
        
        print(f"\nBatch {batch_num} ({quality.upper()} calibration):")
        print(f"  ECE: {result['metrics']['ece']:.4f}")
        print(f"  MCE: {result['metrics']['mce']:.4f}")
        print(f"  Status: {result['assessment']['status']}")
    
    # Show history
    print("\n\nMonitoring History:")
    print("-" * 60)
    history = analyzer.get_history()
    
    for i, record in enumerate(history, 1):
        metrics = record['metrics']
        print(f"{i}. {record['model_name']}: ECE={metrics['ece']:.4f}, Status={record['assessment']['status']}")
    
    # Check for calibration drift
    ece_values = [r['metrics']['ece'] for r in history]
    if len(ece_values) >= 2:
        drift = ece_values[-1] - ece_values[0]
        print(f"\n⚠️  Calibration Drift Detected: {drift:+.4f}")
        if drift > 0.05:
            print("  ALERT: Significant calibration degradation. Recalibration recommended!")


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "CONFIDENCE CALIBRATION SYSTEM DEMO" + " " * 24 + "║")
    print("║" + " " * 25 + "EU AI Act Compliant" + " " * 34 + "║")
    print("╚" + "=" * 78 + "╝")
    
    try:
        demo_basic_evaluation()
        demo_calibration_methods()
        demo_eu_ai_act_compliance()
        demo_post_market_monitoring()
        
        print("\n" + "=" * 80)
        print("Demo completed successfully!")
        print("=" * 80)
        print("\nGenerated files:")
        print("  - demo_reliability_diagram.png")
        print("  - demo_confidence_histogram.png")
        print("  - demo_calibration_comparison.png")
        print("  - demo_eu_ai_act_dashboard.png")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
