---
title: Single Source of Truth (SSOT)
slug: ssot-guide
summary: "SSOT principles and implementation guide"
type: guide
tags: [topic, ai-first, ssot, governance, documentation]
last_updated: 2025-11-19
---

# Topic: Single Source of Truth (SSOT) — Architecture and Governance

## Agent Contract

- **PURPOSE**:
  - Define the Single Source of Truth (SSOT) principle to ensure authoritative, consistent documentation across the project
  - Establish protocols for resolving conflicts between multiple data sources
  - Provide a canonical reference point for AI agents to ground their reasoning and code generation
- **USE_WHEN**:
  - Resolving conflicting definitions found in multiple documents
  - Creating new documentation that requires canonical definitions
  - Implementing data schemas, API contracts, or business policies
  - Verifying system behavior against specified requirements
- **DO_NOT_USE_WHEN**:
  - Documenting implementation details that belong in code comments
  - Tracking temporary tasks (use `PLANS.md`)
  - Recording historical changes (use `CHANGELOG.md`)
  - Writing tutorials or how-to guides (use dedicated `docs/` files)
- **PRIORITY**:
  - `SSOT.md` takes precedence over `README.md`, wiki pages, and code comments when definitions conflict
  - Implementation code must match `SSOT.md`; if they differ, the code is incorrect (bug) or `SSOT.md` needs updating (change request)
- **RELATED_TOPICS**:
  - readme-and-agents
  - exec-plan
  - documentation-as-code
  - governance-policy

---

## TL;DR

- **WHAT**: SSOT is a governance architecture designating exactly **one authoritative location** (`SSOT.md`) for every critical definition, schema, policy, and workflow.
- **WHY**: Eliminates "multiple truths," reduces hallucination in AI agents, ensures system consistency, and simplifies maintenance by propagating changes from one source.
- **WHEN**: Apply immediately upon repository initialization and maintain continuously as the system evolves.
- **HOW**: Create a root `SSOT.md`, define canonical terms/schemas there, and ensure all other documents and code reference it (link to it) rather than duplicating it.
- **WATCH_OUT**: Avoid "implementation as truth" (code is hard to read/verify) and "stale SSOT" (truth must be living); update SSOT *before* code implementation.

---

## Canonical Definitions

### Single Source of Truth (SSOT)

**Definition**: A data structuring and governance principle where every piece of information (definitions, policies, schemas) is mastered in exactly one location, ensuring all stakeholders refer to the same canonical record.

**Scope**:
- **Includes**:
  - Canonical definitions (Domain terms, Acronyms)
  - Data contracts (Database schemas, API specifications)
  - Governance policies (Security, Retention, Coding standards)
  - Architecture decisions (Patterns, Infrastructure)
- **Excludes**:
  - Derived copies (unless auto-generated and read-only)
  - Temporary drafts
  - Implementation-specific variations (must reference SSOT)

