"""
Example: Generating a Comprehensive Governance Plan

This example demonstrates how to generate a complete governance plan
for an AI system.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from governance_agent import GovernanceAIAgent


def main():
    print("="*80)
    print("Example 2: Generating Governance Plan")
    print("="*80)

    # Initialize the agent
    print("\n1. Initializing Governance AI Agent...")
    agent = GovernanceAIAgent()
    print(f"   ✓ Agent initialized")

    # Define system profile
    print("\n2. Defining system profile...")
    system_profile = {
        "purpose": "Automated credit scoring for loan applications",
        "type": "Machine Learning Classification Model",
        "users": "Loan officers and automated underwriting systems",
        "data": "Credit history, employment data, financial records, personal information",
        "geography": "European Union and United States"
    }

    print("\n   System Profile:")
    for key, value in system_profile.items():
        print(f"     {key.title()}: {value}")

    # Generate governance plan
    print("\n3. Generating comprehensive governance plan...")
    plan = agent.generate_governance_plan(system_profile)

    # Display plan summary
    print("\n" + "="*80)
    print("GOVERNANCE PLAN SUMMARY")
    print("="*80)

    print("\nExecutive Summary:")
    print(plan['executive_summary'])

    print(f"\nRisk Classification: {plan['risk_assessment']['category']}")
    print(f"Reasoning: {plan['risk_assessment']['reasoning']}")

    print("\nApplicable Regulations:")
    for reg in plan['compliance_requirements']:
        print(f"  • {reg['name']}")
        print(f"    Reason: {reg['reason']}")

    print("\nArchitecture Recommendations:")
    print("\n  Data Pipeline:")
    for item in plan['architecture_recommendations']['data_pipeline']:
        print(f"    • {item}")

    print("\n  Monitoring:")
    for item in plan['architecture_recommendations']['monitoring']:
        print(f"    • {item}")

    print("\nSafety Implementation:")
    print("\n  Input Guards:")
    for guard in plan['safety_implementation']['guardrails']['input_guards']:
        print(f"    • {guard}")

    print("\n  Output Filters:")
    for filter_item in plan['safety_implementation']['guardrails']['output_filters']:
        print(f"    • {filter_item}")

    print("\nTesting Strategy:")
    print("\n  Pre-Launch Tests:")
    for test in plan['testing_strategy']['pre_launch'][:3]:
        print(f"    • {test}")

    print("\nNext Steps:")
    for phase in plan['next_steps']:
        print(f"\n  {phase['phase']}:")
        for task in phase['tasks']:
            print(f"    • {task}")

    # Export plan
    print("\n4. Exporting plan...")
    output_file = "governance_plan_example.json"
    with open(output_file, 'w') as f:
        json.dump(plan, f, indent=2)
    print(f"   ✓ Plan exported to {output_file}")

    # Export as markdown
    print("\n5. Exporting as markdown...")
    markdown_file = "governance_plan_example.md"
    with open(markdown_file, 'w') as f:
        f.write("# AI Governance Plan\n\n")
        f.write(agent.export_assessment(plan, format="markdown"))
    print(f"   ✓ Markdown exported to {markdown_file}")

    print("\n" + "="*80)
    print("Example Complete!")
    print("="*80)


if __name__ == "__main__":
    main()
