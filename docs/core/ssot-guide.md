---
title: SSOT Guide
slug: ssot-guide
status: living
last_updated: 2025-11-01
tags: [ssot, governance, documentation, data-contracts, policies]
summary: "Comprehensive guide to Single Source of Truth principles and implementation patterns."
authors: []
sources:
  - { id: R1, title: "Single source of truth - Wikipedia", url: "https://en.wikipedia.org/wiki/Single_source_of_truth", accessed: "2025-10-23" }
  - { id: R2, title: "The Twelve-Factor App - III. Config", url: "https://12factor.net/config", accessed: "2025-10-23" }
  - { id: R3, title: "Documentation as Code - Write the Docs", url: "https://www.writethedocs.org/guide/docs-as-code/", accessed: "2025-10-23" }
---

# SSOT Guide

> **For Humans**: This guide explains the Single Source of Truth principle for maintaining authoritative, consistent documentation across your project.
>
> **For AI Agents**: SSOT designates one canonical location for each dataset, document, or policy. Always reference the SSOT when encountering conflicting information. Update the SSOT first before propagating changes elsewhere.

## Overview

Single Source of Truth (SSOT) is a governance principle that designates **one authoritative location** for any given piece of information. All downstream systems, documents, and processes must reference this canonical source to ensure consistency and prevent conflicting or redundant copies.

**Core Idea**: When you need to know the "current truth" about something—a definition, policy, data schema, or workflow—there should be exactly one place to look.

## Why SSOT Matters

### Without SSOT ❌ *(Sample scenario)*

```
Project Structure:
├── docs/api.md          (says endpoint is /v2/users)
├── README.md            (says endpoint is /api/v2/users)
├── wiki/integration.md  (says endpoint is /users/v2)
└── code comments        (say endpoint is /v1/users - outdated)

Result: Confusion, integration failures, wasted time
```

### With SSOT ✅ *(Sample scenario)*

```
Project Structure:
├── SSOT.md                    (Canonical: endpoint is /api/v2/users)
├── docs/api.md                (References SSOT.md)
├── README.md                  (References SSOT.md)
└── wiki/integration.md        (References SSOT.md)

Result: Everyone references the same truth, inconsistencies are eliminated
```

## Core Characteristics

### 1. Authoritative

- The SSOT is the **canonical record**
- Any discrepancies elsewhere must be reconciled back to it
- When conflicts arise, the SSOT wins

### 2. Accessible

- Stakeholders can easily read and reference the SSOT
- Location is well-known and documented
- Format is human and machine-readable

### 3. Versioned

- Changes are tracked via version control (Git)
- Audit trail shows when and why updates occurred
- Historical versions are preserved

### 4. Maintained

- Regular review and update process
- Clear ownership and responsibility
- Staleness is actively prevented

## SSOT Implementation

### Location

**Recommended**: Place `SSOT.md` at repository root

```
repository/
├── SSOT.md              # Single Source of Truth
├── README.md            # References SSOT
├── AGENTS.md            # References SSOT
├── docs/                # References SSOT
└── src/                 # Implementation follows SSOT
```

**Note**: This reference repository stores `SSOT.md` in the repository root. When implementing SSOT in your own projects, place it at the root for easier access and discoverability.

### Structure *(Sample outline)*

```markdown
# SSOT: Single Source of Truth

This document contains canonical definitions, policies, and data contracts for this project.

## Glossary

### Terms

**User**: An authenticated individual with access to the system
**Admin**: A User with elevated privileges
**Session**: An authenticated period lasting up to 24 hours

### Acronyms

- **API**: Application Programming Interface
- **CRUD**: Create, Read, Update, Delete
- **SSOT**: Single Source of Truth

## Data Contracts

### User Schema *(Sample)*

```json
{
  "id": "string (UUID)",
  "email": "string (email format)",
  "role": "enum: user | admin",
  "created_at": "ISO 8601 timestamp"
}
```

### API Endpoints *(Sample)*

- **Base URL**: `https://api.example.com/v2`
- **Authentication**: Bearer token in `Authorization` header
- **Users endpoint**: `/api/v2/users`
- **Sessions endpoint**: `/api/v2/sessions`

