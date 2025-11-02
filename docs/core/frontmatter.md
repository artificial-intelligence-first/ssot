---
title: Frontmatter
slug: frontmatter
status: living
last_updated: 2025-11-01
tags: [conventions, documentation, best-practices, design-patterns]
summary: "YAML frontmatter specification for adding structured metadata to Markdown documents."
authors: []
sources:
  - { id: R1, title: "YAML Ain't Markup Language (YAML™) revision 1.2.2", url: "https://yaml.org/spec/1.2.2/", accessed: "2025-11-01" }
  - { id: R2, title: "Jekyll - Front Matter Official Documentation", url: "https://jekyllrb.com/docs/front-matter/", accessed: "2025-11-01" }
  - { id: R3, title: "Hugo - Front Matter Official Documentation", url: "https://gohugo.io/content-management/front-matter/", accessed: "2025-11-01" }
---

# Frontmatter

> **For Humans**: This guide defines YAML frontmatter standards for consistent metadata across all Markdown documents.
>
> **For AI Agents**: Parse and generate frontmatter according to this v1 Core specification. Validate all required fields and enforce constraints.

## Overview

YAML frontmatter provides structured metadata at the beginning of Markdown files, enabling programmatic discovery, validation, and processing of documentation.

## v1 Core Specification

### Required Fields

```yaml
---
title: Document Title        # Human-readable title
slug: document-slug          # URL-safe identifier
status: living              # draft|living|stable|deprecated
last_updated: 2025-11-01    # ISO 8601 date
tags: [tag1, tag2]          # Maximum 7 tags
summary: "Description < 160 chars"  # Brief description
authors: []                 # Optional author list
sources: []                 # Optional source references
---
```

### Field Specifications

| Field | Type | Required | Constraints | Example |
|-------|------|----------|-------------|---------|
| `title` | String | Yes | 1-100 chars | "Context Engineering" |
| `slug` | String | Yes | `^[a-z0-9]+(-[a-z0-9]+)*$`, 3-64 chars | "context-engineering" |
| `status` | Enum | Yes | draft\|living\|stable\|deprecated | "living" |
| `last_updated` | Date | Yes | ISO 8601 (YYYY-MM-DD) | "2025-11-01" |
| `tags` | Array | Yes | Max 7 items, lowercase | ["agents", "documentation"] |
| `summary` | String | Yes | Max 160 chars, no newlines | "Best practices for AI context design." |
| `authors` | Array | No | Display names | ["Alice Smith", "bob"] |
| `sources` | Array | No | Max 10 items | See sources format below |

### Sources Format

```yaml
sources:
  - id: R1
    title: "Source Title"
    url: "https://example.com/article"
    accessed: "2025-11-01"
```

## YAML Syntax Rules

### Indentation
- Use spaces only (2 or 4 spaces)
- Never use tabs
- Be consistent throughout

### Strings
Quote strings containing:
- Colons (`:`)
- Hashes (`#`)
- Special characters
- Leading/trailing spaces

```yaml
# Good
title: "Introduction: A Guide"
summary: "Learn about #hashtags and more"

# Bad
title: Introduction: A Guide  # Colon will break parsing
```

### Arrays

Two valid formats:

```yaml
# Flow style (compact)
tags: [api, documentation, rest]

# Block style (readable)
tags:
  - api
  - documentation
  - rest
```

### Booleans

Use only lowercase `true` or `false`:

```yaml
# Good
published: true
draft: false

# Bad (YAML 1.1 style - avoid)
published: yes
draft: no
```

## Status Lifecycle

```
draft → living → stable → deprecated
```

| Status | Description | Use Case |
|--------|-------------|----------|
| `draft` | Under development | New documents, major rewrites |
| `living` | Actively maintained | Frequently updated guides |
| `stable` | Mature, rarely changed | Established specifications |
| `deprecated` | Obsolete, kept for reference | Superseded documents |

## Validation

### Required Field Validation

```python
def validate_frontmatter(fm):
    errors = []

    # Required fields
    required = ['title', 'slug', 'status', 'last_updated', 'tags', 'summary']
    for field in required:
        if field not in fm:
            errors.append(f"Missing required field: {field}")

    # Slug format
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', fm.get('slug', '')):
        errors.append("Invalid slug format")

    # Status enum
    if fm.get('status') not in ['draft', 'living', 'stable', 'deprecated']:
        errors.append("Invalid status value")

    # Tag count
    if len(fm.get('tags', [])) > 7:
        errors.append("Too many tags (max 7)")

    # Summary length
    if len(fm.get('summary', '')) > 160:
        errors.append("Summary too long (max 160)")

    return errors
```

### Date Validation

```python
from datetime import datetime

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
```

## Common Patterns

### Multi-author Documents

```yaml
authors:
  - "Jane Doe"
  - "john-smith"
  - "AI Assistant"
```

### Rich Source Citations

```yaml
sources:
  - id: R1
    title: "Comprehensive Guide to YAML"
    url: "https://yaml.org/spec/"
    accessed: "2025-11-01"
  - id: R2
    title: "Frontmatter Best Practices"
    url: "https://example.com/frontmatter"
    accessed: "2025-10-15"
```

### Tag Categories

Group related tags:

```yaml
tags: [concept-context, impl-python, platform-openai]
```

## Anti-patterns

### Tab Characters
❌ **Wrong**: Using tabs for indentation
```yaml
# title:<TAB>"Document"  # Tab character (not allowed)
```
✅ **Right**: Using spaces
```yaml
title: "Document"  # Spaces
```

### Ambiguous Values
❌ **Wrong**: Unquoted special values
```yaml
version: 1.0  # Interpreted as float
port: 080     # Interpreted as octal
```
✅ **Right**: Explicit strings
```yaml
version: "1.0"
port: "080"
```

### Missing Frontmatter
❌ **Wrong**: Starting with content
```markdown
# My Document
Content here...
```
✅ **Right**: Frontmatter first
```markdown
---
title: My Document
slug: my-document
...
---

# My Document
```

## Platform Support

### Jekyll

```yaml
---
layout: post
title: "Jekyll Post"
date: 2025-11-01
categories: [blog, tutorial]
---
```

### Hugo

```yaml
---
title: "Hugo Page"
date: 2025-11-01T10:00:00Z
draft: false
weight: 100
---
```

### GitHub

```yaml
---
title: GitHub Page
labels: [documentation, help-wanted]
assignees: [username]
---
```

## Tools

### Validation Script

```bash
#!/usr/bin/env bash
# validate-frontmatter.sh

find docs -name "*.md" -print0 | while IFS= read -r -d '' file; do
  echo "Checking $file..."

  # Extract frontmatter
  frontmatter=$(awk '
    NR==1 && $0=="---" {in_frontmatter=1; next}
    in_frontmatter && $0=="---" {exit}
    in_frontmatter {print}
  ' "$file")

  # Check required fields
  for field in title slug status last_updated tags summary; do
    if ! echo "$frontmatter" | grep -q "^$field:"; then
      echo "  ERROR: Missing $field"
    fi
  done
done
```

### Auto-generation

```python
def generate_frontmatter(title, tags=None):
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

    return {
        'title': title,
        'slug': slug,
        'status': 'draft',
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
        'tags': tags or [],
        'summary': '',
        'authors': [],
        'sources': []
    }
```

## See Also

- [SSOT.md](../../SSOT.md) - Single Source of Truth principles
- [Style](../governance/style.md) - Repository-wide writing standards
- [Taxonomy](../governance/taxonomy.md) - Controlled vocabulary for tags

## References

- [R1] YAML Ain't Markup Language (YAML™) revision 1.2.2. https://yaml.org/spec/1.2.2/ (accessed 2025-11-01)
- [R2] Jekyll - Front Matter Official Documentation. https://jekyllrb.com/docs/front-matter/ (accessed 2025-11-01)
- [R3] Hugo - Front Matter Official Documentation. https://gohugo.io/content-management/front-matter/ (accessed 2025-11-01)
