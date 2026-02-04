---
name: model-selection
description: Select appropriate AI/ML models based on capability matching, benchmarks, cost-performance tradeoffs, and deployment constraints.
allowed-tools: Read, Write, Glob, Grep, Task
---

# Model Selection Framework

## When to Use This Skill

Use this skill when:

- **Model Selection tasks** - Working on select appropriate ai/ml models based on capability matching, benchmarks, cost-performance tradeoffs, and deployment constraints
- **Planning or design** - Need guidance on Model Selection approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Model selection is the systematic process of choosing the right AI/ML model based on task requirements, performance characteristics, cost constraints, and deployment considerations. Poor model selection leads to suboptimal performance, excessive costs, or deployment failures.

## Model Selection Decision Tree

```text
┌─────────────────────────────────────────────────────────────────┐
│                   MODEL SELECTION FRAMEWORK                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. TASK ANALYSIS                                               │
│     What are the core capabilities needed?                      │
│     ├── Text Generation → LLM                                   │
│     ├── Classification → Traditional ML / Small LM              │
│     ├── Code Generation → Code-specialized LLM                  │
│     ├── Vision → Multimodal / Vision Model                      │
│     ├── Embeddings → Embedding Model                            │
│     └── Structured Output → Instruction-tuned LLM               │
│                                                                  │
│  2. REQUIREMENTS MAPPING                                         │
│     ├── Quality: Accuracy, coherence, factuality                │
│     ├── Latency: Real-time vs batch                             │
│     ├── Cost: Per-token, per-request budgets                    │
│     ├── Privacy: Data residency, local deployment               │
│     └── Scale: Requests per second, concurrent users            │
│                                                                  │
│  3. MODEL EVALUATION                                             │
│     ├── Benchmark analysis                                       │
│     ├── Task-specific testing                                   │
│     └── Cost-performance optimization                           │
│                                                                  │
│  4. DEPLOYMENT PLANNING                                          │
│     ├── Cloud API vs self-hosted                                │
│     ├── Hardware requirements                                   │
│     └── Scaling strategy                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## LLM Capability Matrix

### General Purpose Models (December 2025)

| Model | Provider | Context | Strengths | Weaknesses |
|-------|----------|---------|-----------|------------|
| GPT-4o | OpenAI | 128K | Multimodal, fast, reliable | Cost for high volume |
| GPT-4o-mini | OpenAI | 128K | Cost-effective, good quality | Less capable than full |
| Claude 3.5 Sonnet | Anthropic | 200K | Long context, coding, analysis | Availability |
| Claude 3.5 Haiku | Anthropic | 200K | Fast, cost-effective | Less capable |
| Gemini 1.5 Pro | Google | 1M | Massive context, multimodal | Latency variance |
| Gemini 1.5 Flash | Google | 1M | Fast, cost-effective | Quality tradeoffs |
| o1 | OpenAI | 128K | Deep reasoning, math, coding | Slow, expensive |
| o1-mini | OpenAI | 128K | Reasoning, cost-effective | Narrower than o1 |

### Specialized Models

| Use Case | Recommended Models | Notes |
|----------|-------------------|-------|
| Code Generation | GPT-4o, Claude 3.5 Sonnet, Codex | Claude excels at refactoring |
| Long Documents | Claude 3.5, Gemini 1.5 | 200K-1M context |
| Embeddings | text-embedding-3-large, Cohere embed-v3 | Quality vs cost |
| Vision | GPT-4o, Claude 3.5, Gemini 1.5 | All support images |
| Structured Output | GPT-4o (JSON mode), Claude | Schema enforcement |
| Reasoning | o1, o1-mini | Chain of thought |

### Local/Open Models

| Model | Parameters | VRAM Required | Use Case |
|-------|------------|---------------|----------|
| Llama 3.2 | 1B-90B | 2GB-180GB | General, local deployment |
| Mistral | 7B-8x22B | 14GB-180GB | European data residency |
| Phi-3 | 3.8B-14B | 8GB-28GB | Edge, mobile |
| Qwen 2.5 | 0.5B-72B | 1GB-144GB | Multilingual |
| CodeLlama | 7B-70B | 14GB-140GB | Code-specific |

## Model Comparison Framework

### Benchmark Interpretation

| Benchmark | Measures | Weight |
|-----------|----------|--------|
| MMLU | General knowledge | Medium |
| HumanEval | Code generation | High for coding tasks |
| GSM8K | Math reasoning | High for analytical |
| MT-Bench | Conversation quality | High for chat |
| GPQA | Graduate-level QA | Domain expertise |
| Arena ELO | Human preference | Overall quality |

### Task-Specific Evaluation

```csharp
public class ModelEvaluator
{
    public async Task<EvaluationReport> EvaluateModels(
        List<ModelConfig> candidates,
        EvaluationDataset dataset,
        CancellationToken ct)
    {
        var results = new Dictionary<string, ModelMetrics>();

        foreach (var model in candidates)
        {
            var metrics = new ModelMetrics
            {
                ModelId = model.Id,
                Provider = model.Provider
            };

            // Run task-specific tests
            foreach (var testCase in dataset.TestCases)
            {
                var startTime = Stopwatch.StartNew();

                var response = await CallModel(model, testCase.Prompt, ct);

                startTime.Stop();

                metrics.AddResult(new TestResult
                {
                    TestId = testCase.Id,
                    LatencyMs = startTime.ElapsedMilliseconds,
                    InputTokens = CountTokens(testCase.Prompt),
                    OutputTokens = CountTokens(response),
                    Score = await EvaluateResponse(response, testCase.Expected),
                    Cost = CalculateCost(model, testCase.Prompt, response)
                });
            }

            results[model.Id] = metrics;
        }

        return new EvaluationReport
        {
            Results = results,
            Recommendation = SelectBestModel(results, dataset.Requirements)
        };
    }

