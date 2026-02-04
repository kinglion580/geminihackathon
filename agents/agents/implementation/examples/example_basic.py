"""
Basic Example: Using the Governance AI Agent

This example demonstrates basic usage of the Governance AI Agent
for assessing an AI system and getting recommendations.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from governance_agent import GovernanceAIAgent


def main():
    print("="*80)
    print("Example 1: Basic Assessment")
    print("="*80)

    # Initialize the agent
    print("\n1. Initializing Governance AI Agent...")
    agent = GovernanceAIAgent()
    print(f"   ✓ Agent initialized with {len(agent.skills)} skills")

    # Assess an AI system
    print("\n2. Assessing an AI system...")
    system_description = """
    A customer service chatbot powered by an LLM that helps users with
    product inquiries, order tracking, and basic troubleshooting. The
    system interacts directly with customers via web chat and mobile app.
    """

    assessment = agent.assess_ai_system(system_description.strip())

    # Display results
    print("\n" + "="*80)
    print("ASSESSMENT RESULTS")
    print("="*80)

    print(f"\nRisk Classification: {assessment['risk_classification']['category']}")
    print(f"Confidence: {assessment['risk_classification']['confidence']}")
    print(f"Reasoning: {assessment['risk_classification']['reasoning']}")

    print("\nApplicable Regulations:")
    for reg in assessment['applicable_regulations']:
        print(f"  • {reg['name']}: {reg['reason']}")

    print("\nRecommended Skills to Load:")
    for rec in assessment['recommended_skills']:
        print(f"  • {rec['skill']}")
        print(f"    Reason: {rec['reason']}")

    # Load a recommended skill
    print("\n3. Loading a skill...")
    if assessment['recommended_skills']:
        skill_name = assessment['recommended_skills'][0]['skill']
        agent.load_skill(skill_name)
        print(f"   ✓ Loaded: {skill_name}")

    # List loaded skills
    print("\n4. Currently loaded skills:")
    for skill in agent.loaded_skills:
        print(f"   • {skill}")

    print("\n" + "="*80)
    print("Example Complete!")
    print("="*80)


if __name__ == "__main__":
    main()
