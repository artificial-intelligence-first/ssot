# AI-First SSOT (Single Source of Truth)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A template system for building AI-optimized reference documentation.**

This repository provides structured templates for creating Single Source of Truth (SSOT) documentation that AI agents can reliably consume and reference. The templates are designed for clarity, consistency, and machine-readability while remaining human-friendly.

## What This Repository Provides

- **TOPIC_TEMPLATE.md** - Complete template for creating new reference topics
- **SECTION_TEMPLATE.md** - 11 reusable section templates for extending topics

## Key Features

### For AI Agents

- **Agent Contract** - Every topic declares its purpose, usage conditions, and priorities
- **Canonical Definitions** - Unambiguous terminology with explicit scope boundaries
- **Decision Checklists** - Actionable verification criteria for pattern application
- **Anti-patterns** - Explicit failure modes with detection symptoms
- **Structured Metadata** - YAML frontmatter for discovery and filtering

### For Humans

- **TL;DR Sections** - Quick 5-point summaries (What/Why/When/How/Watch Out)
- **Complete Examples** - Runnable code demonstrating each pattern
- **Trade-off Analysis** - Explicit advantages, disadvantages, and alternatives
- **Update Tracking** - Changelog and version history in every document

## Repository Structure

```
ssot/
├── README.md                    # This file
├── LICENSE                      # MIT License
└── _templates/
    ├── TOPIC_TEMPLATE.md        # Template for complete topic documents
    └── SECTION_TEMPLATE.md      # Templates for individual sections
```

## Quick Start

### Creating a New Topic

1. Copy `_templates/TOPIC_TEMPLATE.md` to your documentation directory
2. Fill in the frontmatter:
   ```yaml
   ---
   title: Your Topic Name
   slug: your-topic-name
   last_updated: YYYY-MM-DD
   tags: [topic, ai-first, domain-tag]
   summary: "One-sentence description"
   ---
   ```
3. Complete the **Agent Contract** section first
4. Fill in **TL;DR** for quick reference
5. Add definitions, patterns, and anti-patterns as needed

### Adding Sections to Existing Topics

1. Open `_templates/SECTION_TEMPLATE.md`
2. Choose the appropriate template:
   - **Pattern** - Design pattern or approach
   - **Anti-pattern** - Common mistake to avoid
   - **Definition** - Terminology clarification
   - **Checklist** - Decision criteria
   - **Evaluation Metric** - Measurement approach
   - **Case Study** - Real-world example
   - **Code Example** - Implementation demo
   - **Comparison** - Feature/approach comparison
   - **Troubleshooting** - Problem diagnosis
   - **Best Practice** - Recommended approach
   - **Migration Guide** - Upgrade pathway
3. Copy the template and replace all `[placeholders]`
4. Update the topic's `last_updated` and `Update Log`

## Frontmatter Schema

All topic documents use this minimal, consistent frontmatter:

```yaml
---
title: Topic Name              # Human-readable title
slug: topic-name               # URL-friendly identifier
last_updated: YYYY-MM-DD       # ISO 8601 date
tags: [topic, ai-first, ...]   # Max 7 tags for categorization
summary: "Brief description"   # Under 160 characters
---
```

### Tag Conventions

- **topic** - Marks actual knowledge documents (vs templates)
- **ai-first** - Indicates AI-optimized content
- **template** - Marks template files (excluded from knowledge search)
- Domain tags as needed (e.g., `prompt-engineering`, `context-management`)

## Document Structure

Every topic document follows this structure:

1. **Agent Contract** - AI usage specification
   - PURPOSE - What this topic defines
   - USE_WHEN - When to apply this
   - DO_NOT_USE_WHEN - When NOT to apply
   - PRIORITY - Conflict resolution rules
   - RELATED_TOPICS - Cross-references

2. **TL;DR** - 5-point summary
   - WHAT - Definition
   - WHY - Value proposition
   - WHEN - Application scenarios
   - HOW - Approach
   - WATCH_OUT - Critical pitfall

3. **Canonical Definitions** - Unambiguous terminology
4. **Core Patterns** - Implementation approaches
5. **Decision Checklist** - Application criteria
6. **Anti-patterns / Pitfalls** - What to avoid
7. **Evaluation** - Metrics and success criteria
8. **Update Log** - Change history
9. **See Also** - Related topics
10. **References** - Source citations

## Design Principles

### AI-First Optimization

- **No Ambiguity** - Every term has explicit scope boundaries
- **No Duplication** - Single source of truth for each concept
- **No Assumed Context** - All prerequisites explicitly stated
- **Executable Examples** - All code samples are complete and runnable

### Human Readability

- **Quick Scanning** - TL;DR and headers enable rapid navigation
- **Progressive Detail** - Start simple, add depth as you read
- **Clear Structure** - Consistent sections across all topics
- **Visual Markers** - ✅/❌/⚠️/💡 for quick pattern recognition

### Maintainability

- **Template-Driven** - Consistent structure reduces cognitive load
- **Version Tracked** - Every change logged in Update Log
- **Cross-Referenced** - Related topics explicitly linked
- **Source Cited** - All claims backed by [R#] references

## Usage Patterns

### For RAG Systems

```python
# Filter out templates from knowledge base
def load_knowledge_docs(docs):
    return [
        doc for doc in docs
        if 'template' not in doc.frontmatter.get('tags', [])
        and 'topic' in doc.frontmatter.get('tags', [])
    ]

# Extract Agent Contract for routing
def get_agent_contract(doc):
    # Parse ## Agent Contract section
    # Use PURPOSE, USE_WHEN for document selection
    pass
```

### For AI Assistants

```python
# Load context with priority awareness
def load_context_for_task(task_type):
    relevant_docs = search_by_tag(task_type)
    # Sort by PRIORITY field in Agent Contract
    # Apply DO_NOT_USE_WHEN filters
    return prioritized_context
```

### For Human Developers

```bash
# Find all topics on a subject
grep -r "tags:.*prompt-engineering" *.md

# View quick summaries
grep "^summary:" *.md

# Check when last updated
grep "^last_updated:" *.md | sort
```

## Contributing

When adding new topics or updating existing ones:

1. **Use the templates** - Consistency is critical for AI consumption
2. **Complete all sections** - Empty sections create ambiguity
3. **Cite your sources** - Add [R#] references for all claims
4. **Update metadata** - Change `last_updated` and add to `Update Log`
5. **Test examples** - Verify all code is runnable
6. **Check cross-references** - Ensure `RELATED_TOPICS` are bidirectional

## License

MIT License - See [LICENSE](./LICENSE) file for details.

## Philosophy

This repository embraces the principle that **documentation optimized for AI consumption is better documentation for humans too**. By eliminating ambiguity, providing complete examples, and maintaining consistent structure, we create references that serve both audiences effectively.

The goal is not to replace human judgment but to provide AI agents with the same quality of reference material that expert developers would use - clear, complete, and authoritative.
