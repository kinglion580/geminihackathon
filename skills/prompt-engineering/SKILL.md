---
name: prompt-engineering
description: Design, test, and version prompts with systematic evaluation and optimization strategies.
allowed-tools: Read, Write, Glob, Grep, Task
---

# Prompt Engineering

## When to Use This Skill

Use this skill when:

- **Prompt Engineering tasks** - Working on design, test, and version prompts with systematic evaluation and optimization strategies
- **Planning or design** - Need guidance on Prompt Engineering approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Prompt engineering is the systematic design, testing, and optimization of prompts for large language models. Good prompts significantly impact model performance, reliability, and cost.

## Prompt Design Patterns

### Pattern Catalog

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Zero-shot | No examples, task description only | Simple, well-defined tasks |
| Few-shot | Include examples | Complex, ambiguous tasks |
| Chain-of-Thought | Step-by-step reasoning | Math, logic, analysis |
| Tree-of-Thought | Multiple reasoning paths | Complex problem solving |
| ReAct | Reasoning + Actions | Tool use, agents |
| Self-Consistency | Multiple outputs, vote | High-stakes decisions |

### Prompt Structure Template

```markdown
# Prompt: [Task Name]

## System Prompt
[Role definition and behavioral constraints]

## User Prompt Template
[Template with {placeholders}]

## Few-Shot Examples (if applicable)
### Example 1
Input: [Example input]
Output: [Expected output]

### Example 2
Input: [Example input]
Output: [Expected output]

## Output Format
[Expected structure, JSON schema if applicable]

## Guardrails
- [Constraint 1]
- [Constraint 2]
```

## Prompt Components

### System Prompt Best Practices

```text
┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM PROMPT STRUCTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. ROLE DEFINITION                                             │
│     "You are a [role] that [primary function]"                  │
│                                                                  │
│  2. CONTEXT                                                     │
│     Background information, domain knowledge                     │
│                                                                  │
│  3. INSTRUCTIONS                                                │
│     Clear, specific directions                                   │
│                                                                  │
│  4. OUTPUT FORMAT                                               │
│     Structure, schema, examples                                  │
│                                                                  │
│  5. CONSTRAINTS                                                 │
│     What NOT to do, boundaries                                  │
│                                                                  │
│  6. EXAMPLES (Optional)                                         │
│     Demonstrate expected behavior                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Example System Prompt

```text
You are a customer service assistant for TechCorp, specializing in product support.

CONTEXT:
- TechCorp sells software products (ProductA, ProductB, ProductC)
- Support hours are 9 AM - 5 PM EST
- Escalation is needed for billing issues and account closures

INSTRUCTIONS:
1. Greet the customer professionally
2. Identify their issue category
3. Provide relevant solutions or resources
4. Offer escalation if needed

OUTPUT FORMAT:
- Keep responses under 150 words
- Use bullet points for multiple items
- Include relevant KB article links

CONSTRAINTS:
- Never share internal pricing
- Don't make promises about refunds
- Don't provide legal advice
- Refer technical issues beyond scope to engineering
```

## Chain-of-Thought Patterns

### Standard CoT

```text
Let's think through this step by step:

1. First, identify the key information...
2. Next, consider the constraints...
3. Then, apply the relevant formula...
4. Finally, calculate the answer...

Therefore, the answer is: [result]
```

### Structured CoT

```markdown
## Analysis

### Given Information
- [Fact 1]
- [Fact 2]

### Reasoning Steps
1. [Step 1 with explanation]
2. [Step 2 with explanation]
3. [Step 3 with explanation]

### Conclusion
[Final answer with confidence level]
```

## Prompt Testing Framework

### Test Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| Functional | Does it work? | Expected outputs |
| Edge Cases | Unusual inputs | Empty, long, special chars |
| Adversarial | Attack resistance | Jailbreaks, injections |
| Consistency | Reproducibility | Same input, similar output |
| Performance | Speed/cost | Latency, token usage |

### Evaluation Metrics

| Metric | Description | Measurement |
|--------|-------------|-------------|
| Accuracy | Correct responses | % match to ground truth |
| Relevance | On-topic responses | Human rating 1-5 |
| Coherence | Logical flow | Human rating 1-5 |
| Helpfulness | Task completion | Success rate |
| Safety | No harmful content | Violation rate |

### Test Case Template

```markdown
# Prompt Test: [Test Name]

## Prompt Version
Version: 1.2.0
Git Hash: abc123

## Test Case
| ID | Input | Expected | Actual | Pass |
|----|-------|----------|--------|------|
| TC-001 | [Input] | [Expected] | [Actual] | ✓/✗ |
| TC-002 | [Input] | [Expected] | [Actual] | ✓/✗ |

