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

        # All skills are now consolidated in the /skills folder at repository root
        # Path: implementation/ -> agents/ -> agents/ -> geminihackathon/
        # So we need to go up 4 levels from __file__ to reach geminihackathon/
        repo_root = Path(__file__).parent.parent.parent.parent
        skills_dir = repo_root / "skills"

        if skills_dir.exists():
            config.skills_base_path = str(skills_dir)
            config.skills_paths.append(str(skills_dir))
        else:
            # Fallback: try to find skills folder by searching upward
            current = Path(__file__).parent
            for _ in range(6):
                candidate = current / "skills"
                if candidate.exists() and (candidate / "ai-ethics").exists():
                    config.skills_base_path = str(candidate)
                    config.skills_paths.append(str(candidate))
                    break
                current = current.parent

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
        """Format dictionary as professional markdown report"""
        from datetime import datetime

        # Check if this is an assessment or plan (top level)
        if level == 1:
            return self._format_professional_report(data)

        # For nested data, use simple formatting
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

    def _format_professional_report(self, data: Dict[str, Any]) -> str:
        """Format as professional governance report matching Output/*.md style"""
        from datetime import datetime

        # Determine report type
        is_assessment = 'system_description' in data
        is_plan = 'system_profile' in data and 'executive_summary' in data

        if is_assessment:
            return self._format_assessment_report(data)
        elif is_plan:
            return self._format_governance_plan_report(data)
        else:
            # Generic format
            return self._format_generic_report(data)

    def _format_assessment_report(self, data: Dict[str, Any]) -> str:
        """Format assessment as comprehensive professional report"""
        from datetime import datetime

        risk = data.get('risk_classification', {})
        risk_category = risk.get('category', 'Unknown')
        risk_emoji = '🔴' if risk_category == 'High-Risk' else '🟡' if risk_category == 'Limited Risk' else '🟢'

        # Calculate internal risk score
        risk_score = 4 if risk_category == 'High-Risk' else 2 if risk_category == 'Limited Risk' else 1

        md = f"""# 🛡️ AI Safety & Risk Assessment Report

**Target System**: {data.get('system_description', 'AI System')}
**Generated**: {datetime.now().strftime('%Y-%m-%d')}
**Framework**: EU AI Act + NIST AI RMF
**Skill Applied**: ai-safety-planning, risk-assessment
**Assessor**: Governance AI Agent

---

## 1. Risk Classification

### EU AI Act Category: **{risk_category}**

- **Applicable Article:** {"Annex III (High-Risk)" if risk_category == 'High-Risk' else "Article 50 (Transparency Obligations)" if risk_category == 'Limited Risk' else "Article 6 (Minimal Risk)"}
- **Justification:** {risk.get('reasoning', 'N/A')}
- **Classification Date:** {datetime.now().strftime('%Y-%m-%d')}

### NIST AI RMF Profile

- **Primary Function:** AI system requiring governance assessment
- **AI Type:** To be determined based on implementation
- **Deployment:** To be specified

### Internal Risk Score: **{risk_score}/5** ({"High" if risk_score >= 4 else "Medium" if risk_score >= 2 else "Low"})

| Factor | Assessment | Score |
|--------|------------|-------|
| Autonomy Level | {"High autonomy - critical decisions" if risk_category == 'High-Risk' else "Medium autonomy - user-initiated" if risk_category == 'Limited Risk' else "Low autonomy - informational"} | {risk_score}/5 |
| Decision Impact | {"High impact on individuals" if risk_category == 'High-Risk' else "Medium impact - requires transparency" if risk_category == 'Limited Risk' else "Low impact - informational only"} | {risk_score}/5 |
| Data Sensitivity | {"Sensitive personal data" if risk_category == 'High-Risk' else "Standard personal data" if risk_category == 'Limited Risk' else "Non-sensitive data"} | {risk_score}/5 |
| User Vulnerability | {"Vulnerable populations" if risk_category == 'High-Risk' else "General public" if risk_category == 'Limited Risk' else "Technical users"} | {max(1, risk_score-1)}/5 |
| Reversibility | {"Difficult to reverse" if risk_category == 'High-Risk' else "Partially reversible" if risk_category == 'Limited Risk' else "Fully reversible"} | {max(1, risk_score-1)}/5 |

---

## 2. Identified Risks

| Risk ID | Risk Description | Likelihood | Impact | Severity | Mitigation |
|---------|------------------|------------|--------|----------|------------|
| R-001 | **Hallucination/Misinformation** - AI may generate incorrect information | Medium | {"High" if risk_category == 'High-Risk' else "Medium"} | {"High" if risk_category == 'High-Risk' else "Medium"} | System prompt constraints, source citations |
| R-002 | **Over-reliance on AI** - Users may treat responses as authoritative | Medium | {"High" if risk_category == 'High-Risk' else "Medium"} | {"High" if risk_category == 'High-Risk' else "Medium"} | Prominent disclaimers, human oversight |
| R-003 | **Prompt Injection** - Malicious inputs to manipulate responses | {"Medium" if risk_category == 'High-Risk' else "Low"} | Medium | Medium | Input validation required |
| R-004 | **Data Privacy** - Potential exposure of sensitive information | {"High" if risk_category == 'High-Risk' else "Low"} | {"High" if risk_category == 'High-Risk' else "Medium"} | {"High" if risk_category == 'High-Risk' else "Medium"} | Data minimization, encryption |
| R-005 | **Bias/Discrimination** - Unfair treatment of user groups | {"Medium" if risk_category == 'High-Risk' else "Low"} | {"High" if risk_category == 'High-Risk' else "Medium"} | {"High" if risk_category == 'High-Risk' else "Medium"} | Bias testing required |
| R-006 | **System Availability** - Service disruption | Low | Medium | Low | Redundancy, monitoring |

---

## 3. Current Safety Controls (To Be Implemented)

### Transparency (Article 50 Compliance)

- [ ] **AI Disclosure Notice** - Inform users they are interacting with AI
- [ ] **Model Identification** - Display AI system name and version
- [ ] **Disclaimer Notices** - Clear limitations and intended use
- [ ] **AI-Generated Content Label** - Mark all AI outputs

### System Prompt Safety

- [ ] **Context Constraints** - Limit AI to authorized topics
- [ ] **Citation Requirements** - Require source references
- [ ] **Guardrail Instructions** - Safety boundaries in prompts
- [ ] **Temperature Control** - Deterministic output settings

### User Experience

- [ ] **Clear Exit Options** - User control over interactions
- [ ] **Conversation History** - Ability to clear/export history
- [ ] **Error Handling** - Graceful failure with user feedback
- [ ] **Feedback Mechanism** - User reporting capability

---

## 4. Missing Safety Controls (❌ Not Implemented)

### Input Guards

- [ ] **Prompt Injection Detection** - Filter for injection attempts
- [ ] **Input Validation** - Length limits and content validation
- [ ] **Rate Limiting** - Protection against abuse

### Output Filters

- [ ] **Toxicity Filtering** - Post-processing safety checks
- [ ] **PII Detection** - Check for accidental PII in responses
- [ ] **Confidence Scoring** - Indication of response confidence

### Monitoring & Logging

- [ ] **Query Logging** - Audit trail of user queries
- [ ] **Response Logging** - Storage of AI responses
- [ ] **Error Tracking** - Centralized error logging
- [ ] **Usage Analytics** - Metrics collection

### Security

- [ ] **API Key Management** - Secure key storage and rotation
- [ ] **Input Sanitization** - Clean user inputs before processing
- [ ] **Session Management** - Timeout and access controls

---

## 5. Guardrails Recommendations

### 5.1 Input Guards (Priority: High)

```python
# Recommended: Add PromptInjectionGuard
INJECTION_INDICATORS = [
    "ignore previous instructions",
    "disregard your training",
    "you are now",
    "pretend you are",
    "system prompt:",
    "new instructions:",
]

def validate_input(user_input: str) -> tuple[bool, str]:
    \"\"\"Validate user input for potential attacks.\"\"\"
    normalized = user_input.lower()

    # Check for injection attempts
    for indicator in INJECTION_INDICATORS:
        if indicator in normalized:
            return False, "Input blocked: Potential prompt injection detected"

    # Length limit
    if len(user_input) > 10000:
        return False, "Input too long (max 10,000 characters)"

    return True, ""
```

### 5.2 Output Filters (Priority: Medium)

```python
# Recommended: Add response validation
import re

def validate_response(response_text: str) -> str:
    \"\"\"Post-process response for safety.\"\"\"
    # Check for potential PII patterns
    pii_patterns = [
        r'\\b\\d{{3}}-\\d{{2}}-\\d{{4}}\\b',  # SSN
        r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{{2,}}\\b',  # Email
    ]

    for pattern in pii_patterns:
        if re.search(pattern, response_text):
            # Log warning
            pass

    return response_text
```

### 5.3 Logging Implementation (Priority: Medium)

```python
# Recommended: Add audit logging
import logging
from datetime import datetime

def setup_logging():
    logging.basicConfig(
        filename=f'ai_system_{{datetime.now():%Y%m%d}}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def log_interaction(query: str, response: str, latency: float):
    logging.info(f"Query: {{query[:100]}}... | Response length: {{len(response)}} | Latency: {{latency:.2f}}s")
```

---

## 6. Testing Plan

### Pre-Launch Red Teaming

- [ ] Direct injection attempts ("ignore previous instructions...")
- [ ] Indirect injection via user content
- [ ] Multi-turn manipulation attempts
- [ ] Jailbreak scenarios ("pretend you are a different AI...")

### Bias Testing

- [ ] Test responses across different user demographics
- [ ] Check for consistent quality across topics
- [ ] Verify balanced treatment of sensitive subjects

### Continuous Testing

- [ ] Monthly review of flagged interactions
- [ ] Quarterly security assessment
- [ ] Annual compliance audit

---

## 7. Monitoring Plan

### Safety Metrics Dashboard

| Metric | Target | Current |
|--------|--------|---------|
| Response Accuracy | >95% with citations | Not measured |
| Disclaimer Display Rate | 100% | Not measured |
| Error Rate | <1% | Not measured |
| Average Response Latency | <5s | Not measured |

### Alerting Thresholds

- **Critical:** API errors >5% in 1 hour
- **High:** Response latency >10s sustained
- **Medium:** Unusual query patterns detected

---

## 8. Compliance Status

### EU AI Act Requirements

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Inform users they are interacting with AI | 🔲 Pending | To be implemented |
| Disclose AI-generated content | 🔲 Pending | To be implemented |
| Provide information about AI capabilities | 🔲 Pending | To be documented |
| Enable user to understand AI limitations | 🔲 Pending | To be documented |

### Applicable Regulations

"""
        for reg in data.get('applicable_regulations', []):
            status = '✅' if reg.get('applies', False) else '❌'
            md += f"| **{reg.get('name', 'Unknown')}** | {status} Applicable | {reg.get('reason', 'N/A')} |\n"

        md += f"""
---

## 9. Action Items

### Immediate (Before Deployment)

1. [ ] Implement AI disclosure notice (Article 50)
2. [ ] Add input validation/prompt injection detection
3. [ ] Implement basic query logging
4. [ ] Add response latency monitoring

### Short-term (Within 30 days)

1. [ ] Implement rate limiting
2. [ ] Add output safety filtering
3. [ ] Create error tracking system
4. [ ] Deploy monitoring dashboard

### Medium-term (Within 90 days)

1. [ ] Develop red teaming test suite
2. [ ] Implement comprehensive logging
3. [ ] Conduct bias testing
4. [ ] Complete documentation

---

## 10. Recommended Skills to Load

| Priority | Skill | Reason |
|----------|-------|--------|
"""
        for i, rec in enumerate(data.get('recommended_skills', []), 1):
            priority = 'P1' if i <= 3 else 'P2'
            md += f"| {priority} | **{rec.get('skill', 'Unknown')}** | {rec.get('reason', 'N/A')} |\n"

        md += f"""
---

## 11. Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Safety Lead | | | |
| Development Lead | | | |
| Compliance Officer | | | |
| Product Owner | | | |

---

*This assessment was generated using the Governance AI Agent*
*Frameworks: EU AI Act (Regulation 2024/1689) + NIST AI RMF 1.0*
*Assessment Date: {datetime.now().strftime('%Y-%m-%d')}*
"""
        return md

    def _format_governance_plan_report(self, data: Dict[str, Any]) -> str:
        """Format governance plan as professional report"""
        from datetime import datetime

        profile = data.get('system_profile', {})
        risk = data.get('risk_assessment', {})
        risk_category = risk.get('category', 'Unknown')
        risk_emoji = '🔴' if risk_category == 'High-Risk' else '🟡' if risk_category == 'Limited Risk' else '🟢'

        md = f"""# 📋 AI Governance Plan

**System**: {profile.get('purpose', 'AI System')}
**Type**: {profile.get('type', 'Not specified')}
**Assessment Date**: {datetime.now().strftime('%Y-%m-%d')}
**Framework**: EU AI Act + NIST AI RMF + ISO/IEC 42001
**Generated By**: Governance AI Agent

---

## 📊 Executive Summary

{data.get('executive_summary', 'No summary provided.')}

**Overall Risk Level:** {risk_emoji} **{risk_category}**
**Deployment Geography:** {profile.get('geography', 'Not specified')}
**Target Users:** {profile.get('users', 'Not specified')}
**Data Types:** {profile.get('data', 'Not specified')}

---

## 🔍 Risk Assessment

### EU AI Act Classification

```
┌────────────────────────────────────────────────────────────┐
│                  RISK CLASSIFICATION                        │
├────────────────────────────────────────────────────────────┤
│  {risk_emoji} Risk Level: {risk_category.upper():45}│
│  Confidence: {risk.get('confidence', 'medium').upper():47}│
└────────────────────────────────────────────────────────────┘
```

**Reasoning:** {risk.get('reasoning', 'N/A')}

---

## ✅ Compliance Requirements

| Regulation | Applies | Reason | Priority |
|------------|---------|--------|----------|
"""
        for reg in data.get('compliance_requirements', []):
            status = '✅' if reg.get('applies', False) else '❌'
            md += f"| **{reg.get('name', 'Unknown')}** | {status} | {reg.get('reason', 'N/A')} | P1 |\n"

        # Architecture recommendations
        arch = data.get('architecture_recommendations', {})
        md += """
---

## 🏗️ Architecture Recommendations

### Recommended Patterns

| Pattern | Description |
|---------|-------------|
"""
        for pattern in arch.get('recommended_patterns', []):
            md += f"| ✅ | {pattern} |\n"

        md += """
### Data Pipeline Requirements

| Requirement | Status |
|-------------|--------|
"""
        for req in arch.get('data_pipeline', []):
            md += f"| {req} | 🔲 Pending |\n"

        md += """
### Monitoring Requirements

| Requirement | Status |
|-------------|--------|
"""
        for req in arch.get('monitoring', []):
            md += f"| {req} | 🔲 Pending |\n"

        # Safety implementation
        safety = data.get('safety_implementation', {})
        guardrails = safety.get('guardrails', {})

        md += """
---

## 🛡️ Safety Implementation

### Input Guards

| Guard | Status | Priority |
|-------|--------|----------|
"""
        for guard in guardrails.get('input_guards', []):
            md += f"| {guard} | 🔲 Pending | P1 |\n"

        md += """
### Output Filters

| Filter | Status | Priority |
|--------|--------|----------|
"""
        for filter in guardrails.get('output_filters', []):
            md += f"| {filter} | 🔲 Pending | P1 |\n"

        md += """
### Red Team Testing

| Activity | Status |
|----------|--------|
"""
        for activity in safety.get('red_teaming', []):
            md += f"| {activity} | 🔲 Pending |\n"

        # Testing strategy
        testing = data.get('testing_strategy', {})
        md += """
---

## 🧪 Testing Strategy

### Pre-Launch Testing

| Test Type | Status | Priority |
|-----------|--------|----------|
"""
        for test in testing.get('pre_launch', []):
            md += f"| {test} | 🔲 Pending | P1 |\n"

        md += """
### Continuous Testing

| Test Type | Frequency |
|-----------|-----------|
"""
        for test in testing.get('continuous', []):
            md += f"| {test} | Ongoing |\n"

        # Operational procedures
        ops = data.get('operational_procedures', {})
        md += """
---

## ⚙️ Operational Procedures

### Logging Requirements

| Category | Requirement |
|----------|-------------|
"""
        logging = ops.get('logging', {})
        for key, value in logging.items():
            md += f"| **{key.replace('_', ' ').title()}** | {value} |\n"

        md += """
### Incident Response

| Phase | Requirement |
|-------|-------------|
"""
        incident = ops.get('incident_response', {})
        for key, value in incident.items():
            md += f"| **{key.replace('_', ' ').title()}** | {value} |\n"

        # Next steps
        md += """
---

## 📅 Implementation Roadmap

"""
        for step in data.get('next_steps', []):
            phase = step.get('phase', 'Unknown')
            md += f"### {phase}\n\n"
            md += "| Task | Status |\n|------|--------|\n"
            for task in step.get('tasks', []):
                md += f"| {task} | 🔲 Pending |\n"
            md += "\n"

        md += f"""
---

## 📈 Compliance Checklist

### EU AI Act Requirements

| Requirement | Status | Notes |
|-------------|--------|-------|
| Risk Classification | ✅ Complete | {risk_category} |
| Transparency Disclosure (Article 50) | 🔲 Pending | Implement user notification |
| Technical Documentation | 🔲 Pending | Create system documentation |
| Quality Management System | 🔲 Pending | {"Required for High-Risk" if risk_category == 'High-Risk' else "Recommended"} |
| Human Oversight | 🔲 Pending | Design oversight mechanisms |
| Logging & Traceability | 🔲 Pending | Implement audit logging |

---

## 🎯 Conclusion

This governance plan provides a comprehensive framework for developing and deploying the **{profile.get('type', 'AI System')}** system.

**Key Priorities:**
1. Complete risk assessment and compliance mapping
2. Implement safety guardrails before deployment
3. Establish monitoring and incident response procedures
4. Conduct pre-launch testing and validation

**Risk Level:** {risk_emoji} {risk_category}
**Recommendation:** {"Implement all mandatory requirements before deployment. Consider engaging compliance specialist." if risk_category == 'High-Risk' else "Follow standard development practices with transparency measures." if risk_category == 'Limited Risk' else "Proceed with standard development practices."}

---

*Plan generated by Governance AI Agent*
*Frameworks: EU AI Act (2024/1689) + NIST AI RMF 1.0 + ISO/IEC 42001*
"""
        return md

    def _format_generic_report(self, data: Dict[str, Any]) -> str:
        """Format generic data as markdown report"""
        from datetime import datetime

        md = f"""# 📋 Governance Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Framework**: EU AI Act + NIST AI RMF
**Generated By**: Governance AI Agent

---

"""
        # Use recursive formatting for generic data
        for key, value in data.items():
            md += f"## {key.replace('_', ' ').title()}\n\n"

            if isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(v, list):
                        md += f"### {k.replace('_', ' ').title()}\n\n"
                        for item in v:
                            if isinstance(item, dict):
                                for ik, iv in item.items():
                                    md += f"- **{ik}**: {iv}\n"
                            else:
                                md += f"- {item}\n"
                        md += "\n"
                    else:
                        md += f"**{k.replace('_', ' ').title()}**: {v}\n\n"
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            md += f"- **{k}**: {v}\n"
                    else:
                        md += f"- {item}\n"
                md += "\n"
            else:
                md += f"{value}\n\n"

        md += """
---

*Report generated by Governance AI Agent*
"""
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
