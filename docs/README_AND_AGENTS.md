---
title: AGENTS.md and README.md for AI-First Repositories
slug: agents-readme
summary: "Agents & README Guide"
type: guide
tags: [topic, ai-first, documentation, agents, readme, repository-structure]
last_updated: 2024-11-19
---

# Topic: AGENTS.md and README.md for AI-First Repositories

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

---

## TL;DR

- **WHAT**: A dual-documentation pattern separating human-facing (README.md) and AI-facing (AGENTS.md) concerns across repository hierarchies, with clear worldview boundaries determining where documentation should exist
- **WHY**: Humans need context/setup while AI agents need operational specifications; separation of concerns prevents information overload, enables scalability, and reduces documentation drift
- **WHEN**: Use at repository initialization, when adding new subsystems/services, introducing AI agents to existing projects, or refactoring monorepo structures
- **HOW**: Create root-level README.md (orientation) and AGENTS.md (agent catalog) with bidirectional links; add subdirectory versions ONLY at architectural boundaries (apps/*, packages/*, services/*); maintain parent (map) vs. child (guidebook) relationship
- **WATCH_OUT**: Avoid over-documentation in low-level directories, duplicating content between README and AGENTS, missing navigation links, or using abstract templates without concrete examples

---

## Canonical Definitions

### README.md

**Definition**: The authoritative human-facing instruction manual for a repository or subsystem, providing orientation, setup instructions, and navigation to deeper documentation.

**Scope**:
- **Includes**:
  - Repository/module purpose and value proposition
  - Technical stack and prerequisites
  - Installation and quick start procedures
  - High-level directory structure explanation
  - Links to specialized documentation (AGENTS.md, SSOT.md, PLANS.md)
- **Excludes**:
  - Detailed API specifications (belongs in dedicated docs)
  - Agent-specific operational instructions (belongs in AGENTS.md)
  - Low-level implementation details (belongs in code comments)

**Authoritative Source**: [GitHub README Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

### AGENTS.md

**Definition**: A machine-readable catalog defining all autonomous agents operating within a repository boundary, specifying their capabilities, constraints, and operational parameters.

**Scope**:
- **Includes**:
  - Complete agent inventory with unique identifiers
  - Per-agent specifications (role, mission, inputs/outputs, tools, constraints)
  - Build, test, and deployment commands agents should execute
  - Code style guidelines and conventions
  - Security considerations and boundaries
- **Excludes**:
  - Human onboarding procedures (belongs in README.md)
  - General repository philosophy (belongs in README.md)
  - Narrative explanations of "why" (agents need "what" and "how")

**Authoritative Source**: [AGENTS.md Specification](https://agents.md)

### Worldview Boundary

**Definition**: An architectural division point where a subsystem has sufficiently distinct purpose, dependencies, or operational context to warrant independent documentation.

**Scope**:
- **Includes**:
  - Separate applications in a monorepo (`apps/frontend`, `apps/api`)
  - Independent packages (`packages/ui-kit`, `packages/auth`)
  - Domain-specific service boundaries (`services/billing`, `services/notifications`)
- **Excludes**:
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

---

## Core Patterns

### Pattern: Root Documentation Pair

**Intent**: Establish a single, predictable entry point for both human and AI consumers at the repository root.

**Context**: New repository setup, repository refactoring, onboarding new team members or agents.

**Implementation**:

```text
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
bash
# Prerequisites
npm install -g pnpm

# Setup
pnpm install

# Common commands
pnpm dev      # Start development
pnpm test     # Run tests
pnpm lint     # Check code quality

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
- ✅ **Advantages**: Single source of truth for entry points, clear separation of human vs. AI concerns, predictable location for documentation discovery
- ⚠️ **Disadvantages**: Requires discipline to keep README concise, AGENTS.md can become large in complex systems (use subdirectory versions)

### Pattern: Subdirectory Documentation Inheritance

**Intent**: Provide localized context at architectural boundaries while maintaining navigation to parent-level documentation.

**Context**: Monorepos with multiple applications, multi-service architectures, packages with independent lifecycles.

**Implementation**:

```text
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
- ✅ **Advantages**: Localized documentation reduces noise for subsystem work, clear ownership boundaries for agent responsibilities, easier to maintain subsystem-specific conventions
- ⚠️ **Disadvantages**: Risk of duplication if not carefully scoped, requires navigation links to prevent documentation silos, can proliferate if "worldview boundary" criteria unclear

### Pattern: README ↔ AGENTS Navigation Chain

**Intent**: Ensure humans and AI can seamlessly traverse between orientation (README) and operational specifications (AGENTS) at every documentation level.

**Context**: All documentation pairs (root and subdirectories).

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

```text
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
- ✅ **Advantages**: Prevents documentation dead-ends, supports both human and AI navigation patterns, makes relationships explicit
- ⚠️ **Disadvantages**: Requires maintenance when documentation moves, can create circular reference confusion if not clearly labeled

### Pattern: Agent Capability Matrix

**Intent**: Provide a quick-reference grid of agent capabilities across different repository scopes for routing decisions.

**Context**: Repositories with 5+ agents or multi-agent orchestration needs.

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
- ✅ **Advantages**: Fast decision-making for agent selection, visual clarity of capability coverage, identifies gaps or overlaps
- ⚠️ **Disadvantages**: Requires updates when agents evolve, can oversimplify nuanced capabilities

---

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

---

## Anti-patterns / Pitfalls

### Anti-pattern: Documentation Duplication

**Symptom**: Same content appears in both README.md and AGENTS.md, or in parent and child documents.

**Why It Happens**: Unclear boundaries between human-facing and AI-facing concerns, or fear of missing information.

**Impact**:
- Documentation skew (one copy updated, others stale)
- Maintenance burden (changes require multiple edits)
- Confusion about authoritative source

**Solution**: Define ownership (README = context, AGENTS = operations), use cross-references instead of copying, and perform regular audits for duplication.

### Anti-pattern: Over-Specification in Low-Level Directories

**Symptom**: README.md and AGENTS.md files appear in `src/components/Button/`, `src/utils/formatters/`, etc.

**Why It Happens**: Zealous application of "document everything" principle without considering boundaries.

**Impact**:
- Documentation overwhelms actual code
- Impossible to maintain as code evolves
- Noise reduces value of legitimate documentation

**Solution**: Apply the "worldview boundary" test strictly. If a directory is purely organizational (not architectural), skip documentation.

### Anti-pattern: Abstract Agent Definitions

**Symptom**: Agent specifications use vague language like "handles data processing" or "manages frontend tasks."

**Why It Happens**: Template-driven approach without concrete use case analysis.

**Impact**:
- AI agents cannot determine if they're the right choice for a task
- Overlapping responsibilities cause conflicts
- Humans cannot predict agent behavior

**Solution**: Use real task examples when defining agents, specify exact tools with versions, define measurable constraints, and include error scenarios.

### Anti-pattern: Missing Navigation Links

**Symptom**: README.md and AGENTS.md exist but don't reference each other or parent/child documents.

**Why It Happens**: Documents created independently without considering navigation flow.

**Impact**:
- Dead-ends force users to manually browse file structure
- AI agents cannot discover related context
- Documentation feels fragmented

**Solution**: Include navigation sections in documentation templates, validate links in CI/CD, and regular documentation reviews for connectivity.

---

## Evaluation

### Metrics

**Documentation Coverage Ratio**: Percentage of worldview boundaries with documentation.
- **Target**: 100% of worldview boundaries have README.md, 80%+ of boundaries with agents have AGENTS.md, 0% of implementation directories have documentation.
- **Measurement**: Custom script or CI/CD validation counting directories with/without docs.

**Navigation Depth Score**: Number of clicks/links needed to reach relevant documentation from entry point.
- **Target**: Root to any subsystem doc ≤ 2 links, any doc back to root ≤ 2 links.
- **Measurement**: Manual audit or documentation graph analysis.

**Agent Specification Completeness**: Percentage of agents with all required fields.
- **Target**: 100% of agents have ID, Type, Scope, Mission, Inputs, Outputs, Tools, Constraints.
- **Measurement**: Script parsing AGENTS.md files.

**Documentation Freshness**: Time since last update relative to code changes.
- **Target**: README.md updated within 30 days of major dependency changes, AGENTS.md updated within 7 days of agent capability changes.
- **Measurement**: Git commit history comparison.

### Test Strategies

**Human Comprehension Test**:
- New developer joins team without prior context.
- Measure time to understand repo purpose, complete setup, and identify agent for task.
- Success if targets met without external help and < 2 navigation errors.

**AI Agent Self-Service Test**:
- New AI agent onboards to repository reading only README.md and AGENTS.md.
- Agent attempts to describe architecture, identify agent for tasks, and generate build commands.
- Success if 100% accuracy on architecture/build commands and 80%+ on agent selection.

**Documentation Drift Detection**:
- Code changes occur without documentation updates (e.g., new dependency).
- CI checks should flag inconsistency (e.g., package.json changed without README update).

---

## Practical Examples

### CI/CD Automation

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
```

### Migration Guide

**Intent**: Provide step-by-step process for introducing this documentation pattern to existing repositories without disrupting development.

**Phase 1: Assessment (Day 1)**
- Analyze current structure and identify worldview boundaries.
- Check for existing agent/AI documentation.

**Phase 2: Root Documentation (Day 2-3)**
- Create root README.md with clear sections and navigation.
- Create root AGENTS.md with Primary Directive and link back to README.

**Phase 3: Subsystem Documentation (Week 1-2)**
- Scaffolding script to create README/AGENTS at boundaries.

**Phase 4: Content Migration (Week 2-3)**
- Move docs/ content to appropriate README/AGENTS locations.

**Phase 5: Validation and Cleanup (Week 3-4)**
- CI/CD validation workflow and removal of old docs structure.

---

## Update Log

- **2024-11-19** – Added comprehensive CI/CD Automation section with validation workflows, automated agent extraction from code, and validation scripts. Added Migration Guide with phased approach for converting existing projects to README/AGENTS structure. (Author: AI-First)
- **2025-11-17** – Updated AGENTS.md basic structure section to include Primary Directive as the first section, providing repository-wide behavior rules for all autonomous agents. Reorganized structure documentation for clarity. (Author: AI-First)
- **2025-11-14** – Standardized Agent Contract and TL;DR sections for consistency with other SSOT documents. Updated canonical URL for renamed file. (Author: AI-First)
- **2025-11-15** – Initial document creation based on AGENTS.md spec, README best practices, and AI-first architecture patterns. (Author: AI-First)

---

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

---

## References

- [R1] AGENTS.md Specification. (2025). *AGENTS.md: A simple, open format for guiding coding agents*. https://agents.md
- [R2] OpenAI. (2025). *AGENTS.md GitHub Repository*. https://github.com/openai/agents.md
- [R3] Make a README. (2025). *Best practices for creating README files*. https://www.makeareadme.com
- [R4] GitHub Documentation. (2025). *About READMEs*. https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- [R5] Markdown Guide. (2025). *GitHub Flavored Markdown Specification*. https://github.github.com/gfm/

---

**Document ID**: `agents-readme-guide-v1`
**Canonical URL**: `https://github.com/artificial-intelligence-first/ssot/blob/main/docs/README_AND_AGENTS.md`
**Version**: 1.0.0
**License**: MIT
**Maintained By**: Repository documentation team
**Last Review**: 2025-11-15
**Next Review Due**: 2025-12-15 (monthly review cycle)
