---
title: Claude Agent SDK
slug: claude-agent-sdk
status: living
last_updated: 2025-11-01
tags: [agents, sdk, anthropic, tool-calling, orchestration]
summary: "SDK for building custom AI agents with tool access, file operations, and command execution capabilities."
authors: []
sources:
  - { id: R1, title: "Claude Agent SDK Overview", url: "https://docs.claude.com/en/api/agent-sdk/overview", accessed: "2025-10-23" }
  - { id: R2, title: "Claude Agent SDK Python GitHub", url: "https://github.com/anthropics/claude-agent-sdk-python", accessed: "2025-10-23" }
  - { id: R3, title: "Building Agents with the Claude Agent SDK", url: "https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk", accessed: "2025-10-23" }
  - { id: R4, title: "Claude Agent SDK TypeScript GitHub", url: "https://github.com/anthropics/claude-agent-sdk-typescript", accessed: "2025-11-03" }
---

# Claude Agent SDK

> **For Humans**: This document explains the Claude Agent SDK, a toolkit for building custom AI agents using the same infrastructure that powers Claude Code. Use this when building autonomous agents that need to interact with files, run commands, access external tools, or execute complex multi-step workflows.
>
> **For AI Agents**: Apply these patterns when building custom agents, implementing tool calling, managing context, or integrating with MCP servers. Cross-reference with AGENTS.md for operational procedures.

## Overview

The Claude Agent SDK is a developer toolkit for building autonomous AI agents with access to tools, file systems, and command execution. It provides the same underlying infrastructure that powers Claude Code, enabling developers to create custom agents tailored to specific workflows and domains.

## Installation

### Python SDK

```bash
# Install from PyPI
pip install claude-agent-sdk

# Install with extras
pip install claude-agent-sdk[mcp,tools]

# Install from source
git clone https://github.com/anthropics/claude-agent-sdk-python
cd claude-agent-sdk-python
pip install -e .
```

### JavaScript/TypeScript SDK

Anthropic has not published an official Node.js package for the Agent SDK as of this update. Integrations typically rely on direct HTTP calls to the Claude API or thin wrappers you maintain in-house. [R1]

## Core Architecture

### Agent Components

```python
from claude_agent_sdk import Agent, Tool, Context, Memory

# Core components
agent = Agent(
    name="my-agent",
    model="claude-3-opus-20240229",
    tools=[...],        # Available tools
    context=Context(),   # Context management
    memory=Memory(),     # Conversation memory
    config={...}        # Configuration
)
```

### Tool System

Tools provide agents with capabilities:

```python
from claude_agent_sdk.tools import (
    FileSystemTool,     # File operations
    CommandLineTool,    # Execute commands
    WebBrowserTool,     # Web browsing
    DatabaseTool,       # Database access
    APIClientTool,      # API calls
    MCPServerTool       # MCP integration
)
```

## Creating Custom Agents

### Basic Agent

```python
from claude_agent_sdk import Agent, Tool

# Define custom tool
class CalculatorTool(Tool):
    name = "calculator"
    description = "Perform mathematical calculations"

    async def execute(self, expression: str):
        try:
            result = eval(expression)  # Use safe eval in production
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}

# Create agent with tool
agent = Agent(
    name="math-assistant",
    tools=[CalculatorTool()],
    system_prompt="""You are a helpful math assistant.
    Use the calculator tool for computations."""
)

# Run agent
response = await agent.run("What is 15% of 240?")
```

### Advanced Agent

```python
from claude_agent_sdk import Agent, Context, Memory
from claude_agent_sdk.tools import FileSystemTool, CommandLineTool

class CodeReviewAgent(Agent):
    """Agent for automated code review."""

    def __init__(self):
        super().__init__(
            name="code-reviewer",
            tools=[
                FileSystemTool(allowed_paths=["./src"]),
                CommandLineTool(allowed_commands=["git", "pytest"])
            ],
            system_prompt=self.load_prompt()
        )

    def load_prompt(self):
        return """You are an expert code reviewer.
        Analyze code for:
        1. Style violations
        2. Potential bugs
        3. Performance issues
        4. Security vulnerabilities
        5. Best practice violations
        """

    async def review_file(self, file_path: str):
        # Read file
        content = await self.tools["filesystem"].read(file_path)

        # Analyze
        analysis = await self.analyze_code(content)

        # Generate report
        return self.format_report(analysis)
```

## Tool Development

### Custom Tool Template

