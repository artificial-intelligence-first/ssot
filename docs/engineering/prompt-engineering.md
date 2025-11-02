---
title: Prompt Engineering
slug: prompt-engineering
status: living
last_updated: 2025-11-01
tags: [prompt-engineering, prompting, agents, best-practices]
summary: "Cross-platform prompt engineering best practices from major AI providers for reliable AI outputs."
authors: []
sources:
  - { id: R1, title: "Anthropic Prompt Engineering Overview", url: "https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview", accessed: "2025-10-20" }
  - { id: R2, title: "Anthropic Prompt Engineering Interactive Tutorial", url: "https://github.com/anthropics/prompt-eng-interactive-tutorial", accessed: "2025-10-20" }
  - { id: R3, title: "Google Vertex AI Prompt Design", url: "https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design", accessed: "2025-10-20" }
  - { id: R4, title: "OpenAI Prompt Engineering Guide", url: "https://platform.openai.com/docs/guides/prompt-engineering", accessed: "2025-10-20" }
---

# Prompt Engineering

> **For Humans**: This guide consolidates prompt engineering best practices from major AI platforms. Use it to design effective prompts that produce reliable, high-quality outputs from AI coding assistants.
>
> **For AI Agents**: Apply these patterns when generating prompts, structuring complex requests, or optimizing interactions with other AI systems. Follow platform-specific guidelines when available.

## Overview

Prompt engineering is the practice of designing and refining inputs to AI systems to elicit desired outputs. This guide synthesizes best practices from Anthropic, Google, and OpenAI to provide cross-platform techniques for reliable AI interactions.

## Canonical Definitions

### Core Terms

**Prompt**: The complete input provided to an AI model, including instructions, context, and examples.

**System Prompt**: Initial instructions that set the AI's role, behavior, and constraints.

**Few-Shot Learning**: Providing examples in the prompt to demonstrate desired behavior.

**Chain-of-Thought (CoT)**: Prompting technique that encourages step-by-step reasoning.

**Constitutional AI**: Anthropic's approach to training AI systems with explicit principles.

## Core Patterns

### Pattern: Clear Instructions

Be specific and unambiguous:

```python
# ❌ Vague
prompt = "Fix the code"

# ✅ Clear
prompt = """
Fix the Python function below to handle edge cases:
1. Add input validation for non-integer inputs
2. Handle empty list inputs
3. Add appropriate error messages
4. Maintain existing functionality

def calculate_average(numbers):
    return sum(numbers) / len(numbers)
"""
```

### Pattern: Structured Output

Specify exact format needed:

```python
prompt = """
Analyze this code and provide a JSON response:

{
  "issues": [
    {"line": <int>, "type": <"error"|"warning">, "message": <string>}
  ],
  "suggestions": [<string>],
  "complexity": <"low"|"medium"|"high">
}

Code to analyze:
{code}
"""
```

### Pattern: Few-Shot Examples

Demonstrate desired behavior:

```python
prompt = """
Convert these function names to the specified style:

getUserName -> get_user_name
calculateTotal -> calculate_total
validateInput -> validate_input

Now convert: processPaymentMethod
"""
```

### Pattern: Chain-of-Thought

Encourage reasoning:

```python
prompt = """
Let's approach this step-by-step:

1. First, identify the algorithm being used
2. Then, analyze its time complexity
3. Next, identify potential optimizations
4. Finally, provide the optimized code

Code to optimize:
{code}
"""
```

## Platform-Specific Guidelines

### Anthropic (Claude)

```python
# Use XML tags for structure
prompt = """
<task>Refactor this function</task>

<requirements>
- Maintain backward compatibility
- Improve readability
- Add type hints
</requirements>

<code>
{function_code}
</code>
"""

# Be direct and conversational
prompt = "Please help me refactor this function to be more readable while maintaining backward compatibility."
```

### OpenAI (GPT)

```python
# Use system messages effectively
messages = [
    {"role": "system", "content": "You are an expert Python developer focused on clean code."},
    {"role": "user", "content": "Refactor this function:\n{code}"}
]

# Use functions/tools for structured output
tools = [{
    "type": "function",
    "function": {
        "name": "analyze_code",
        "description": "Analyze code quality",
        "parameters": {...}
    }
}]
```

### Google (Gemini/Vertex)

```python
# Use safety settings appropriately
safety_settings = {
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

# Leverage multimodal capabilities
prompt = """
Analyze this architecture diagram and suggest improvements.
Consider the code structure shown in the image.
"""
```

## Decision Checklist

Before sending a prompt:

- [ ] Is the task clearly defined?
- [ ] Are success criteria specified?
- [ ] Is the output format defined?
- [ ] Are edge cases mentioned?
- [ ] Are examples provided for complex tasks?
- [ ] Is unnecessary information removed?
- [ ] Is the tone appropriate for the model?

## Anti-patterns

### Ambiguous Instructions
❌ **Wrong**: "Make it better"
✅ **Right**: "Improve performance by reducing time complexity from O(n²) to O(n log n)"

### Information Overload
❌ **Wrong**: Including entire codebase
✅ **Right**: Relevant functions and immediate dependencies only

### Assuming Context
❌ **Wrong**: "Fix it like last time"
✅ **Right**: "Apply the same validation pattern used in user_auth.py"

## Evaluation

### Metrics

- **Task Completion Rate**: Percentage of prompts achieving desired outcome
- **Iteration Count**: Number of refinements needed
- **Output Consistency**: Variance in outputs for same prompt
- **Token Efficiency**: Output quality / tokens used
- **Error Rate**: Percentage of outputs with errors

### Testing Framework

```python
def test_prompt_effectiveness(prompt_template, test_cases):
    results = []
    for test in test_cases:
        prompt = prompt_template.format(**test.inputs)
        output = model.generate(prompt)
        score = evaluate_output(output, test.expected)
        results.append({
            "test": test.name,
            "score": score,
            "output": output
        })
    return aggregate_results(results)
```

## Advanced Techniques

### Meta-Prompting

```python
meta_prompt = """
You are about to receive a prompt. First, analyze what makes a good response:
1. What is the core task?
2. What constraints exist?
3. What would excellence look like?

Then provide your response.

Original prompt: {user_prompt}
"""
```

### Self-Consistency

```python
# Generate multiple outputs and select consensus
outputs = []
for i in range(5):
    output = model.generate(prompt, temperature=0.7)
    outputs.append(output)

final_answer = find_consensus(outputs)
```

## See Also

- [Context Engineering](./context-engineering.md)
- [LangChain Guide](../platforms/langchain/langchain.md)
- [AGENTS.md](../../AGENTS.md)

## References

- [R1] Anthropic Prompt Engineering Overview. https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview (accessed 2025-10-20)
- [R2] Anthropic Prompt Engineering Interactive Tutorial. https://github.com/anthropics/prompt-eng-interactive-tutorial (accessed 2025-10-20)
- [R3] Google Vertex AI Prompt Design. https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design (accessed 2025-10-20)
- [R4] OpenAI Prompt Engineering Guide. https://platform.openai.com/docs/guides/prompt-engineering (accessed 2025-10-20)
