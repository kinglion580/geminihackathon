# Governance AI Agent - Quick Start Guide

## What is the Governance AI Agent?

The **Governance AI Agent** is a comprehensive "super agent" that consolidates ALL skills from the AI Act skills packages into a single, powerful agent. It provides end-to-end AI governance capabilities including:

- EU AI Act compliance and risk classification
- Multi-regulation compliance (GDPR, HIPAA, PCI-DSS)
- AI safety planning and guardrails
- Bias detection and fairness validation
- ML architecture and testing
- Incident response and monitoring
- Documentation generation

## Quick Start

### 1. Basic Usage

To use the Governance AI Agent in Claude Code, you can invoke it through the Task tool or agent system:

```
I need help with AI governance for my [project description].
Please use the governance-ai-agent to assess requirements and create a plan.
```

### 2. Example First Interaction

**Your Prompt:**
```
I'm building a customer service chatbot using an LLM. Help me ensure it's
safe, compliant, and follows best practices.
```

**What the Agent Will Do:**
1. Ask clarifying questions about your system
2. Classify the risk level (likely "Limited Risk" for chatbots)
3. Identify applicable regulations
4. Load relevant skills (ai-safety-planning, prompt-engineering, ai-testing)
5. Generate a comprehensive safety and compliance plan

### 3. Key Capabilities

#### Comprehensive Assessment
```
Assess my AI system for EU AI Act compliance:
- Healthcare diagnostic assistant
- Used by doctors in EU hospitals
- Analyzes patient data and medical history
```

#### Architecture Design
```
Design a RAG architecture for legal document analysis with:
- High accuracy requirements
- Full explainability
- Citation tracking
- Human-in-the-loop review
```

#### Compliance Audit
```
Audit our existing credit scoring AI system for:
- EU AI Act compliance
- GDPR compliance
- Bias and fairness
- Documentation gaps
```

#### Safety Implementation
```
Help me implement safety guardrails for our LLM including:
- Prompt injection detection
- Toxic content filtering
- PII protection
- Brand voice maintenance
```

## Skills Available

The agent has access to **53 skills** across 4 categories:

### AI Act Package (16 skills)
`ai-ethics`, `ai-governance`, `ai-testing`, `ai-safety-planning`, `risk-assessment`, `incident-responder`, `fact-checker`, `transparency-instructions`, and more

### AI/ML Planning (10 skills)
`ml-project-lifecycle`, `model-selection`, `rag-architecture`, `bias-assessment`, `explainability-planning`, `hitl-design`, and more

### Compliance Planning (9 skills)
`gdpr-compliance`, `hipaa-compliance`, `pci-dss-compliance`, `data-classification`, `security-frameworks`, and more

### Google Ecosystem (18 skills)
`gemini-cli-execution`, `gemini-mcp-integration`, `gemini-token-optimization`, and more

## Common Use Cases

### 1. Starting a New AI Project
**Prompt:** "I'm starting a new AI project for [use case]. Help me plan governance from the beginning."

**Agent provides:**
- Risk classification
- Compliance requirements
- Architecture recommendations
- Testing strategy
- Documentation templates

### 2. Compliance Check
**Prompt:** "Does my [AI system description] comply with the EU AI Act?"

**Agent provides:**
- Risk category assessment
- Compliance requirements
- Gap analysis
- Remediation roadmap

### 3. Safety & Testing
**Prompt:** "How do I test my AI system for safety and bias?"

**Agent provides:**
- Testing methodology
- Test case templates
- Red team strategies
- Bias evaluation metrics
- Automated testing setup

### 4. Documentation
**Prompt:** "Generate documentation for my AI system for [purpose]."

**Agent provides:**
- Technical documentation
- Risk assessments
- Compliance reports
- User documentation
- Audit trails

### 5. Incident Response
**Prompt:** "My AI system [incident description]. How do I respond?"

**Agent provides:**
- Immediate response steps
- Investigation procedures
- Root cause analysis
- Prevention measures
- Stakeholder communication

