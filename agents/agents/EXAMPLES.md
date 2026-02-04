# Governance AI Agent - Usage Examples

This document provides practical examples of using the Governance AI Agent for various AI governance scenarios.

## Example 1: New Healthcare AI Project

**Scenario:** You're building a diagnostic AI assistant for healthcare providers.

**Prompt:**
```
I'm developing an AI system that assists healthcare providers with preliminary diagnosis
based on patient symptoms and medical history. The system will be used in EU hospitals.
Help me design a comprehensive governance plan ensuring compliance with EU AI Act, GDPR,
and HIPAA requirements.
```

**Expected Agent Actions:**
1. Classify system as "High-Risk" under EU AI Act (healthcare, medical devices)
2. Load skills:
   - `risk-assessment` - Identify specific risks
   - `gdpr-compliance` - Data protection requirements
   - `hipaa-compliance` - Healthcare data security
   - `ai-safety-planning` - Safety guardrails
   - `explainability-planning` - Medical transparency requirements
   - `bias-assessment` - Clinical fairness validation
3. Generate comprehensive governance plan with:
   - Risk classification and justification
   - Compliance requirements matrix
   - Safety guardrail architecture
   - Testing strategy including bias testing
   - Documentation requirements
   - Incident response plan

## Example 2: Credit Scoring System Audit

**Scenario:** Audit existing credit scoring AI for compliance gaps.

**Prompt:**
```
We have an existing AI-based credit scoring system deployed for 6 months.
We need to audit it for EU AI Act compliance, identify gaps, and create
a remediation roadmap.
```

**Expected Agent Actions:**
1. Classify as "High-Risk" (employment, credit, essential services)
2. Load skills:
   - `ai-governance` - Governance framework assessment
   - `risk-assessment` - Comprehensive risk evaluation
   - `bias-assessment` - Fairness and discrimination analysis
   - `explainability-planning` - Transparency assessment
   - `ai-testing` - Quality and reliability testing
   - `automatic-logging` - Audit trail verification
3. Generate audit report with:
   - Current compliance status
   - Gap analysis (Critical/High/Medium/Low)
   - Remediation roadmap with priorities
   - Testing requirements
   - Documentation gaps
   - Timeline and resource estimates

## Example 3: Customer Service Chatbot

**Scenario:** Implementing safety guardrails for customer service LLM.

**Prompt:**
```
We're deploying a customer service chatbot powered by an LLM. We need to implement
guardrails to prevent prompt injection, ensure safe responses, and maintain brand
voice. Help us design the safety architecture.
```

**Expected Agent Actions:**
1. Classify as "Limited Risk" (chatbot, transparency required)
2. Load skills:
   - `ai-safety-planning` - Guardrail architecture
   - `prompt-engineering` - System prompt design
   - `ai-testing` - Security and safety testing
   - `fact-checker` - Response validation
   - `incident-responder` - Safety incident handling
3. Generate implementation plan:
   - Input guard architecture (injection detection)
   - Output filter design (toxicity, PII)
   - System prompt with safety instructions
   - Red team testing scenarios
   - Monitoring and alerting setup
   - Incident response procedures

## Example 4: RAG System for Legal Research

**Scenario:** Building a retrieval-augmented generation system for legal document analysis.

**Prompt:**
```
We're building a RAG-based AI system for legal research that retrieves and analyzes
case law and regulations. It needs to be highly accurate, explainable, and compliant.
Design the architecture and governance framework.
```

**Expected Agent Actions:**
1. Classify based on use case (potentially High-Risk if used for legal decisions)
2. Load skills:
   - `rag-architecture` - RAG design patterns
   - `explainability-planning` - Citation and sourcing
   - `ai-testing` - Accuracy and hallucination testing
   - `fact-checker` - Legal fact verification
   - `model-selection` - Model choice for legal domain
   - `token-budgeting` - Cost optimization
   - `hitl-design` - Lawyer oversight integration
3. Generate comprehensive plan:
   - RAG architecture with retrieval strategy
   - Citation and explanation mechanisms
   - Accuracy testing methodology
   - Human-in-the-loop checkpoints
   - Cost estimates and optimization
   - Documentation requirements

## Example 5: Automated Hiring Assistant

**Scenario:** AI system for initial resume screening and candidate ranking.

**Prompt:**
```
We want to build an AI assistant that screens resumes and ranks candidates for
initial interviews. What are the governance requirements and how do we ensure
fairness and compliance?
```

**Expected Agent Actions:**
1. Classify as "High-Risk" (employment, HR, potential discrimination)
2. Load skills:
   - `risk-assessment` - Discrimination and bias risks
   - `bias-assessment` - Fairness metrics and testing
   - `ai-governance` - HR AI governance policies
   - `explainability-planning` - Decision explainability
   - `hitl-design` - Human recruiter oversight
   - `gdpr-compliance` - Candidate data protection
   - `ai-testing` - Bias and fairness testing
3. Generate compliance plan:
   - EU AI Act High-Risk requirements
   - Bias mitigation strategies
   - Fairness testing methodology (demographic parity, etc.)
   - Explainability for candidates and recruiters
   - Human oversight architecture
   - GDPR compliance measures
   - Documentation and audit trail
   - Appeals and recourse mechanisms

## Example 6: Multi-Agent AI System

