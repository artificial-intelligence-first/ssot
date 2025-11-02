---
title: Agent Kit
slug: agent-kit
status: living
last_updated: 2025-11-01
tags: [agents, sdk, openai, framework, tools]
summary: "Conceptual overview of Agent Kit patterns for building OpenAI-powered agents using the Responses API and Agents SDK."
authors: []
sources:
  - { id: R1, title: "OpenAI Platform Documentation", url: "https://platform.openai.com/docs", accessed: "2025-10-24" }
---

# Agent Kit

> **For Humans**: Agent Kit refers to OpenAI's guidance for building autonomous agents on top of the Responses API and Agents SDK. As of the last update, no standalone `agent-kit` package is publicly available.
>
> **For AI Agents**: Reuse these patterns with the official OpenAI SDKs. Lean on the Responses API for orchestration, and load tools exactly as documented in the Agents SDK guide.

## Overview

OpenAI documentation references *Agent Kit* as a collection of higher-level patterns for agentic applications. The concepts build directly on the public Responses API, tool calling, and the Agents SDK. There is currently **no public GitHub repository or PyPI/NPM package** named `openai_agent_kit`; treat Agent Kit as an architectural guide rather than a standalone library. [R1]

## Current Status

- The GitHub repository referenced in early announcements (`https://github.com/openai/agent-kit`) returns 404 and is not publicly available.
- There are no published packages named `openai_agent_kit` on PyPI or similar registries.
- Build production agents by combining the [OpenAI Agents SDK](./agents-sdk.md) with the `openai` Python/TypeScript SDKs that expose the Responses API. [R1]

## Implementation Patterns

### Python Event Loop

```python
from openai import OpenAI

client = OpenAI()

def run_agent(task: str, *, metadata: dict | None = None, tools: list | None = None) -> str:
    """Execute an agent task using the Responses API."""
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "You are a helpful data analyst."},
            {"role": "user", "content": task}
        ],
        tools=tools or [],
        metadata=metadata or {}
    )

    return response.output_text
```

### Tool Definition

```python
search_database_tool = {
    "type": "function",
    "function": {
        "name": "search_database",
        "description": "Search the analytics warehouse for relevant information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Natural language search query"
                }
            },
            "required": ["query"]
        }
    }
}
```

### Orchestration Example

```python
def analyze_sales():
    output = run_agent(
        "Analyze the sales data and highlight the top three drivers.",
        metadata={"data_source": "sales_db"},
        tools=[search_database_tool]
    )
    return output
```

## See Also

- [OpenAI Agents SDK](./agents-sdk.md) - Lower-level SDK
- [Codex](./codex.md) - Code generation patterns

## References

- [R1] OpenAI Platform Documentation. https://platform.openai.com/docs (accessed 2025-10-24)
