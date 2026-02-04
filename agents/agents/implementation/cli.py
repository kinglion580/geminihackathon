"""
Command Line Interface for Governance AI Agent

Provides an interactive CLI for using the Governance AI Agent.
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional

from governance_agent import GovernanceAIAgent, AgentConfig


def interactive_mode(agent: GovernanceAIAgent):
    """Run agent in interactive chat mode"""
    print("\n" + "="*80)
    print("Governance AI Agent - Interactive Mode")
    print("="*80)
    print("\nType 'help' for available commands, 'exit' to quit\n")

    commands = {
        "help": "Show available commands",
        "skills": "List all available skills",
        "load <skill>": "Load a specific skill",
        "assess": "Assess an AI system",
        "plan": "Generate a governance plan",
        "export": "Export last assessment/plan",
        "clear": "Clear conversation history",
        "exit": "Exit the program"
    }

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() == "exit":
                print("\nGoodbye!")
                break

            elif user_input.lower() == "help":
                print("\nAvailable Commands:")
                for cmd, desc in commands.items():
                    print(f"  {cmd:20} - {desc}")
                continue

            elif user_input.lower() == "skills":
                skills = agent.list_available_skills()
                print(f"\nAvailable Skills ({len(skills)}):")
                for i, skill in enumerate(skills, 1):
                    desc = agent.get_skill_description(skill)
                    print(f"\n{i}. {skill}")
                    if desc:
                        print(f"   {desc[:100]}...")
                continue

            elif user_input.lower().startswith("load "):
                skill_name = user_input[5:].strip()
                if agent.load_skill(skill_name):
                    print(f"\n✓ Skill '{skill_name}' loaded successfully")
                    print(f"\nDescription: {agent.get_skill_description(skill_name)}")
                else:
                    print(f"\n✗ Failed to load skill '{skill_name}'")
                continue

            elif user_input.lower() == "assess":
                print("\nPlease describe the AI system you want to assess:")
                system_desc = input("System description: ").strip()
                if system_desc:
                    print("\nAnalyzing...")
                    assessment = agent.assess_ai_system(system_desc)
                    print(f"\n{assessment['initial_assessment']}")

                    print("\n\nRecommended Skills:")
                    for rec in assessment['recommended_skills']:
                        print(f"  • {rec['skill']}: {rec['reason']}")
                continue

            elif user_input.lower() == "plan":
                print("\nGenerate Governance Plan")
                print("Please provide the following information:")

                purpose = input("System purpose: ").strip()
                sys_type = input("System type (LLM/ML/Agent/etc.): ").strip()
                users = input("Target users: ").strip()
                data = input("Data types processed: ").strip()
                geography = input("Deployment geography: ").strip()

                system_profile = {
                    "purpose": purpose,
                    "type": sys_type,
                    "users": users,
                    "data": data,
                    "geography": geography
                }

                print("\nGenerating comprehensive governance plan...")
                plan = agent.generate_governance_plan(system_profile)

                print("\n" + "="*80)
                print("GOVERNANCE PLAN")
                print("="*80)
                print(agent.export_assessment(plan, format="markdown"))

                # Offer to export
                export_choice = input("\nWould you like to export this plan? (y/n): ").strip().lower()
                if export_choice == 'y':
                    filename = input("Enter filename (default: governance_plan.json): ").strip()
                    if not filename:
                        filename = "governance_plan.json"

                    with open(filename, 'w') as f:
                        json.dump(plan, f, indent=2)
                    print(f"\n✓ Plan exported to {filename}")

                continue

            elif user_input.lower() == "clear":
                agent.conversation_history = []
                print("\n✓ Conversation history cleared")
                continue

            # Regular chat
            response = agent.chat(user_input)
            print(f"\nAgent: {response}")

        except KeyboardInterrupt:
            print("\n\nUse 'exit' to quit")
            continue
        except Exception as e:
            print(f"\nError: {e}")
            continue


def assess_mode(agent: GovernanceAIAgent, description: str, output: Optional[str] = None, output_format: str = 'json'):
    """Run assessment mode"""
    print("\nAssessing AI System...")
    print("="*80)

    assessment = agent.assess_ai_system(description)

    print(assessment['initial_assessment'])
    print("\nRecommended Skills:")
    for rec in assessment['recommended_skills']:
        print(f"  • {rec['skill']}: {rec['reason']}")

    if output:
        # Normalize format
        fmt = 'markdown' if output_format in ['md', 'markdown'] else output_format

        # Auto-detect format from extension if not specified
        if output_format == 'json' and output.endswith('.md'):
            fmt = 'markdown'
        elif output_format == 'json' and (output.endswith('.yaml') or output.endswith('.yml')):
            fmt = 'yaml'

        # Export in requested format
        content = agent.export_assessment(assessment, format=fmt)

        with open(output, 'w') as f:
            f.write(content)
        print(f"\n✓ Assessment exported to {output} ({fmt} format)")


def plan_mode(agent: GovernanceAIAgent, config_file: str, output: Optional[str] = None, output_format: str = 'json'):
    """Generate governance plan from config file"""
    print("\nGenerating Governance Plan...")
    print("="*80)

    # Load system profile from config
    with open(config_file, 'r') as f:
        if config_file.endswith('.json'):
            system_profile = json.load(f)
        elif config_file.endswith('.yaml') or config_file.endswith('.yml'):
            import yaml
            system_profile = yaml.safe_load(f)
        else:
            print("Error: Config file must be JSON or YAML")
            return

    plan = agent.generate_governance_plan(system_profile)

    # Print summary
    print(plan['executive_summary'])
    print("\nRisk Classification:", plan['risk_assessment']['category'])
    print("\nApplicable Regulations:")
    for reg in plan['compliance_requirements']:
        print(f"  • {reg['name']}: {reg['reason']}")

    # Determine output format
    fmt = 'markdown' if output_format in ['md', 'markdown'] else output_format

    # Default filename based on format
    if output:
        output_file = output
    else:
        ext = '.md' if fmt == 'markdown' else '.yaml' if fmt == 'yaml' else '.json'
        output_file = f"governance_plan{ext}"

    # Auto-detect format from extension if not specified
    if output_format == 'json':
        if output_file.endswith('.md'):
            fmt = 'markdown'
        elif output_file.endswith('.yaml') or output_file.endswith('.yml'):
            fmt = 'yaml'

    # Export plan
    content = agent.export_assessment(plan, format=fmt)
    with open(output_file, 'w') as f:
        f.write(content)
    print(f"\n✓ Full plan exported to {output_file} ({fmt} format)")


def skills_mode(agent: GovernanceAIAgent, skill_name: Optional[str] = None):
    """List or describe skills"""
    if skill_name:
        desc = agent.get_skill_description(skill_name)
        if desc:
            print(f"\n{skill_name}")
            print("="*80)
            print(desc)
        else:
            print(f"\nSkill '{skill_name}' not found")
    else:
        skills = agent.list_available_skills()
        print(f"\nAvailable Skills ({len(skills)}):")
        print("="*80)

        # Group by package
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

        for package, skills in packages.items():
            if skills:
                print(f"\n{package} ({len(skills)} skills):")
                for skill in sorted(skills):
                    print(f"  • {skill}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Governance AI Agent - Comprehensive AI Governance CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python cli.py

  # Assess an AI system
  python cli.py assess "Healthcare chatbot for patient scheduling"

  # Generate governance plan
  python cli.py plan --config system_profile.json

  # List all skills
  python cli.py skills

  # Describe a specific skill
  python cli.py skills --name ai-safety-planning
        """
    )

    parser.add_argument(
        'mode',
        nargs='?',
        choices=['interactive', 'assess', 'plan', 'skills'],
        default='interactive',
        help='Operation mode'
    )

    parser.add_argument(
        'description',
        nargs='?',
        help='System description for assessment mode'
    )

    parser.add_argument(
        '--config',
        help='Configuration file for plan mode (JSON or YAML)'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output file for assessment or plan'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['json', 'yaml', 'md', 'markdown'],
        default='json',
        help='Output format: json, yaml, or md/markdown (default: json)'
    )

    parser.add_argument(
        '--name',
        help='Skill name for skills mode'
    )

    parser.add_argument(
        '--api-key',
        help='API key for LLM (or set GEMINI_API_KEY/OPENAI_API_KEY env var)'
    )

    args = parser.parse_args()

    # Initialize agent
    # Always use None to let agent load default config with proper skills_base_path
    agent = GovernanceAIAgent(None)

    # Override API key if provided via command line
    if args.api_key:
        agent.config.api_key = args.api_key

    print("\n" + "="*80)
    print("GOVERNANCE AI AGENT")
    print("="*80)
    print(f"Initialized with {len(agent.skills)} skills available")
    print("="*80)

    # Run appropriate mode
    if args.mode == 'interactive' or (args.mode is None and args.description is None):
        interactive_mode(agent)

    elif args.mode == 'assess':
        if not args.description:
            print("Error: System description required for assess mode")
            sys.exit(1)
        assess_mode(agent, args.description, args.output, args.format)

    elif args.mode == 'plan':
        if not args.config:
            print("Error: Configuration file required for plan mode")
            sys.exit(1)
        plan_mode(agent, args.config, args.output, args.format)

    elif args.mode == 'skills':
        skills_mode(agent, args.name)


if __name__ == "__main__":
    main()
