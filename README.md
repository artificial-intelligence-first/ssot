# AI-First Development Reference

[![Link Check](https://github.com/artificial-intelligence-first/ssot/actions/workflows/linkcheck.yml/badge.svg)](https://github.com/artificial-intelligence-first/ssot/actions/workflows/linkcheck.yml)
[![Markdown Lint](https://github.com/artificial-intelligence-first/ssot/actions/workflows/markdownlint.yml/badge.svg)](https://github.com/artificial-intelligence-first/ssot/actions/workflows/markdownlint.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **For Humans**: This repository contains best practices and conventions for working effectively with AI coding assistants. Use these guides to structure your projects for maximum AI productivity.
>
> **For AI Agents**: This repository contains canonical reference documentation for AI-first development patterns. Start with AGENTS.md for operational instructions and SSOT.md for canonical definitions. Follow the governance documents when updating content.

## Quick Start

### Essential Documents

1. **[AGENTS.md](./AGENTS.md)** - AI agent operational documentation (start here for AI agents)
2. **[SSOT.md](./SSOT.md)** - Single Source of Truth principles and canonical definitions

### For Humans

```bash
# Clone repository
git clone https://github.com/artificial-intelligence-first/ssot.git
cd ssot

# Review core documentation
cat AGENTS.md  # Understand AI agent setup
cat SSOT.md    # Learn SSOT principles

# Browse specific topics
ls docs/       # All documentation
```

### For AI Agents

```python
# 1. Read operational instructions
with open('AGENTS.md') as f:
    operations = f.read()

# 2. Check canonical definitions
with open('SSOT.md') as f:
    definitions = f.read()

# 3. Follow update procedures
with open('docs/contributing.md') as f:
    procedures = f.read()
```

## Repository Structure

```
ssot/
├── AGENTS.md                 # AI agent operational documentation
├── SSOT.md                   # Single Source of Truth principles
├── README.md                 # This file
├── docs/                     # All documentation
│   ├── core/                 # Core concepts & detailed guides
│   ├── engineering/          # Engineering methodologies
│   ├── governance/           # Governance & standards
│   ├── platforms/            # Platform-specific implementations
│   ├── research/             # Information about AI research
│   ├── systems/              # System tools
│   ├── tools/                # Development tools
│   └── workflows/            # Workflow management
└── _templates/               # Document templates
    ├── TOPIC_TEMPLATE.md     # New topic template
    └── SECTION_TEMPLATE.md   # Section templates
```

## Core Concepts

### Single Source of Truth (SSOT)

Each piece of information has exactly one authoritative location. All other references point back to this canonical source.

```yaml
# Example: API versioning policy
Canonical Location: /SSOT.md#versioning-policy
References: All other docs link to this section
```

### AI-First Development

Design patterns and practices optimized for AI-assisted development:

- **Structured Documentation**: Machine-readable formats with YAML frontmatter
- **Clear Conventions**: Predictable patterns AI agents can follow
- **Explicit Context**: All necessary information in one place
- **Testable Patterns**: Verifiable implementations and examples

## Documentation Standards

### Frontmatter (v1 Core)

All documents must include:

```yaml
---
title: Document Title
slug: document-slug
status: draft|living|stable|deprecated
last_updated: YYYY-MM-DD
tags: [max, seven, tags]
summary: "Brief description under 160 characters."
authors: []
sources: []
---
```

### Document Structure

1. **Frontmatter**: Metadata for discovery and management
2. **Title**: Matches frontmatter title
3. **Dual-Audience Statement**: For humans and AI agents
4. **Content**: Structured sections with clear hierarchy
5. **References**: Cited sources with access dates

## Usage Patterns

### Finding Information

```bash
# Search by topic
grep -r "context engineering" docs/

# Find by tag
grep "tags:.*prompt" docs/*.md

# List all guides
ls docs/*.md | xargs head -n 20 | grep "^title:"
```

### Contributing Updates

1. **Check SSOT.md** for canonical definitions
2. **Follow AGENTS.md** for operational procedures
3. **Use templates** from _templates/ for new content
4. **Validate** with markdownlint before submitting
5. **Update** last_updated field and changelog

## Platform Support

### Supported Platforms

- **Anthropic**: Claude, Agent SDK
- **OpenAI**: GPT models, Agents SDK
- **Google**: Gemini, Vertex AI
- **MCP**: Model Context Protocol

### Integration Examples

```python
# Load context for AI assistant
def load_ai_context():
    context = {}
    context['operations'] = read_file('AGENTS.md')
    context['definitions'] = read_file('SSOT.md')
    context['domain'] = read_file('docs/your-domain.md')
    return context

# Apply to your AI workflow
context = load_ai_context()
response = ai_model.generate(
    prompt=user_query,
    context=context
)
```

## Governance

### Update Frequency

- **Living documents**: Updated as needed
- **Stable documents**: Quarterly review
- **Deprecated**: Marked but preserved

### Quality Assurance

- Automated markdown linting
- Link checking
- Frontmatter validation
- Cross-reference verification

### Decision Process

1. **Proposal**: Submit via pull request
2. **Review**: Technical and content review
3. **Validation**: Automated checks must pass
4. **Approval**: Maintainer approval required
5. **Merge**: Integrated into main branch

## License

MIT License - See [LICENSE](./LICENSE) file for details.

## Acknowledgments

This repository synthesizes best practices from:
- Anthropic's documentation standards
- OpenAI's agent conventions
- Google's AI development guides
- Open source community patterns

## Contact

- **Issues**: [GitHub Issues](https://github.com/artificial-intelligence-first/ssot/issues)
- **Contributing**: See [CONTRIBUTING.md](./docs/governance/contributing.md)