## Policies *(Sample)*

### Authentication Policy *(Sample)*

- Sessions expire after 24 hours of inactivity
- Maximum 5 active sessions per user
- Passwords must be ≥12 characters with mixed case/numbers/symbols

### Data Retention Policy

- User data retained for 7 years after account closure
- Audit logs retained for 90 days
- Session data purged after 30 days

## Workflows *(Sample)*

### Pull Request Approval *(Sample)*

1. Code review required from ≥1 team member
2. All CI checks must pass
3. CHANGELOG.md updated
4. SSOT.md updated if definitions changed

### Deployment Process *(Sample)*

1. Merge to `main` branch
2. Automated tests run
3. Deploy to staging
4. Manual QA verification
5. Deploy to production

## Update Log

- 2025-01-20: Added authentication policy section
- 2025-01-15: Updated API base URL to v2
- 2025-01-10: Initial SSOT creation
```

## What Belongs in SSOT

### ✅ Include

- **Canonical definitions** - Terms, acronyms, concepts
- **Data schemas** - Database models, API contracts
- **API specifications** - Endpoints, authentication, formats
- **Policies** - Security, retention, compliance
- **Workflows** - Standard processes, approval chains
- **Architecture decisions** - Chosen patterns, rationale
- **Environment configuration** - URLs, ports, service names

### ❌ Don't Include

- Implementation details (belongs in code)
- Tutorials or guides (belongs in docs/)
- Project status updates (belongs in CHANGELOG.md)
- Task tracking (belongs in ExecPlans or issue tracker)
- Personal notes or drafts

## SSOT Workflow

SSOT updates must stay in sync with companion documents. When terms or policies change, update the operational procedures in `AGENTS.md`, the relevant ExecPlans documented in [docs/workflows/plans.md](../workflows/plans.md), and any user-facing announcements in `CHANGELOG.md`.

### Creating New Definitions

```markdown
## Process

1. Identify need for canonical definition
2. Draft definition in SSOT.md
3. Review with team
4. Merge to repository
5. Update all dependent documents to reference SSOT
6. Deprecate/remove redundant definitions elsewhere
```

### Updating Existing Definitions

```markdown
## Process

1. Identify needed change
2. Update SSOT.md with new canonical definition
3. Add entry to Update Log with rationale
4. Propagate changes to dependent documents
5. Update implementation to match
6. Communicate change to team
```

### Resolving Conflicts

```markdown
## When Conflicts Arise

1. Check SSOT.md for canonical definition
2. If SSOT is correct: Update conflicting document
3. If SSOT is outdated: Update SSOT first, then propagate
4. Document the conflict and resolution in Update Log
```

## Integration with Other Conventions

### SSOT + AGENTS.md

**Relationship**: SSOT defines **what**, AGENTS.md defines **how**

```markdown
# SSOT.md
API endpoint: /api/v2/users

# AGENTS.md
## Testing Instructions
Test the /api/v2/users endpoint (defined in SSOT.md) by running:
  curl -H "Authorization: Bearer $TOKEN" https://api.example.com/api/v2/users
```

### SSOT + CHANGELOG.md

**Relationship**: SSOT is current state, CHANGELOG tracks changes

```markdown
# SSOT.md
Current API version: v2

# CHANGELOG.md
## [2.0.0] - 2025-01-15
### Changed
- API endpoints migrated from v1 to v2 (see SSOT.md for current endpoints)
```

### SSOT + ExecPlans

**Relationship**: ExecPlans use SSOT terminology consistently

```markdown
# ExecPlan: Implement User Dashboard

## Context and Orientation
User schema defined in SSOT.md Section "Data Contracts"
Authentication follows policy in SSOT.md Section "Policies"

