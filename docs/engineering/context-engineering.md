---
title: Context Engineering
slug: context-engineering
status: living
last_updated: 2025-11-01
tags: [context, rag, retrieval, prompt-engineering, agents]
summary: "Best practices for designing, retrieving, and evaluating context bundles that feed AI workflows across platforms."
authors: []
sources:
  - { id: R1, title: "Effective Context Engineering for AI Agents", url: "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents", accessed: "2025-10-20" }
  - { id: R2, title: "Claude Long Context Tips", url: "https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/long-context-tips", accessed: "2025-10-20" }
  - { id: R3, title: "Context Engineering Guide", url: "https://www.promptingguide.ai/guides/context-engineering-guide", accessed: "2025-10-20" }
---

# Context Engineering

> **For Humans**: This guide consolidates best practices for designing, retrieving, and evaluating context bundles that feed AI workflows. Use it to understand how to structure context effectively across different AI platforms.
>
> **For AI Agents**: Review this guide when designing context pipelines, structuring multi-document prompts, or implementing retrieval systems. Follow these patterns to maintain high-quality, relevant context delivery.

## Overview

Context engineering is the discipline of designing, retrieving, and evaluating the information bundles that feed AI workflows. Unlike traditional prompt engineering that focuses on instruction clarity, context engineering optimizes the **relevant background information** that helps AI systems produce accurate, grounded responses.

## Canonical Definitions

### Core Terms

**Context Window**: The maximum amount of text (measured in tokens) that an AI model can process in a single request.

**Context Bundle**: A curated collection of documents, examples, and metadata assembled for a specific AI task.

**Retrieval-Augmented Generation (RAG)**: A pattern where relevant documents are dynamically retrieved and included in the prompt context.

**Semantic Chunking**: Dividing documents into meaningful segments that preserve semantic coherence.

**Context Compression**: Techniques for reducing context size while preserving essential information.

## Core Patterns

### Pattern: Hierarchical Context

Structure context from general to specific:

```python
context = {
    "system": "You are a technical documentation assistant.",
    "project": "Project overview and architecture...",
    "module": "Specific module documentation...",
    "task": "Current task details...",
    "examples": ["Example 1...", "Example 2..."]
}
```

### Pattern: Semantic Chunking

Break documents at natural boundaries:

```python
def semantic_chunk(text, max_tokens=1000):
    # Split by sections first
    sections = text.split("\n## ")

    chunks = []
    current_chunk = ""

    for section in sections:
        if len(tokenize(current_chunk + section)) > max_tokens:
            chunks.append(current_chunk)
            current_chunk = section
        else:
            current_chunk += "\n## " + section

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
```

### Pattern: Dynamic Retrieval

Retrieve context based on query similarity:

```python
def retrieve_context(query, documents, top_k=5):
    # Compute embeddings
    query_embedding = embed(query)
    doc_embeddings = [embed(doc) for doc in documents]

    # Calculate similarities
    similarities = [
        cosine_similarity(query_embedding, doc_emb)
        for doc_emb in doc_embeddings
    ]

    # Return top-k documents
    top_indices = sorted(range(len(similarities)),
                        key=lambda i: similarities[i],
                        reverse=True)[:top_k]

    return [documents[i] for i in top_indices]
```

## Decision Checklist

When designing context:

- [ ] Is the context relevant to the specific task?
- [ ] Is information ordered from general to specific?
- [ ] Are examples representative and diverse?
- [ ] Is redundant information minimized?
- [ ] Are semantic boundaries preserved in chunks?
- [ ] Is the total context within model limits?
- [ ] Are source references included for verification?

## Anti-patterns

### Kitchen Sink Context
❌ **Wrong**: Including all available documentation
✅ **Right**: Curated, relevant information only

### Lost in the Middle
❌ **Wrong**: Important information buried in middle of context
✅ **Right**: Critical information at beginning and end

### Semantic Fragmentation
❌ **Wrong**: Splitting mid-sentence or mid-paragraph
✅ **Right**: Splitting at section or paragraph boundaries

## Evaluation

### Metrics

- **Relevance Score**: Percentage of context actually used in response
- **Compression Ratio**: Original size / Compressed size
- **Retrieval Precision**: Relevant docs / Retrieved docs
- **Context Utilization**: Tokens referenced / Total context tokens
- **Response Accuracy**: Factual correctness with given context

### Testing Strategy

```python
def evaluate_context_quality(context, query, response):
    metrics = {
        "relevance": calculate_relevance(context, response),
        "coverage": calculate_coverage(query, context),
        "redundancy": calculate_redundancy(context),
        "coherence": calculate_coherence(context)
    }
    return metrics
```

## Platform-Specific Guidelines

### Claude (Anthropic)
- Maximum context: 200K tokens
- Place instructions after context
- Use XML tags for structure

### GPT-4 (OpenAI)
- Maximum context: 128K tokens
- System message separate from context
- JSON structure preferred

### Gemini (Google)
- Maximum context: 1M tokens
- Multimodal context supported
- Hierarchical prompting available

## See Also

- [Prompt Engineering](./prompt-engineering.md)
- [Prompt Engineering](./prompt-engineering.md)
- [AGENTS.md](../../AGENTS.md)

## References

- [R1] Effective Context Engineering for AI Agents. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (accessed 2025-10-20)
- [R2] Claude Long Context Tips. https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/long-context-tips (accessed 2025-10-20)
- [R3] Context Engineering Guide. https://www.promptingguide.ai/guides/context-engineering-guide (accessed 2025-10-20)