```python
from claude_agent_sdk import Tool, ToolResult

class CustomTool(Tool):
    """Template for custom tools."""

    # Tool metadata
    name = "custom_tool"
    description = "Tool description for agent"

    # Parameter schema
    parameters = {
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Parameter 1"},
            "param2": {"type": "number", "description": "Parameter 2"}
        },
        "required": ["param1"]
    }

    async def execute(self, **kwargs) -> ToolResult:
        """Execute tool logic."""
        param1 = kwargs.get("param1")
        param2 = kwargs.get("param2", 0)

        try:
            # Tool logic here
            result = self.process(param1, param2)

            return ToolResult(
                success=True,
                data=result
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e)
            )

    def process(self, param1, param2):
        """Internal processing logic."""
        return {"processed": param1, "value": param2}
```

### Tool Composition

```python
# Combine multiple tools
class CompositeAgent(Agent):
    def __init__(self):
        # File operations
        file_tool = FileSystemTool(
            allowed_paths=["./workspace"],
            max_file_size=10 * 1024 * 1024  # 10MB
        )

        # Command execution
        cmd_tool = CommandLineTool(
            allowed_commands=["npm", "git", "docker"],
            timeout=30000  # 30 seconds
        )

        # Web access
        web_tool = WebBrowserTool(
            allowed_domains=["*.github.com", "docs.python.org"]
        )

        super().__init__(
            name="composite-agent",
            tools=[file_tool, cmd_tool, web_tool]
        )
```

## Context Management

### Static Context

```python
from claude_agent_sdk import Context

# Define static context
context = Context(
    project_info="E-commerce platform built with React and Node.js",
    conventions={
        "naming": "camelCase",
        "testing": "Jest with 80% coverage",
        "style": "ESLint + Prettier"
    },
    constraints=[
        "Must maintain backward compatibility",
        "Performance budget: <3s page load",
        "Accessibility: WCAG 2.1 AA compliant"
    ]
)

agent = Agent(name="dev-assistant", context=context)
```

### Dynamic Context

```python
class DynamicContext(Context):
    """Context that updates based on project state."""

    async def load(self):
        """Load context dynamically."""
        # Read project files
        package_json = await self.read_json("package.json")
        readme = await self.read_file("README.md")

        # Extract information
        self.data = {
            "dependencies": package_json.get("dependencies", {}),
            "scripts": package_json.get("scripts", {}),
            "description": self.extract_description(readme)
        }

    async def refresh(self):
        """Refresh context when needed."""
        await self.load()
```

## Memory Systems

### Conversation Memory

```python
from claude_agent_sdk import Memory

# Short-term memory
memory = Memory(
    type="conversation",
    max_messages=50,
    summarize_after=30
)

# Long-term memory with persistence
persistent_memory = Memory(
    type="persistent",
    storage="sqlite:///agent_memory.db",
    index_type="vector",
    embedding_model="text-embedding-ada-002"
)
```

### Knowledge Base

```python
class KnowledgeBase:
    """Structured knowledge storage."""

    def __init__(self, path="./knowledge"):
        self.path = path
        self.index = self.build_index()

    def add_document(self, doc):
        """Add to knowledge base."""
        # Process document
        processed = self.process(doc)

        # Update index
        self.index.add(processed)

        # Persist
        self.save()

    def query(self, question):
        """Query knowledge base."""
        return self.index.search(question, k=5)
```

## MCP Integration

### Connecting to MCP Servers

```python
from claude_agent_sdk.mcp import MCPClient

# Create MCP client
mcp_client = MCPClient()

# Connect to server
await mcp_client.connect("ws://localhost:8765")

# Create tool from MCP server
mcp_tool = MCPServerTool(
    client=mcp_client,
    server_name="database-server"
)

# Use in agent
agent = Agent(
    name="data-analyst",
    tools=[mcp_tool]
)
```

### Custom MCP Server

```python
from claude_agent_sdk.mcp import MCPServer, Resource

class CustomMCPServer(MCPServer):
    """Custom MCP server for agent."""

    async def initialize(self):
        # Register resources
        self.register_resource(Resource(
            uri="custom://data",
            name="Custom Data Source",
            handler=self.handle_data
        ))

    async def handle_data(self, params):
        """Handle data requests."""
        return {"data": "Custom response"}
```

## Orchestration Patterns

### Sequential Execution

```python
class SequentialAgent(Agent):
    """Execute tasks in sequence."""

    async def run_workflow(self, tasks):
        results = []

        for task in tasks:
            # Execute task
            result = await self.execute_task(task)
            results.append(result)

            # Check for errors
            if not result.success:
                break

        return results
```

### Parallel Execution

```python
import asyncio

class ParallelAgent(Agent):
    """Execute tasks in parallel."""

    async def run_workflow(self, tasks):
        # Create coroutines
        coroutines = [
            self.execute_task(task)
            for task in tasks
        ]

        # Run in parallel
        results = await asyncio.gather(*coroutines)

        return results
```

