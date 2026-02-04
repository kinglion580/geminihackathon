# Governance AI Agent - Python Implementation

This is a Python implementation of the Governance AI Agent based on `governance-ai-agent.md`. It provides a programmatic interface and CLI for comprehensive AI governance, compliance, and safety guidance.

## Features

- **Comprehensive Governance**: Access to all 53 skills across AI Act skills packages
- **Risk Assessment**: Automated EU AI Act risk classification
- **Compliance Mapping**: Identify applicable regulations (GDPR, HIPAA, PCI-DSS, etc.)
- **Governance Plans**: Generate comprehensive governance and compliance plans
- **Skill System**: Dynamically load and use specialized skills
- **Multiple Interfaces**: Python API, CLI, and interactive mode
- **Export Capabilities**: Export assessments and plans in JSON, YAML, or Markdown

## Installation

### Requirements

- Python 3.8+
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Setup

Set your API key (if using LLM features):

```bash
# For Gemini
export GEMINI_API_KEY="your-api-key"

# Or for OpenAI
export OPENAI_API_KEY="your-api-key"
```

## Quick Start

### 1. Basic Usage (Python API)

```python
from governance_agent import GovernanceAIAgent

# Initialize agent
agent = GovernanceAIAgent()

# Assess an AI system
assessment = agent.assess_ai_system(
    "A healthcare chatbot for patient appointment scheduling"
)

print(assessment['initial_assessment'])
print(assessment['recommended_skills'])
```

### 2. Command Line Interface

#### Interactive Mode

```bash
python cli.py
```

This launches an interactive session where you can:
- Assess AI systems
- Generate governance plans
- Load and explore skills
- Chat with the agent

#### Assessment Mode

```bash
python cli.py assess "Customer service chatbot using LLM" --output assessment.json
```

#### Plan Generation Mode

Create a system profile file (`system_profile.json`):

```json
{
  "purpose": "Credit scoring for loan applications",
  "type": "ML Classification Model",
  "users": "Loan officers",
  "data": "Credit history, employment data",
  "geography": "European Union"
}
```

Generate plan:

```bash
python cli.py plan --config system_profile.json --output governance_plan.json
```

#### Skills Mode

List all available skills:

```bash
python cli.py skills
```

Describe a specific skill:

```bash
python cli.py skills --name ai-safety-planning
```

## Examples

See the `examples/` directory for complete examples:

- **`example_basic.py`** - Basic assessment and skill loading
- **`example_governance_plan.py`** - Generating comprehensive governance plans
- **`example_skills.py`** - Working with the skill system

Run examples:

```bash
cd examples
python example_basic.py
python example_governance_plan.py
python example_skills.py
```

## Architecture

### Core Components

1. **`governance_agent.py`** - Main agent implementation
   - `GovernanceAIAgent` - Core agent class
   - `AgentConfig` - Configuration dataclass
   - `SkillMetadata` - Skill information

2. **`cli.py`** - Command-line interface
   - Interactive mode
   - Assessment mode
   - Plan generation mode
   - Skills browser

3. **`config.yaml`** - Configuration file
   - Agent settings
   - Skill definitions
   - Risk classification rules
   - Compliance frameworks

### Agent Capabilities

#### Risk Classification

The agent automatically classifies AI systems per EU AI Act:

- **Unacceptable Risk**: Prohibited systems (social scoring, manipulation)
- **High-Risk**: Significant impact (healthcare, credit, employment)
- **Limited Risk**: Transparency required (chatbots, content generation)
- **Minimal Risk**: Low concern (spam filters, games)

#### Compliance Identification

Automatically identifies applicable regulations:

- **EU AI Act**: Always applicable
- **GDPR**: For personal data processing
- **HIPAA**: For healthcare applications
- **PCI-DSS**: For payment systems

#### Skill Recommendations

Based on system description, recommends relevant skills to load:

- Core governance skills (always recommended)
- Context-specific skills (based on use case)
- Compliance skills (based on applicable regulations)

## API Reference

### GovernanceAIAgent

#### Initialization

```python
from governance_agent import GovernanceAIAgent, AgentConfig

# Default configuration
agent = GovernanceAIAgent()

# Custom configuration
config = AgentConfig(
    model="opus",
    temperature=0.7,
    api_key="your-api-key"
)
agent = GovernanceAIAgent(config)
```

#### Methods

**`assess_ai_system(system_description: str) -> Dict[str, Any]`**

Assess an AI system and provide governance recommendations.

```python
assessment = agent.assess_ai_system(
    "Healthcare diagnostic AI for preliminary patient screening"
)

# Returns:
# {
#   "risk_classification": {...},
#   "applicable_regulations": [...],
#   "recommended_skills": [...],
#   "initial_assessment": "..."
# }
```

**`generate_governance_plan(system_profile: Dict[str, Any]) -> Dict[str, Any]`**

Generate a comprehensive governance plan.

```python
plan = agent.generate_governance_plan({
    "purpose": "Customer sentiment analysis",
    "type": "NLP Classification Model",
    "users": "Customer service teams",
    "data": "Customer feedback, support tickets",
    "geography": "Global"
})

# Returns comprehensive plan with:
# - Executive summary
# - Risk assessment
# - Compliance requirements
# - Architecture recommendations
# - Safety implementation guide
# - Testing strategy
# - Operational procedures
# - Next steps
```

**`list_available_skills() -> List[str]`**

List all available skills.

```python
skills = agent.list_available_skills()
# Returns: ['ai-ethics', 'ai-governance', 'ai-safety-planning', ...]
```

**`load_skill(skill_name: str) -> bool`**

Load a skill for use in the current session.