## Metrics
| Metric | Target | Actual |
|--------|--------|--------|
| Accuracy | >90% | 92% |
| Latency | <2s | 1.5s |
| Tokens | <500 | 420 |
```

## Prompt Versioning

### Version Control Strategy

```text
prompts/
├── customer-service/
│   ├── v1.0.0/
│   │   ├── system.txt
│   │   ├── template.txt
│   │   ├── examples.json
│   │   └── metadata.yaml
│   ├── v1.1.0/
│   │   └── ...
│   └── changelog.md
├── summarization/
│   └── ...
└── registry.yaml
```

### Metadata Schema

```yaml
# metadata.yaml
name: customer-service-prompt
version: 1.2.0
description: Customer service response generation
model:
  recommended: gpt-4o
  compatible:
    - gpt-4o
    - gpt-4o-mini
    - claude-3-5-sonnet
parameters:
  temperature: 0.7
  max_tokens: 500
  top_p: 1.0
metrics:
  accuracy: 0.92
  latency_p95_ms: 1500
  avg_tokens: 420
created: 2024-12-15
author: data-team
tags:
  - production
  - customer-facing
```

## C# Prompt Management

```csharp
public class PromptManager
{
    private readonly IPromptRepository _repository;

    public async Task<Prompt> GetPrompt(
        string name,
        string version = "latest",
        CancellationToken ct = default)
    {
        var prompt = await _repository.GetAsync(name, version, ct);

        return new Prompt
        {
            SystemMessage = prompt.System,
            Template = prompt.Template,
            Examples = prompt.Examples,
            Parameters = new PromptParameters
            {
                Temperature = prompt.Metadata.Parameters.Temperature,
                MaxTokens = prompt.Metadata.Parameters.MaxTokens
            }
        };
    }

    public string Render(Prompt prompt, Dictionary<string, string> variables)
    {
        var rendered = prompt.Template;

        foreach (var (key, value) in variables)
        {
            rendered = rendered.Replace($"{{{key}}}", value);
        }

        return rendered;
    }
}

// Usage with Semantic Kernel
var promptManager = new PromptManager(repository);
var prompt = await promptManager.GetPrompt("customer-service", "1.2.0");

var kernel = Kernel.CreateBuilder()
    .AddAzureOpenAIChatCompletion(deployment, endpoint, apiKey)
    .Build();

var function = kernel.CreateFunctionFromPrompt(
    prompt.Template,
    new OpenAIPromptExecutionSettings
    {
        Temperature = prompt.Parameters.Temperature,
        MaxTokens = prompt.Parameters.MaxTokens
    });

var result = await kernel.InvokeAsync(function, new KernelArguments
{
    ["customer_name"] = "John",
    ["issue"] = "Password reset"
});
```

## Optimization Techniques

### Token Optimization

| Technique | Savings | Trade-off |
|-----------|---------|-----------|
| Shorter examples | 20-40% | Less context |
| Remove redundancy | 10-20% | Less robustness |
| Structured output | 15-30% | Parsing needed |
| Summarize context | 30-50% | Information loss |

### Prompt Compression

```csharp
public class PromptOptimizer
{
    public OptimizedPrompt Optimize(string prompt, OptimizationOptions options)
    {
        var optimized = prompt;
        var savings = 0;

        if (options.RemoveWhitespace)
        {
            var before = CountTokens(optimized);
            optimized = Regex.Replace(optimized, @"\s+", " ");
            savings += before - CountTokens(optimized);
        }

        if (options.UseAbbreviations)
        {
            optimized = ApplyAbbreviations(optimized);
        }

        if (options.CompressExamples)
        {
            optimized = CompressExamples(optimized, options.MaxExamples);
        }

        return new OptimizedPrompt
        {
            Content = optimized,
            OriginalTokens = CountTokens(prompt),
            OptimizedTokens = CountTokens(optimized),
            SavingsPercent = savings * 100.0 / CountTokens(prompt)
        };
    }
}
```

## Validation Checklist

- [ ] Clear role and context defined
- [ ] Instructions are specific and unambiguous
- [ ] Output format specified
- [ ] Constraints and guardrails included
- [ ] Few-shot examples provided (if needed)
- [ ] Test cases cover happy path and edge cases
- [ ] Adversarial testing completed
- [ ] Version control in place
- [ ] Performance metrics measured
- [ ] Token usage optimized

## Integration Points

**Inputs from**:

- Business requirements → Task definition
- `ai-safety-planning` skill → Guardrail requirements

**Outputs to**:

- `token-budgeting` skill → Cost estimation
- `agentic-workflow-design` skill → Agent prompts
- Application code → Prompt templates
