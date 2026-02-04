"""
Governance AI Agent - Python Implementation

This module provides a Python implementation of the Governance AI Agent
that consolidates all AI Act skills packages for comprehensive AI governance.

Based on: governance-ai-agent.md
"""

import os
import json
import yaml
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
from dataclasses import dataclass, field
import re


@dataclass
class AgentConfig:
    """Configuration for the Governance AI Agent"""
    name: str = "governance-ai-agent"
    description: str = ""
    model: str = "opus"
    color: str = "purple"
    tools: List[str] = field(default_factory=list)
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096
    skills_base_path: Optional[str] = None
    skills_paths: List[str] = field(default_factory=list)  # Support multiple skill directories


@dataclass
class SkillMetadata:
    """Metadata for a loaded skill"""
    name: str
    description: str
    path: str
    content: str
    allowed_tools: List[str] = field(default_factory=list)


class GovernanceAIAgent:
    """
    Comprehensive AI Governance Agent with access to all AI Act skills packages.

    Provides end-to-end guidance on building compliant, safe, ethical, and robust
    AI systems that meet regulatory requirements including the EU AI Act, GDPR,
    HIPAA, PCI-DSS, and other frameworks.
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """
        Initialize the Governance AI Agent

        Args:
            config: Agent configuration. If None, uses default configuration.
        """
        self.config = config or self._load_default_config()
        self.skills: Dict[str, SkillMetadata] = {}
        self.loaded_skills: List[str] = []
        self.conversation_history: List[Dict[str, str]] = []

        # Initialize LLM client
        self.llm_client = self._initialize_llm()

        # Load available skills
        self._discover_skills()

    def _load_default_config(self) -> AgentConfig:
        """Load default agent configuration"""
        config = AgentConfig()

        # Try to load API keys from environment
        config.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")

        # Set skills base path (backward compatibility)
        # From implementation/ go up to "AI Act package/"
        current_dir = Path(__file__).parent.parent.parent
        config.skills_base_path = str(current_dir)

        # Set multiple skills paths to search
        # 1. AI Act skills packages directory
        config.skills_paths.append(str(current_dir))

        # 2. Root-level skills folder (if exists)
        # From implementation/ go up 4 levels to repository root
        repo_root = Path(__file__).parent.parent.parent.parent.parent
        root_skills_dir = repo_root / "skills"
        if root_skills_dir.exists():
            config.skills_paths.append(str(root_skills_dir))

        return config

    def _initialize_llm(self) -> Optional[Any]:
        """Initialize LLM client based on configuration"""
        # This is a placeholder - in production, would initialize actual LLM client
        # Could support Gemini, OpenAI, Claude, etc.
        return None

    def _discover_skills(self):
        """Discover and load metadata for all available skills from multiple directories"""
        # Determine which paths to search
        search_paths = []

        # Use skills_paths if available (new multi-path approach)
        if self.config.skills_paths:
            search_paths = self.config.skills_paths
        # Fall back to single skills_base_path for backward compatibility
        elif self.config.skills_base_path:
            search_paths = [self.config.skills_base_path]
        else:
            return

        # Track discovered skill names to avoid duplicates
        discovered_skills = set()

        # Search all configured paths
        for base_path in search_paths:
            skills_path = Path(base_path)
            if not skills_path.exists():
                continue

            # Search for all SKILL.md files in this path
            skill_files = list(skills_path.rglob("SKILL.md"))

            for skill_file in skill_files:
                try:
                    skill_metadata = self._parse_skill_file(skill_file)
                    if skill_metadata:
                        # Only add if not already discovered (prevents duplicates)
                        if skill_metadata.name not in discovered_skills:
                            self.skills[skill_metadata.name] = skill_metadata
                            discovered_skills.add(skill_metadata.name)
                        else:
                            print(f"Info: Skipping duplicate skill '{skill_metadata.name}' from {skill_file}")
                except Exception as e:
                    print(f"Warning: Could not load skill from {skill_file}: {e}")

    def _parse_skill_file(self, file_path: Path) -> Optional[SkillMetadata]:
        """Parse a SKILL.md file and extract metadata"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract YAML frontmatter
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not frontmatter_match:
            return None

        try:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))

            return SkillMetadata(
                name=frontmatter.get('name', ''),
                description=frontmatter.get('description', ''),
                path=str(file_path),
                content=content,
                allowed_tools=frontmatter.get('allowed-tools', [])
            )
        except Exception as e:
            print(f"Warning: Could not parse frontmatter in {file_path}: {e}")
            return None

    def list_available_skills(self) -> List[str]:
        """List all available skills"""
        return sorted(self.skills.keys())

    def get_skill_description(self, skill_name: str) -> Optional[str]:
        """Get description of a specific skill"""
        skill = self.skills.get(skill_name)
        return skill.description if skill else None

    def load_skill(self, skill_name: str) -> bool:
        """
        Load a skill for use in the current session

        Args:
            skill_name: Name of the skill to load

        Returns:
            True if skill was loaded successfully, False otherwise
        """
        if skill_name not in self.skills:
            print(f"Skill '{skill_name}' not found")
            return False

        if skill_name in self.loaded_skills:
            print(f"Skill '{skill_name}' is already loaded")
            return True

        self.loaded_skills.append(skill_name)
        print(f"Loaded skill: {skill_name}")
        return True

    def get_skill_content(self, skill_name: str) -> Optional[str]:
        """Get the full content of a skill"""
        skill = self.skills.get(skill_name)
        return skill.content if skill else None

    def assess_ai_system(self, system_description: str) -> Dict[str, Any]:
        """
        Assess an AI system and provide governance recommendations

        Args:
            system_description: Description of the AI system to assess

        Returns:
            Dictionary containing assessment results
        """
        assessment = {
            "system_description": system_description,
            "risk_classification": self._classify_risk(system_description),
            "applicable_regulations": self._identify_regulations(system_description),
            "recommended_skills": self._recommend_skills(system_description),
            "initial_assessment": self._generate_initial_assessment(system_description)
        }

        return assessment

    def _classify_risk(self, system_description: str) -> Dict[str, Any]:
        """
        Classify the risk level of an AI system per EU AI Act

        Returns classification and reasoning
        """
        # Simplified risk classification logic
        # In production, this would use LLM and more sophisticated analysis

        high_risk_keywords = [
            "healthcare", "medical", "diagnosis", "credit", "scoring",
            "employment", "hiring", "recruitment", "biometric", "law enforcement"
        ]

        description_lower = system_description.lower()

        for keyword in high_risk_keywords:
            if keyword in description_lower:
                return {
                    "category": "High-Risk",
                    "confidence": "high",
                    "reasoning": f"System description contains '{keyword}' which indicates High-Risk category per EU AI Act"
                }

        if any(word in description_lower for word in ["chatbot", "customer service", "content generation"]):
            return {
                "category": "Limited Risk",
                "confidence": "medium",
                "reasoning": "System appears to interact with users, requiring transparency per Article 52"
            }

        return {
            "category": "Minimal Risk",
            "confidence": "low",
            "reasoning": "System does not appear to fall into High-Risk or Limited Risk categories"
        }

    def _identify_regulations(self, system_description: str) -> List[Dict[str, Any]]:
        """Identify applicable regulations based on system description"""
        regulations = []
        description_lower = system_description.lower()

        # Always applicable
        regulations.append({
            "name": "EU AI Act",
            "applies": True,
            "reason": "Applies to all AI systems deployed in EU"
        })

        # GDPR
        if any(word in description_lower for word in ["personal data", "user data", "privacy", "eu"]):
            regulations.append({
                "name": "GDPR",
                "applies": True,
                "reason": "System processes personal data in EU context"
            })

        # HIPAA
        if any(word in description_lower for word in ["healthcare", "medical", "patient", "health"]):
            regulations.append({
                "name": "HIPAA",
                "applies": True,
                "reason": "System processes healthcare/patient data"
            })

        # PCI-DSS
        if any(word in description_lower for word in ["payment", "credit card", "transaction"]):
            regulations.append({
                "name": "PCI-DSS",
                "applies": True,
                "reason": "System processes payment card data"
            })

        return regulations

    def _recommend_skills(self, system_description: str) -> List[Dict[str, str]]:
        """Recommend skills to load based on system description"""
        recommended = []
        description_lower = system_description.lower()

        # Always recommend these core skills
        core_skills = [
            ("risk-assessment", "Essential for identifying and mitigating risks"),
            ("ai-governance", "Core governance framework and policies"),
            ("ai-safety-planning", "Safety measures and guardrails")
        ]

        for skill_name, reason in core_skills:
            if skill_name in self.skills:
                recommended.append({"skill": skill_name, "reason": reason})

        # Context-specific recommendations
        if any(word in description_lower for word in ["bias", "fairness", "discrimination"]):
            if "bias-assessment" in self.skills:
                recommended.append({
                    "skill": "bias-assessment",
                    "reason": "System description mentions fairness/bias concerns"
                })

        if any(word in description_lower for word in ["test", "testing", "quality"]):
            if "ai-testing" in self.skills:
                recommended.append({
                    "skill": "ai-testing",
                    "reason": "Testing and quality assurance needed"
                })

        if any(word in description_lower for word in ["gdpr", "privacy", "personal data"]):
            if "gdpr-compliance" in self.skills:
                recommended.append({
                    "skill": "gdpr-compliance",
                    "reason": "GDPR compliance required"
                })

        if any(word in description_lower for word in ["rag", "retrieval", "search"]):
            if "rag-architecture" in self.skills:
                recommended.append({
                    "skill": "rag-architecture",
                    "reason": "RAG architecture design needed"
                })

        return recommended

    def _generate_initial_assessment(self, system_description: str) -> str:
        """Generate initial assessment narrative"""
        risk_info = self._classify_risk(system_description)
        regulations = self._identify_regulations(system_description)

        assessment = f"""
Initial Assessment:

System Risk Level: {risk_info['category']}
Reasoning: {risk_info['reasoning']}

Applicable Regulations:
"""
        for reg in regulations:
            assessment += f"- {reg['name']}: {reg['reason']}\n"

        assessment += """
Next Steps:
1. Load recommended skills for detailed guidance
2. Conduct comprehensive risk assessment
3. Map compliance requirements
4. Design governance framework
5. Implement safety measures and testing
"""

        return assessment

    def generate_governance_plan(self, system_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive governance plan

        Args:
            system_profile: Dictionary containing system information including:
                - purpose: Business objective
                - type: Type of AI system (LLM, ML model, agent, etc.)
                - users: Target users
                - data: Data types processed
                - geography: Deployment geography

        Returns:
            Comprehensive governance plan
        """
        plan = {
            "system_profile": system_profile,
            "executive_summary": self._generate_executive_summary(system_profile),
            "risk_assessment": self._classify_risk(system_profile.get("purpose", "")),
            "compliance_requirements": self._identify_regulations(system_profile.get("purpose", "")),
            "architecture_recommendations": self._generate_architecture_recommendations(system_profile),
            "safety_implementation": self._generate_safety_recommendations(system_profile),
            "testing_strategy": self._generate_testing_strategy(system_profile),
            "operational_procedures": self._generate_operational_procedures(system_profile),
            "next_steps": self._generate_next_steps(system_profile)
        }

        return plan

    def _generate_executive_summary(self, system_profile: Dict[str, Any]) -> str:
        """Generate executive summary for governance plan"""
        return f"""
This governance plan addresses the {system_profile.get('type', 'AI system')} with
purpose: {system_profile.get('purpose', 'Not specified')}.

The system will be deployed to {system_profile.get('users', 'users')} in
{system_profile.get('geography', 'unspecified regions')}, processing
{system_profile.get('data', 'various data types')}.

This plan provides comprehensive guidance on compliance, safety, ethics, and operational excellence.
"""

    def _generate_architecture_recommendations(self, system_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate architecture recommendations"""
        return {
            "recommended_patterns": [
                "Microservices architecture for scalability",
                "API gateway for controlled access",
                "Model versioning and registry",
                "Feature store for data consistency"
            ],
            "data_pipeline": [
                "Implement data validation and quality checks",
                "Set up data lineage tracking",
                "Configure privacy-preserving techniques"
            ],
            "monitoring": [
                "Real-time performance monitoring",
                "Bias detection in production",
                "Audit logging per Article 12"
            ]
        }

    def _generate_safety_recommendations(self, system_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate safety implementation recommendations"""
        return {
            "guardrails": {
                "input_guards": [
                    "Prompt injection detection",
                    "Content filtering",
                    "Rate limiting"
                ],
                "output_filters": [
                    "Toxicity filtering",
                    "PII detection and redaction",
                    "Topic restrictions"
                ]
            },
            "red_teaming": [
                "Pre-launch adversarial testing",
                "Ongoing red team exercises",
                "Vulnerability disclosure program"
            ],
            "monitoring": [
                "Safety metrics dashboard",
                "Automated alerting",
                "Incident detection"
            ]
        }

    def _generate_testing_strategy(self, system_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate testing strategy"""
        return {
            "pre_launch": [
                "Unit tests for all components",
                "Integration testing",
                "Red team testing",
                "Bias evaluation",
                "Performance benchmarking",
                "Security testing"
            ],
            "continuous": [
                "Automated test suite",
                "Ongoing red teaming",
                "User feedback monitoring",
                "Performance monitoring",
                "Compliance auditing"
            ],
            "tools": [
                "Deepeval for AI testing",
                "Custom bias evaluation framework",
                "Performance testing suite"
            ]
        }

    def _generate_operational_procedures(self, system_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate operational procedures"""
        return {
            "logging": {
                "audit_logs": "Log all AI system interactions per Article 12",
                "metrics": "Track performance, safety, and compliance metrics",
                "retention": "Configure appropriate retention policies"
            },
            "incident_response": {
                "detection": "Automated monitoring and alerting",
                "response": "Documented response procedures",
                "escalation": "Clear escalation paths",
                "reporting": "15-day reporting for serious incidents (Article 73)"
            },
            "deployment": {
                "training": "Deployer training program",
                "rollout": "Phased deployment with monitoring",
                "validation": "Post-deployment validation checks"
            }
        }

    def _generate_next_steps(self, system_profile: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate prioritized next steps"""
        return [
            {
                "phase": "Immediate (Week 1-2)",
                "tasks": [
                    "Finalize risk classification",
                    "Load and review relevant skills",
                    "Begin compliance documentation"
                ]
            },
            {
                "phase": "Short-term (Month 1)",
                "tasks": [
                    "Complete architecture design",
                    "Implement core guardrails",
                    "Set up testing framework"
                ]
            },
            {
                "phase": "Medium-term (Month 2-3)",
                "tasks": [
                    "Complete testing and validation",
                    "Finalize documentation",
                    "Conduct pre-launch review"
                ]
            },
            {
                "phase": "Long-term (Month 4+)",
                "tasks": [
                    "Deploy to production",
                    "Establish monitoring and maintenance",
                    "Continuous improvement"
                ]
            }
        ]

    def chat(self, user_message: str) -> str:
        """
        Interactive chat interface with the agent

        Args:
            user_message: User's message/question

        Returns:
            Agent's response
        """
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_message})

        # Generate response (simplified - in production would use LLM)
        response = self._generate_response(user_message)

        # Add response to history
        self.conversation_history.append({"role": "assistant", "content": response})

        return response

    def _generate_response(self, user_message: str) -> str:
        """Generate response to user message"""
        # This is a simplified version - in production would use actual LLM

        message_lower = user_message.lower()

        # Check if asking about skills
        if "skill" in message_lower and ("list" in message_lower or "available" in message_lower):
            skills = self.list_available_skills()
            return f"I have access to {len(skills)} skills:\n\n" + "\n".join(f"- {s}" for s in skills[:10]) + "\n\n(and more...)"

        # Check if asking about a specific skill
        if "what is" in message_lower or "describe" in message_lower:
            for skill_name in self.skills.keys():
                if skill_name in message_lower:
                    desc = self.get_skill_description(skill_name)
                    return f"**{skill_name}**:\n\n{desc}"

        # Check if asking for assessment
        if any(word in message_lower for word in ["assess", "evaluate", "analyze"]):
            if any(word in message_lower for word in ["chatbot", "system", "application"]):
                assessment = self.assess_ai_system(user_message)
                return f"""I've analyzed your request. Here's my initial assessment:

{assessment['initial_assessment']}

Recommended skills to load:
{chr(10).join(f"- {r['skill']}: {r['reason']}" for r in assessment['recommended_skills'][:5])}

Would you like me to proceed with a detailed governance plan?"""

        return """I'm the Governance AI Agent, here to help with AI governance, compliance, and safety.

I can help you with:
- Assessing AI systems for risk and compliance
- Generating governance plans
- Recommending appropriate skills and frameworks
- Providing guidance on EU AI Act, GDPR, HIPAA, and other regulations

How can I assist you today?"""

    def export_assessment(self, assessment: Dict[str, Any], format: str = "json") -> str:
        """
        Export assessment or plan to specified format

        Args:
            assessment: Assessment or plan dictionary
            format: Export format ('json', 'yaml', 'markdown')

        Returns:
            Formatted export string
        """
        if format == "json":
            return json.dumps(assessment, indent=2)
        elif format == "yaml":
            return yaml.dump(assessment, default_flow_style=False)
        elif format == "markdown":
            return self._format_as_markdown(assessment)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _format_as_markdown(self, data: Dict[str, Any], level: int = 1) -> str:
        """Format dictionary as markdown"""
        md = ""
        for key, value in data.items():
            heading = "#" * level
            md += f"\n{heading} {key.replace('_', ' ').title()}\n\n"

            if isinstance(value, dict):
                md += self._format_as_markdown(value, level + 1)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            md += f"**{k}**: {v}\n\n"
                    else:
                        md += f"- {item}\n"
                md += "\n"
            else:
                md += f"{value}\n\n"

        return md


def main():
    """Main entry point for testing"""
    print("Initializing Governance AI Agent...")
    agent = GovernanceAIAgent()

    print(f"\nAgent initialized with {len(agent.skills)} skills available")
    print(f"\nLoaded skills: {', '.join(agent.list_available_skills()[:5])}...")

    # Example assessment
    print("\n" + "="*80)
    print("Example Assessment:")
    print("="*80)

    system_desc = "A healthcare AI chatbot that helps patients schedule appointments and get preliminary diagnosis information"
    assessment = agent.assess_ai_system(system_desc)

    print(assessment['initial_assessment'])

    print("\nRecommended skills:")
    for rec in assessment['recommended_skills']:
        print(f"  - {rec['skill']}: {rec['reason']}")


if __name__ == "__main__":
    main()
