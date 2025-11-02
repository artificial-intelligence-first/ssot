---
title: Contributing
slug: contributing
status: living
last_updated: 2025-11-01
tags: [governance, workflow, documentation, collaboration]
summary: "Guidelines for contributing to this repository including workflows, standards, and review processes."
authors: []
sources: []
---

# Contributing

> **For Humans**: This guide outlines how to contribute to this repository, including submission workflows, quality standards, and review processes.
>
> **For AI Agents**: Follow these procedures when making changes. Ensure all modifications comply with standards, update metadata, and maintain backward compatibility.

## Overview

This document defines the contribution workflow for maintaining and expanding this AI-first development reference repository. All contributions must follow these guidelines to ensure consistency and quality.

## Contribution Workflow

### 1. Before You Start

```bash
# Fork and clone
git clone https://github.com/YOUR-USERNAME/ssot.git
cd ssot

# Add upstream
git remote add upstream https://github.com/artificial-intelligence-first/ssot.git

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Making Changes

#### Adding New Documents

1. Use appropriate template from `_templates/`
2. Follow v1 Core frontmatter specification
3. Place in `docs/` with matching slug
4. Update relevant index files

```bash
# Copy template
cp _templates/TOPIC_TEMPLATE.md docs/your-topic.md

# Edit with required frontmatter
---
title: Your Topic
slug: your-topic
status: draft
last_updated: 2025-11-01
tags: [relevant, tags, here]
summary: "Brief description under 160 characters."
authors: ["Your Name"]
sources: []
---
```

#### Updating Existing Documents

1. Preserve existing structure
2. Update `last_updated` field
3. Add entry to document's update log
4. Maintain backward compatibility

```markdown
## Update Log

### 2025-11-01
- **Added**: New section on advanced patterns
- **Updated**: Examples with latest syntax
- **Fixed**: Broken link to external resource
```

### 3. Quality Checks

Run all validation before submitting:

```bash
# Markdown lint
npx markdownlint "**/*.md"

# Link check
find docs -name "*.md" -print0 | xargs -0 -n1 npx markdown-link-check

# Frontmatter validation
./scripts/validate-frontmatter.sh

# Spell check
npx cspell "**/*.md"
```

### 4. Submission

#### Commit Messages

Follow conventional commits:

```bash
# Format
<type>(<scope>): <description>

# Examples
docs(context-engineering): add RAG patterns section
fix(frontmatter): correct date format in examples
feat(docs): add new MCP integration guide
refactor(structure): reorganize platform guides
```

Types:
- `feat`: New feature or document
- `fix`: Bug fix or correction
- `docs`: Documentation changes
- `style`: Formatting changes
- `refactor`: Restructuring
- `test`: Test additions
- `chore`: Maintenance tasks

#### Pull Request

Create PR with this template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New document
- [ ] Update existing document
- [ ] Bug fix
- [ ] Refactoring
- [ ] Other (describe)

## Checklist
- [ ] Frontmatter follows v1 Core spec
- [ ] Links are valid and relative
- [ ] Markdown lint passes
- [ ] Tags from TAXONOMY.md
- [ ] Summary under 160 chars
- [ ] last_updated is current
- [ ] Tests pass (if applicable)

## Related Issues
Fixes #123
```

## Standards Compliance

### Documentation Standards

All documents must:
- Include v1 Core compliant frontmatter
- Use consistent heading hierarchy
- Provide dual-audience statements
- Include practical examples
- Reference sources properly

### Code Examples

```python
# ✅ Good: Complete, runnable example
def process_document(path):
    """Process a markdown document.

    Args:
        path: Path to the document

    Returns:
        Processed content dictionary
    """
    with open(path) as f:
        content = f.read()

    # Parse frontmatter
    fm, body = parse_frontmatter(content)

    # Validate
    errors = validate_frontmatter(fm)
    if errors:
        raise ValueError(f"Invalid frontmatter: {errors}")

    return {
        'frontmatter': fm,
        'body': body
    }
```