**Scenario:** Complex multi-agent system with multiple AI components.

**Prompt:**
```
We're building a multi-agent AI system where different agents handle customer
inquiries, route to specialists, and execute tasks. How do we govern this
complex system?
```

**Expected Agent Actions:**
1. Assess overall system risk and component risks
2. Load skills:
   - `agentic-workflow-design` - Agent architecture patterns
   - `ai-governance` - Multi-component governance
   - `ai-safety-planning` - Safety across agent interactions
   - `automatic-logging` - Comprehensive audit trails
   - `ai-testing` - Integration and system testing
   - `incident-responder` - Cross-agent incident handling
3. Generate governance framework:
   - System architecture with governance boundaries
   - Risk assessment per agent and system-wide
   - Safety guardrails at agent and orchestration levels
   - Testing strategy (unit, integration, system)
   - Monitoring and observability
   - Incident detection and response
   - Documentation structure

## Example 7: Deploying AI to Production

**Scenario:** Ready to deploy AI system and need deployment checklist.

**Prompt:**
```
Our AI system is ready for production deployment. What's the governance
checklist to ensure we've covered all requirements before launch?
```

**Expected Agent Actions:**
1. Review system risk classification
2. Load skills:
   - `deployer-training` - Deployment team training
   - `automatic-logging` - Production logging setup
   - `downstream-notifier` - Stakeholder communication
   - `incident-responder` - Incident procedures
   - `ai-testing` - Pre-launch testing
   - `standards-compliance-interoperability` - Standards verification
3. Generate deployment checklist:
   - Pre-launch testing completion verification
   - Documentation completeness check
   - Training completion for deployers
   - Logging and monitoring activation
   - Incident response team readiness
   - Stakeholder communication plan
   - Rollback procedures
   - Post-deployment validation
   - Compliance certification status

## Example 8: Gemini-Based Application

**Scenario:** Building application using Google's Gemini with Claude Code.

**Prompt:**
```
I'm building a Gemini-powered application using Claude Code. Help me set up
the development environment, governance, and best practices.
```

**Expected Agent Actions:**
1. Assess application risk level
2. Load skills:
   - `gemini-cli-execution` - Gemini CLI setup
   - `gemini-config-management` - Configuration
   - `gemini-mcp-integration` - MCP server integration
   - `gemini-context-bridge` - Context management
   - `gemini-token-optimization` - Cost optimization
   - `ai-safety-planning` - Gemini safety features
   - `prompt-engineering` - Gemini prompt design
3. Generate implementation guide:
   - Gemini CLI setup and configuration
   - MCP integration for tools
   - Context and memory management
   - Token optimization strategies
   - Safety and content filtering
   - Testing and evaluation
   - Cost monitoring and budgeting

## Example 9: Incident Response

**Scenario:** AI system produced harmful output and needs investigation.

**Prompt:**
```
Our AI system generated inappropriate content that violated our policies.
How do we investigate and prevent this in the future?
```

**Expected Agent Actions:**
1. Activate incident response mode
2. Load skills:
   - `incident-responder` - Investigation procedures
   - `automatic-logging` - Log analysis
   - `ai-testing` - Reproduce and test
   - `ai-safety-planning` - Enhanced guardrails
   - `fact-checker` - Output validation
3. Generate incident response:
   - Immediate containment actions
   - Investigation methodology
   - Log analysis and root cause
   - Reproduction testing
   - Guardrail enhancement recommendations
   - Preventive measures
   - Stakeholder communication
   - Documentation and reporting

## Example 10: Continuous Compliance Monitoring

**Scenario:** Setting up ongoing compliance monitoring for AI system.

**Prompt:**
```
We need to set up continuous compliance monitoring for our High-Risk AI
system to ensure ongoing regulatory adherence. What should we monitor
and how?
```

**Expected Agent Actions:**
1. Review system risk and compliance obligations
2. Load skills:
   - `ai-governance` - Governance metrics
   - `automatic-logging` - Audit trail configuration
   - `ai-testing` - Continuous testing
   - `bias-assessment` - Ongoing fairness monitoring
   - `ai-performance-testing` - Performance tracking
3. Generate monitoring plan:
   - Compliance metrics and KPIs
   - Automated monitoring dashboards
   - Alert thresholds and escalation
   - Continuous testing schedule
   - Bias and fairness monitoring
   - Performance degradation detection
   - Audit log retention and analysis
   - Periodic review schedule
   - Compliance reporting

## Tips for Using the Governance AI Agent

1. **Be Specific:** Provide context about your AI system, industry, and geography
2. **Ask Follow-ups:** The agent can drill deeper into any aspect
3. **Request Examples:** Ask for code examples, templates, or specific implementations
4. **Iterate:** Start with high-level planning, then iterate on specific components
5. **Load Skills Gradually:** Don't try to use all skills at once; let the agent guide you
6. **Document Everything:** Ask the agent to generate documentation as you go
7. **Stay Updated:** Use the agent to check for regulatory updates and best practices

## Common Patterns

- **Assessment → Planning → Implementation → Monitoring**
- **Risk Classification → Compliance Mapping → Mitigation Design**
- **Architecture Design → Safety Layer → Testing Strategy → Deployment**
- **Audit → Gap Analysis → Remediation → Validation**
