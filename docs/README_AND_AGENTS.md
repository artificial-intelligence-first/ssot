---
title: AGENTS.md and README.md for AI-First Repositories
slug: agents-readme
summary: "Agents & README Guide"
type: guide
tags: [topic, ai-first, documentation, agents, readme, repository-structure]
last_updated: 2024-11-19
---

# AGENTS.md and README.md for AI-First Repositories

## Agent Contract

- **PURPOSE**:
  - Provide a comprehensive specification for using README.md and AGENTS.md files in AI-first repository architectures
  - Establish clear patterns for documentation placement, content structure, and the relationship between human-facing and AI-facing documentation
  - Define worldview boundaries and navigation patterns for hierarchical documentation
- **USE_WHEN**:
  - Setting up new repositories with AI agent collaboration
  - Refactoring existing repositories for AI-first workflows
  - Establishing documentation standards across multi-agent systems
  - Creating monorepos with multiple autonomous subsystems
- **DO_NOT_USE_WHEN**:
  - Building single-file scripts or tools without agent collaboration
  - Creating implementation-detail directories (src/*, lib/*, utils/*)
  - Working on repositories where AI agents are not collaborators
- **PRIORITY**:
  - README.md at repository root is MANDATORY for human orientation
  - AGENTS.md at repository root is MANDATORY for AI agent catalog
  - Subdirectory documentation ONLY at worldview boundaries (apps/*, packages/*, services/*)
  - NEVER create documentation in implementation-detail directories
- **RELATED_TOPICS**:
  - agent-skill
  - code-mcp
  - repository-structure
  - multi-agent-architecture
  - documentation-as-code

## TL;DR

- **WHAT**: A dual-documentation pattern separating human-facing (README.md) and AI-facing (AGENTS.md) concerns across repository hierarchies, with clear worldview boundaries determining where documentation should exist
- **WHY**: Humans need context/setup while AI agents need operational specifications; separation of concerns prevents information overload, enables scalability, and reduces documentation drift
- **WHEN**: Use at repository initialization, when adding new subsystems/services, introducing AI agents to existing projects, or refactoring monorepo structures
- **HOW**: Create root-level README.md (orientation) and AGENTS.md (agent catalog) with bidirectional links; add subdirectory versions ONLY at architectural boundaries (apps/*, packages/*, services/*); maintain parent (map) vs. child (guidebook) relationship
- **WATCH_OUT**: Avoid over-documentation in low-level directories, duplicating content between README and AGENTS, missing navigation links, or using abstract templates without concrete examples

## Canonical Definitions

### README.md
**Definition**: The authoritative human-facing instruction manual for a repository or subsystem, providing orientation, setup instructions, and navigation to deeper documentation.

**Scope**:
- Repository/module purpose and value proposition
- Technical stack and prerequisites
- Installation and quick start procedures
- High-level directory structure explanation
- Links to specialized documentation (AGENTS.md, SSOT.md, PLANS.md)

**NOT in Scope**:
- Detailed API specifications (belongs in dedicated docs)
- Agent-specific operational instructions (belongs in AGENTS.md)
- Low-level implementation details (belongs in code comments)

**Authoritative Source**: [GitHub README Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

### AGENTS.md
**Definition**: A machine-readable catalog defining all autonomous agents operating within a repository boundary, specifying their capabilities, constraints, and operational parameters.

**Scope**:
- Complete agent inventory with unique identifiers
- Per-agent specifications (role, mission, inputs/outputs, tools, constraints)
- Build, test, and deployment commands agents should execute
- Code style guidelines and conventions
- Security considerations and boundaries

**NOT in Scope**:
- Human onboarding procedures (belongs in README.md)
- General repository philosophy (belongs in README.md)
- Narrative explanations of "why" (agents need "what" and "how")

**Authoritative Source**: [AGENTS.md Specification](https://agents.md)

### Worldview Boundary
**Definition**: An architectural division point where a subsystem has sufficiently distinct purpose, dependencies, or operational context to warrant independent documentation.

**Examples**:
- Separate applications in a monorepo (`apps/frontend`, `apps/api`)
- Independent packages (`packages/ui-kit`, `packages/auth`)
- Domain-specific service boundaries (`services/billing`, `services/notifications`)

**Counter-examples** (NOT boundaries):
- Utility folders (`src/utils`, `src/helpers`)
- Shared libraries (`src/lib`, `src/common`)
- Component organization (`src/components/buttons`)

### AI-First Repository
**Definition**: A repository architecture designed with AI agents as first-class collaborators, where documentation, structure, and conventions optimize for both human and machine interpretation.

**Characteristics**:
- Predictable documentation locations
- Machine-parseable specifications (AGENTS.md, structured frontmatter)
- Clear agent role definitions and boundaries
- Executable instructions over narrative prose

## Core Patterns

### Pattern: Root Documentation Pair

**Intent**: Establish a single, predictable entry point for both human and AI consumers at the repository root.

**Context**:
- New repository setup
- Repository refactoring
- Onboarding new team members or agents

**Implementation**:

```
/
├── README.md          # Human entry point
├── AGENTS.md          # AI entry point
├── apps/
├── packages/
└── docs/
```

**Root README.md Template**:

```markdown
# <Project Name>

## Overview
- What this repository does
- Who it serves / What problems it solves

## Tech Stack
- Runtime, package manager, languages, infrastructure

## Quick Start
```bash
# Prerequisites
npm install -g pnpm

# Setup
pnpm install

# Common commands
pnpm dev      # Start development
pnpm test     # Run tests
pnpm lint     # Check code quality
```

## Repository Layout
- `apps/` - Deployable applications
- `packages/` - Shared libraries and components
- `catalog/` - Agent definitions and templates
- `docs/` - Extended documentation

## Documentation
- [AGENTS.md](./AGENTS.md) - Agent catalog and specifications
- [SSOT.md](./docs/SSOT.md) - Single source of truth topics
- [PLANS.md](./docs/PLANS.md) - Project roadmap and planning

## License
MIT
```

**⏺ AGENTS.md Basic Structure**

After reviewing the README_AND_AGENTS.md document, the basic structure of AGENTS.md is as follows:

**📄 AGENTS.md Standard Structure**

**1. Primary Directive Section**

```markdown
## Primary Directive
Repository wide behavior rules for all autonomous agents in this repository.
```

- Defines common behaviors and policies for all autonomous agents operating in this repository
- Describes invariant conditions regarding language, interaction, safety, style, and quality

**2. Scope Section**

```markdown
## Scope
Complete inventory of autonomous agents operating across this repository.
```

- Describes the complete inventory of all autonomous agents operating in this repository

**3. Agent List Section**

```markdown
## Agent List

| ID | Type | Scope | Role |
|----|------|-------|------|
| repo-orchestrator | manager | whole repo | Coordinates cross-cutting concerns |
| supabase-agent | specialist | database | Schema migration and query optimization |
| frontend-builder | specialist | apps/web | UI component development |
```

- Lists agents in a concise table format
- Clearly states ID, type, scope, and role

**4. Agent Definitions Section**

Detailed definition including the following elements for each agent:

```markdown
### [agent-id]

- **Type**: Manager/Specialist etc.
- **Scope**: Operational scope of the agent
- **Mission**: Specific, measurable mission
- **Inputs**: Concrete input specifications (environment variables, configs, requests, etc.)
- **Outputs**: Concrete output specifications (files, metrics, deliverables, etc.)
- **Tools**: Tools to use (including versions)
- **Constraints**: "Must" and "must not" rules
```

**5. Agent Capability Matrix (Optional)**

Recommended capability matrix when there are 5+ agents:

```markdown
## Agent Capability Matrix

| Agent ID | Code Gen | Testing | Deploy | Schema | Review | Scope |
|----------|----------|---------|--------|--------|--------|-------|
| repo-orchestrator | ● | ● | ◐ | ○ | ● | Global |

Legend:
- ● Full capability
- ◐ Partial/assisted capability
- ○ No capability
```

**6. Routing Rules Section**

Decision rules for which agent to assign tasks to:

```markdown
## Routing Rules

**Code Generation Request** → Check scope:
- Frontend (apps/web/*) → `frontend-builder`
- API (apps/api/*) → `api-developer`
- Cross-cutting → `repo-orchestrator`
```

**7. Context Section**

Navigation links to other documentation:

```markdown
## Context
For repository overview and human setup instructions, see [README.md](./README.md).
For architectural context, see [SSOT.md](./docs/SSOT.md).
```

**🔑 Key Points**

1. **Specificity**: Avoid abstract expressions, use concrete and measurable definitions
2. **Completeness**: Include all required fields (ID, Type, Scope, Mission, Inputs, Outputs, Tools, Constraints)
3. **Navigation**: Bidirectional links to README.md and other related documentation
4. **Hierarchical Structure**: Subdirectory AGENTS.md only lists agents specific to that module

**📍 Placement Rules**

- **Root Level**: Repository-wide agent catalog
- **Subdirectories**: Create only at worldview boundaries (apps/*, packages/*, services/*)
- **Implementation Directories**: Do not create in src/*, lib/*, utils/*

**Root AGENTS.md Template**:

```markdown
# Agents Catalog

## Primary Directive
Repository wide behavior rules for all autonomous agents in this repository.

## Scope
Complete inventory of autonomous agents operating across this repository.

## Agent List

| ID | Type | Scope | Role |
|----|------|-------|------|
| repo-orchestrator | manager | whole repo | Coordinates cross-cutting concerns |
| supabase-agent | specialist | database | Schema migration and query optimization |
| frontend-builder | specialist | apps/web | UI component development |

## Agent Definitions

### repo-orchestrator

- **Type**: Manager
- **Scope**: Entire repository
- **Mission**: Coordinate multi-agent workflows, resolve conflicts, maintain architectural consistency
- **Inputs**: Task requests, agent capability queries, conflict reports
- **Outputs**: Task assignments, resolution decisions, architecture guidance
- **Tools**: GitHub API, project management systems, static analysis tools
- **Constraints**:
  - Cannot modify database schemas directly
  - Must consult specialists before cross-cutting changes
  - Requires approval for dependency updates

### supabase-agent

- **Type**: Specialist
- **Scope**: Database and backend services
- **Mission**: Manage database schema evolution, optimize queries, ensure data integrity
- **Inputs**: Schema change requests, performance reports, migration scripts
- **Outputs**: Migration files, query optimizations, schema documentation
- **Tools**: Supabase CLI, SQL analyzers, migration generators
- **Constraints**:
  - All schema changes require migration files
  - Must maintain backward compatibility for 2 versions
  - Production changes require peer review
```

**Trade-offs**:
- ✅ Single source of truth for entry points
- ✅ Clear separation of human vs. AI concerns
- ✅ Predictable location for documentation discovery
- ⚠️ Requires discipline to keep README concise
- ⚠️ AGENTS.md can become large in complex systems (use subdirectory versions)

### Pattern: Subdirectory Documentation Inheritance

**Intent**: Provide localized context at architectural boundaries while maintaining navigation to parent-level documentation.

**Context**:
- Monorepos with multiple applications
- Multi-service architectures
- Packages with independent lifecycles

**Implementation**:

```
/
├── README.md              # "Repository map"
├── AGENTS.md              # "Full agent roster"
├── apps/
│   ├── web/
│   │   ├── README.md      # "Web app guidebook"
│   │   ├── AGENTS.md      # "Web app agents only"
│   │   └── src/           # ← NO README/AGENTS here
│   │       ├── components/ # ← NO README/AGENTS here
│   │       └── lib/        # ← NO README/AGENTS here
│   └── api/
│       ├── README.md
│       └── AGENTS.md
└── packages/
    └── ui-kit/
        ├── README.md
        └── AGENTS.md
```

**Subdirectory README.md Template**:

```markdown
# <Module Name>

## Role
This module's responsibility within the larger system.

## Entry Points
- `src/index.ts` - Public API exports
- `src/main.ts` - Application entry for standalone execution

## Local Layout
```
src/
├── components/  # Reusable UI components
├── services/    # Business logic layer
├── utils/       # Helper functions
└── types/       # TypeScript definitions
```

## Development
```bash
# From repository root
pnpm --filter @repo/web dev

# Run tests
pnpm --filter @repo/web test
```

## Parent Documentation
See [root README](../../README.md) for overall repository setup.
```

**Subdirectory AGENTS.md Template**:

```markdown
# Agents in <Module Name>

## Scope
Agents operating exclusively within this module.

## Local Agents

### web-component-builder

- **Type**: Specialist
- **Scope**: apps/web/src/components
- **Mission**: Create, refactor, and optimize React components following design system
- **Inputs**: Design specs, accessibility requirements, performance budgets
- **Outputs**: Component implementations, Storybook stories, unit tests
- **Tools**: React, TypeScript, Storybook, Jest, Testing Library
- **Constraints**:
  - Must follow design tokens from @repo/ui-kit
  - All components require accessibility tests
  - Performance budget: < 10KB gzipped per component

## Inherited Agents
Agents from parent scope (see [/AGENTS.md](../../AGENTS.md)):
- `repo-orchestrator` - Available for cross-cutting coordination
- `ci-validator` - Runs on all commits
```

**Decision Rules**:

```yaml
Create subdirectory README.md when:
  - Subsystem has independent deployment lifecycle: YES
  - Different tech stack from parent: YES
  - Separate team ownership: YES
  - Distinct user-facing purpose: YES

Create subdirectory AGENTS.md when:
  - Module has agents not relevant to other modules: YES
  - Agent constraints differ significantly from parent: YES
  - Module is > 10k LOC with complex logic: CONSIDER

Do NOT create in:
  - Implementation detail folders (src/utils, src/lib): NEVER
  - Single-purpose subdirectories (src/components/Button): NEVER
  - Test directories (tests/, __tests__): NEVER
```

**Trade-offs**:
- ✅ Localized documentation reduces noise for subsystem work
- ✅ Clear ownership boundaries for agent responsibilities
- ✅ Easier to maintain subsystem-specific conventions
- ⚠️ Risk of duplication if not carefully scoped
- ⚠️ Requires navigation links to prevent documentation silos
- ⚠️ Can proliferate if "worldview boundary" criteria unclear

### Pattern: README ↔ AGENTS Navigation Chain

**Intent**: Ensure humans and AI can seamlessly traverse between orientation (README) and operational specifications (AGENTS) at every documentation level.

**Context**: All documentation pairs (root and subdirectories)

**Implementation**:

In README.md:
```markdown
## Documentation
- [AGENTS.md](./AGENTS.md) - Agent specifications and operational instructions
- [Architecture Decision Records](./docs/adr/) - Key technical decisions
```

In AGENTS.md:
```markdown
## Context
For repository overview and human setup instructions, see [README.md](./README.md).

For architectural context, see [SSOT.md](./docs/SSOT.md).
```

**Visual Representation**:

```
Human enters → README.md
                 ↓
         Needs agent info?
                 ↓
             AGENTS.md → Links to subdirectory agents
                 ↓
         Needs context?
                 ↓
         Back to README.md

AI enters → AGENTS.md
               ↓
       Needs setup context?
               ↓
          README.md → Links to installation/stack
               ↓
       Ready to execute
               ↓
       Returns to AGENTS.md
```

**Trade-offs**:
- ✅ Prevents documentation dead-ends
- ✅ Supports both human and AI navigation patterns
- ✅ Makes relationships explicit
- ⚠️ Requires maintenance when documentation moves
- ⚠️ Can create circular reference confusion if not clearly labeled

### Pattern: Agent Capability Matrix

**Intent**: Provide a quick-reference grid of agent capabilities across different repository scopes for routing decisions.

**Context**: Repositories with 5+ agents or multi-agent orchestration needs

**Implementation**:

In root AGENTS.md:

```markdown
## Agent Capability Matrix

| Agent ID | Code Gen | Testing | Deploy | Schema | Review | Scope |
|----------|----------|---------|--------|--------|--------|-------|
| repo-orchestrator | ● | ● | ◐ | ○ | ● | Global |
| frontend-builder | ● | ● | ○ | ○ | ◐ | apps/web |
| api-developer | ● | ● | ○ | ◐ | ◐ | apps/api |
| db-specialist | ○ | ◐ | ○ | ● | ● | database |
| ci-validator | ○ | ● | ● | ○ | ● | CI/CD |

Legend:
- ● Full capability
- ◐ Partial/assisted capability
- ○ No capability

## Routing Rules

**Code Generation Request** → Check scope:
- Frontend (apps/web/*) → `frontend-builder`
- API (apps/api/*) → `api-developer`
- Cross-cutting → `repo-orchestrator`

**Schema Change** → Always route to `db-specialist`

**Deployment** → `ci-validator` for validation + `repo-orchestrator` for execution
```

**Trade-offs**:
- ✅ Fast decision-making for agent selection
- ✅ Visual clarity of capability coverage
- ✅ Identifies gaps or overlaps
- ⚠️ Requires updates when agents evolve
- ⚠️ Can oversimplify nuanced capabilities

## Decision Checklist

### Before Creating README.md

- [ ] **Worldview Boundary**: Does this directory represent a distinct subsystem with independent purpose?
- [ ] **Independent Lifecycle**: Can this module be developed, tested, or deployed separately?
- [ ] **New Human Contributor**: Would a new developer need context specific to this directory?
- [ ] **Different Tech Stack**: Does this use technologies not covered by parent README?
- [ ] **Parent Linkage**: Have I included links back to parent README for shared context?

**If 2+ checks fail**, consider whether directory-level README adds value or creates maintenance burden.

### Before Creating AGENTS.md

- [ ] **Unique Agents**: Are there agents specific to this subsystem not relevant elsewhere?
- [ ] **Operational Complexity**: Does this module require agent-specific build/test/deploy procedures?
- [ ] **Scope Constraints**: Do agents here have constraints that differ from parent scope?
- [ ] **Size Threshold**: Is this module > 10k LOC or > 20 files?
- [ ] **Capability Matrix**: Have I defined clear capability boundaries vs. parent agents?

**If fewer than 3 checks pass**, consider listing agents in parent AGENTS.md instead.

### Content Quality Checks

README.md:
- [ ] Overview answers "what" and "why" in < 3 sentences
- [ ] Quick start commands are copy-paste executable
- [ ] Directory layout explains top-level folders (not deep nesting)
- [ ] Links to AGENTS.md and other specialized docs present
- [ ] Tech stack lists versions where relevant (Node 18+, pnpm 8.x)

AGENTS.md:
- [ ] Every agent has unique ID following naming convention
- [ ] Mission statements are specific and measurable
- [ ] Input/output specifications are concrete (not abstract)
- [ ] Tools list is exhaustive (including CLI tools, APIs, services)
- [ ] Constraints include both "must" and "must not" rules
- [ ] Links back to README for context

### Anti-Documentation Locations

**NEVER create README.md or AGENTS.md in**:
- [ ] `src/` (implementation root)
- [ ] `src/utils/`, `src/lib/`, `src/helpers/` (utility folders)
- [ ] `src/components/common/`, `src/components/shared/` (component organization)
- [ ] `tests/`, `__tests__/`, `spec/` (test directories)
- [ ] `dist/`, `build/`, `out/` (build artifacts)
- [ ] `node_modules/`, `.git/` (system directories)

**Rationale**: These are implementation details, not architectural boundaries. Documentation here creates maintenance debt without value.

## Anti-patterns / Pitfalls

### Anti-pattern: Documentation Duplication

**Symptom**: Same content appears in both README.md and AGENTS.md, or in parent and child documents.

**Why It Happens**: Unclear boundaries between human-facing and AI-facing concerns, or fear of missing information.

**Impact**:
- Documentation skew (one copy updated, others stale)
- Maintenance burden (changes require multiple edits)
- Confusion about authoritative source

**Solution**:

```markdown
# ❌ BAD: Duplication in README.md
## Tech Stack
- Node.js 18+
- pnpm 8.x
- TypeScript 5.3

## Build Commands
pnpm build
pnpm test

---

# ❌ BAD: Same content duplicated in AGENTS.md
## Development Environment
- Node.js 18+
- pnpm 8.x
- TypeScript 5.3

## Build Instructions
pnpm build
pnpm test

---

# ✅ GOOD: Clear separation

## README.md
## Tech Stack
- Node.js 18+
- pnpm 8.x
- TypeScript 5.3

See [AGENTS.md](./AGENTS.md) for build procedures.

## AGENTS.md
## Build Commands
```bash
pnpm install          # Install dependencies
pnpm build           # Production build
pnpm test            # Run test suite
pnpm lint --fix      # Auto-fix linting issues
```

For tech stack details, see [README.md](./README.md#tech-stack).
```

**Prevention**:
- Define ownership: README = context, AGENTS = operations
- Use cross-references instead of copying
- Regular audits for duplication

### Anti-pattern: Over-Specification in Low-Level Directories

**Symptom**: README.md and AGENTS.md files appear in `src/components/Button/`, `src/utils/formatters/`, etc.

**Why It Happens**: Zealous application of "document everything" principle without considering boundaries.

**Impact**:
- Documentation overwhelms actual code
- Impossible to maintain as code evolves
- Noise reduces value of legitimate documentation

**Example**:

```
# ❌ BAD: Excessive documentation
src/
├── components/
│   ├── Button/
│   │   ├── README.md          # ← Overkill
│   │   ├── Button.tsx
│   │   └── Button.test.tsx
│   ├── Input/
│   │   ├── README.md          # ← Overkill
│   │   ├── Input.tsx
│   │   └── Input.test.tsx
│   └── README.md              # ← Maybe useful
└── utils/
    ├── formatters/
    │   ├── README.md          # ← Overkill
    │   └── currency.ts
    └── README.md              # ← Overkill

# ✅ GOOD: Documentation at boundaries only
apps/
└── web/
    ├── README.md              # ← App-level context
    ├── AGENTS.md              # ← App-level agents
    └── src/
        ├── components/        # ← No docs (code is self-documenting)
        │   ├── Button.tsx
        │   └── Input.tsx
        └── utils/             # ← No docs (use JSDoc in code)
            └── currency.ts
```

**Solution**: Apply the "worldview boundary" test strictly. If a directory is purely organizational (not architectural), skip documentation.

### Anti-pattern: Abstract Agent Definitions

**Symptom**: Agent specifications use vague language like "handles data processing" or "manages frontend tasks."

**Why It Happens**: Template-driven approach without concrete use case analysis.

**Impact**:
- AI agents cannot determine if they're the right choice for a task
- Overlapping responsibilities cause conflicts
- Humans cannot predict agent behavior

**Example**:

```markdown
# ❌ BAD: Vague specification
### data-processor
- **Mission**: Process data efficiently
- **Inputs**: Various data types
- **Outputs**: Processed results
- **Tools**: Standard tools

# ✅ GOOD: Concrete specification
### clickhouse-etl-agent
- **Mission**: Extract data from PostgreSQL source tables, transform according to analytics schema v2, load into ClickHouse warehouse tables with deduplication
- **Inputs**:
  - PostgreSQL connection string (env: `SOURCE_DB_URL`)
  - Table whitelist (config: `etl.tables[]`)
  - Incremental sync cursor (last processed timestamp)
- **Outputs**:
  - ClickHouse materialized views
  - ETL run metadata (rows processed, errors, duration)
  - Prometheus metrics (etl_rows_total, etl_errors_total)
- **Tools**:
  - `dbt` 1.6+ for transformations
  - `airbyte` for extraction
  - `clickhouse-client` for loading
  - `sentry` for error tracking
- **Constraints**:
  - Must run during off-peak hours (00:00-04:00 UTC)
  - Maximum 10k rows per batch to prevent memory issues
  - Must preserve source data for 7 days before deletion
  - Requires read-replica access (not production primary)
```

**Prevention**:
- Use real task examples when defining agents
- Specify exact tools with versions
- Define measurable constraints
- Include error scenarios

### Anti-pattern: Missing Navigation Links

**Symptom**: README.md and AGENTS.md exist but don't reference each other or parent/child documents.

**Why It Happens**: Documents created independently without considering navigation flow.

**Impact**:
- Dead-ends force users to manually browse file structure
- AI agents cannot discover related context
- Documentation feels fragmented

**Solution**:

```markdown
# ❌ BAD: Isolated documents

## /README.md
# Project Name
Overview and setup...
(no links to AGENTS.md or subdirectories)

## /AGENTS.md
# Agents
Agent definitions...
(no links to README.md or where agents are used)

## /apps/web/README.md
# Web App
App-specific details...
(no links to root README or AGENTS)

---

# ✅ GOOD: Connected documentation

## /README.md
# Project Name
Overview and setup...

## Documentation
- [AGENTS.md](./AGENTS.md) - AI agent catalog
- [apps/web/README.md](./apps/web/README.md) - Web application
- [apps/api/README.md](./apps/api/README.md) - API service

## /AGENTS.md
# Agents

> For repository overview and setup, see [README.md](./README.md)

## Subsystem Agents
- Web app agents: [apps/web/AGENTS.md](./apps/web/AGENTS.md)
- API agents: [apps/api/AGENTS.md](./apps/api/AGENTS.md)

## /apps/web/README.md
# Web Application

> Part of the larger monorepo. See [root README](../../README.md) for overall setup.

Agents for this app: [AGENTS.md](./AGENTS.md)

## /apps/web/AGENTS.md
# Web App Agents

> For general context, see [README.md](./README.md)
> For repository-wide agents, see [root AGENTS.md](../../AGENTS.md)
```

**Prevention**:
- Include navigation sections in documentation templates
- Validate links in CI/CD
- Regular documentation reviews for connectivity

## Evaluation

### Metrics

#### Documentation Coverage Ratio
**Why It Matters**: Ensures worldview boundaries are documented without over-documentation.

**Target**:
- 100% of worldview boundaries have README.md
- 80%+ of boundaries with agents have AGENTS.md
- 0% of implementation directories have documentation

**Measurement**:
```bash
# Count worldview boundaries (apps/*, packages/*, services/*)
boundaries=$(find . -type d \( -path "*/apps/*" -o -path "*/packages/*" -o -path "*/services/*" \) -maxdepth 2 | wc -l)

# Count README.md at boundaries
readmes=$(find . -type d \( -path "*/apps/*" -o -path "*/packages/*" -o -path "*/services/*" \) -maxdepth 2 -exec test -f "{}/README.md" \; -print | wc -l)

# Calculate ratio
coverage=$((readmes * 100 / boundaries))
echo "README coverage: ${coverage}%"
```

**Tools**: Custom script, CI/CD validation

#### Navigation Depth Score
**Why It Matters**: Measures how many clicks/links needed to reach relevant documentation from entry point.

**Target**:
- Root to any subsystem doc: ≤ 2 links
- Any doc back to root: ≤ 2 links

**Measurement**: Manual audit or documentation graph analysis

**Failure Indicators**:
- Orphaned documents (no inbound links)
- Dead-end documents (no outbound links)
- Circular references without escape

#### Agent Specification Completeness
**Why It Matters**: Incomplete agent specs lead to ambiguity and conflicts.

**Target**: 100% of agents have all required fields:
- ID
- Type
- Scope
- Mission
- Inputs
- Outputs
- Tools
- Constraints

**Measurement**:
```bash
# Parse AGENTS.md files and validate structure
python scripts/validate-agents.py --check-required-fields
```

**Failure Indicators**:
- Missing constraint definitions
- Vague mission statements
- Unspecified tool versions

#### Documentation Freshness
**Why It Matters**: Stale documentation is worse than no documentation.

**Target**:
- README.md updated within 30 days of major dependency changes
- AGENTS.md updated within 7 days of agent capability changes

**Measurement**:
```bash
# Compare last git commit touching README vs. package.json
readme_date=$(git log -1 --format=%ct README.md)
deps_date=$(git log -1 --format=%ct package.json)
days_delta=$(( (deps_date - readme_date) / 86400 ))

if [ $days_delta -gt 30 ]; then
  echo "WARNING: README outdated by $days_delta days"
fi
```

**Tools**: Git hooks, scheduled CI checks

### Test Strategies

#### Human Comprehension Test
**Scenario**: New developer joins team without prior context.

**Test Protocol**:
1. Provide only repository URL
2. Time how long to:
   - Understand repository purpose (target: < 5 minutes)
   - Complete local setup (target: < 15 minutes)
   - Identify which agent handles specific task (target: < 3 minutes)

**Success Criteria**:
- All targets met without external help
- < 2 navigation errors (wrong document followed)

#### AI Agent Self-Service Test
**Scenario**: New AI agent onboards to repository.

**Test Protocol**:
1. Agent reads only README.md and AGENTS.md (no code access)
2. Agent attempts to:
   - Describe repository architecture
   - Identify appropriate agent for given task types (5 scenarios)
   - Generate valid build/test commands

**Success Criteria**:
- 100% accuracy on architecture description
- 80%+ accuracy on agent selection
- 100% accuracy on build commands (must execute successfully)

#### Documentation Drift Detection
**Scenario**: Code changes occur without documentation updates.

**Test Protocol**:
1. Make significant change (add dependency, change build tool, modify agent capability)
2. Submit PR without updating docs
3. CI should flag inconsistency

**Success Criteria**:
- CI blocks merge when:
  - package.json changes without README tech stack update
  - New scripts added without AGENTS.md build commands update
  - New agent code added without AGENTS.md catalog entry

**Implementation**:
```yaml
# .github/workflows/docs-check.yml
name: Documentation Consistency

on: [pull_request]

jobs:
  check-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check package.json vs README
        run: |
          if git diff main --name-only | grep -q "package.json"; then
            if ! git diff main --name-only | grep -q "README.md"; then
              echo "ERROR: package.json changed without README.md update"
              exit 1
            fi
          fi

      - name: Validate AGENTS.md structure
        run: python scripts/validate-agents.py --strict
```

### Success Criteria

**Tier 1 (Essential)**:
- ✅ Root README.md and AGENTS.md exist
- ✅ Both link to each other
- ✅ All worldview boundaries have README.md
- ✅ All agents in AGENTS.md have complete specifications
- ✅ Zero documentation in implementation directories

**Tier 2 (Optimal)**:
- ✅ Navigation depth ≤ 2 links to any document
- ✅ Agent capability matrix present
- ✅ Documentation freshness < 30 days
- ✅ CI validates documentation consistency
- ✅ Templates exist for README and AGENTS at each level

**Tier 3 (Exemplary)**:
- ✅ AI agent self-service test passes at 90%+
- ✅ Human comprehension test passes within targets
- ✅ Documentation coverage metrics published in README
- ✅ Automated changelog generation from commits
- ✅ Documentation versioning for major releases

## Practical Examples

### CI/CD Automation

#### Automated Validation and Generation

**Intent**: Maintain documentation quality and consistency through automated CI/CD pipelines that validate structure, generate boilerplate, and ensure synchronization between README.md and AGENTS.md.

**Implementation**:

```yaml
# .github/workflows/validate-docs.yml
name: Validate Documentation

on:
  push:
    paths:
      - '**/*.md'
      - '**/AGENTS.md'
      - '**/README.md'
  pull_request:
    paths:
      - '**/*.md'

jobs:
  validate-structure:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install validation tools
        run: |
          npm install -g @ssot/doc-validator
          pip install pyyaml jsonschema

      - name: Validate frontmatter
        run: |
          find . -name "*.md" -type f | while read file; do
            python scripts/validate-frontmatter.py "$file"
          done

      - name: Check README/AGENTS pairs
        run: |
          # Find all worldview boundaries
          for dir in $(find . -type d \( -path "*/apps/*" -o -path "*/packages/*" -o -path "*/services/*" \) -maxdepth 2); do
            if [ -f "$dir/README.md" ] && [ ! -f "$dir/AGENTS.md" ]; then
              echo "Warning: $dir has README.md but missing AGENTS.md"
            fi
            if [ -f "$dir/AGENTS.md" ] && [ ! -f "$dir/README.md" ]; then
              echo "Error: $dir has AGENTS.md but missing README.md"
              exit 1
            fi
          done

      - name: Validate cross-references
        run: |
          python scripts/validate-links.py --check-bidirectional

      - name: Check agent specifications
        run: |
          for agents_file in $(find . -name "AGENTS.md" -type f); do
            python scripts/validate-agents.py "$agents_file" \
              --check-mission \
              --check-triggers \
              --check-tools \
              --check-constraints
          done

  generate-documentation:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Generate AGENTS.md from code annotations
        run: |
          python scripts/generate-agents-from-code.py \
            --source-dirs "src,lib,apps" \
            --output-file "AGENTS.generated.md"

      - name: Generate capability matrix
        run: |
          python scripts/generate-capability-matrix.py \
            --input-pattern "**/AGENTS.md" \
            --output-file "CAPABILITY_MATRIX.md"

      - name: Update documentation index
        run: |
          python scripts/update-doc-index.py \
            --root-readme "README.md" \
            --discover-pattern "**/*.md"

      - name: Commit generated documentation
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git diff --staged --quiet || git commit -m "chore: auto-generate documentation [skip ci]"
          git push
```

```python
# scripts/validate-agents.py
import yaml
import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Any

class AgentValidator:
    """Validates AGENTS.md files for completeness and correctness"""

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.content = self.filepath.read_text()
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_structure(self) -> bool:
        """Check for required sections"""
        required_sections = [
            r'^#\s+Primary Directive',
            r'^##\s+Agent Catalog',
            r'^##\s+Coordination',
        ]

        for pattern in required_sections:
            if not re.search(pattern, self.content, re.MULTILINE):
                self.errors.append(f"Missing required section: {pattern}")

        return len(self.errors) == 0

    def validate_agent_specs(self) -> bool:
        """Validate individual agent specifications"""
        agent_pattern = r'###\s+([a-z0-9-]+)\n(.*?)(?=\n###|\n##|\Z)'
        agents = re.findall(agent_pattern, self.content, re.DOTALL)

        for agent_name, agent_content in agents:
            # Check for required fields
            if '**Mission**:' not in agent_content:
                self.errors.append(f"Agent '{agent_name}' missing Mission")

            if '**Triggers**:' not in agent_content and '**Command**:' not in agent_content:
                self.warnings.append(f"Agent '{agent_name}' has no triggers or command")

            if '**Tools**:' not in agent_content:
                self.errors.append(f"Agent '{agent_name}' missing Tools specification")

            # Validate tool references exist
            tools_match = re.search(r'\*\*Tools\*\*:\s*(.+?)(?=\n\*\*|\n###|\Z)',
                                   agent_content, re.DOTALL)
            if tools_match:
                tools = tools_match.group(1).strip()
                if tools == 'None' or tools == 'N/A':
                    self.warnings.append(f"Agent '{agent_name}' has no tools - consider if needed")

        return len(self.errors) == 0

    def validate_cross_references(self) -> bool:
        """Check that links to README.md exist and are valid"""
        readme_path = self.filepath.parent / 'README.md'

        if not readme_path.exists():
            self.errors.append(f"README.md not found at {readme_path}")
            return False

        # Check for bidirectional linking
        readme_content = readme_path.read_text()
        agents_filename = self.filepath.name

        if agents_filename not in readme_content:
            self.warnings.append("README.md doesn't reference this AGENTS.md file")

        if 'README.md' not in self.content:
            self.warnings.append("AGENTS.md doesn't reference README.md")

        return True

    def generate_report(self) -> Dict[str, Any]:
        """Generate validation report"""
        return {
            'file': str(self.filepath),
            'valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'stats': {
                'agent_count': len(re.findall(r'^###\s+[a-z0-9-]+',
                                             self.content, re.MULTILINE)),
                'has_primary_directive': bool(re.search(r'^#\s+Primary Directive',
                                                       self.content, re.MULTILINE)),
                'has_coordination': bool(re.search(r'^##\s+Coordination',
                                                  self.content, re.MULTILINE))
            }
        }