## Decision Log
- [2025-01-20] Chose to display user role (per SSOT.md User schema)
```

### SSOT + SKILL.md (Agent Skills)

**Relationship**: Skills reference SSOT for domain knowledge

```markdown
# Skill: API Client Generator

## Prerequisites
- API base URL from SSOT.md
- Authentication method per SSOT.md authentication policy

## Procedures
1. Read endpoint definitions from SSOT.md
2. Generate client code matching SSOT.md data contracts
```

## Examples

### Example 1: Technology Glossary

```markdown
# SSOT.md

## Technology Stack

### Frontend
- **Framework**: React 18.x
- **Language**: TypeScript 5.x
- **Build Tool**: Vite 5.x
- **Styling**: Tailwind CSS 3.x

### Backend
- **Runtime**: Node.js 20.x LTS
- **Framework**: Express 4.x
- **Language**: TypeScript 5.x
- **Database**: PostgreSQL 16.x

### Infrastructure
- **Hosting**: AWS (us-east-1)
- **CDN**: CloudFront
- **CI/CD**: GitHub Actions
```

### Example 2: Data Schema

```markdown
# SSOT.md

## Database Schemas

### users Table

| Column      | Type         | Constraints           |
|-------------|--------------|-----------------------|
| id          | UUID         | PRIMARY KEY           |
| email       | VARCHAR(255) | UNIQUE, NOT NULL      |
| password    | VARCHAR(255) | NOT NULL (hashed)     |
| role        | ENUM         | 'user' or 'admin'     |
| created_at  | TIMESTAMP    | DEFAULT NOW()         |
| updated_at  | TIMESTAMP    | DEFAULT NOW()         |

### sessions Table

| Column      | Type         | Constraints           |
|-------------|--------------|-----------------------|
| id          | UUID         | PRIMARY KEY           |
| user_id     | UUID         | FOREIGN KEY → users   |
| token       | VARCHAR(512) | UNIQUE, NOT NULL      |
| expires_at  | TIMESTAMP    | NOT NULL              |
| created_at  | TIMESTAMP    | DEFAULT NOW()         |
```

### Example 3: API Contract

```markdown
# SSOT.md

## API Contracts

### GET /api/v2/users/:id

**Authentication**: Required (Bearer token)

**Request**:
```http
GET /api/v2/users/123e4567-e89b-12d3-a456-426614174000
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "role": "user",
  "created_at": "2025-01-15T10:30:00Z"
}
```

**Errors**:
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: User does not exist
```

### Example 4: Business Rules

```markdown
# SSOT.md

## Business Rules

### User Registration

1. Email must be unique across all users
2. Password must meet complexity requirements:
   - Minimum 12 characters
   - At least 1 uppercase letter
   - At least 1 lowercase letter
   - At least 1 number
   - At least 1 special character
3. Default role is 'user'
4. Email verification required within 24 hours

### Session Management

1. Maximum 5 concurrent sessions per user
2. Sessions expire after 24 hours of inactivity
3. Logging out invalidates only the current session
4. "Logout all devices" invalidates all user sessions
```

## Benefits of SSOT

### 1. Eliminates Inconsistency

- No conflicting definitions across documents
- Single update propagates everywhere
- Reduced confusion and errors

### 2. Improves Trust

- Clear authority on "current truth"
- Automation can rely on SSOT
- Reduces need for verification from multiple sources

### 3. Simplifies Maintenance

- Update once, reference everywhere
- Easy to audit and review
- Clear change history

### 4. Enables Automation

- CI/CD can validate against SSOT
- Code generation from canonical schemas
- Automated testing uses SSOT contracts

### 5. Facilitates Onboarding

- New team members know where to look
- Consistent terminology across project
- Clear documentation hierarchy

## Common Patterns

### Pattern 1: Reference from Documentation

```markdown
# docs/api-integration.md

## Authentication

