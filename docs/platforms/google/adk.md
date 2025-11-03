---
title: ADK
slug: adk
status: living
last_updated: 2025-11-01
tags: [agents, sdk, google, vertex-ai, development]
summary: "Agent Development Kit for building and deploying AI agents on Google Cloud Vertex AI platform."
authors: []
sources:
  - { id: R1, title: "Google Cloud Vertex AI Agent Builder", url: "https://cloud.google.com/vertex-ai/docs/agents", accessed: "2025-10-23" }
  - { id: R2, title: "Vertex AI SDK Documentation", url: "https://cloud.google.com/vertex-ai/docs/python-sdk/use-vertex-ai-python-sdk", accessed: "2025-10-23" }
  - { id: R3, title: "ADK JavaScript/TypeScript SDK", url: "https://github.com/google/adk-js", accessed: "2025-11-03" }
---

# ADK

> **For Humans**: The Agent Development Kit (ADK) provides tools for building and deploying AI agents on Google Cloud's Vertex AI platform.
>
> **For AI Agents**: Use ADK patterns for Vertex AI agent deployment, model serving, and integration with Google Cloud services.

## Overview

ADK is Google's comprehensive toolkit for developing, testing, and deploying AI agents on Vertex AI, providing integration with Google's AI models and cloud infrastructure.

## Core Features

### Agent Creation

```python
from google.cloud import aiplatform
from adk import Agent

agent = Agent(
    name="my-agent",
    model="gemini-pro",
    tools=["code_interpreter", "search"]
)

agent.deploy(
    project="my-project",
    location="us-central1"
)
```

### Tool Integration

```python
from adk.tools import SearchTool, DatabaseTool

agent.add_tool(SearchTool(api_key="..."))
agent.add_tool(DatabaseTool(connection_string="..."))
```

### Vertex AI Integration

```python
endpoint = aiplatform.Endpoint.create(
    display_name="adk-agent-endpoint"
)

agent.serve(endpoint=endpoint)
```

## See Also

- [A2A Protocol](./a2a.md) - Agent interoperability
- [Vertex AI](https://cloud.google.com/vertex-ai) - Platform documentation

## References

- [R1] Google Cloud Vertex AI Agent Builder. https://cloud.google.com/vertex-ai/docs/agents (accessed 2025-10-23)
- [R2] Vertex AI SDK Documentation. https://cloud.google.com/vertex-ai/docs/python-sdk/use-vertex-ai-python-sdk (accessed 2025-10-23)
- [R3] ADK JavaScript/TypeScript SDK. https://github.com/google/adk-js (accessed 2025-11-03)
