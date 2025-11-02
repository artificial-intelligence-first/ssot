---
title: Claude Code
slug: claude-code
status: living
last_updated: 2025-11-01
tags: [code-generation, agents, anthropic, cli, vscode]
summary: "Agentic coding tool from Anthropic that works in terminal and browser for AI-assisted development."
authors: []
sources:
  - { id: R1, title: "Claude Code Official Site", url: "https://www.anthropic.com/claude-code", accessed: "2025-10-24" }
  - { id: R2, title: "Claude Code GitHub Repository", url: "https://github.com/anthropics/claude-code", accessed: "2025-10-24" }
  - { id: R3, title: "Anthropic Cookbook", url: "https://github.com/anthropics/anthropic-cookbook", accessed: "2025-10-24" }
  - { id: R4, title: "Claude Code Best Practices", url: "https://www.anthropic.com/engineering/claude-code-best-practices", accessed: "2025-10-24" }
  - { id: R5, title: "Enabling Claude Code to work more autonomously", url: "https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously", accessed: "2025-10-24" }
---

# Claude Code

> **For Humans**: This document explains Claude Code, Anthropic's agentic coding tool that works in your terminal and browser. Use this when building AI-assisted development workflows, automating routine coding tasks, or integrating Claude into your development environment.
>
> **For AI Agents**: Claude Code provides command-line and VS Code extension interfaces for code generation, debugging, and refactoring. Use the CLI commands and extension features documented here to assist with development tasks.

## Overview

Claude Code is Anthropic's agentic coding tool designed to understand entire codebases and help developers code faster through natural language commands. It operates both as a CLI tool and VS Code extension, providing seamless integration into existing development workflows.

## Installation

### CLI Installation

```bash
# macOS/Linux
curl -fsSL https://claude.ai/install.sh | sh

# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex

# Verify installation
claude --version
```

### VS Code Extension

```bash
# Install from marketplace
code --install-extension anthropic.claude-code

# Or search "Claude Code" in VS Code extensions
```

## Core Features

### Code Generation

Generate complete implementations from descriptions:

```bash
# Generate function
claude generate "create a function that validates email addresses"

# Generate class
claude generate "implement a caching layer with TTL support"

# Generate tests
claude generate tests for src/utils/validator.js
```

### Code Understanding

Analyze and explain existing code:

```bash
# Explain code
claude explain src/complex-algorithm.js

# Find dependencies
claude deps analyze package.json

# Architecture overview
claude analyze --architecture ./src
```

### Refactoring

Improve code quality and structure:

```bash
# Refactor for readability
claude refactor --improve-readability src/legacy.js

# Extract methods
claude refactor --extract-method src/long-function.js

# Apply design pattern
claude refactor --pattern factory src/creator.js
```

## CLI Commands

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `claude init` | Initialize project | `claude init --language python` |
| `claude chat` | Interactive session | `claude chat` |
| `claude run` | Execute with context | `claude run "fix the bug in auth"` |
| `claude test` | Generate/run tests | `claude test src/` |
| `claude fix` | Auto-fix issues | `claude fix --lint` |

### Advanced Commands

```bash
# Multi-file operations
claude refactor "convert callbacks to async/await" src/**/*.js

# Project-wide search
claude search "TODO" --context

# Generate documentation
claude docs generate --format markdown

# Performance optimization
claude optimize --target speed src/bottleneck.js
```

## VS Code Integration

### Extension Commands

Access via Command Palette (Cmd/Ctrl+Shift+P):

- `Claude: Generate Code` - Generate code at cursor
- `Claude: Explain Selection` - Explain selected code
- `Claude: Refactor Selection` - Refactor selected code
- `Claude: Fix Problems` - Fix diagnostics in file
- `Claude: Generate Tests` - Create tests for selection

### Keyboard Shortcuts

Default keybindings:

```json
{
  "key": "cmd+k cmd+g",
  "command": "claude.generate",
  "when": "editorTextFocus"
},
{
  "key": "cmd+k cmd+e",
  "command": "claude.explain",
  "when": "editorHasSelection"
},
{
  "key": "cmd+k cmd+r",
  "command": "claude.refactor",
  "when": "editorHasSelection"
}
```

## Configuration

### Global Configuration

```yaml
# ~/.claude/config.yaml
api_key: ${ANTHROPIC_API_KEY}
model: claude-3-opus-20240229
temperature: 0.2
max_tokens: 4096

preferences:
  language: javascript
  style: airbnb
  test_framework: jest

context:
  max_files: 50
  include_patterns:
    - "**/*.js"
    - "**/*.ts"
  exclude_patterns:
    - "node_modules/**"
    - "dist/**"
```