### Writing Style

- **Clear**: Direct, unambiguous language
- **Concise**: No unnecessary words
- **Consistent**: Same terminology throughout
- **Complete**: All necessary information included
- **Correct**: Technically accurate

## Review Process

### Review Criteria

Reviewers check for:

1. **Technical Accuracy**: Information is correct
2. **Completeness**: All sections present
3. **Consistency**: Follows repository patterns
4. **Quality**: Clear, well-written content
5. **Compliance**: Meets all standards

### Review Timeline

- **Initial Review**: Within 48 hours
- **Feedback Response**: Within 7 days
- **Final Decision**: Within 14 days

### Approval Requirements

- 1 maintainer approval for minor changes
- 2 maintainer approvals for major changes
- All CI checks must pass
- No unresolved comments

## Maintenance Tasks

### Monthly Tasks

```bash
# Check for broken links
find docs -name "*.md" -print0 | xargs -0 -n1 npx markdown-link-check

# Update dependencies
npm update

# Review draft documents
rg -l "status: draft" docs
```

### Quarterly Tasks

- Audit tag usage against TAXONOMY.md
- Review and update deprecated documents
- Archive obsolete content
- Update platform-specific guides

### Annual Tasks

- Major version review
- Repository structure evaluation
- Template updates
- Process improvement

## Special Procedures

### Breaking Changes

For changes that break compatibility:

1. Propose in issue first
2. Provide migration guide
3. Use deprecation period
4. Update major version
5. Announce in changelog

### Emergency Fixes

For critical issues:

1. Create hotfix branch
2. Make minimal change
3. Fast-track review
4. Deploy immediately
5. Follow up with full fix

### New Categories

To add new document categories:

1. Propose in issue
2. Update TAXONOMY.md first
3. Create category template
4. Add example document
5. Update navigation

## Governance

### Roles

| Role | Responsibilities | Permissions |
|------|-----------------|-------------|
| **Contributor** | Submit PRs, report issues | Fork, PR |
| **Reviewer** | Review PRs, provide feedback | Comment |
| **Maintainer** | Merge PRs, release versions | Write |
| **Admin** | Repository settings, access | Admin |

### Decision Making

1. **Minor Changes**: Single maintainer
2. **Major Changes**: Maintainer consensus
3. **Breaking Changes**: Full team vote
4. **Architecture**: RFC process

### Conflict Resolution

1. Technical discussion in PR
2. Escalate to maintainers
3. Vote if no consensus
4. Document decision rationale

## Recognition

### Contributors

All contributors are recognized in:
- Git history
- Contributors file
- Release notes
- Annual report

### Contribution Levels

- 🥉 **Bronze**: 1-5 merged PRs
- 🥈 **Silver**: 6-20 merged PRs
- 🥇 **Gold**: 21+ merged PRs
- 🏆 **Core**: Ongoing maintainer

## Getting Help

### Resources

- [Issue Templates](../../.github/ISSUE_TEMPLATE/)
- [Discussions](https://github.com/artificial-intelligence-first/ssot/discussions)
- [Style Guide](./style.md)
- [Taxonomy](./taxonomy.md)

### Communication

- **Questions**: Open a discussion
- **Bugs**: File an issue
- **Ideas**: Start RFC discussion
- **Help**: Tag @maintainers

## License

By contributing, you agree that your contributions will be licensed under the repository's MIT License.

## See Also

- [SSOT.md](../../SSOT.md) - Single Source of Truth principles
- [AGENTS.md](../../AGENTS.md) - AI agent operations
- [Style Guide](./style.md) - Writing standards
- [Taxonomy](./taxonomy.md) - Controlled vocabulary

## References

Contribution guidelines inspired by:
- Open source best practices
- Conventional Commits specification
- GitHub community standards
