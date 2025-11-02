---
title: Skill
slug: skill
status: living
last_updated: 2025-11-01
tags: [skill, anthropic, agents, domain-expertise]
summary: "Anthropic's Agent Skills specification for packaging domain expertise that AI agents can load on-demand."
authors: []
sources:
  - { id: R1, title: "Anthropic Skills - Official Announcement", url: "https://www.anthropic.com/news/skills", accessed: "2025-10-23" }
  - { id: R2, title: "anthropics/skills - Official GitHub Repository", url: "https://github.com/anthropics/skills", accessed: "2025-10-23" }
  - { id: R3, title: "Claude Skills Documentation", url: "https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview", accessed: "2025-10-23" }
  - { id: R4, title: "Claude Skills are awesome, maybe a bigger deal than MCP - Simon Willison", url: "https://simonwillison.net/2025/Oct/16/claude-skills/", accessed: "2025-10-23" }
---

# Skill

> **For Humans**: This guide explains Anthropic's Agent Skills specification for packaging domain expertise that Claude can load on-demand.
>
> **For AI Agents**: Agent Skills are filesystem packages containing YAML metadata, Markdown instructions, and optional resources. Load Skills when their descriptions match user tasks to access specialized knowledge without consuming excessive context.

## Overview

Agent Skills are modular knowledge packages that AI agents can dynamically load based on task requirements. Instead of including all possible instructions in every context, Skills enable progressive disclosure of specialized expertise only when needed.

## Skill Structure

### Directory Layout

```
skill-name/
├── skill.yaml           # Metadata and configuration
├── README.md           # Human-readable documentation
├── instructions.md     # Agent-facing instructions
├── resources/         # Optional supporting files
│   ├── templates/
│   ├── examples/
│   └── schemas/
└── tests/            # Validation tests
    └── test_cases.yaml
```

### Metadata Format (skill.yaml)

```yaml
name: python-testing
version: 1.0.0
description: "Comprehensive Python testing patterns and best practices"
author: engineering-team
tags:
  - testing
  - python
  - quality-assurance
dependencies:
  - python-basics: ">=1.0.0"
triggers:
  keywords:
    - "write tests"
    - "pytest"
    - "test coverage"
  patterns:
    - ".*test.*\\.py$"
    - ".*_test\\.py$"
configuration:
  min_coverage: 80
  test_framework: pytest
```

## Core Components

### Instructions File

The `instructions.md` contains agent-executable knowledge:

```markdown
# Python Testing Instructions

## Setup

Install required packages:
\`\`\`bash
pip install pytest pytest-cov pytest-mock
\`\`\`

## Writing Tests

### Basic Test Structure

\`\`\`python
import pytest

def test_function_name():
    # Arrange
    input_data = prepare_test_data()

    # Act
    result = function_under_test(input_data)

    # Assert
    assert result == expected_output
\`\`\`

### Parametrized Tests

\`\`\`python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_multiplication(input, expected):
    assert input * 2 == expected
\`\`\`

## Coverage Requirements

Maintain minimum {min_coverage}% code coverage.
```

### Resource Files

Optional supporting materials:

```yaml
# resources/templates/test_template.py
import pytest
from unittest.mock import Mock, patch

class Test{ClassName}:
    @pytest.fixture
    def setup(self):
        # Setup code here
        yield
        # Teardown code here

    def test_{method_name}(self, setup):
        # Test implementation
        pass
```

## Loading Mechanism

### Automatic Loading

Skills load when trigger conditions match:

```python
def should_load_skill(user_input, file_context, skill_config):
    # Check keyword triggers
    for keyword in skill_config['triggers']['keywords']:
        if keyword in user_input.lower():
            return True

    # Check file pattern triggers
    for pattern in skill_config['triggers']['patterns']:
        if any(re.match(pattern, f) for f in file_context):
            return True

    return False
```

### Manual Loading

Users can explicitly request skills:

```bash
# Load specific skill
/skill load python-testing

# List available skills
/skill list

# Show skill details
/skill info python-testing
```

## Creating Skills

### Development Workflow