### Conditional Execution

```python
class ConditionalAgent(Agent):
    """Execute based on conditions."""

    async def run_workflow(self, initial_task):
        result = await self.execute_task(initial_task)

        if result.get("requires_review"):
            result = await self.review_task(result)

        if result.get("needs_approval"):
            result = await self.request_approval(result)

        return result
```

## Best Practices

### Error Handling

```python
from claude_agent_sdk import AgentError

class RobustAgent(Agent):
    async def execute(self, task):
        try:
            return await super().execute(task)
        except AgentError as e:
            # Handle agent-specific errors
            return self.handle_agent_error(e)
        except Exception as e:
            # Handle unexpected errors
            return self.handle_unexpected_error(e)

    def handle_agent_error(self, error):
        if error.code == "TOOL_NOT_FOUND":
            return {"error": "Required tool not available"}
        elif error.code == "CONTEXT_TOO_LARGE":
            return {"error": "Context exceeds limits"}
        else:
            return {"error": str(error)}
```

### Rate Limiting

```python
from claude_agent_sdk import RateLimiter

# Configure rate limits
rate_limiter = RateLimiter(
    requests_per_minute=60,
    tokens_per_minute=100000,
    concurrent_requests=5
)

agent = Agent(
    name="rate-limited-agent",
    rate_limiter=rate_limiter
)
```

### Monitoring

```python
from claude_agent_sdk import Monitor

# Setup monitoring
monitor = Monitor(
    metrics=["latency", "token_usage", "error_rate"],
    export_to="prometheus",
    alert_threshold={"error_rate": 0.05}
)

agent = Agent(
    name="monitored-agent",
    monitor=monitor
)
```

## Testing

### Unit Testing

```python
import pytest
from claude_agent_sdk.testing import AgentTestCase

class TestCustomAgent(AgentTestCase):
    def setup_method(self):
        self.agent = CustomAgent()

    @pytest.mark.asyncio
    async def test_basic_response(self):
        response = await self.agent.run("Hello")
        assert response.success
        assert "greeting" in response.data

    @pytest.mark.asyncio
    async def test_tool_execution(self):
        # Mock tool response
        self.mock_tool("calculator", {"result": 42})

        response = await self.agent.run("Calculate something")
        assert response.data["result"] == 42
```

### Integration Testing

```python
class IntegrationTest:
    @pytest.mark.integration
    async def test_full_workflow(self):
        # Create agent with real tools
        agent = Agent(
            name="test-agent",
            tools=[FileSystemTool(), CommandLineTool()]
        )

        # Run workflow
        result = await agent.run_workflow([
            "Create test file",
            "Run tests",
            "Generate report"
        ])

        assert all(r.success for r in result)
```

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install SDK
RUN pip install claude-agent-sdk

# Copy agent code
COPY agent.py .
COPY config.yaml .

# Run agent
CMD ["python", "agent.py"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: claude-agent
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: agent
        image: claude-agent:latest
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: anthropic
        resources:
          limits:
            memory: "1Gi"
            cpu: "500m"
```

## Security

### API Key Management

```python
import os
from claude_agent_sdk import SecureConfig

# Secure configuration
config = SecureConfig(
    api_key=os.environ["ANTHROPIC_API_KEY"],
    encryption_key=os.environ["ENCRYPTION_KEY"]
)

agent = Agent(
    name="secure-agent",
    config=config
)
```

### Sandboxing

```python
from claude_agent_sdk.security import Sandbox

# Create sandboxed environment
sandbox = Sandbox(
    filesystem_access=["./safe_dir"],
    network_access=["api.anthropic.com"],
    max_memory="512MB",
    max_cpu="50%"
)

agent = Agent(
    name="sandboxed-agent",
    sandbox=sandbox
)
```

## See Also

- [Claude Code](./claude-code.md) - CLI and VS Code integration
- [AGENTS.md](../../../AGENTS.md) - Operational documentation
- [MCP](../../tools/mcp.md) - Model Context Protocol

## References

- [R1] Claude Agent SDK Overview. https://docs.claude.com/en/api/agent-sdk/overview (accessed 2025-10-23)
- [R2] Claude Agent SDK Python GitHub. https://github.com/anthropics/claude-agent-sdk-python (accessed 2025-10-23)
- [R3] Building Agents with the Claude Agent SDK. https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk (accessed 2025-10-23)
- [R4] Claude Agent SDK TypeScript GitHub. https://github.com/anthropics/claude-agent-sdk-typescript (accessed 2025-11-03)