    private ModelRecommendation SelectBestModel(
        Dictionary<string, ModelMetrics> results,
        Requirements requirements)
    {
        // Score based on requirements weights
        var scores = results.Select(r => new
        {
            Model = r.Key,
            Score = CalculateWeightedScore(r.Value, requirements)
        }).OrderByDescending(s => s.Score);

        return new ModelRecommendation
        {
            Primary = scores.First().Model,
            Fallback = scores.Skip(1).FirstOrDefault()?.Model,
            Reasoning = GenerateReasoning(scores, requirements)
        };
    }
}
```

## Cost-Performance Analysis

### Pricing Comparison (December 2025, per 1M tokens)

| Model | Input Cost | Output Cost | Notes |
|-------|------------|-------------|-------|
| GPT-4o | $2.50 | $10.00 | Standard |
| GPT-4o-mini | $0.15 | $0.60 | Budget option |
| Claude 3.5 Sonnet | $3.00 | $15.00 | Premium |
| Claude 3.5 Haiku | $0.25 | $1.25 | Budget |
| Gemini 1.5 Pro | $1.25 | $5.00 | Pay-as-you-go |
| Gemini 1.5 Flash | $0.075 | $0.30 | High volume |
| o1 | $15.00 | $60.00 | Reasoning tasks |
| o1-mini | $3.00 | $12.00 | Reasoning budget |

### Cost Optimization Strategies

| Strategy | Savings | Trade-off |
|----------|---------|-----------|
| Smaller model for simple tasks | 80-95% | Quality on complex tasks |
| Prompt caching | 50-90% | Cache management complexity |
| Batch processing | 50% | Latency increase |
| Prompt optimization | 20-40% | Development effort |
| Response length limits | 10-30% | Potentially truncated output |

### ROI Calculator

```csharp
public class ModelCostCalculator
{
    public CostProjection CalculateMonthlyCost(
        ModelConfig model,
        UsageEstimate usage)
    {
        var inputCost = usage.MonthlyInputTokens / 1_000_000m
            * model.InputPricePerMillion;

        var outputCost = usage.MonthlyOutputTokens / 1_000_000m
            * model.OutputPricePerMillion;

        var cachedSavings = usage.CacheHitRate * inputCost
            * model.CacheDiscount;

        return new CostProjection
        {
            GrossInputCost = inputCost,
            GrossOutputCost = outputCost,
            CacheSavings = cachedSavings,
            NetMonthlyCost = inputCost + outputCost - cachedSavings,
            CostPerRequest = (inputCost + outputCost - cachedSavings)
                / usage.MonthlyRequests
        };
    }

