#!/usr/bin/env python3
"""
Download GitHub repositories organized by category and tool name.
"""

import os
import subprocess
from pathlib import Path

# Base directory
BASE_DIR = Path("github download")

# Tools data: {category: [(tool_name, github_url), ...]}
TOOLS = {
    "Cybersecurity": [
        ("Prompt Injection Detector", "https://github.com/protectai/rebuff"),
    ],
    "Environment": [
        ("CodeCarbon", "https://github.com/mlco2/codecarbon"),
        ("ML CO2 Impact Calculator", "https://mlco2.github.io/impact/"),
        ("Cloud Carbon Footprint", "https://github.com/cloud-carbon-footprint/cloud-carbon-footprint"),
        ("WattTime Carbon Calculator", "https://api.watttime.org/"),
    ],
    "Technical": [
        ("Evidently AI", "https://github.com/evidentlyai/evidently"),
        ("Alibi Detect", "https://github.com/SeldonIO/alibi-detect"),
        ("RAGAS", "https://github.com/explodinggradients/ragas"),
        ("Deepeval", "https://github.com/confident-ai/deepeval"),
        ("Hugging Face Evaluate", "https://github.com/huggingface/evaluate"),
        ("LangSmith", "https://smith.langchain.com/"),
        ("Weights & Biases", "https://wandb.ai/"),
        ("Promptfoo", "https://github.com/promptfoo/promptfoo"),
    ],
    "Trust": [
        ("SHAP Explainer", "https://github.com/slundberg/shap"),
        ("LIME", "https://github.com/marcotcr/lime"),
        ("Captum", "https://github.com/pytorch/captum"),
        ("InterpretML", "https://github.com/interpretml/interpret"),
        ("What-If Tool", "https://github.com/PAIR-code/what-if-tool"),
        ("Axe Accessibility", "https://github.com/dequelabs/axe-core"),
    ],
    "Fundamental Rights": [
        ("AI Fairness 360", "https://github.com/Trusted-AI/AIF360"),
        ("Fairlearn", "https://github.com/fairlearn/fairlearn"),
        ("Aequitas", "https://github.com/dssg/aequitas"),
        ("Perspective API", "https://perspectiveapi.com/"),
        ("Moderate Content API", "https://api.openai.com/v1/moderations"),
        ("Disaggregated Evaluation", "https://github.com/Trusted-AI/AIF360"),
    ],
    "Societal": [
        ("Perspective API", "https://perspectiveapi.com/"),
        ("Detoxify", "https://github.com/unitaryai/detoxify"),
        ("Claimbuster API", "https://idir.uta.edu/claimbuster/api/"),
        ("TextBlob Sentiment", "https://github.com/sloria/TextBlob"),
        ("VADER Sentiment", "https://github.com/cjhutto/vaderSentiment"),
        ("Hate Speech Detector", "https://github.com/Hironsan/HateSonar"),
        ("AI Content Detector", ""),
    ],
    "Third-Party": [
        ("Snyk.io", "https://snyk.io/"),
        ("Safety (PyUp)", "https://github.com/pyupio/safety"),
        ("npm audit", ""),
        ("Syft SBOM Generator", "https://github.com/anchore/syft"),
        ("Grype Vulnerability Scanner", "https://github.com/anchore/grype"),
        ("OSS Scorecard", "https://github.com/ossf/scorecard"),
        ("License Checker", "https://github.com/iweb/scancode-toolkit"),
    ],
    "Health & Safety": [
        ("Conformance Calibration", "https://github.com/uncertainty-toolbox/uncertainty-toolbox"),
    ],
    "EU AI Act Compliance": [
        ("Model Cards Generator", "https://huggingface.co/docs/hub/model-cards"),
        ("AI System Registry", "https://ec.europa.eu/"),
        ("Model Card Generation Generator", "https://github.com/mkdocs/mkdocs"),
        ("AI Transparency Labels", "https://openprompts.ai/label/"),
        ("Quality Management System (QMS) Tracker", "https://linkiso.com/"),
        ("AI Logging System", "https://grafana.com/oss/loki/"),
        ("CE Marking Generator", "https://ce-marking.help/"),
    ],
}


def is_github_repo(url):
    """Check if URL is a GitHub repository."""
    return url.startswith("https://github.com/") and len(url.split("/")) >= 5


def clone_repo(repo_url, target_dir):
    """Clone a GitHub repository to target directory."""
    try:
        print(f"  Cloning {repo_url}...")
        result = subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, str(target_dir)],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print(f"  ✓ Successfully cloned to {target_dir}")
            return True
        else:
            print(f"  ✗ Failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout cloning {repo_url}")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Main download function."""
    print("=" * 80)
    print("GitHub Repository Downloader")
    print("=" * 80)
    print()

    # Create base directory
    BASE_DIR.mkdir(exist_ok=True)

    total_repos = 0
    successful = 0
    skipped = 0
    failed = 0

    for category, tools in TOOLS.items():
        print(f"\n{'=' * 80}")
        print(f"Category: {category}")
        print(f"{'=' * 80}")

        # Create category folder
        category_dir = BASE_DIR / category
        category_dir.mkdir(exist_ok=True)

        for tool_name, github_url in tools:
            print(f"\n[{tool_name}]")

            # Create tool folder
            tool_dir = category_dir / tool_name
            tool_dir.mkdir(exist_ok=True)

            if not github_url:
                print(f"  ⊘ No GitHub URL provided - skipping")
                skipped += 1
                continue

            if not is_github_repo(github_url):
                print(f"  ⊘ Not a GitHub repository: {github_url}")
                # Create a reference file instead
                ref_file = tool_dir / "URL_REFERENCE.txt"
                ref_file.write_text(f"Tool: {tool_name}\nURL: {github_url}\n")
                print(f"  → Created reference file")
                skipped += 1
                continue

            total_repos += 1

            # Check if already cloned
            if (tool_dir / ".git").exists() or len(list(tool_dir.iterdir())) > 0:
                print(f"  ⊙ Already exists - skipping")
                successful += 1
                continue

            # Clone the repository
            if clone_repo(github_url, tool_dir):
                successful += 1
            else:
                failed += 1
                # Create a reference file as fallback
                ref_file = tool_dir / "URL_REFERENCE.txt"
                ref_file.write_text(f"Tool: {tool_name}\nURL: {github_url}\nStatus: Failed to clone\n")

    # Summary
    print("\n" + "=" * 80)
    print("DOWNLOAD SUMMARY")
    print("=" * 80)
    print(f"Total GitHub repos: {total_repos}")
    print(f"✓ Successfully downloaded: {successful}")
    print(f"⊘ Skipped (not GitHub/no URL): {skipped}")
    print(f"✗ Failed: {failed}")
    print(f"\nAll files organized in: {BASE_DIR.absolute()}")
    print("=" * 80)


if __name__ == "__main__":
    main()