### Project Configuration

```yaml
# .claude/project.yaml
name: my-project
description: "E-commerce platform"

context:
  entry_points:
    - src/index.js
    - src/api/server.js

  important_files:
    - README.md
    - docs/core/agents-guide.md

conventions:
  naming: camelCase
  imports: relative
  async: await_syntax

integrations:
  github: true
  jira: PROJECT-KEY
```

## Context Management

### Automatic Context

Claude Code automatically includes:

```
Project Structure:
├── Package files (package.json, requirements.txt)
├── Configuration files (.env, config/*)
├── Entry points (index.*, main.*, app.*)
├── Recent changes (git diff)
└── Open files in editor
```

### Manual Context

```bash
# Add specific context
claude --context src/important.js generate "related feature"

# Include documentation
claude --include-docs generate "implement OAuth"

# Reference examples
claude --examples tests/ generate "new test suite"
```

## Best Practices

### Effective Prompting

```bash
# ✅ Good: Specific and contextual
claude generate "implement user authentication with JWT,
  including refresh tokens and role-based access control"

# ❌ Bad: Vague
claude generate "add auth"

# ✅ Good: Clear requirements
claude refactor "extract validation logic into separate
  middleware functions following Express.js patterns"

# ❌ Bad: Unclear intent
claude refactor "clean up"
```

### Project Organization

```
.claude/
├── project.yaml        # Project configuration
├── agents/            # Custom agents
│   └── reviewer.yaml
├── templates/         # Code templates
│   └── component.js
└── context/          # Additional context
    └── decisions.md
```

### Performance Optimization

```yaml
# .claude/project.yaml
performance:
  cache: true
  cache_ttl: 3600

  chunking:
    enabled: true
    max_chunk_size: 8192

  parallel:
    enabled: true
    max_workers: 4
```

## Autonomous Features

### Auto-completion

Enable smart completions:

```json
// VS Code settings.json
{
  "claude.autocomplete": {
    "enabled": true,
    "triggerDelay": 500,
    "contextLines": 50
  }
}
```

### Auto-debugging

```bash
# Enable auto-debug mode
claude debug --auto

# Watch for errors
claude watch --fix-errors

# Continuous testing
claude test --watch --auto-fix
```

### Batch Operations

```bash
# Process multiple files
claude batch refactor "add TypeScript types" src/**/*.js

# Migration assistant
claude migrate --from express@4 --to express@5

# Codebase-wide updates
claude update-deps --auto-fix
```

## Integration

### Git Integration

```bash
# Generate commit message
claude commit --generate-message

# PR description
claude pr describe

# Code review
claude review --branch feature/new-feature
```

### CI/CD Integration

```yaml
# .github/workflows/claude.yml
name: Claude Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: anthropic/claude-code-action@v1
        with:
          api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          command: review
          auto-fix: true
```

## Troubleshooting

### Common Issues

**API Key Not Found**
```bash
export ANTHROPIC_API_KEY="your-key-here"
# Or
claude auth login
```

**Context Too Large**
```yaml
# Reduce context size
context:
  max_files: 25
  max_file_size: 100000
```

**Slow Performance**
```bash
# Enable caching
claude config set cache.enabled true

# Reduce context
claude --minimal-context generate "..."
```

## Security

### API Key Management

```bash
# Secure storage
claude auth login  # Stores encrypted

# Environment variable
export ANTHROPIC_API_KEY="sk-..."

# Config file (not recommended)
echo "api_key: sk-..." > ~/.claude/config.yaml
chmod 600 ~/.claude/config.yaml
```

### Data Privacy

- Code is not used for training
- Sessions are ephemeral
- Local caching optional
- Enterprise SSO available

## See Also

- [Claude Agent SDK](./claude-agent-sdk.md)
- [AGENTS.md](../../../AGENTS.md)
- [MCP](../../tools/mcp.md)

## References

- [R1] Claude Code Official Site. https://www.anthropic.com/claude-code (accessed 2025-10-24)
- [R2] Claude Code GitHub Repository. https://github.com/anthropics/claude-code (accessed 2025-10-24)
- [R3] Anthropic Cookbook. https://github.com/anthropics/anthropic-cookbook (accessed 2025-10-24)
- [R4] Claude Code Best Practices. https://www.anthropic.com/engineering/claude-code-best-practices (accessed 2025-10-24)
- [R5] Enabling Claude Code to work more autonomously. https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously (accessed 2025-10-24)
