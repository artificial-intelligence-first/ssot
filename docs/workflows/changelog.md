---
title: Changelog
slug: changelog
status: stable
last_updated: 2025-11-01
tags: [changelog, versioning, documentation]
summary: "Semantic versioning and changelog format specification following Keep a Changelog principles."
authors: []
sources:
  - { id: R1, title: "Keep a Changelog", url: "https://keepachangelog.com/", accessed: "2025-10-23" }
  - { id: R2, title: "Semantic Versioning", url: "https://semver.org/", accessed: "2025-10-23" }
---

# Changelog

> **For Humans**: This guide defines the format and principles for maintaining changelogs across projects, ensuring clear communication of changes between versions.
>
> **For AI Agents**: Follow this specification when generating changelog entries. Parse existing changelogs according to these patterns. Always maintain reverse chronological order and semantic versioning.

## Overview

A changelog is a file containing a curated, chronologically ordered list of notable changes for each version of a project. This guide defines the standard format based on Keep a Changelog principles.

## Format Specification

### File Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security vulnerability fixes
```

### Version Format

Follow Semantic Versioning (SemVer):
- **MAJOR.MINOR.PATCH** (e.g., 2.1.3)
- **MAJOR**: Breaking API changes
- **MINOR**: Backwards-compatible functionality
- **PATCH**: Backwards-compatible bug fixes

### Change Categories

| Category | Description | Example |
|----------|-------------|---------|
| **Added** | New features | Added user authentication |
| **Changed** | Existing feature changes | Updated error message format |
| **Deprecated** | Features to be removed | Deprecated legacy API endpoint |
| **Removed** | Deleted features | Removed Python 2.7 support |
| **Fixed** | Bug fixes | Fixed memory leak in parser |
| **Security** | Security fixes | Fixed XSS vulnerability |

## Entry Guidelines

### Good Changelog Entries

```markdown
### Added
- User authentication with OAuth 2.0 support
- CSV export functionality for reports
- Batch processing mode with `--batch` flag

### Fixed
- Memory leak in image processing pipeline (#123)
- Incorrect date formatting in logs
- Race condition in concurrent requests
```

### Poor Changelog Entries

```markdown
### Changed
- Updated code  # Too vague
- Misc fixes    # Non-specific
- Changes       # No information
```

## Automation

### Git Integration

```bash
# Generate changelog from commits
git log --pretty=format:"- %s (%h)" v1.0.0..v1.1.0

# Filter by conventional commits
git log --grep="^feat:" --pretty=format:"- %s"
git log --grep="^fix:" --pretty=format:"- %s"
```

### Conventional Commits Mapping

| Commit Type | Changelog Category |
|-------------|-------------------|
| `feat:` | Added |
| `fix:` | Fixed |
| `docs:` | Changed |
| `style:` | Changed |
| `refactor:` | Changed |
| `perf:` | Changed |
| `test:` | (Usually omitted) |
| `chore:` | (Usually omitted) |
| `security:` | Security |
| `deprecate:` | Deprecated |
| `remove:` | Removed |

## Release Process

### Workflow

1. **Development**: Add entries to `[Unreleased]` section
2. **Pre-release**: Review and curate entries
3. **Release**: Move `[Unreleased]` to new version section
4. **Tag**: Create git tag matching version
5. **Publish**: Update links and publish

### Release Checklist

- [ ] All changes documented in Unreleased
- [ ] Entries are clear and user-focused
- [ ] Version number follows SemVer
- [ ] Date is correct (YYYY-MM-DD)
- [ ] Links at bottom are updated
- [ ] Git tag created
- [ ] Release notes published

## Anti-patterns

### Missing Context
❌ **Wrong**: "Fixed bug"
✅ **Right**: "Fixed authentication timeout in OAuth flow"

### Technical Jargon
❌ **Wrong**: "Refactored AbstractFactoryBean singleton"
✅ **Right**: "Improved application startup performance"

### Commit Hash Dumps
❌ **Wrong**: Direct commit log paste
✅ **Right**: Curated, meaningful entries

## Evaluation

### Quality Metrics

- **Completeness**: All notable changes included
- **Clarity**: Entries understandable by users
- **Accuracy**: Versions and dates correct
- **Consistency**: Format uniform throughout
- **Linkability**: All versions have anchors

## Examples

### Library Changelog

```markdown
## [2.0.0] - 2025-11-01

### Added
- TypeScript type definitions
- New `configure()` method for initialization

### Changed
- **BREAKING**: Renamed `init()` to `initialize()`
- Minimum Node.js version raised to 18.0

### Removed
- **BREAKING**: Dropped CommonJS support

### Security
- Updated dependencies to fix CVE-2025-1234
```

### Application Changelog

```markdown
## [1.5.0] - 2025-11-01

### Added
- Dark mode support
- Export to PDF functionality
- Keyboard shortcuts for common actions

### Fixed
- Memory leak when processing large files
- Incorrect timezone handling in reports
- UI freezing during long operations
```

## See Also

- [Semantic Versioning](./semantic-versioning.md)
- [Release Management](./release-management.md)
- [AGENTS.md](../../AGENTS.md)

## References

- [R1] Keep a Changelog. https://keepachangelog.com/ (accessed 2025-10-23)
- [R2] Semantic Versioning. https://semver.org/ (accessed 2025-10-23)
