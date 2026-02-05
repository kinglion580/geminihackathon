"""
Calibration Visualization

Generate reliability diagrams, calibration curves, and confidence distributions.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Dict, Tuple
import warnings

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)


def plot_reliability_diagram(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    n_bins: int = 10,
    title: Optional[str] = None,
    save_path: Optional[str] = None,
    show: bool = True
) -> plt.Figure:
    """
    Plot reliability diagram showing calibration quality.
    
    The reliability diagram plots predicted confidence vs actual accuracy.
    A well-calibrated model should have points close to the diagonal line.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted classes
        confidences: Predicted confidence scores
        n_bins: Number of bins
        title: Plot title
        save_path: Path to save figure
        show: Whether to display the plot
        
    Returns:
        Matplotlib figure
    """
    from ..core.metrics import get_calibration_bins_data, calculate_all_metrics
    
    # Get bin data
    bin_data = get_calibration_bins_data(y_true, y_pred, confidences, n_bins)
    metrics = calculate_all_metrics(y_true, y_pred, confidences, n_bins)
    
    bin_confidences = bin_data["bin_confidences"]
    bin_accuracies = bin_data["bin_accuracies"]
    bin_counts = bin_data["bin_counts"]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot perfect calibration line
    ax.plot([0, 1], [0, 1], 'k--', label='Perfect Calibration', linewidth=2)
    
    # Plot reliability diagram as bar chart
    bar_width = 1.0 / n_bins * 0.8
    colors = plt.cm.RdYlGn(bin_accuracies)
    
    bars = ax.bar(
        bin_confidences,
        bin_accuracies,
        width=bar_width,
        alpha=0.7,
        color=colors,
        edgecolor='black',
        linewidth=1.5,
        label='Actual Accuracy'
    )
    
    # Add gap indicators (difference from diagonal)
    for conf, acc in zip(bin_confidences, bin_accuracies):
        if conf != acc:
            ax.plot([conf, conf], [conf, acc], 'r-', alpha=0.5, linewidth=2)
    
    # Add sample count labels on bars
    for i, (conf, acc, count) in enumerate(zip(bin_confidences, bin_accuracies, bin_counts)):
        if count > 0:
            ax.text(conf, acc + 0.02, f'n={count}', 
                   ha='center', va='bottom', fontsize=8)
    
    # Styling
    ax.set_xlabel('Predicted Confidence', fontsize=12, fontweight='bold')
    ax.set_ylabel('Actual Accuracy', fontsize=12, fontweight='bold')
    
    if title is None:
        title = 'Reliability Diagram (Calibration Plot)'
    
    # Add metrics to title
    title += f"\nECE: {metrics['ece']:.4f} | MCE: {metrics['mce']:.4f} | Accuracy: {metrics['accuracy']:.4f}"
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig


def plot_confidence_histogram(
    confidences: np.ndarray,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    n_bins: int = 20,
    title: Optional[str] = None,
    save_path: Optional[str] = None,
    show: bool = True
) -> plt.Figure:
    """
    Plot histogram of confidence scores, separated by correct/incorrect predictions.
    
    Args:
        confidences: Predicted confidence scores
        y_true: Ground truth labels
        y_pred: Predicted classes
        n_bins: Number of histogram bins
        title: Plot title
        save_path: Path to save figure
        show: Whether to display the plot
        
    Returns:
        Matplotlib figure
    """
    # Separate correct and incorrect predictions
    correct_mask = y_true == y_pred
    conf_correct = confidences[correct_mask]
    conf_incorrect = confidences[~correct_mask]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot histograms
    ax.hist(conf_correct, bins=n_bins, alpha=0.6, color='green', 
            label=f'Correct ({len(conf_correct)} samples)', density=True)
    ax.hist(conf_incorrect, bins=n_bins, alpha=0.6, color='red', 
            label=f'Incorrect ({len(conf_incorrect)} samples)', density=True)
    
    # Add vertical lines for mean confidences
    ax.axvline(np.mean(conf_correct), color='darkgreen', linestyle='--', 
               linewidth=2, label=f'Mean Correct: {np.mean(conf_correct):.3f}')
    ax.axvline(np.mean(conf_incorrect), color='darkred', linestyle='--', 
               linewidth=2, label=f'Mean Incorrect: {np.mean(conf_incorrect):.3f}')
    
    # Styling
    ax.set_xlabel('Confidence Score', fontsize=12, fontweight='bold')
    ax.set_ylabel('Density', fontsize=12, fontweight='bold')
    
    if title is None:
        title = 'Confidence Distribution'
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig


def plot_calibration_comparison(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences_dict: Dict[str, np.ndarray],
    n_bins: int = 10,
    title: Optional[str] = None,
    save_path: Optional[str] = None,
    show: bool = True
) -> plt.Figure:
    """
    Compare calibration across multiple methods.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted classes
        confidences_dict: Dictionary mapping method names to confidence scores
        n_bins: Number of bins
        title: Plot title
        save_path: Path to save figure
        show: Whether to display the plot
        
    Returns:
        Matplotlib figure
    """
    from ..core.metrics import get_calibration_bins_data, calculate_all_metrics
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot perfect calibration
    ax.plot([0, 1], [0, 1], 'k--', label='Perfect Calibration', linewidth=2)
    
    # Plot each method
    colors = plt.cm.tab10(np.linspace(0, 1, len(confidences_dict)))
    
    for (method_name, confidences), color in zip(confidences_dict.items(), colors):
        bin_data = get_calibration_bins_data(y_true, y_pred, confidences, n_bins)
        metrics = calculate_all_metrics(y_true, y_pred, confidences, n_bins)
        
        bin_confidences = bin_data["bin_confidences"]
        bin_accuracies = bin_data["bin_accuracies"]
        
        # Plot line
        ax.plot(bin_confidences, bin_accuracies, 'o-', color=color, 
                linewidth=2, markersize=8, alpha=0.7,
                label=f'{method_name} (ECE: {metrics["ece"]:.4f})')
    
    # Styling
    ax.set_xlabel('Predicted Confidence', fontsize=12, fontweight='bold')
    ax.set_ylabel('Actual Accuracy', fontsize=12, fontweight='bold')
    
    if title is None:
        title = 'Calibration Comparison Across Methods'
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig


def plot_calibration_curve_with_histogram(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    confidences: np.ndarray,
    n_bins: int = 10,
    title: Optional[str] = None,
    save_path: Optional[str] = None,
    show: bool = True
) -> plt.Figure:
    """
    Plot reliability diagram with confidence histogram below.
    
    Args:
        y_true: Ground truth labels
        y_pred: Predicted classes
        confidences: Predicted confidence scores
        n_bins: Number of bins
        title: Plot title
        save_path: Path to save figure
        show: Whether to display the plot
        
    Returns:
        Matplotlib figure
    """
    from ..core.metrics import get_calibration_bins_data, calculate_all_metrics
    
    # Get data
    bin_data = get_calibration_bins_data(y_true, y_pred, confidences, n_bins)
    metrics = calculate_all_metrics(y_true, y_pred, confidences, n_bins)
    
    # Create figure with subplots
    fig = plt.figure(figsize=(12, 10))
    gs = fig.add_gridspec(3, 1, height_ratios=[2, 1, 0.5], hspace=0.3)
    
    # Top: Reliability diagram
    ax1 = fig.add_subplot(gs[0])
    ax1.plot([0, 1], [0, 1], 'k--', label='Perfect Calibration', linewidth=2)
    
    bin_confidences = bin_data["bin_confidences"]
    bin_accuracies = bin_data["bin_accuracies"]
    bin_counts = bin_data["bin_counts"]
    
    colors = plt.cm.RdYlGn(bin_accuracies)
    bar_width = 1.0 / n_bins * 0.8
    
    ax1.bar(bin_confidences, bin_accuracies, width=bar_width, alpha=0.7,
            color=colors, edgecolor='black', linewidth=1.5)
    
    ax1.set_ylabel('Actual Accuracy', fontsize=12, fontweight='bold')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    if title:
        ax1.set_title(title, fontsize=14, fontweight='bold', pad=10)
    
    # Middle: Confidence histogram
    ax2 = fig.add_subplot(gs[1])
    ax2.hist(confidences, bins=30, alpha=0.7, color='steelblue', edgecolor='black')
    ax2.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Confidence Score', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Bottom: Metrics text
    ax3 = fig.add_subplot(gs[2])
    ax3.axis('off')
    
    metrics_text = (
        f"ECE: {metrics['ece']:.4f}  |  "
        f"MCE: {metrics['mce']:.4f}  |  "
        f"ACE: {metrics['ace']:.4f}  |  "
        f"Accuracy: {metrics['accuracy']:.4f}  |  "
        f"Samples: {metrics['num_samples']}"
    )
    
    ax3.text(0.5, 0.5, metrics_text, ha='center', va='center',
             fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig


def plot_eu_ai_act_dashboard(
    evaluation_result: Dict,
    save_path: Optional[str] = None,
    show: bool = True
) -> plt.Figure:
    """
    Create EU AI Act compliance dashboard visualization.
    
    Args:
        evaluation_result: Result from CalibrationAnalyzer.evaluate()
        save_path: Path to save figure
        show: Whether to display the plot
        
    Returns:
        Matplotlib figure
    """
    metrics = evaluation_result["metrics"]
    assessment = evaluation_result["assessment"]
    bin_data = evaluation_result["bin_data"]
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
    
    # 1. Calibration Status
    ax1 = fig.add_subplot(gs[0, 0])
    status_colors = {
        "well_calibrated": "green",
        "moderately_calibrated": "orange",
        "poorly_calibrated": "red"
    }
    status_color = status_colors.get(assessment["status"], "gray")
    
    ax1.text(0.5, 0.6, assessment["status"].replace("_", " ").title(),
             ha='center', va='center', fontsize=16, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor=status_color, alpha=0.3))
    ax1.text(0.5, 0.3, f"ECE: {metrics['ece']:.4f}\nMCE: {metrics['mce']:.4f}",
             ha='center', va='center', fontsize=12)
    ax1.set_title('Calibration Status\n(safety-001)', fontweight='bold')
    ax1.axis('off')
    
    # 2. Metrics Overview
    ax2 = fig.add_subplot(gs[0, 1])
    metric_names = ['ECE', 'MCE', 'ACE', 'Accuracy']
    metric_values = [
        metrics['ece'],
        metrics['mce'],
        metrics['ace'],
        metrics['accuracy']
    ]
    bars = ax2.barh(metric_names, metric_values, color='steelblue', alpha=0.7)
    ax2.set_xlim(0, 1)
    ax2.set_xlabel('Score', fontweight='bold')
    ax2.set_title('Key Metrics\n(tech-004)', fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for i, (name, val) in enumerate(zip(metric_names, metric_values)):
        ax2.text(val + 0.02, i, f'{val:.4f}', va='center')
    
    # 3. Trust Score
    ax3 = fig.add_subplot(gs[0, 2])
    trust_score = (1 - metrics['ece']) * 100  # Simple trust score
    
    wedges, texts = ax3.pie(
        [trust_score, 100 - trust_score],
        colors=['#2ecc71', '#ecf0f1'],
        startangle=90,
        counterclock=False
    )
    
    ax3.text(0, 0, f'{trust_score:.1f}%',
             ha='center', va='center', fontsize=20, fontweight='bold')
    ax3.set_title('Trust Score\n(trust-001)', fontweight='bold')
    
    # 4. Reliability Diagram
    ax4 = fig.add_subplot(gs[1, :2])
    ax4.plot([0, 1], [0, 1], 'k--', linewidth=2, alpha=0.5)
    
    bin_confidences = bin_data["bin_confidences"]
    bin_accuracies = bin_data["bin_accuracies"]
    
    colors = plt.cm.RdYlGn(bin_accuracies)
    bar_width = 1.0 / len(bin_confidences) * 0.8
    
    ax4.bar(bin_confidences, bin_accuracies, width=bar_width,
            alpha=0.7, color=colors, edgecolor='black')
    ax4.set_xlabel('Predicted Confidence', fontweight='bold')
    ax4.set_ylabel('Actual Accuracy', fontweight='bold')
    ax4.set_title('Reliability Diagram (tech-004)', fontweight='bold')
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.grid(True, alpha=0.3)
    
    # 5. Compliance Summary
    ax5 = fig.add_subplot(gs[1, 2])
    requirements = ['tech-004', 'safety-001', 'safety-002', 'trust-001']
    compliance_status = [1, 1 if assessment["well_calibrated"] else 0.5, 1, 1 if assessment["well_calibrated"] else 0.7]
    
    bars = ax5.barh(requirements, compliance_status, color=['green' if s >= 1 else 'orange' for s in compliance_status])
    ax5.set_xlim(0, 1.2)
    ax5.set_xlabel('Compliance', fontweight='bold')
    ax5.set_title('EU AI Act Compliance\n(safety-002)', fontweight='bold')
    ax5.grid(True, alpha=0.3, axis='x')
    
    # Add status labels
    for i, (req, status) in enumerate(zip(requirements, compliance_status)):
        label = '✓' if status >= 1 else '⚠'
        ax5.text(status + 0.05, i, label, va='center', fontsize=14)
    
    # Main title
    fig.suptitle('EU AI Act Calibration Compliance Dashboard',
                 fontsize=18, fontweight='bold', y=0.98)
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig
