---
title: Style
slug: style
status: stable
last_updated: 2025-11-01
tags: [documentation, style-guide, standards, governance]
summary: "Documentation style guide defining writing standards, formatting rules, and conventions for consistency."
authors: []
sources: []
---

# Style

> **For Humans**: This style guide ensures consistent, clear documentation across the repository. Follow these conventions for all written content.
>
> **For AI Agents**: Apply these style rules when generating or modifying documentation. Enforce consistency in formatting, structure, and terminology.

## Overview

This style guide establishes writing standards for all documentation in this repository. It covers language usage, formatting conventions, structural patterns, and technical terminology to ensure consistency and clarity.

## Writing Principles

### Clarity

Write for comprehension:

- **Simple language**: Prefer common words over jargon
- **Active voice**: "The function returns" not "A value is returned"
- **Direct statements**: Avoid unnecessary qualifiers
- **Concrete examples**: Show, don't just tell

### Conciseness

Eliminate redundancy:

- **One idea per sentence**
- **Short paragraphs** (3-5 sentences)
- **Bulleted lists** for multiple items
- **Tables** for comparisons

### Consistency

Maintain uniformity:

- **Terminology**: Same term for same concept
- **Structure**: Predictable document organization
- **Format**: Consistent code examples
- **Style**: Uniform voice and tone

## Document Structure

### Standard Sections

All documents follow this order:

1. **Frontmatter**: YAML metadata
2. **Title** (H1): Matches frontmatter title
3. **Dual-Audience Statement**: For humans/AI agents
4. **Overview**: Brief introduction
5. **Core Content**: Main sections
6. **Examples**: Practical demonstrations
7. **See Also**: Related documents
8. **References**: External sources

### Heading Hierarchy

```markdown
# Document Title (H1 - one per document)

## Major Section (H2)

### Subsection (H3)

#### Detail Level (H4)

##### Rarely Used (H5)
```

Rules:
- One H1 per document
- Don't skip levels (H1 → H3 ❌)
- Use sentence case for H3-H5
- Use title case for H1-H2

## Formatting Conventions

### Text Emphasis

- **Bold** for important terms first use
- *Italic* for emphasis (sparingly)
- `Code` for inline code, commands, filenames
- > Blockquote for important notes

### Lists

Unordered lists:
- Use hyphens (`-`) not asterisks
- Single space after hyphen
- Capitalize first word
- Period only for complete sentences

Ordered lists:
1. Use `1.` format
2. Let Markdown auto-number
3. Use for sequential steps
4. Include result after steps

### Code Blocks

\`\`\`language
// Always specify language
// Include helpful comments
// Make examples runnable
const example = "complete code";
\`\`\`

Languages: `javascript`, `python`, `bash`, `yaml`, `json`, `markdown`

### Tables

| Column | Format | Example |
|--------|--------|---------|
| Headers | Bold | **Name** |
| Alignment | Pipes | Standard |
| Width | Auto | Flexible |

Rules:
- Always include header row
- Use pipes for all cells
- Align pipes for readability
- Keep cells concise

## Language Usage

### Technical Terms

First occurrence:
- **Define on first use**
- Provide context
- Link to glossary if available

Example:
> **Single Source of Truth (SSOT)** is the practice of designating one authoritative location for any piece of information.

### Abbreviations

- Spell out on first use: "Application Programming Interface (API)"
- Use consistently after introduction
- Common exceptions: URL, JSON, YAML, SQL

### Voice and Tone

- **Professional**: Technical but accessible
- **Direct**: No unnecessary words
- **Neutral**: Avoid marketing language
- **Inclusive**: No assumptions about reader

## Code Documentation

### Inline Comments

```python
# Good: Explains why
result = value * 1.1  # Add 10% buffer for network latency

# Bad: Explains what (obvious)
result = value * 1.1  # Multiply by 1.1
```

### Function Documentation

```python
def process_data(input_data, options=None):
    """Process input data according to options.

    Args:
        input_data: Raw data to process
        options: Optional processing configuration

    Returns:
        Processed data dictionary

    Raises:
        ValueError: If input_data is invalid
    """
```

### Example Code

✅ **Good Example**:
```python
# Complete, runnable example
import json

def load_config(path):
    """Load configuration from JSON file."""
    with open(path, 'r') as f:
        return json.load(f)

# Usage
config = load_config('config.json')
print(f"Loaded {len(config)} settings")
```

❌ **Bad Example**:
```python
# Incomplete snippet
def load_config(path):
    # ... implementation ...
    pass
```

## Cross-References

### Internal Links

```markdown
See [SSOT principles](../../SSOT.md#principles)
Refer to [Context Engineering](./context-engineering.md)
```

Rules:
- Use relative paths
- Include section anchors when specific
- Verify links work

### External Links

```markdown
According to the [Official Documentation](https://example.com/docs)
```

Rules:
- Use descriptive link text
- Include access date in references
- Archive important external content

### Citations

In text:
```markdown
The approach follows established patterns [R1].
Multiple sources confirm this [R2][R3].
```

In references:
```markdown
## References

- [R1] Author. "Title." Source. URL (accessed YYYY-MM-DD)
- [R2] Organization. "Document." URL (accessed YYYY-MM-DD)
```

## Common Patterns

### Decision Documentation

```markdown
## Decision: Choose PostgreSQL

**Context**: Need reliable database with JSON support

**Options Considered**:
1. PostgreSQL - Full JSON support, proven reliability
2. MySQL - Limited JSON, wide adoption
3. MongoDB - Native JSON, different paradigm

**Decision**: PostgreSQL for JSON features with SQL benefits

**Trade-offs**: Higher operational complexity
```

### Warning Blocks

```markdown
> ⚠️ **Warning**: This operation is destructive and cannot be undone.
> Ensure you have backups before proceeding.
```

### Version Notes

```markdown
> **Version Note**: This feature requires v2.0.0 or higher.
> For earlier versions, see [legacy documentation](./legacy.md).
```

## Anti-patterns

### Avoid Ambiguity

❌ **Wrong**: "This might work sometimes"
✅ **Right**: "This works when X condition is met"

### Avoid Passive Voice

❌ **Wrong**: "The file is created by the system"
✅ **Right**: "The system creates the file"

### Avoid Walls of Text

❌ **Wrong**: Long paragraph with multiple ideas
✅ **Right**: Short paragraphs, bulleted lists, clear sections

### Avoid Inconsistent Terms

❌ **Wrong**: Mixing "function", "method", "procedure"
✅ **Right**: Choose one term and use consistently

## Quality Checklist

Before submitting:

- [ ] Spell check passed
- [ ] Grammar check completed
- [ ] Links verified
- [ ] Code examples tested
- [ ] Formatting consistent
- [ ] Terms used consistently
- [ ] References complete
- [ ] Frontmatter valid

## Glossary

Common terms in this repository:

| Term | Definition |
|------|------------|
| **Agent** | AI system that performs tasks autonomously |
| **Context** | Information provided to AI for task completion |
| **Frontmatter** | YAML metadata at document start |
| **SSOT** | Single Source of Truth |
| **Prompt** | Input instructions to AI model |

## Tools

### Linting

```bash
# Markdown linting
npx markdownlint "**/*.md"

# Spell checking
npx cspell "**/*.md"

# Style checking
vale docs/
```

### Formatting

```bash
# Format Markdown
npx prettier --write "**/*.md"

# Fix common issues
npx markdownlint --fix "**/*.md"
```

## See Also

- [Frontmatter](../core/frontmatter.md) - Metadata specification
- [Contributing](./contributing.md) - Contribution guidelines
- [SSOT.md](../../SSOT.md) - Truth principles

## References

Style guides that influenced this document:
- Google Developer Documentation Style Guide
- Microsoft Writing Style Guide
- Write the Docs Documentation Guide
