---
title: Taxonomy
slug: taxonomy
status: stable
last_updated: 2025-11-01
tags: [governance, taxonomy, metadata, standards]
summary: "Controlled vocabulary for document tagging, ensuring consistent categorization across the repository."
authors: []
sources: []
---

# Taxonomy

> **For Humans**: This document defines the controlled vocabulary for tagging documents. Use only these approved tags to ensure consistent categorization.
>
> **For AI Agents**: When adding or modifying tags in frontmatter, validate against this authoritative list. Never create new tags without updating this taxonomy first.

## Overview

This taxonomy provides a controlled vocabulary for document tagging, enabling consistent categorization, improved discoverability, and automated processing of documentation.

## Tag Categories

### Core Concepts

Fundamental architectural concepts:

| Tag | Description | Usage |
|-----|-------------|-------|
| `ssot` | Single Source of Truth principles | Canonical references |
| `agents` | AI agent systems and operations | Agent documentation |
| `context` | Context engineering and management | Context patterns |
| `workflow` | Process and workflow definitions | Operational procedures |
| `governance` | Rules, policies, standards | Control documents |
| `documentation` | Documentation practices | Meta-documentation |

### Technical Domains

Technology-specific tags:

| Tag | Description | Usage |
|-----|-------------|-------|
| `api` | API design and development | Interface specifications |
| `cli` | Command-line interfaces | CLI tools and usage |
| `sdk` | Software development kits | SDK documentation |
| `protocol` | Communication protocols | Protocol specifications |
| `integration` | System integration patterns | Integration guides |
| `architecture` | System architecture | Design documents |

### Platforms

Platform and vendor tags:

| Tag | Description | Usage |
|-----|-------------|-------|
| `anthropic` | Anthropic Claude and tools | Claude-specific docs |
| `openai` | OpenAI GPT and tools | GPT-specific docs |
| `google` | Google AI and Vertex | Google AI docs |
| `azure` | Microsoft Azure AI | Azure AI docs |
| `aws` | Amazon Web Services AI | AWS AI docs |

### Development Practices

Software development tags:

| Tag | Description | Usage |
|-----|-------------|-------|
| `best-practices` | Recommended approaches | Guidelines |
| `design-patterns` | Reusable solutions | Pattern documentation |
| `testing` | Testing strategies | Test documentation |
| `debugging` | Debugging techniques | Troubleshooting |
| `performance` | Performance optimization | Optimization guides |
| `security` | Security practices | Security documentation |

### Languages & Frameworks

Programming language tags:

| Tag | Description | Usage |
|-----|-------------|-------|
| `python` | Python language | Python-specific docs |
| `javascript` | JavaScript/TypeScript | JS/TS documentation |
| `java` | Java language | Java-specific docs |
| `go` | Go language | Go-specific docs |
| `rust` | Rust language | Rust-specific docs |
| `sql` | SQL and databases | Database docs |

### AI/ML Specific

AI and ML domain tags:

| Tag | Description | Usage |
|-----|-------------|-------|
| `prompt-engineering` | Prompt design and optimization | Prompting guides |
| `rag` | Retrieval-Augmented Generation | RAG patterns |
| `fine-tuning` | Model fine-tuning | Training guides |
| `embeddings` | Vector embeddings | Embedding docs |
| `llm` | Large Language Models | LLM documentation |
| `ml-ops` | Machine Learning Operations | MLOps guides |

### Project Management

Project and process tags:

| Tag | Description | Usage |
|-----|-------------|-------|
| `project-management` | Project planning and tracking | PM documentation |
| `execplans` | Execution plans | Plan templates |
| `changelog` | Change tracking | Version history |
| `versioning` | Version management | Version guides |
| `collaboration` | Team collaboration | Team processes |
| `review` | Review processes | Review guidelines |

### Documentation Types

Document classification tags:

| Tag | Description | Usage |
|-----|-------------|-------|
| `guide` | How-to guides | Instructional docs |
| `reference` | Reference documentation | API/spec docs |
| `tutorial` | Step-by-step tutorials | Learning materials |
| `concept` | Conceptual explanations | Theory docs |
| `example` | Example implementations | Sample code |
| `template` | Document templates | Reusable formats |

### Tool Categories

Development tool tags:

| Tag | Description | Usage |
|-----|-------------|-------|
| `ide` | Integrated Development Environments | IDE guides |
| `vscode` | Visual Studio Code | VS Code specific |
| `git` | Git version control | Git documentation |
| `docker` | Containerization | Docker guides |
| `ci-cd` | Continuous Integration/Deployment | Pipeline docs |
| `monitoring` | Monitoring and observability | Monitoring guides |