# CLI usage
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Validate AGENTS.md files')
    parser.add_argument('filepath', help='Path to AGENTS.md file')
    parser.add_argument('--check-mission', action='store_true')
    parser.add_argument('--check-triggers', action='store_true')
    parser.add_argument('--check-tools', action='store_true')
    parser.add_argument('--check-constraints', action='store_true')
    parser.add_argument('--json', action='store_true',
                       help='Output as JSON')

    args = parser.parse_args()

    validator = AgentValidator(args.filepath)
    validator.validate_structure()
    validator.validate_agent_specs()
    validator.validate_cross_references()

    report = validator.generate_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        if report['errors']:
            print(f"❌ Errors found in {args.filepath}:")
            for error in report['errors']:
                print(f"  - {error}")
            sys.exit(1)

        if report['warnings']:
            print(f"⚠️  Warnings for {args.filepath}:")
            for warning in report['warnings']:
                print(f"  - {warning}")

        print(f"✅ {args.filepath} is valid")
        print(f"   Found {report['stats']['agent_count']} agents")
```

```python
# scripts/generate-agents-from-code.py
"""
Generates AGENTS.md documentation from code annotations
Looks for special comments like:
  # @agent: agent-name
  # @mission: What this code does
  # @tools: tool1, tool2
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Set

class AgentExtractor:
    def __init__(self):
        self.agents: Dict[str, Dict] = {}

    def extract_from_file(self, filepath: Path):
        """Extract agent annotations from Python/TypeScript files"""
        content = filepath.read_text()

        # Python annotations
        if filepath.suffix == '.py':
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    docstring = ast.get_docstring(node)
                    if docstring and '@agent:' in docstring:
                        self._parse_agent_annotation(docstring, filepath, node.name)

        # TypeScript/JavaScript annotations
        elif filepath.suffix in ['.ts', '.js', '.tsx', '.jsx']:
            pattern = r'/\*\*[\s\S]*?@agent:\s*([a-z0-9-]+)[\s\S]*?\*/'
            matches = re.findall(pattern, content)
            for match in matches:
                # Extract full comment block
                comment_pattern = rf'/\*\*([\s\S]*?@agent:\s*{match}[\s\S]*?)\*/'
                comment = re.search(comment_pattern, content)
                if comment:
                    self._parse_agent_annotation(comment.group(1), filepath, match)

    def _parse_agent_annotation(self, annotation: str, filepath: Path, context: str):
        """Parse agent metadata from annotation"""
        agent_match = re.search(r'@agent:\s*([a-z0-9-]+)', annotation)
        if not agent_match:
            return

        agent_name = agent_match.group(1)

        if agent_name not in self.agents:
            self.agents[agent_name] = {
                'name': agent_name,
                'files': set(),
                'mission': '',
                'tools': set(),
                'triggers': set()
            }

        self.agents[agent_name]['files'].add(str(filepath))

        # Extract other metadata
        mission_match = re.search(r'@mission:\s*(.+?)(?=@|\n\n|\Z)', annotation, re.DOTALL)
        if mission_match:
            self.agents[agent_name]['mission'] = mission_match.group(1).strip()

        tools_match = re.search(r'@tools:\s*(.+?)(?=@|\n\n|\Z)', annotation, re.DOTALL)
        if tools_match:
            tools = [t.strip() for t in tools_match.group(1).split(',')]
            self.agents[agent_name]['tools'].update(tools)

        triggers_match = re.search(r'@triggers:\s*(.+?)(?=@|\n\n|\Z)', annotation, re.DOTALL)
        if triggers_match:
            triggers = [t.strip() for t in triggers_match.group(1).split(',')]
            self.agents[agent_name]['triggers'].update(triggers)

    def generate_markdown(self) -> str:
        """Generate AGENTS.md content from extracted agents"""
        lines = [
            "# Generated Agent Documentation",
            "",
            "> Auto-generated from code annotations. Do not edit manually.",
            "",
            "## Agent Catalog",
            ""
        ]

        for agent_name, agent_data in sorted(self.agents.items()):
            lines.extend([
                f"### {agent_name}",
                "",
                f"**Mission**: {agent_data['mission'] or 'Not specified'}",
                "",
                f"**Source Files**:",
                ""
            ])

            for filepath in sorted(agent_data['files']):
                lines.append(f"- `{filepath}`")

            lines.append("")

            if agent_data['tools']:
                lines.extend([
                    "**Tools**:",
                    ""
                ])
                for tool in sorted(agent_data['tools']):
                    lines.append(f"- {tool}")
                lines.append("")

            if agent_data['triggers']:
                lines.extend([
                    "**Triggers**:",
                    ""
                ])
                for trigger in sorted(agent_data['triggers']):
                    lines.append(f"- {trigger}")
                lines.append("")

            lines.append("---")
            lines.append("")

        return '\n'.join(lines)

# CLI usage
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dirs', required=True,
                       help='Comma-separated source directories')
    parser.add_argument('--output-file', required=True,
                       help='Output AGENTS.md file')

    args = parser.parse_args()

    extractor = AgentExtractor()

    for source_dir in args.source_dirs.split(','):
        source_path = Path(source_dir.strip())
        for filepath in source_path.rglob('*'):
            if filepath.suffix in ['.py', '.ts', '.js', '.tsx', '.jsx']:
                try:
                    extractor.extract_from_file(filepath)
                except Exception as e:
                    print(f"Warning: Failed to parse {filepath}: {e}")

    output_content = extractor.generate_markdown()

    output_path = Path(args.output_file)
    output_path.write_text(output_content)

    print(f"Generated {args.output_file} with {len(extractor.agents)} agents")
```

### Migration Guide

### Migrating Existing Projects to README/AGENTS Structure

**Intent**: Provide step-by-step process for introducing this documentation pattern to existing repositories without disrupting development.

**Phase 1: Assessment (Day 1)**

```bash
# 1. Analyze current structure
find . -name "README*" -o -name "CONTRIBUTING*" -o -name "docs" -type d | head -20

# 2. Identify worldview boundaries
find . -type d \( -name "apps" -o -name "packages" -o -name "services" -o -name "libs" \) | head -10

# 3. Check for existing agent/AI documentation
grep -r "agent\|AI\|LLM" --include="*.md" . | head -20
```

**Phase 2: Root Documentation (Day 2-3)**

```markdown
# Step 1: Create root README.md
1. Consolidate existing README content
2. Add clear sections: Setup, Architecture, Documentation
3. Add navigation to future AGENTS.md

# Step 2: Create root AGENTS.md
1. Start with Primary Directive (if agents exist)
2. Add placeholder Agent Catalog
3. Link back to README.md
```

**Phase 3: Subsystem Documentation (Week 1-2)**

```bash
#!/bin/bash
# Automated subsystem documentation scaffolding

for boundary in apps/* packages/* services/*; do
  if [ -d "$boundary" ]; then
    # Create README if missing
    if [ ! -f "$boundary/README.md" ]; then
      cat > "$boundary/README.md" <<EOF
# $(basename $boundary)

> Part of $(basename $(pwd)) monorepo. See [root README](../../README.md).

## Overview

TODO: Add subsystem description

## Setup

TODO: Add setup instructions

## Agents

See [AGENTS.md](./AGENTS.md) for AI agent specifications.
EOF
    fi

    # Create AGENTS.md if agents will be used
    if [ ! -f "$boundary/AGENTS.md" ]; then
      cat > "$boundary/AGENTS.md" <<EOF
# $(basename $boundary) Agents

> For context, see [README.md](./README.md)
> For repository-wide agents, see [root AGENTS.md](../../AGENTS.md)

## Agent Catalog

*No agents defined yet.*
EOF
    fi
  fi
done
```

**Phase 4: Content Migration (Week 2-3)**

```python
# scripts/migrate-docs.py
"""Migrate existing documentation to new structure"""

import re
from pathlib import Path
import shutil

class DocumentationMigrator:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def migrate_docs_folder(self):
        """Move docs/ content to appropriate README/AGENTS locations"""
        docs_path = self.repo_root / 'docs'

        if not docs_path.exists():
            return

        for doc_file in docs_path.glob('**/*.md'):
            content = doc_file.read_text()

            # Determine destination based on content
            if 'agent' in content.lower() or 'ai' in content.lower():
                # Move to AGENTS.md structure
                self._merge_into_agents(doc_file)
            elif 'setup' in content.lower() or 'install' in content.lower():
                # Move to README.md structure
                self._merge_into_readme(doc_file)
            else:
                # Archive for manual review
                self._archive_doc(doc_file)

    def _merge_into_agents(self, doc_file: Path):
        """Merge content into appropriate AGENTS.md"""
        # Implementation: Parse content and append to relevant AGENTS.md
        pass

    def _merge_into_readme(self, doc_file: Path):
        """Merge content into appropriate README.md"""
        # Implementation: Parse content and append to relevant README.md
        pass

    def validate_migration(self):
        """Ensure all documentation is accessible"""
        issues = []

        # Check for orphaned docs
        old_docs = list(self.repo_root.glob('docs/**/*.md'))
        if old_docs:
            issues.append(f"Unmigrated docs remain: {len(old_docs)} files")

        # Verify cross-references
        for md_file in self.repo_root.glob('**/*.md'):
            content = md_file.read_text()
            # Check for broken links to docs/
            if 'docs/' in content:
                issues.append(f"Outdated docs/ reference in {md_file}")

        return issues
```

**Phase 5: Validation and Cleanup (Week 3-4)**

```yaml
# .github/workflows/migration-validation.yml
name: Validate Documentation Migration

on:
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # Daily during migration

jobs:
  validate-migration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check documentation structure
        run: |
          # Ensure no docs/ folder at root (migrated)
          if [ -d "docs" ]; then
            echo "Warning: docs/ folder still exists"
          fi

          # Ensure worldview boundaries have documentation
          for boundary in apps/* packages/* services/*; do
            if [ -d "$boundary" ]; then
              if [ ! -f "$boundary/README.md" ]; then
                echo "Error: $boundary missing README.md"
                exit 1
              fi
            fi
          done

      - name: Validate cross-references
        run: python scripts/validate-links.py --fix-paths

      - name: Generate migration report
        run: |
          python scripts/migration-report.py \
            --before "docs/" \
            --after "README.md,AGENTS.md" \
            --output "migration-status.md"
```

**Migration Checklist**:

- [ ] Root README.md created with navigation
- [ ] Root AGENTS.md created (if using agents)
- [ ] All worldview boundaries identified
- [ ] README.md exists at each boundary
- [ ] AGENTS.md exists where agents are used
- [ ] Old docs/ content migrated or archived
- [ ] Cross-references updated
- [ ] CI/CD validation in place
- [ ] Team trained on new structure
- [ ] Documentation for documentation (meta) updated

**Common Migration Pitfalls**:

1. **Rushing the migration**: Take time to properly categorize content
2. **Over-creating AGENTS.md**: Only create where agents actually exist
3. **Losing information**: Archive everything, delete nothing initially
4. **Breaking links**: Use automated tools to find and fix references
5. **Ignoring team habits**: Provide clear examples and templates

## Update Log

- **2024-11-19** – Added comprehensive CI/CD Automation section with validation workflows, automated agent extraction from code, and validation scripts. Added Migration Guide with phased approach for converting existing projects to README/AGENTS structure. (Author: AI-First)
- **2025-11-17** – Updated AGENTS.md basic structure section to include Primary Directive as the first section, providing repository-wide behavior rules for all autonomous agents. Reorganized structure documentation for clarity. (Author: AI-First)
- **2025-11-14** – Standardized Agent Contract and TL;DR sections for consistency with other SSOT documents. Updated canonical URL for renamed file. (Author: AI-First)
- **2025-11-15** – Initial document creation based on AGENTS.md spec, README best practices, and AI-first architecture patterns. (Author: AI-First)

## See Also

### Prerequisite Knowledge
- Markdown syntax and GitHub Flavored Markdown
- Repository structure patterns (monorepo, polyrepo)
- AI agent architectures and multi-agent systems
- Documentation as code principles

### Related Topics
- **SSOT (Single Source of Truth)**: Overlaps with canonical definitions and avoiding duplication
- **ADR (Architecture Decision Records)**: Complements AGENTS.md for "why" documentation
- **Code Style Guides**: Agent constraints should reference style guides
- **CI/CD Pipeline Docs**: Build/test commands in AGENTS.md should align with pipeline definitions

### Complementary Specifications
- [Semantic Versioning](https://semver.org) for documentation versioning
- [Conventional Commits](https://www.conventionalcommits.org) for changelog automation
- [OpenAPI/Swagger](https://swagger.io) for API agent specifications

## References

[R1] AGENTS.md Specification. (2025). *AGENTS.md: A simple, open format for guiding coding agents*. https://agents.md

[R2] OpenAI. (2025). *AGENTS.md GitHub Repository*. https://github.com/openai/agents.md

[R3] Make a README. (2025). *Best practices for creating README files*. https://www.makeareadme.com

[R4] GitHub Documentation. (2025). *About READMEs*. https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes

[R5] Markdown Guide. (2025). *GitHub Flavored Markdown Specification*. https://github.github.com/gfm/

---

**Document ID**: `agents-readme-guide-v1`

**Canonical URL**: `https://github.com/artificial-intelligence-first/ssot/blob/main/docs/README_AND_AGENTS.md`

**Version**: 1.0.0

**License**: MIT

**Maintained By**: Repository documentation team

**Last Review**: 2025-11-15

**Next Review Due**: 2025-12-15 (monthly review cycle)
