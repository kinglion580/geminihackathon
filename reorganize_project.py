#!/usr/bin/env python3
"""
Project Reorganization Script
Tổ chức lại toàn bộ repo theo cấu trúc mới:

NEW STRUCTURE:
geminihackathon/
├── skills/                     # ALL skills consolidated here
│   ├── ai-governance/
│   ├── risk-assessment/
│   └── ...
│
├── testing/                    # Testing models & CLIs
│   ├── ai_act_cli.py
│   ├── lisa_rag.py
│   ├── bias_testing.py
│   └── ...
│
├── datasets/                   # All data files
│   ├── articles/
│   ├── AI_Act_datapoints/
│   ├── Questionnaires/
│   └── ...
│
├── outputs/                    # All output folders
│   ├── Output/
│   ├── incidents/
│   ├── bias_test_results/
│   └── ...
│
├── agents/                     # Agent implementations
│   └── governance_agent/
│
├── config/                     # Configuration files
│   ├── grafana_config/
│   └── ...
│
├── docs/                       # Documentation
│   ├── README.md
│   ├── SETUP.md
│   └── ...
│
└── utils/                      # Utility scripts
    ├── download_from_list.py
    └── ...
"""

import os
import shutil
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).parent

# Define new structure mapping
STRUCTURE = {
    # Skills - consolidate all
    "skills": {
        "sources": [
            "AI Act skills packages/AI Act package/ai-ethics",
            "AI Act skills packages/AI Act package/ai-ethics-advisor",
            "AI Act skills packages/AI Act package/ai-governance",
            "AI Act skills packages/AI Act package/ai-performance-testing",
            "AI Act skills packages/AI Act package/ai-safety-planning",
            "AI Act skills packages/AI Act package/ai-testing",
            "AI Act skills packages/AI Act package/automatic-logging",
            "AI Act skills packages/AI Act package/deployer-training",
            "AI Act skills packages/AI Act package/downstream-notifier",
            "AI Act skills packages/AI Act package/fact-checker",
            "AI Act skills packages/AI Act package/incident-responder",
            "AI Act skills packages/AI Act package/multilingual-localization",
            "AI Act skills packages/AI Act package/risk-assessment",
            "AI Act skills packages/AI Act package/standards-compliance-interoperability",
            "AI Act skills packages/AI Act package/validating-ai-ethics-and-fairness",
            "AI Act skills packages/ai-ml-planning/skills",
            "AI Act skills packages/compliance-planning/skills",
            "AI Act skills packages/google-ecosystem/skills",
            "AI Act skills packages/ai-ethics",
            "AI Act skills packages/ai-ethics-advisor",
            "Risks packages/Cybersecurity",
            "Risks packages/EU AI Act Compliance",
            "Risks packages/Environment",
            "Risks packages/Fundamental Rights",
            "Risks packages/Health & Safety",
            "Risks packages/Societal",
            "Risks packages/Technical",
            "Risks packages/Third-Party",
            "Risks packages/Trust",
        ],
        "type": "merge_skills"
    },

    # Testing models & CLIs
    "testing": {
        "sources": [
            "ai_act_cli.py",
            "ai_risk_classifier.py",
            "bias_testing.py",
            "bias_testing_cli.py",
            "change_management_cli.py",
            "human_oversight_cli.py",
            "incident_cli.py",
            "cybersecurity_assessment.py",
            "query_ai_act.py",
            "autofill/lisa_rag.py",
            "autofill/run_mock_tests.py",
            "demo_change_management.py",
            "demo_cybersecurity_performance.py",
            "demo_incident.py",
            "demo_security_monitoring.py",
            "test_critical_alert_detector.py",
        ],
        "type": "copy"
    },

    # Datasets
    "datasets": {
        "sources": [
            "articles",
            "AI_Act_datapoints",
            "Questionnaires",
            "AI_Risk_Assessment_Guide.xlsx",
            "EU_AI_Act_Regulation_2024_1689.html",
        ],
        "type": "copy"
    },

    # Outputs
    "outputs": {
        "sources": [
            "Output",
            "incidents",
            "bias_test_results",
            "change_management",
            "risk_analysis_accessibility",
        ],
        "type": "copy"
    },

    # Agents
    "agents": {
        "sources": [
            "AI Act skills packages/AI Act package/agents",
        ],
        "type": "copy"
    },

    # Config
    "config": {
        "sources": [
            "grafana_config",
            "pmm_system",
            "AI Act skills packages/compliance_checklist_high_risk.yaml",
        ],
        "type": "copy"
    },

    # Docs
    "docs": {
        "sources": [
            "README.md",
            "SETUP.md",
            "SETUP_REPORT.md",
            "AGENTS.md",
            "incident_management.md",
            "AI Act skills packages/AI_ACT_COMPLIANCE_GUIDE.md",
            "AI Act skills packages/AI_ETHICS_ASSESSMENT_ai_act_cli.md",
            "AI Act skills packages/AI_SAFETY_PLAN_ai_act_cli.md",
            "AI Act skills packages/model_card_template.md",
        ],
        "type": "copy"
    },

    # Utils
    "utils": {
        "sources": [
            "download_from_list.py",
            "download_github_tools.py",
            "download_risk_tools.py",
            "setup_ai_act_store.py",
            "finalize_skill_setup.py",
            "check_key.py",
            "AI Act skills packages/md_to_pdf.py",
        ],
        "type": "copy"
    },

    # Core modules (keep at root or move to src/)
    "src": {
        "sources": [
            "change_management.py",
            "human_oversight.py",
            "incident_management.py",
            "security_monitoring.py",
            "critical_alert_detector.py",
            "alert_webhook_handler.py",
            "metrics_exporter.py",
            "eu_ai_act_metrics.py",
            "batch_fact_checker.py",
            "analyze_high_risk_gaps.py",
            "security_input.py",
        ],
        "type": "copy"
    },
}


