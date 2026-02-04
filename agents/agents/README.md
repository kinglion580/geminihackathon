# AI Act Package Agents

This directory contains specialized AI agents for comprehensive AI governance and compliance.

## Available Agents

### Governance AI Agent

**File:** `governance-ai-agent.md`

**Description:** A comprehensive super agent with access to ALL AI Act skills packages. This agent provides end-to-end AI governance from planning through deployment and monitoring.

**Capabilities:**
- Complete AI governance planning
- EU AI Act compliance and risk classification
- Multi-regulation compliance (GDPR, HIPAA, PCI-DSS)
- AI safety planning and guardrails
- Bias detection and fairness validation
- ML architecture and project lifecycle
- Automated AI testing and performance evaluation
- Incident response and operational procedures
- Documentation and audit trail generation
- Gemini/Google ecosystem integration

**When to Use:**
- Starting a new AI project and need comprehensive governance
- Auditing existing AI systems for compliance
- Designing safe, ethical, and fair AI systems
- Implementing regulatory compliance (EU AI Act, GDPR, etc.)
- Creating comprehensive AI system documentation
- Setting up monitoring and incident response

## Skills Available to Agents

The Governance AI Agent has access to 53 skills across 4 major categories:

### AI Act Package Skills (16)
AI ethics, governance, testing, safety planning, risk assessment, incident response, transparency instructions, and more.

### AI/ML Planning Skills (10)
ML project lifecycle, model selection, RAG architecture, bias assessment, explainability, HITL design, and more.

### Compliance Planning Skills (9)
GDPR, HIPAA, PCI-DSS compliance, data classification, security frameworks, SBOM management, and more.

### Google Ecosystem Skills (18)
Gemini CLI, context management, MCP integration, token optimization, workspace bridge, and more.

## Usage

To use the Governance AI Agent in Claude Code:

1. **Load the agent** using the Task tool or agent invocation mechanism in Claude Code
2. **Describe your AI project** or governance needs
3. **The agent will:**
   - Assess your requirements
   - Classify risks and compliance obligations
   - Load relevant skills as needed
   - Provide comprehensive guidance
   - Generate documentation and plans

## Example Prompts

```
"I'm building a healthcare AI chatbot. Help me ensure it's compliant with HIPAA and the EU AI Act."
```

```
"Audit my existing customer service AI system for compliance gaps and safety issues."
```

```
"Design a comprehensive governance plan for our new credit scoring AI system."
```

```
"Help me implement guardrails and red team testing for our LLM-based application."
```

## Integration

The Governance AI Agent can work standalone or alongside specialized agents:
- ML Architect (ai-ml-planning)
- Compliance Analyst (compliance-planning)
- Security Auditor (compliance-planning)
- Gemini specialists (google-ecosystem)

## Documentation

Each skill loaded by the agent contains detailed:
- Implementation guidelines
- Code examples
- Best practices
- Regulatory requirements
- Testing strategies
- Documentation templates

## Contributing

To add new skills or capabilities:
1. Create skill in appropriate package directory
2. Document in SKILL.md format
3. Update this README
4. Test integration with Governance AI Agent

## Support

For questions or issues:
- Review skill documentation in respective package directories
- Check AI Act package documentation
- Consult regulatory guidance documents in parent directory
