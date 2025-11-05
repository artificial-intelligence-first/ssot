---
title: GitHub Actions
slug: github-actions
status: living
last_updated: 2025-11-04
tags: [github, ci-cd, automation, workflows, agents]
summary: "Comprehensive guide to integrating AI agents with GitHub Actions for automated workflows, CI/CD pipelines, and intelligent automation."
authors: []
sources:
  - { id: R1, title: "GitHub Actions Documentation", url: "https://docs.github.com/en/actions", accessed: "2025-11-04" }
  - { id: R2, title: "GitHub Actions API", url: "https://docs.github.com/en/rest/actions", accessed: "2025-11-04" }
  - { id: R3, title: "Creating GitHub Actions", url: "https://docs.github.com/en/actions/creating-actions", accessed: "2025-11-04" }
  - { id: R4, title: "Workflow syntax for GitHub Actions", url: "https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions", accessed: "2025-11-04" }
---

# GitHub Actions

> **For Humans**: This document provides patterns and examples for building AI-powered GitHub Actions workflows. Use this when you need to automate development workflows, integrate AI agents into CI/CD pipelines, or create intelligent automation for your repositories.
>
> **For AI Agents**: Apply these patterns when implementing GitHub Actions workflows, creating custom actions, or integrating with GitHub's automation platform. Cross-reference with other platform documentation for multi-platform orchestration.

## Overview

GitHub Actions is a CI/CD and automation platform that allows you to build, test, and deploy code directly from GitHub repositories. This guide focuses on integrating AI agents with GitHub Actions to create intelligent, automated workflows that enhance development productivity.

## Core Concepts

### Workflows

Workflows are automated processes defined in YAML files stored in `.github/workflows/`:

```yaml
name: AI Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: AI Code Review
        uses: ./actions/ai-review
        with:
          api-key: ${{ secrets.ANTHROPIC_API_KEY }}
```

### Actions

Actions are reusable units of code that perform specific tasks:

- **JavaScript Actions**: Run directly in the runner
- **Docker Actions**: Execute in containers
- **Composite Actions**: Combine multiple steps

### Events

Workflows trigger on various GitHub events:

- `push`: Code pushed to repository
- `pull_request`: PR opened, updated, or merged
- `issues`: Issue created or modified
- `schedule`: Cron-based scheduling
- `workflow_dispatch`: Manual triggering

## AI-Powered Workflows

### Automated Code Review

```yaml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changed files
        id: changed-files
        uses: tj-actions/changed-files@v40
        with:
          files: |
            **/*.py
            **/*.js
            **/*.ts

      - name: Run AI Code Review
        uses: anthropics/claude-code-review@v1
        with:
          api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-3-5-sonnet-20241022
          files: ${{ steps.changed-files.outputs.all_changed_files }}
          focus: |
            - Security vulnerabilities
            - Performance issues
            - Best practices
            - Code quality

      - name: Post review comments
        uses: actions/github-script@v7
        with:
          script: |
            const review = require('./review-output.json');
            await github.rest.pulls.createReview({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.payload.pull_request.number,
              event: 'COMMENT',
              comments: review.comments
            });
```

### Automated Documentation Generation

```yaml
name: Generate Documentation

on:
  push:
    branches: [main]
    paths:
      - 'src/**/*.py'
      - 'src/**/*.ts'

jobs:
  generate-docs:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Generate API documentation
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          pip install anthropic
          python scripts/generate_docs.py

      - name: Commit documentation
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "docs: auto-generate API documentation"
          file_pattern: "docs/api/*.md"
```

### Intelligent Issue Triage