**Related Concepts**:
- **Similar**: DRY (Don't Repeat Yourself), Golden Record, System of Record
- **Contrast**: Data silos, Fragmented documentation, "Tribal knowledge"
- **Contains**: Glossary, Schemas, Policies, Workflows

**Example**:

```markdown
# SSOT.md
## API Endpoints
- **Base URL**: `https://api.example.com/v2` (Canonical Definition)

# README.md
For API usage, see [SSOT.md](./SSOT.md#api-endpoints). (Reference)
```

**Sources**: [R1], [R2]

### Data Contract

**Definition**: A formal agreement defined in the SSOT that specifies the structure, format, and constraints of data exchanged between system components (APIs, databases, events).

**Scope**:
- **Includes**:
  - JSON Schemas / OpenAPI specs embedded or linked
  - Database table definitions (columns, types, constraints)
  - Event payloads and topic names
- **Excludes**:
  - Internal variable names in code
  - Temporary data structures used only within a single function

**Related Concepts**:
- **Similar**: Interface Definition Language (IDL), API Schema
- **Contrast**: Implicit data handling, "Schemaless" chaos
- **Contains**: Field names, Data types, Validation rules

**Example**:

```json
// User Schema (SSOT)
{
  "id": "UUID (v4)",
  "email": "String (format: email, unique)",
  "role": "Enum [user, admin, system]",
  "created_at": "ISO8601 Timestamp"
}
```

**Sources**: [R3]

### Living Governance

**Definition**: The practice of maintaining the SSOT as a dynamic, version-controlled artifact that evolves synchronously with the software it describes, rather than as static, "write-once" documentation.

**Scope**:
- **Includes**:
  - Git-based versioning of `SSOT.md`
  - Review process for SSOT changes in Pull Requests
  - Regular auditing for staleness
- **Excludes**:
  - PDF specifications stored in separate file servers
  - Wiki pages detached from the codebase
  - Unwritten oral traditions

**Related Concepts**:
- **Similar**: Documentation as Code, GitOps
- **Contrast**: Waterfall documentation, Archived specs

**Sources**: [R3]

---

## Core Patterns

### Pattern: The Root SSOT File

**Intent**: Establish a predictable, accessible, and authoritative location for canonical information at the repository root.

**Context**: Any AI-first repository where agents and humans need a shared understanding of domain concepts and rules.

**Implementation**:

```
repository/
├── SSOT.md              # 👑 The King: Canonical Definitions
├── README.md            # 🗺️ The Map: References SSOT
├── AGENTS.md            # 🤖 The Workforce: References SSOT
├── docs/                # 📚 The Library: Deep dives linking to SSOT
└── src/                 # 🏗️ The Construction: Implements SSOT
```

**Key Principles**:
- **Centralization**: One file (or directory) to rule them all.
- **Discoverability**: Placed at root for zero-friction access.
- **Immutability of Truth**: Other docs update to match SSOT, not vice versa.

**Trade-offs**:
- ✅ **Advantages**: Zero ambiguity, easy for agents to ingest, simplified updates.
- ⚠️ **Disadvantages**: `SSOT.md` can become large (mitigation: split into `docs/ssot/*.md` if >2000 lines).
- 💡 **Alternatives**: Distributed docs (harder to maintain consistency).

**Sources**: [R3]

---

### Pattern: Reference-Based Documentation

**Intent**: Prevent duplication and inconsistencies by forcing downstream documentation to link to the SSOT instead of repeating information.

**Context**: Writing `README.md`, API guides, or integration manuals that rely on core definitions.

**Implementation**:

```markdown
# ❌ Anti-pattern: Duplication
## API Configuration
The base URL is `https://api.example.com/v1`.
(Risk: What if SSOT says v2?)

# ✅ Correct pattern: Reference
## API Configuration
See [SSOT.md](./SSOT.md#api-endpoints) for the current Base URL and authentication protocols.
```

**Key Principles**:
- **Link, Don't Copy**: Hyperlinks are live; copies are dead.
- **Contextual Context**: Provide enough context to understand *why* to click, but leave the *what* to the SSOT.

**Trade-offs**:
- ✅ **Advantages**: Maintenance reduced to one location, guaranteed consistency.
- ⚠️ **Disadvantages**: Requires navigation (clicks); agents need tool capability to read referenced files.

**Sources**: [R3]

---

### Pattern: Code Generation from SSOT

**Intent**: Automate the enforcement of data contracts by generating implementation code (types, schemas) directly from the SSOT definitions.

**Context**: Ensuring that TypeScript interfaces, SQL schemas, or Pydantic models strictly adhere to the documented contracts.

**Implementation**:

```bash
# scripts/generate-types.sh
# Conceptual workflow:
# 1. Parse SSOT.md to extract JSON Schema blocks
# 2. Use quicktype or similar tools to generate interfaces

echo "Generating types from SSOT..."
python scripts/extract_schemas.py SSOT.md > schemas.json
quicktype -s schema schemas.json -o src/types/ssot.ts
```

**Key Principles**:
- **Single Direction**: SSOT → Code. Never Code → SSOT (unless SSOT is auto-generated from a higher spec).
- **Automation**: Manual syncing leads to drift.

**Trade-offs**:
- ✅ **Advantages**: Zero divergence between documentation and code, type safety.
- ⚠️ **Disadvantages**: Requires tooling setup (`extract_schemas.py` implementation).

**Sources**: [R2]

---

### Pattern: CI/CD Validation

**Intent**: Enforce SSOT compliance automatically to prevent "drift" where implementation deviates from documentation.

**Context**: Continuous Integration pipelines.

**Implementation**:

```yaml
# .github/workflows/validate-ssot.yml
name: Validate SSOT Compliance
on: [pull_request]
steps:
  - uses: actions/checkout@v3
  - name: Verify Constants
    run: |
      # Check if API_VERSION in code matches SSOT
      SSOT_VER=$(grep "API Version" SSOT.md | awk '{print $3}')
      CODE_VER=$(grep "export const API_VERSION" src/config.ts | awk -F'"' '{print $2}')
      if [ "$SSOT_VER" != "$CODE_VER" ]; then
        echo "❌ Mismatch: SSOT says $SSOT_VER but Code says $CODE_VER"
        exit 1
      fi
```

**Trade-offs**:
- ✅ **Advantages**: Catches inconsistencies before merge.
- ⚠️ **Disadvantages**: Fragile regex parsing; requires structured SSOT format.

---

## Decision Checklist

- [ ] **SSOT Exists**: Is there a file named `SSOT.md` at the repository root?
- [ ] **Unique Definitions**: Are definitions (e.g., "User") defined ONLY in SSOT and referenced elsewhere?
- [ ] **Schema Completeness**: Do data contracts include types, constraints, and examples?
- [ ] **Policy Clarity**: Are policies (e.g., "Retention") specific and measurable?
- [ ] **Agent Accessible**: Is the format Markdown, structured with clear headers for AI parsing?
- [ ] **Version Controlled**: Is the SSOT part of the Git repository?
- [ ] **Update Process**: Is "Update SSOT" a required step in the PR checklist?

---

## Anti-patterns / Pitfalls

### Anti-pattern: Multiple Sources of Truth

**Symptom**: `README.md` says API v1, `docs/api.md` says API v2, and code uses v1.5.

**Why It Happens**: Laziness or lack of governance; developers update the file closest to them.

**Impact**:
- AI agents hallucinate or generate incorrect code.
- New developers are confused.
- Integration bugs arise from mismatched assumptions.

**Solution**: Designate `SSOT.md` as the master. Delete definitions from other files and replace with links.

### Anti-pattern: Implementation as SSOT

**Symptom**: "The code is the documentation."

**Why It Happens**: Belief that code is the only thing that matters (true for execution, false for understanding).

**Impact**:
- Business logic becomes opaque.
- Non-engineers (and AI agents needing high-level context) cannot understand system behavior without reading all code.
- "Why" is lost, only "How" remains.

**Solution**: Extract contracts and policies to `SSOT.md`. Code should *implement* the truth, not *be* the only record of it.

### Anti-pattern: Stale SSOT

**Symptom**: SSOT defines fields that were removed from the database 6 months ago.

**Why It Happens**: Documentation updates are not enforced during code review.

**Impact**: Trust in documentation erodes; developers stop reading it.

**Solution**: CI/CD validation and strict PR checklists ("No merge without SSOT update").

---

## Evaluation

### Metrics

**SSOT Coverage**: Percentage of domain terms/schemas defined in SSOT vs. scattered.
- **Target**: 100% of core entities defined in SSOT.
- **Measurement**: Grep for entity names across `docs/` and check for definitions vs references.

**Documentation Drift**: Number of discrepancies between SSOT and implementation.
- **Target**: 0.
- **Measurement**: Automated scripts (Pattern: CI/CD Validation).
- **Frequency**: On every Pull Request.

**Agent Hallucination Rate**: Frequency of AI agents asking clarifying questions about basic terms.
- **Target**: Low.
- **Measurement**: Review agent interaction logs.

### Testing Strategies

**Manual Review**:
- Check `SSOT.md` freshness during Sprint Retrospectives.

**Automated Testing**:
- **Link Checker**: Ensure all links in `README.md` pointing to `SSOT.md` are valid.
- **Schema Validator**: Extract JSON schemas from SSOT and validate sample data payloads.

---

## Update Log

- **2025-11-19** – Created `docs/SSOT.md` with comprehensive guide structure, integrating definitions, core patterns, and evaluation metrics based on `ssot-guide.md`. (Author: AI-First)
- **2025-11-01** – Initial reference content from `ssot-guide.md` covering 12-Factor App and Docs-as-Code principles.

---

## See Also

### Prerequisites
- [documentation-as-code] – Understanding docs as engineering artifacts.
- [git-flow] – Managing version control for documentation.

### Related Topics
- [README_AND_AGENTS.md](./README_AND_AGENTS.md) – How SSOT supports the agent ecosystem.
- [CODE_MCP.md](./CODE_MCP.md) – Implementing SSOT schemas in code.

---

## References

- [R1] Wikipedia. "Single source of truth." https://en.wikipedia.org/wiki/Single_source_of_truth (accessed 2025-10-23)
- [R2] The Twelve-Factor App. "III. Config." https://12factor.net/config (accessed 2025-10-23)
- [R3] Write the Docs. "Documentation as Code." https://www.writethedocs.org/guide/docs-as-code/ (accessed 2025-10-23)

---

**Document ID**: `docs/SSOT.md`
**Canonical URL**: `https://github.com/artificial-intelligence-first/ssot/blob/main/docs/SSOT.md`
**License**: MIT

