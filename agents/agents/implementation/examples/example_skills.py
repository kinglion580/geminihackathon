"""
Example: Working with Skills

This example demonstrates how to discover, load, and work with skills.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from governance_agent import GovernanceAIAgent


def main():
    print("="*80)
    print("Example 3: Working with Skills")
    print("="*80)

    # Initialize the agent
    print("\n1. Initializing Governance AI Agent...")
    agent = GovernanceAIAgent()
    print(f"   ✓ Agent initialized")

    # List all available skills
    print("\n2. Listing available skills...")
    skills = agent.list_available_skills()
    print(f"\n   Total available skills: {len(skills)}")

    # Group skills by category
    packages = {
        "AI Act Package": [],
        "AI/ML Planning": [],
        "Compliance Planning": [],
        "Google Ecosystem": []
    }

    for skill in skills:
        skill_obj = agent.skills.get(skill)
        if skill_obj:
            path = skill_obj.path
            if "AI Act package" in path:
                packages["AI Act Package"].append(skill)
            elif "ai-ml-planning" in path:
                packages["AI/ML Planning"].append(skill)
            elif "compliance-planning" in path:
                packages["Compliance Planning"].append(skill)
            elif "google-ecosystem" in path:
                packages["Google Ecosystem"].append(skill)

    for package, skills_list in packages.items():
        if skills_list:
            print(f"\n   {package} ({len(skills_list)} skills):")
            for skill in sorted(skills_list)[:3]:  # Show first 3
                print(f"     • {skill}")
            if len(skills_list) > 3:
                print(f"     ... and {len(skills_list) - 3} more")

    # Get description of specific skills
    print("\n3. Getting skill descriptions...")
    example_skills = ["risk-assessment", "ai-safety-planning", "gdpr-compliance"]

    for skill_name in example_skills:
        desc = agent.get_skill_description(skill_name)
        if desc:
            print(f"\n   • {skill_name}")
            print(f"     {desc[:100]}...")

    # Load skills
    print("\n4. Loading skills...")
    for skill_name in ["risk-assessment", "ai-governance"]:
        success = agent.load_skill(skill_name)
        if success:
            print(f"   ✓ Loaded: {skill_name}")

    # List loaded skills
    print("\n5. Currently loaded skills:")
    for skill in agent.loaded_skills:
        print(f"   • {skill}")

    # Get skill content
    print("\n6. Getting skill content...")
    skill_content = agent.get_skill_content("risk-assessment")
    if skill_content:
        print(f"\n   risk-assessment content (first 200 chars):")
        print(f"   {skill_content[:200]}...")

    # Demonstrate skill recommendation
    print("\n7. Getting skill recommendations based on use case...")
    use_case = "Healthcare AI system for diagnostic support"
    assessment = agent.assess_ai_system(use_case)

    print(f"\n   Use case: {use_case}")
    print("\n   Recommended skills:")
    for rec in assessment['recommended_skills']:
        print(f"     • {rec['skill']}: {rec['reason']}")

    print("\n" + "="*80)
    print("Example Complete!")
    print("="*80)


if __name__ == "__main__":
    main()