    public ModelComparison CompareModels(
        List<ModelConfig> models,
        UsageEstimate usage,
        QualityRequirements requirements)
    {
        var comparisons = models.Select(m => new
        {
            Model = m,
            Cost = CalculateMonthlyCost(m, usage),
            MeetsRequirements = EvaluateQuality(m, requirements)
        }).Where(c => c.MeetsRequirements)
          .OrderBy(c => c.Cost.NetMonthlyCost)
          .ToList();

        return new ModelComparison
        {
            CheapestQualified = comparisons.FirstOrDefault()?.Model,
            AllOptions = comparisons,
            Savings = CalculateSavings(comparisons)
        };
    }
}
```

## Fine-Tuning Decision Framework

### When to Fine-Tune

| Consider Fine-Tuning | Use Prompting Instead |
|---------------------|----------------------|
| Consistent specific format | Few-shot examples work |
| Domain vocabulary | General vocabulary |
| Latency critical (shorter prompts) | Latency acceptable |
| High volume (amortize cost) | Low volume |
| Specialized behavior | Standard behavior |
| Proprietary knowledge | Public knowledge |

### Fine-Tuning ROI Analysis

```markdown
## Fine-Tuning Decision: [Use Case]

### Current State (Prompting)
- Prompt tokens: [X] tokens
- Output quality: [Score]
- Cost per request: $[X]
- Monthly cost: $[X]

### Projected State (Fine-Tuned)
- Prompt tokens: [Y] tokens (reduced)
- Output quality: [Score] (maintained/improved)
- Fine-tuning cost: $[X] (one-time)
- Inference cost per request: $[Y]
- Monthly cost: $[Y]

### Break-Even Analysis
- Monthly savings: $[X]
- Break-even: [N] months
- 12-month ROI: [X]%

### Recommendation
[Fine-tune / Continue prompting / Hybrid approach]
```

## Deployment Considerations

### Cloud vs Self-Hosted Decision

| Factor | Cloud API | Self-Hosted |
|--------|-----------|-------------|
| Initial cost | Low (pay-per-use) | High (infrastructure) |
| Scaling | Automatic | Manual |
| Latency | Network dependent | Controlled |
| Data privacy | Limited | Full control |
| Customization | Limited | Full |
| Maintenance | None | Significant |

### Hardware Requirements (Self-Hosted)

| Model Size | GPU Memory | Recommended GPU |
|------------|------------|-----------------|
| 7B | 14GB | RTX 4090, A10 |
| 13B | 26GB | A100-40GB |
| 30B | 60GB | 2x A100-40GB |
| 70B | 140GB | 2x A100-80GB |
| 8x7B (MoE) | 100GB+ | Multiple A100s |

## Model Selection Template

```markdown
# Model Selection: [Project Name]

## Task Requirements
- **Primary Use Case**: [Description]
- **Quality Requirements**: [Accuracy/coherence targets]
- **Latency Requirements**: [P95 target]
- **Volume**: [Requests/day]
- **Budget**: [Monthly budget]

## Evaluation Results

| Model | Quality Score | P95 Latency | Monthly Cost | Notes |
|-------|--------------|-------------|--------------|-------|
| [Model A] | [Score] | [ms] | $[X] | [Notes] |
| [Model B] | [Score] | [ms] | $[X] | [Notes] |
| [Model C] | [Score] | [ms] | $[X] | [Notes] |

## Recommendation

**Primary Model**: [Model]
- Rationale: [Why this model]

**Fallback Model**: [Model]
- Use when: [Conditions]

**Cost Projection**: $[X]/month

## Implementation Notes
- [Deployment approach]
- [Monitoring strategy]
- [Scaling considerations]
```

## Validation Checklist

- [ ] Task requirements clearly defined
- [ ] Capability mapping completed
- [ ] Candidate models identified
- [ ] Benchmarks reviewed
- [ ] Task-specific evaluation conducted
- [ ] Cost analysis completed
- [ ] Latency requirements validated
- [ ] Deployment constraints considered
- [ ] Fine-tuning decision made
- [ ] Fallback strategy defined

## Integration Points

**Inputs from**:

- Business requirements → Task definition
- `ml-project-lifecycle` skill → Project constraints

**Outputs to**:

- `token-budgeting` skill → Cost estimation
- `rag-architecture` skill → Embedding model selection
- Application code → Model configuration