```yaml
name: Issue Triage

on:
  issues:
    types: [opened]

jobs:
  triage:
    runs-on: ubuntu-latest
    permissions:
      issues: write

    steps:
      - name: Analyze issue
        id: analyze
        uses: actions/github-script@v7
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        with:
          script: |
            const Anthropic = require('@anthropic-ai/sdk');
            const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

            const issue = context.payload.issue;

            const response = await client.messages.create({
              model: 'claude-3-5-sonnet-20241022',
              max_tokens: 1024,
              messages: [{
                role: 'user',
                content: `Analyze this GitHub issue and suggest labels and priority:

                Title: ${issue.title}
                Body: ${issue.body}

                Return JSON with: labels (array), priority (string), category (string)`
              }]
            });

            const analysis = JSON.parse(response.content[0].text);
            return analysis;

      - name: Apply labels
        uses: actions/github-script@v7
        with:
          script: |
            const analysis = ${{ steps.analyze.outputs.result }};
            await github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.payload.issue.number,
              labels: analysis.labels
            });

      - name: Add comment
        uses: actions/github-script@v7
        with:
          script: |
            const analysis = ${{ steps.analyze.outputs.result }};
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.payload.issue.number,
              body: `🤖 **AI Analysis**\n\nPriority: ${analysis.priority}\nCategory: ${analysis.category}`
            });
```

## Creating Custom Actions

### JavaScript Action Structure

```
action-name/
├── action.yml          # Action metadata
├── index.js            # Main entry point
├── package.json        # Dependencies
└── README.md          # Documentation
```

### Example: AI Code Analyzer Action

**action.yml**:

```yaml
name: 'AI Code Analyzer'
description: 'Analyze code using AI to detect issues and suggest improvements'
author: 'Your Organization'

inputs:
  api-key:
    description: 'Anthropic API key'
    required: true
  model:
    description: 'Claude model to use'
    required: false
    default: 'claude-3-5-sonnet-20241022'
  files:
    description: 'Files to analyze (space-separated)'
    required: true
  focus:
    description: 'Analysis focus areas'
    required: false

outputs:
  report:
    description: 'Analysis report in JSON format'
  summary:
    description: 'Brief summary of findings'

runs:
  using: 'node20'
  main: 'index.js'
```

**index.js**:

```javascript
const core = require('@actions/core');
const github = require('@actions/github');
const Anthropic = require('@anthropic-ai/sdk');
const fs = require('fs').promises;

async function analyzeCode() {
  try {
    // Get inputs
    const apiKey = core.getInput('api-key', { required: true });
    const model = core.getInput('model');
    const files = core.getInput('files').split(' ');
    const focus = core.getInput('focus');

    // Initialize Anthropic client
    const client = new Anthropic({ apiKey });

    // Read files
    const fileContents = await Promise.all(
      files.map(async (file) => ({
        path: file,
        content: await fs.readFile(file, 'utf-8')
      }))
    );

    // Analyze with Claude
    const response = await client.messages.create({
      model,
      max_tokens: 4096,
      messages: [{
        role: 'user',
        content: `Analyze these code files and provide detailed feedback.

Focus areas: ${focus || 'General code quality'}

Files:
${fileContents.map(f => `
File: ${f.path}
\`\`\`
${f.content}
\`\`\`
`).join('\n')}

Provide analysis in JSON format with:
- issues: array of {file, line, severity, message, suggestion}
- summary: overall assessment
- metrics: {score, complexity, maintainability}
`
      }]
    });

    const analysis = JSON.parse(response.content[0].text);

    // Set outputs
    core.setOutput('report', JSON.stringify(analysis));
    core.setOutput('summary', analysis.summary);

    // Create annotations
    for (const issue of analysis.issues) {
      core.warning(issue.message, {
        file: issue.file,
        startLine: issue.line,
        title: `${issue.severity}: Code Issue`
      });
    }

    core.info(`✅ Analysis complete. Found ${analysis.issues.length} issues.`);

  } catch (error) {
    core.setFailed(`Action failed: ${error.message}`);
  }
}

analyzeCode();
```

**package.json**:

```json
{
  "name": "ai-code-analyzer",
  "version": "1.0.0",
  "description": "AI-powered code analysis action",
  "main": "index.js",
  "scripts": {
    "test": "jest"
  },
  "dependencies": {
    "@actions/core": "^1.10.1",
    "@actions/github": "^6.0.0",
    "@anthropic-ai/sdk": "^0.27.0"
  },
  "devDependencies": {
    "jest": "^29.7.0"
  }
}
```

### Docker Action Structure

**Dockerfile**:

```dockerfile
FROM python:3.11-slim

# Install dependencies
COPY requirements.txt /
RUN pip install -r requirements.txt

# Copy action code
COPY entrypoint.py /entrypoint.py
RUN chmod +x /entrypoint.py

ENTRYPOINT ["/entrypoint.py"]
```

**entrypoint.py**:

```python
#!/usr/bin/env python3
import os
import sys
import json
from anthropic import Anthropic

def main():
    # Get inputs from environment
    api_key = os.environ['INPUT_API-KEY']
    model = os.environ.get('INPUT_MODEL', 'claude-3-5-sonnet-20241022')
    task = os.environ['INPUT_TASK']

    # Initialize client
    client = Anthropic(api_key=api_key)

    # Process task
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": task
        }]
    )

    result = response.content[0].text

    # Set outputs
    print(f"::set-output name=result::{result}")
    print(f"✅ Task completed successfully")

if __name__ == "__main__":
    main()
```

## Advanced Patterns

### Multi-Agent Workflow

```yaml
name: Multi-Agent Development

on:
  workflow_dispatch:
    inputs:
      feature:
        description: 'Feature to implement'
        required: true

jobs:
  research:
    runs-on: ubuntu-latest
    outputs:
      research: ${{ steps.research.outputs.result }}
    steps:
      - name: Research feature
        id: research
        uses: ./.github/actions/ai-research
        with:
          api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          topic: ${{ inputs.feature }}

  design:
    needs: research
    runs-on: ubuntu-latest
    outputs:
      design: ${{ steps.design.outputs.result }}
    steps:
      - name: Design solution
        id: design
        uses: ./.github/actions/ai-architect
        with:
          api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          research: ${{ needs.research.outputs.research }}

  implement:
    needs: design
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref }}

      - name: Generate code
        uses: ./.github/actions/ai-coder
        with:
          api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          design: ${{ needs.design.outputs.design }}

      - name: Create pull request
        uses: peter-evans/create-pull-request@v5
        with:
          title: "feat: ${{ inputs.feature }}"
          body: |
            ## AI-Generated Feature Implementation

            **Research**: ${{ needs.research.outputs.research }}
            **Design**: ${{ needs.design.outputs.design }}

            This PR was automatically generated by AI agents.
          branch: ai/${{ inputs.feature }}
```

### Continuous Documentation

```yaml
name: Maintain Documentation

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Scan for outdated docs
        id: scan
        uses: ./.github/actions/doc-scanner
        with:
          api-key: ${{ secrets.ANTHROPIC_API_KEY }}

      - name: Update documentation
        if: steps.scan.outputs.needs-update == 'true'
        uses: ./.github/actions/doc-updater
        with:
          api-key: ${{ secrets.ANTHROPIC_API_KEY }}
          files: ${{ steps.scan.outputs.files }}

      - name: Create PR for docs
        if: steps.scan.outputs.needs-update == 'true'
        uses: peter-evans/create-pull-request@v5
        with:
          title: "docs: automated documentation update"
          labels: documentation, automated
```

## Integration with GitHub API

### Using Octokit in Actions

```javascript
const { Octokit } = require('@octokit/rest');
const Anthropic = require('@anthropic-ai/sdk');

async function processIssues() {
  const octokit = new Octokit({
    auth: process.env.GITHUB_TOKEN
  });

  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  // Get open issues
  const { data: issues } = await octokit.rest.issues.listForRepo({
    owner: context.repo.owner,
    repo: context.repo.repo,
    state: 'open'
  });

  // Process each issue with AI
  for (const issue of issues) {
    const response = await anthropic.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 1024,
      messages: [{
        role: 'user',
        content: `Analyze this issue and suggest next steps:\n\n${issue.title}\n${issue.body}`
      }]
    });

    // Add AI suggestions as comment
    await octokit.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: issue.number,
      body: `🤖 **AI Suggestions**\n\n${response.content[0].text}`
    });
  }
}
```

## Security Best Practices

### Secret Management

```yaml
# Use GitHub Secrets
- name: Secure action
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: python secure_script.py

# Never log secrets
- name: Safe logging
  run: |
    echo "::add-mask::${{ secrets.API_KEY }}"
    # Secret is now masked in logs
```

### Permission Scoping