def copy_item(src: Path, dest: Path, is_dir: bool = False):
    """Copy file or directory"""
    try:
        if not src.exists():
            print(f"  ⚠️  Not found: {src}")
            return False

        if dest.exists():
            print(f"  ⏭️  Already exists: {dest.name}")
            return False

        if is_dir or src.is_dir():
            shutil.copytree(src, dest)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def merge_skills(sources: list, dest_dir: Path):
    """Merge skills from multiple sources, handling duplicates"""
    dest_dir.mkdir(parents=True, exist_ok=True)
    existing = set(d.name for d in dest_dir.iterdir() if d.is_dir())
    copied = 0

    for src_path in sources:
        src = PROJECT_ROOT / src_path
        if not src.exists():
            print(f"  ⚠️  Not found: {src_path}")
            continue

        if src.is_dir():
            # Check if it's a skills container or a single skill
            skill_md = src / "SKILL.md"
            if skill_md.exists():
                # Single skill directory
                skill_name = src.name
                if skill_name in existing:
                    # Find unique name
                    counter = 2
                    while f"{skill_name}-{counter}" in existing:
                        counter += 1
                    skill_name = f"{skill_name}-{counter}"

                dest = dest_dir / skill_name
                if copy_item(src, dest, is_dir=True):
                    existing.add(skill_name)
                    copied += 1
                    print(f"  ✅ {src.name} -> {skill_name}")
            else:
                # Container with multiple skills inside
                for item in src.iterdir():
                    if item.is_dir() and (item / "SKILL.md").exists():
                        skill_name = item.name
                        if skill_name in existing:
                            counter = 2
                            while f"{skill_name}-{counter}" in existing:
                                counter += 1
                            skill_name = f"{skill_name}-{counter}"

                        dest = dest_dir / skill_name
                        if copy_item(item, dest, is_dir=True):
                            existing.add(skill_name)
                            copied += 1
                            print(f"  ✅ {item.name} -> {skill_name}")

    return copied


def main():
    print("=" * 70)
    print("PROJECT REORGANIZATION")
    print("=" * 70)
    print(f"\nProject root: {PROJECT_ROOT}")
    print()

    stats = {"copied": 0, "skipped": 0, "errors": 0}

    for folder_name, config in STRUCTURE.items():
        print(f"\n{'='*50}")
        print(f"📁 Creating: {folder_name}/")
        print(f"{'='*50}")

        dest_dir = PROJECT_ROOT / folder_name

        if config["type"] == "merge_skills":
            # Special handling for skills
            count = merge_skills(config["sources"], dest_dir)
            stats["copied"] += count

        elif config["type"] == "copy":
            dest_dir.mkdir(parents=True, exist_ok=True)

            for src_path in config["sources"]:
                src = PROJECT_ROOT / src_path
                dest = dest_dir / Path(src_path).name

                print(f"  📄 {src_path}")
                if copy_item(src, dest):
                    stats["copied"] += 1
                else:
                    stats["skipped"] += 1

    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"✅ Copied: {stats['copied']}")
    print(f"⏭️  Skipped: {stats['skipped']}")

    # Save mapping
    mapping_file = PROJECT_ROOT / "reorganization_mapping.json"
    with open(mapping_file, 'w') as f:
        json.dump(STRUCTURE, f, indent=2)
    print(f"\n📄 Mapping saved to: {mapping_file}")

    print(f"\n{'='*70}")
    print("NEW STRUCTURE:")
    print(f"{'='*70}")
    for folder in STRUCTURE.keys():
        folder_path = PROJECT_ROOT / folder
        if folder_path.exists():
            count = len(list(folder_path.iterdir()))
            print(f"  📁 {folder}/ ({count} items)")


if __name__ == "__main__":
    main()
