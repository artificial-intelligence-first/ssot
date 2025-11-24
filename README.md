# AI-First SSOT

> **Single Source of Truth for AI-First Development**
> A centralized repository managing structured knowledge documents optimized for both AI agents and human developers

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This repository establishes a **Single Source of Truth (SSOT)** for AI-first development practices, providing canonical documentation that serves as the authoritative reference for both autonomous agents and development teams. Each document follows a rigorous 11-section structure designed to eliminate ambiguity and ensure consistency across all knowledge artifacts.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/artificial-intelligence-first/ssot.git

# Navigate to documentation
cd ssot/docs

# Create new topic from template
cp _templates/TOPIC_TEMPLATE.md docs/YOUR_TOPIC.md
```

## Repository Layout

```
ssot/
│
├── docs/                        # Core documentation
│   ├── AGENT_SKILL.md          # Agent Skill All Model specification
│   ├── CODE_MCP.md             # Code MCP implementation guide
│   ├── EXEC_PLAN.md            # ExecPlan methodology documentation
│   └── README_AND_AGENTS.md   # Repository documentation patterns
│
├── _templates/                  # Document templates
│   ├── TOPIC_TEMPLATE.md       # Standard topic structure
│   ├── SECTION_TEMPLATE.md     # Section patterns (11 types)
│   └── FRONT_MATTER.md         # Metadata requirements
│
├── README.md                    # Repository overview (this file)
└── LICENSE                      # MIT License
```

## Document Architecture

### Mandatory Structure

Every document in this repository adheres to a standardized 11-section architecture:

| Section | Purpose | Requirements |
|---------|---------|--------------|
| **Frontmatter** | Metadata and classification | `title`, `slug`, `tags`, `summary`, `last_updated` |
| **Agent Contract** | Operational boundaries | Purpose, use conditions, priorities, related topics |
| **TL;DR** | Executive summary | What, Why, When, How, Watch Out |
| **Canonical Definitions** | Terminology standardization | Unambiguous definitions with scope boundaries |
| **Core Patterns** | Implementation approaches | Solutions with explicit trade-offs |
| **Decision Checklist** | Verification criteria | Actionable validation points |
| **Anti-patterns** | Common pitfalls | What to avoid and why |
| **Evaluation** | Quality metrics | Testing strategies and success criteria |
| **Update Log** | Change tracking | Dated entries with author attribution |
| **See Also** | Navigation | Prerequisites and related topics |
| **References** | Citations | Authoritative sources with access dates |

### Creating Documentation

#### Step 1: Initialize from Template

```bash
cp _templates/TOPIC_TEMPLATE.md docs/YOUR_TOPIC.md
```

#### Step 2: Complete Frontmatter

```yaml
---
title: Your Topic Name
slug: your-topic-name
summary: "Concise description"
type: spec|guide|reference|policy|concept
tags: [topic, ai-first, relevant-domain]
last_updated: YYYY-MM-DD
---
```

#### Step 3: Populate Sections

Follow the structured templates in `_templates/SECTION_TEMPLATE.md` for consistent formatting across all documentation types.

## Standards and Conventions

### Tag Taxonomy

| Tag Category | Purpose | Examples |
|--------------|---------|----------|
| **Structural** | Document classification | `topic`, `template`, `draft` |
| **Optimization** | Target audience | `ai-first`, `human-readable` |
| **Domain** | Subject matter | `agent`, `mcp`, `skill`, `architecture` |
| **Maturity** | Document status | `stable`, `beta`, `experimental` |

### Quality Requirements

**Mandatory Criteria**
- All 11 sections must be present and populated
- Definitions must eliminate ambiguity
- Trade-offs must be explicitly stated
- Examples must be executable
- References must include access dates

**Validation Checklist**
- [ ] Frontmatter validates against schema
- [ ] No placeholder text remaining
- [ ] Cross-references resolve correctly
- [ ] Code examples tested and functional
- [ ] Update log reflects all modifications

## Navigation

### Primary Documents

| Document | Purpose | Status |
|----------|---------|--------|
| [AGENT_SKILL.md](./docs/AGENT_SKILL.md) | Agent Skill All Model specification | Stable |
| [CODE_MCP.md](./docs/CODE_MCP.md) | Model Context Protocol implementation | Stable |
| [EXEC_PLAN.md](./docs/EXEC_PLAN.md) | ExecPlan methodology and patterns | Stable |
| [SSOT.md](./docs/SSOT.md) | Single Source of Truth governance guide | Stable |
| [README_AND_AGENTS.md](./docs/README_AND_AGENTS.md) | Documentation architecture patterns | Stable |

### Templates and Tools

| Resource | Usage | Location |
|----------|-------|----------|
| Topic Template | New document creation | [`_templates/TOPIC_TEMPLATE.md`](./_templates/TOPIC_TEMPLATE.md) |
| Section Patterns | Content structure guides | [`_templates/SECTION_TEMPLATE.md`](./_templates/SECTION_TEMPLATE.md) |
| Frontmatter Guide | Metadata requirements | [`_templates/FRONT_MATTER.md`](./_templates/FRONT_MATTER.md) |

## Contributing

### Submission Process

1. **Fork** the repository
2. **Create** topic branch: `git checkout -b topic/your-topic-name`
3. **Apply** template structure
4. **Validate** against quality requirements
5. **Submit** pull request with detailed description

### Review Criteria

Pull requests must satisfy:
- Complete 11-section structure
- No ambiguous definitions
- Executable code examples
- Proper citation formatting
- Update log entry added

## Governance

### Maintenance Schedule

| Activity | Frequency | Responsibility |
|----------|-----------|----------------|
| Content review | Monthly | Document owners |
| Reference validation | Quarterly | Automation tools |
| Structure updates | Semi-annually | Architecture team |
| Template evolution | As needed | Community consensus |

### Version Control

- **Main branch**: Production-ready documentation
- **Feature branches**: Topic development
- **Release tags**: Quarterly snapshots
- **Archive policy**: Annual consolidation

## License

MIT License - See [LICENSE](./LICENSE) for full terms.

---

**Repository**: [github.com/artificial-intelligence-first/ssot](https://github.com/artificial-intelligence-first/ssot)
**Maintained by**: AI-First Development Team
**Last Updated**: 2025-11-22