```yaml
name: Secure Workflow

on: [pull_request]

permissions:
  contents: read
  pull-requests: write
  issues: read

jobs:
  secure-job:
    runs-on: ubuntu-latest
    # Job-specific permissions (override workflow permissions)
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
```

## Testing Actions

### Local Testing with act

```bash
# Install act
brew install act  # macOS
# or
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflow locally
act push

# Run specific job
act -j test

# With secrets
act -s ANTHROPIC_API_KEY=sk-ant-xxx
```

### Unit Testing

```javascript
const { analyzeCode } = require('./index');
const core = require('@actions/core');

jest.mock('@actions/core');
jest.mock('@anthropic-ai/sdk');

describe('AI Code Analyzer', () => {
  test('analyzes code successfully', async () => {
    const mockFiles = ['test.js'];

    await analyzeCode(mockFiles);

    expect(core.setOutput).toHaveBeenCalledWith(
      'report',
      expect.any(String)
    );
  });

  test('handles errors gracefully', async () => {
    const mockFiles = ['nonexistent.js'];

    await analyzeCode(mockFiles);

    expect(core.setFailed).toHaveBeenCalled();
  });
});
```

## Monitoring and Debugging

### Workflow Logging

```yaml
- name: Debug information
  run: |
    echo "::group::Environment"
    env | sort
    echo "::endgroup::"

    echo "::group::Context"
    echo "${{ toJSON(github) }}"
    echo "::endgroup::"

- name: Set outputs with debugging
  run: |
    echo "::debug::Processing file $FILE"
    echo "::notice::Analysis complete"
    echo "::warning::Found potential issue"
    echo "::error::Critical error detected"
```

### Action Annotations

```javascript
core.info('ℹ️ Informational message');
core.notice('📢 Notice message');
core.warning('⚠️ Warning message', {
  file: 'src/app.js',
  startLine: 42
});
core.error('❌ Error message', {
  file: 'src/app.js',
  startLine: 42,
  endLine: 45
});
```

## Performance Optimization

### Caching

```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: |
      ~/.npm
      ~/.cache/pip
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json', '**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-deps-

- name: Cache AI responses
  uses: actions/cache@v3
  with:
    path: .ai-cache
    key: ai-${{ hashFiles('**/*.py', '**/*.js') }}
```

### Parallel Execution

```yaml
jobs:
  analyze:
    strategy:
      matrix:
        component: [frontend, backend, api, workers]
      max-parallel: 4
    steps:
      - name: Analyze ${{ matrix.component }}
        uses: ./.github/actions/ai-analyzer
        with:
          path: src/${{ matrix.component }}
```

## Best Practices

### 1. Fail Fast

```yaml
- name: Quick validation
  run: |
    if ! python -m py_compile *.py; then
      echo "::error::Syntax errors detected"
      exit 1
    fi
```

### 2. Idempotent Actions

```yaml
- name: Idempotent operation
  run: |
    # Check if already done
    if [ -f .done ]; then
      echo "Already completed"
      exit 0
    fi

    # Perform operation
    ./do_work.sh

    # Mark as done
    touch .done
```

### 3. Timeout Protection

```yaml
- name: AI analysis with timeout
  timeout-minutes: 10
  run: python analyze.py
```

### 4. Conditional Execution

```yaml
- name: Only on main branch
  if: github.ref == 'refs/heads/main'
  run: deploy.sh

- name: Only for Python files
  if: contains(github.event.head_commit.modified, '.py')
  run: python lint.py
```

## See Also

- [GitHub API Integration](./api.md) - GitHub REST and GraphQL APIs
- [GitHub Apps](./apps.md) - Building GitHub Apps
- [AGENTS.md](../../../AGENTS.md) - Operational documentation

## References

- [R1] GitHub Actions Documentation. https://docs.github.com/en/actions (accessed 2025-11-04)
- [R2] GitHub Actions API. https://docs.github.com/en/rest/actions (accessed 2025-11-04)
- [R3] Creating GitHub Actions. https://docs.github.com/en/actions/creating-actions (accessed 2025-11-04)
- [R4] Workflow syntax for GitHub Actions. https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions (accessed 2025-11-04)