```python
success = agent.load_skill('risk-assessment')
if success:
    print("Skill loaded successfully")
```

**`get_skill_description(skill_name: str) -> Optional[str]`**

Get the description of a specific skill.

```python
desc = agent.get_skill_description('ai-safety-planning')
print(desc)
```

**`get_skill_content(skill_name: str) -> Optional[str]`**

Get the full content of a skill (markdown).

```python
content = agent.get_skill_content('gdpr-compliance')
```

**`chat(user_message: str) -> str`**

Interactive chat interface with the agent.

```python
response = agent.chat("How do I ensure my AI system is GDPR compliant?")
print(response)
```

**`export_assessment(assessment: Dict[str, Any], format: str) -> str`**

Export assessment or plan in specified format.

```python
# JSON
json_output = agent.export_assessment(assessment, format="json")

# YAML
yaml_output = agent.export_assessment(assessment, format="yaml")

# Markdown
md_output = agent.export_assessment(assessment, format="markdown")
```

## Configuration

### config.yaml Structure

```yaml
agent:
  name: governance-ai-agent
  model: opus
  temperature: 0.7
  max_tokens: 4096

tools:
  - Read
  - Write
  - Skill
  # ... etc

skills:
  base_path: ../../
  auto_load:
    - risk-assessment
    - ai-governance

risk_classification:
  high_risk:
    - healthcare
    - credit
    # ... etc

compliance:
  frameworks:
    - name: EU AI Act
      always_applicable: true
    # ... etc
```

## Skills System

The agent has access to **53 skills** across 4 categories:

### AI Act Package (16 skills)

Core AI governance and compliance skills from the AI Act package.

Examples: `ai-ethics`, `ai-governance`, `ai-testing`, `risk-assessment`, `incident-responder`

### AI/ML Planning (10 skills)

ML architecture and project lifecycle skills.

Examples: `ml-project-lifecycle`, `model-selection`, `rag-architecture`, `bias-assessment`

### Compliance Planning (9 skills)

Regulatory compliance and security frameworks.

Examples: `gdpr-compliance`, `hipaa-compliance`, `security-frameworks`, `data-classification`

### Google Ecosystem (18 skills)

Gemini and Google-specific integration skills.

Examples: `gemini-cli-execution`, `gemini-mcp-integration`, `gemini-context-bridge`

## Development

### Project Structure

```
implementation/
├── governance_agent.py      # Core agent implementation
├── cli.py                   # Command-line interface
├── config.yaml              # Configuration
├── requirements.txt         # Dependencies
├── README.md               # This file
├── examples/               # Usage examples
│   ├── example_basic.py
│   ├── example_governance_plan.py
│   └── example_skills.py
└── __init__.py             # Package init
```

### Running Tests

```bash
# Run the main module (self-test)
python governance_agent.py

# Run CLI examples
python cli.py --help
python cli.py skills

# Run examples
cd examples
python example_basic.py
```

## Use Cases

### 1. New AI Project Assessment

```python
agent = GovernanceAIAgent()

assessment = agent.assess_ai_system(
    "An AI-powered hiring assistant that screens resumes and ranks candidates"
)

# Get risk classification and compliance requirements
print(f"Risk: {assessment['risk_classification']['category']}")
for reg in assessment['applicable_regulations']:
    print(f"- {reg['name']}: {reg['reason']}")
```

### 2. Compliance Audit

```python
agent = GovernanceAIAgent()

# Load relevant compliance skills
agent.load_skill('gdpr-compliance')
agent.load_skill('ai-governance')
agent.load_skill('risk-assessment')

# Generate comprehensive governance plan
plan = agent.generate_governance_plan({
    "purpose": "Customer behavior prediction",
    "type": "ML Model",
    "users": "Marketing teams",
    "data": "Purchase history, browsing data",
    "geography": "EU"
})

# Export for review
with open('compliance_audit.json', 'w') as f:
    json.dump(plan, f, indent=2)
```

### 3. Interactive Governance Session

```bash
python cli.py

# In interactive mode:
You: assess my healthcare chatbot
Agent: [Provides assessment...]

You: load ai-safety-planning
Agent: ✓ Skill loaded

You: What safety measures should I implement?
Agent: [Provides guidance based on loaded skills...]
```

## Troubleshooting

### Skills Not Loading

**Issue**: Skills not discovered or loaded

**Solution**:
1. Check `skills_base_path` in config
2. Verify SKILL.md files exist in expected locations
3. Ensure proper YAML frontmatter in SKILL.md files

### API Key Errors

**Issue**: LLM API calls failing

**Solution**:
1. Set environment variable: `export GEMINI_API_KEY="your-key"`
2. Or set in AgentConfig: `config.api_key = "your-key"`
3. Check API key validity

### Import Errors

**Issue**: Cannot import modules

**Solution**:
```bash
# Install dependencies
pip install -r requirements.txt

# Add to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/implementation"
```

## Contributing

To extend the agent:

1. **Add New Skills**: Create SKILL.md files with proper frontmatter
2. **Enhance Risk Classification**: Update `_classify_risk()` method
3. **Add Compliance Frameworks**: Update `config.yaml` and `_identify_regulations()`
4. **Improve LLM Integration**: Implement `_initialize_llm()` with actual API clients

## License

This implementation is part of the AI Act skills packages project.

## Support

For issues and questions:
- Check the examples in `examples/`
- Review the main documentation in `../README.md`
- Refer to individual skill documentation in SKILL.md files

## Related Files

- **`../governance-ai-agent.md`** - Agent specification
- **`../QUICKSTART.md`** - Quick start guide
- **`../EXAMPLES.md`** - Use case examples
- **`../../README.md`** - AI Act package documentation