### Special Purpose

Specialized tags:

| Tag | Description | Usage |
|-----|-------------|-------|
| `mcp` | Model Context Protocol | MCP documentation |
| `skill` | Agent Skills | Skill specifications |
| `conventions` | Coding conventions | Style standards |
| `metadata` | Metadata management | Meta information |
| `taxonomy` | Classification systems | This document |
| `frontmatter` | Document frontmatter | Metadata specs |

## Tag Usage Rules

### Selection Guidelines

1. **Maximum 7 tags** per document
2. **Order by relevance** - most relevant first
3. **Mix categories** - combine concept + platform + type
4. **Avoid redundancy** - don't use similar tags
5. **Be specific** - prefer specific over general

### Combination Patterns

Good combinations:

```yaml
# AI agent implementation guide
tags: [agents, prompt-engineering, anthropic, guide]

# API reference documentation
tags: [api, reference, rest, documentation]

# Testing best practices
tags: [testing, best-practices, python, tutorial]
```

Bad combinations:

```yaml
# Too many similar tags
tags: [doc, documentation, docs, guide, reference]  # ❌

# Too general
tags: [software, computer, technology]  # ❌

# Exceeds limit
tags: [a, b, c, d, e, f, g, h]  # ❌ Max 7
```

## Adding New Tags

### Proposal Process

1. **Check existing tags** - ensure no duplicates
2. **Justify need** - explain gap in current taxonomy
3. **Define clearly** - provide description and usage
4. **Submit PR** - update this document first
5. **Get approval** - requires maintainer review

### New Tag Template

```markdown
| `new-tag` | Clear description | When to use |
```

Requirements:
- Lowercase only
- Hyphen-separated
- 3-20 characters
- Self-explanatory
- Unique in taxonomy

## Validation

### Automated Checking

```python
def validate_tags(tags, taxonomy):
    """Validate document tags against taxonomy."""
    errors = []

    # Check count
    if len(tags) > 7:
        errors.append(f"Too many tags: {len(tags)} (max 7)")

    # Check validity
    valid_tags = set(taxonomy.keys())
    invalid = set(tags) - valid_tags

    if invalid:
        errors.append(f"Invalid tags: {invalid}")

    # Check format
    for tag in tags:
        if not re.match(r'^[a-z]+(-[a-z]+)*$', tag):
            errors.append(f"Invalid format: {tag}")

    return errors
```

### Manual Review

Check for:
- Appropriate categorization
- Consistent usage across similar documents
- No deprecated tags
- Logical combinations

## Deprecation

### Deprecated Tags

Tags no longer in use:

| Tag | Deprecated | Replacement |
|-----|------------|-------------|
| `ai-first` | 2025-11-01 | `agents` |
| `patterns` | 2025-11-01 | `design-patterns` |
| `infra` | 2025-11-01 | `architecture` |

### Migration Process

1. Identify documents with deprecated tags
2. Update to replacement tags
3. Validate no breaking changes
4. Update in bulk commit

```bash
# Find deprecated tags
grep -r "tags:.*ai-first" docs/

# Replace with new tag
find docs -name "*.md" -exec sed -i 's/ai-first/agents/g' {} \;
```

## Reporting

### Tag Usage Statistics

```bash
# Count tag usage
rg -ho '^tags:.*' docs | tr -d '[]' | tr ',' '\n' | sort | uniq -c

# Find untagged documents
rg --files-without-match '^tags:' docs

# Find over-tagged documents
rg -n '^tags:' docs | awk -F',' 'NF>7 {print $0}'
```

### Coverage Report

Monitor taxonomy coverage:

- Documents with tags: 100% target
- Average tags per document: 3-5
- Most used tags: Track top 10
- Least used tags: Review quarterly

## Maintenance

### Quarterly Review

1. Analyze tag usage patterns
2. Identify unused tags
3. Propose new tags based on gaps
4. Deprecate obsolete tags
5. Update documentation

### Annual Audit

1. Full taxonomy evaluation
2. Category reorganization
3. Cross-reference with industry standards
4. Stakeholder feedback
5. Major version update

## See Also

- [Frontmatter](../core/frontmatter.md) - Metadata specification
- [Style](./style.md) - Documentation standards
- [Contributing](./contributing.md) - How to contribute

## References

Taxonomy design influenced by:
- Dublin Core Metadata Standards
- Schema.org vocabulary
- Library of Congress Subject Headings