1. **Identify Domain**: Specialized knowledge area
2. **Define Triggers**: When skill should activate
3. **Write Instructions**: Clear, actionable guidance
4. **Add Resources**: Templates, examples, schemas
5. **Create Tests**: Validation scenarios
6. **Package**: Bundle into skill directory
7. **Publish**: Share via registry or repository

### Validation

```yaml
# tests/test_cases.yaml
test_cases:
  - name: "Basic test generation"
    input: "Write a test for calculate_average function"
    expected_outputs:
      - "import pytest"
      - "def test_calculate_average"
      - "assert"

  - name: "Coverage check"
    input: "Check test coverage"
    expected_outputs:
      - "pytest --cov"
      - "coverage report"
```

## Best Practices

### Skill Design

1. **Single Responsibility**: One domain per skill
2. **Progressive Disclosure**: Basic → Advanced
3. **Self-Contained**: Minimal external dependencies
4. **Version Control**: Semantic versioning
5. **Documentation**: Both human and agent readable

### Instruction Writing

```markdown
# GOOD: Clear, actionable steps
## Database Migration
1. Back up current database
2. Run migration script: `python migrate.py`
3. Verify with: `python check_migration.py`

# BAD: Vague guidance
## Database Migration
Handle the database migration carefully.
```

## Anti-patterns

### Kitchen Sink Skill
❌ **Wrong**: One skill with everything
✅ **Right**: Focused, composable skills

### Hardcoded Paths
❌ **Wrong**: `/home/user/project/file.py`
✅ **Right**: Relative paths or variables

### Missing Triggers
❌ **Wrong**: No automatic activation
✅ **Right**: Keywords and patterns defined

## Registry Integration

### Publishing

```bash
# Package skill
skill package ./my-skill

# Publish to registry
skill publish my-skill-1.0.0.tar.gz

# Install from registry
skill install python-testing
```

### Discovery

```yaml
# Registry metadata
registry:
  url: https://skills.anthropic.com
  categories:
    - development
    - testing
    - documentation
  featured:
    - python-testing
    - api-design
    - security-audit
```

## Platform Support

### Claude Desktop

```yaml
# Claude Desktop config
skills:
  enabled: true
  auto_load: true
  directories:
    - ~/.claude/skills
    - ./project/.claude/skills
```

### API Integration

```python
from anthropic import Skills

# Load skill programmatically
skills = Skills()
skill = skills.load('python-testing')

# Apply to conversation
response = claude.messages.create(
    messages=[...],
    skills=[skill]
)
```

## Examples

### Testing Skill

```yaml
name: frontend-testing
version: 2.0.0
description: "React component testing with Jest and Testing Library"
triggers:
  keywords: ["test react", "jest", "testing library"]
  patterns: [".*\\.test\\.(jsx?|tsx?)$"]
```

### Documentation Skill

```yaml
name: api-documentation
version: 1.5.0
description: "OpenAPI/Swagger documentation generation"
triggers:
  keywords: ["document api", "openapi", "swagger"]
  patterns: [".*openapi\\.yaml$", ".*swagger\\.json$"]
```

### Security Skill

```yaml
name: security-audit
version: 3.0.0
description: "Security vulnerability scanning and remediation"
triggers:
  keywords: ["security scan", "vulnerability", "CVE"]
  patterns: [".*security.*", ".*audit.*"]
```

## See Also

- [AGENTS.md](../../AGENTS.md) - AI agent operational documentation
- [MCP](./mcp.md) - Model Context Protocol
- [Progressive Disclosure](./progressive-disclosure.md)

## References

- [R1] Anthropic Skills - Official Announcement. https://www.anthropic.com/news/skills (accessed 2025-10-23)
- [R2] anthropics/skills - Official GitHub Repository. https://github.com/anthropics/skills (accessed 2025-10-23)
- [R3] Claude Skills Documentation. https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview (accessed 2025-10-23)
- [R4] Claude Skills are awesome, maybe a bigger deal than MCP - Simon Willison. https://simonwillison.net/2025/Oct/16/claude-skills/ (accessed 2025-10-23)