## Best Practices

### 1. Provide Context
The more context you provide, the better the agent can help:
- What type of AI system?
- What's the use case?
- Who are the users?
- What data is processed?
- What geography (EU, US, global)?
- What industry (healthcare, finance, etc.)?

### 2. Iterate and Refine
Start with high-level planning, then drill into specifics:
- Get initial assessment and plan
- Ask follow-up questions on specific areas
- Request code examples or templates
- Refine based on your constraints

### 3. Load Skills as Needed
Don't try to use all skills at once. Let the agent:
- Determine which skills are relevant
- Load them strategically
- Guide you through their usage

### 4. Document as You Go
Ask the agent to generate documentation throughout:
- Initial assessments
- Architecture decisions
- Testing results
- Compliance evidence
- Incident reports

## Advanced Usage

### Custom Governance Frameworks
```
Create a custom AI governance framework for our organization that combines:
- EU AI Act requirements
- Our internal policies on [topic]
- Industry best practices for [industry]
- Risk tolerance level of [level]
```

### Multi-System Governance
```
We have multiple AI systems:
1. Customer service chatbot (LLM)
2. Fraud detection (ML classifier)
3. Recommendation engine (collaborative filtering)

Help us create a unified governance approach.
```

### Continuous Monitoring Setup
```
Set up continuous compliance monitoring for our High-Risk AI system including:
- Automated testing
- Bias monitoring
- Performance tracking
- Audit log analysis
- Alert thresholds
```

## Integration with Claude Code

The Governance AI Agent is designed to work seamlessly with Claude Code:

### Using with MCP Servers
The agent can use MCP servers for:
- Research (perplexity search)
- Documentation (microsoft-learn)
- Current best practices
- Regulatory updates

### Using with Other Tools
The agent has access to:
- `Read/Write` - File operations
- `Glob/Grep` - Code search
- `Skill` - Load additional skills
- `Task` - Delegate to specialized agents
- `Bash` - Execute commands

### Workspace Integration
The agent can:
- Analyze your codebase
- Review AI implementations
- Generate compliant code
- Create documentation files
- Set up testing frameworks

## Troubleshooting

### Agent Doesn't Load
- Ensure the agent file is in the correct location
- Check YAML frontmatter syntax
- Verify Claude Code configuration

### Skills Not Loading
- Skills should auto-load based on needs
- You can explicitly request: "Load the ai-safety-planning skill"
- Check skill availability in parent directories

### Too Much Information
- Ask for summaries: "Give me the executive summary"
- Focus on priorities: "What are the critical items?"
- Iterate: "Let's start with risk assessment only"

## Getting Help

### For More Information
- **README.md** - Overview of agents
- **EXAMPLES.md** - Detailed usage examples
- **governance-ai-agent.md** - Full agent documentation

### Common Questions

**Q: Do I need to load all skills manually?**
A: No, the agent automatically loads relevant skills based on your needs.

**Q: Can I use this for non-EU projects?**
A: Yes, the agent covers multiple regulations and can adapt to different jurisdictions.

**Q: How detailed should my initial prompt be?**
A: Provide key context (system type, use case, industry, geography), the agent will ask for more details if needed.

**Q: Can the agent generate code?**
A: Yes, the agent can generate implementation code, test cases, configuration files, and more.

**Q: How often should I consult the agent?**
A: Use it for initial planning, major changes, compliance reviews, incidents, and periodic audits.

## Next Steps

1. **Try it now:** Start with a simple prompt about your AI project
2. **Review examples:** Check EXAMPLES.md for your use case
3. **Explore skills:** Browse the skills packages to see what's available
4. **Iterate:** Work with the agent to refine your governance approach
5. **Document:** Generate comprehensive documentation for your AI systems

## Feedback and Contributions

To improve the Governance AI Agent:
- Suggest new skills or capabilities
- Share use cases and examples
- Report issues or gaps
- Contribute to documentation

---

**Ready to start?** Just describe your AI governance needs and the agent will guide you through the process!
