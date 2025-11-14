# AI-First SSOT (Single Source of Truth)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A centralized repository for AI-First SSOT documentation. This repository manages structured knowledge documents optimized for both AI agents and human developers.

---

## Repository Structure

```
ssot/
├── docs/                        # SSOT topic documents
│   ├── AGENT_SKILL.md          # Agent Skill All Model specification
│   └── CODE_MCP.md             # Code MCP implementation guide
├── _templates/
│   ├── TOPIC_TEMPLATE.md       # Template for new topic documents
│   └── SECTION_TEMPLATE.md     # Section templates (11 types)
├── README.md                    # This file
└── LICENSE                      # MIT License
```

---

## Document Structure

All topic documents follow a consistent structure:

1. **Frontmatter** - Metadata (title, slug, tags, summary, last_updated)
2. **Agent Contract** - Purpose, usage conditions, priorities
3. **TL;DR** - Five-point summary (What/Why/When/How/Watch Out)
4. **Canonical Definitions** - Unambiguous terminology with scope boundaries
5. **Core Patterns** - Implementation approaches with trade-offs
6. **Decision Checklist** - Verification criteria for application
7. **Anti-patterns / Pitfalls** - Common mistakes to avoid
8. **Evaluation** - Metrics, testing strategies, success criteria
9. **Update Log** - Change history
10. **See Also** - Related topics and prerequisites
11. **References** - Source citations

---

## Creating New Topics

1. Copy `_templates/TOPIC_TEMPLATE.md` to `docs/`
2. Fill in frontmatter with title, slug, tags, and summary
3. Complete all sections following the template structure
4. Update `last_updated` and add entry to Update Log

---

## Tag Conventions

- `topic` - Marks actual knowledge documents
- `ai-first` - Indicates AI-optimized content
- `template` - Marks template files (excluded from knowledge base)
- Domain tags - Categorization (e.g., `agent`, `mcp`, `skill`, `code`)

---

## License

MIT License - See [LICENSE](./LICENSE) file for details.