This API uses Bearer token authentication as defined in [SSOT.md](../../SSOT.md#authentication-policy).

See SSOT.md for current endpoint URLs and token format.
```

### Pattern 2: Validate in CI

```yaml
# .github/workflows/validate.yml
name: Validate SSOT Compliance

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check API endpoints match SSOT
        run: |
          # Extract endpoints from SSOT.md
          # Validate code references match
          ./scripts/validate-ssot.sh
```

### Pattern 3: Generate Code from SSOT

```bash
# scripts/generate-types.sh
# Generate TypeScript types from SSOT.md data schemas

# Extract JSON schemas from SSOT.md
# Generate TypeScript interfaces
# Validate existing code matches
```

## Anti-Patterns to Avoid

### ❌ Multiple Sources of Truth

```
SSOT.md says: API version is v2
README.md says: API version is v3
docs/api.md says: Use v1 endpoints

Problem: Which is correct?
```

### ❌ Outdated SSOT

```
SSOT.md: Last updated 2023-06-15
Actual system: Migrated to new API in 2024-12-20

Problem: SSOT is no longer truthful
```

### ❌ Implementation as SSOT

```
# Someone asks: What's the session timeout?
Response: "Check the code in auth.service.ts"

Problem: Code is not documentation, hard to find, may have bugs
```

### ✅ Correct Approach

```
SSOT.md clearly states:
  Session timeout: 24 hours of inactivity

auth.service.ts implements this (references SSOT.md in comments)
tests/auth.test.ts validates this matches SSOT.md
```

## Maintenance Checklist

### Daily
- [ ] Review for conflicts when merging PRs
- [ ] Update SSOT when definitions change
- [ ] Add Update Log entries

### Weekly
- [ ] Scan for references to outdated definitions
- [ ] Check that downstream docs reference SSOT
- [ ] Validate implementation matches SSOT

### Monthly
- [ ] Full SSOT review for accuracy
- [ ] Archive obsolete sections
- [ ] Update links and references
- [ ] Communicate major changes to team

### Quarterly
- [ ] Compare SSOT against actual system behavior
- [ ] Audit for completeness
- [ ] Refactor structure if needed
- [ ] Train new team members on SSOT usage

## Adoption Checklist

- [ ] Create `SSOT.md` at repository root
- [ ] Define initial canonical terms and schemas
- [ ] Document current policies and workflows
- [ ] Add Update Log section
- [ ] Update AGENTS.md to reference SSOT
- [ ] Update README.md to link to SSOT
- [ ] Migrate scattered definitions into SSOT
- [ ] Remove or deprecate redundant definitions elsewhere
- [ ] Train team on SSOT workflow
- [ ] Set up CI validation (optional)
- [ ] Establish regular review cadence

## Further Resources

- [Single Source of Truth - Wikipedia](https://en.wikipedia.org/wiki/Single_source_of_truth) [R1]
- [The Twelve-Factor App](https://12factor.net/) [R2] - Configuration and environment management
- [Write the Docs - Documentation as Code](https://www.writethedocs.org/guide/docs-as-code/) [R3]
- Data governance best practices
- Documentation architecture patterns

## References

- [R1] [Single source of truth - Wikipedia](https://en.wikipedia.org/wiki/Single_source_of_truth) - Foundational SSOT concept and principles
- [R2] [The Twelve-Factor App - III. Config](https://12factor.net/config) - Configuration management and single source principles for cloud-native applications
- [R3] [Documentation as Code - Write the Docs](https://www.writethedocs.org/guide/docs-as-code/) - Version-controlled documentation practices

## Update Log

- 2025-10-23: Added official references (Wikipedia, Twelve-Factor App, Write the Docs) for SSOT principles and documentation best practices.
- 2025-10-20: Published the initial edition (organized around SSOT principles and real-world AI-assisted development practices).

---

**Remember**: SSOT is about clarity and consistency. Maintain one authoritative source, reference it everywhere, and keep it current. When in doubt about any definition, policy, or data contract—check the SSOT first.
