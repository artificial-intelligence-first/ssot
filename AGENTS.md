# Agents Catalog

## Primary Directive
- Think in **English** for analysis, planning, and all technical artifacts.
- Interact with the user in **Japanese**, unless the user explicitly requests English.
- When creating any text that will be used in Git or GitHub (branches, commits, PRs, issues, docs, comments), always write in **English**, even if the user spoke in Japanese.
- Use **English** for all code, docs, commits, and GitHub actions.
- Never include rhetorical questions or reflective prompts at the end of responses.
- Do not make the code unnecessarily complex or bloated during implementation.
- Continuously clean up technical debt, outdated logic, and unnecessary descriptions.

## Scope
Complete inventory of autonomous agents operating across this repository.

## Agent List

| ID | Type | Scope | Role |
|----|------|-------|------|
| repo-orchestrator | manager | whole repo | Coordinates cross-cutting concerns and documentation consistency |
| doc-maintainer | specialist | docs/ | Manages SSOT and documentation updates |

## Agent Definitions

### repo-orchestrator

- **Type**: Manager
- **Scope**: Entire repository
- **Mission**: Coordinate multi-agent workflows, resolve conflicts, maintain architectural consistency
- **Inputs**: Task requests, agent capability queries, conflict reports
- **Outputs**: Task assignments, resolution decisions, architecture guidance
- **Tools**: GitHub API, project management systems, static analysis tools
- **Constraints**:
  - Must consult specialists before cross-cutting changes
  - Ensures all documentation follows SSOT principles

### doc-maintainer

- **Type**: Specialist
- **Scope**: `docs/` directory and repository root documentation
- **Mission**: Maintain the Single Source of Truth (SSOT), ensure documentation freshness, and validate structure against templates.
- **Inputs**: Documentation update requests, new feature specs, policy changes
- **Outputs**: Updated `.md` files, validation reports
- **Tools**: Markdown linters, text editors, git
- **Constraints**:
  - Must strictly follow the 11-section structure for all topic documents
  - Must verify no duplication exists against `SSOT.md`
  - Must update `last_updated` field on modifications

## Agent Capability Matrix

| Agent ID | Code Gen | Testing | Deploy | Schema | Review | Scope |
|----------|----------|---------|--------|--------|--------|-------|
| repo-orchestrator | ● | ● | ◐ | ○ | ● | Global |
| doc-maintainer | ○ | ○ | ○ | ● | ● | docs/ |

Legend:
- ● Full capability
- ◐ Partial/assisted capability
- ○ No capability

## Routing Rules

**Documentation Request** → Check scope:
- General architecture or cross-cutting → `repo-orchestrator`
- Specific SSOT topic or maintenance → `doc-maintainer`

## Context
For repository overview and human setup instructions, see [README.md](./README.md).
For architectural context and governance, see [docs/SSOT.md](./docs/SSOT.md).

