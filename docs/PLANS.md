---
title: ExecPlan and PLANS.md
slug: exec-plan
summary: "AI-driven task management"
type: spec
tags: [topic, ai-first, agent, planning, execution, all-model]
last_updated: 2025-11-16
---

# Topic: ExecPlan and PLANS.md — Model-Agnostic Execution Planning for AI-Driven Development

## Agent Contract

- **PURPOSE**:
  - Define a vendor-neutral specification for long-running AI agent task management using living Markdown documents
  - Enable coding agents (OpenAI Codex, Claude, GPT-5, Gemini, etc.) to autonomously execute multi-hour complex tasks
  - Maintain comprehensive context and progress tracking across extended development sessions
- **USE_WHEN**:
  - Implementing complex features requiring multiple hours or days of work
  - Managing AI agent sessions that span multiple context windows
  - Coordinating work across different AI models and development environments
  - Building self-contained task specifications for autonomous execution
- **DO_NOT_USE_WHEN**:
  - Simple single-file edits or trivial changes
  - Tasks completable in under 30 minutes
  - Projects without AI agent involvement
  - Real-time collaborative editing where multiple humans are actively working
- **PRIORITY**:
  - ExecPlan methodology takes precedence over ad-hoc task management when working with AI agents
  - Self-containment requirement overrides external documentation references
  - Living document updates are mandatory, not optional
- **RELATED_TOPICS**:
  - agents-md
  - task-decomposition
  - context-management
  - ai-driven-development

---

## TL;DR

- **WHAT**: ExecPlan is a structured Markdown-based methodology for managing multi-hour AI-driven development tasks through living documents that agents continuously update
- **WHY**: Enables AI agents to maintain context, track progress, and autonomously complete complex tasks without losing state across sessions or context windows
- **WHEN**: Use for any development task requiring >30 minutes of AI agent work, complex features, significant refactors, or multi-step implementations
- **HOW**: Create a PLANS.md file with mandatory sections (Progress, Surprises, Decisions, Outcomes), maintain it as work progresses, and ensure complete self-containment
- **WATCH_OUT**: Never rely on external documentation links; all knowledge must be embedded directly in the plan for true self-containment

---

## Canonical Definitions

### ExecPlan

**Definition**: A self-contained, living Markdown document that serves as both specification and execution guide for AI agents performing complex multi-hour development tasks.

**Scope**:
- **Includes**:
  - Complete task specification with acceptance criteria
  - Progress tracking with timestamped checkboxes
  - Decision logging and discovery documentation
  - All necessary context and knowledge embedded
  - Recovery and rollback strategies
- **Excludes**:
  - External documentation dependencies
  - Undefined technical jargon
  - Implementation details without user-visible outcomes
  - Static requirements that never update

**Related Concepts**:
- **Similar**: Project plans, technical specifications, runbooks
- **Contrast**: Simple TODO lists, static requirements documents, issue tickets
- **Contains**: Milestones, concrete steps, validation criteria, living sections

**Example**:

```markdown
# ExecPlan: Implement OAuth2 Authentication

## Purpose/Big Picture
Enable users to sign in using Google OAuth2, visible as a "Sign in with Google"
button that redirects to Google and returns authenticated users to the dashboard.

## Progress
- [x] 2025-11-16 14:00 - Read existing auth implementation
- [x] 2025-11-16 14:15 - Set up Google OAuth2 credentials
- [ ] Implement OAuth2 callback handler
- [ ] Add session management

## Surprises & Discoveries
- 2025-11-16 14:10 - Existing auth uses JWT, need to integrate OAuth2 tokens
  with JWT session management (evidence: auth.ts:42 shows JWT implementation)
```

**Sources**: [R1]

### Living Document Sections

**Definition**: Four mandatory sections in every ExecPlan that must be continuously updated throughout task execution to maintain accurate state and learnings.

**Scope**:
- **Includes**:
  - **Progress**: Granular checkbox lists with timestamps
  - **Surprises & Discoveries**: Unexpected findings with evidence
  - **Decision Log**: Choices made with rationale and attribution
  - **Outcomes & Retrospective**: Achievement summary and lessons
- **Excludes**:
  - Static requirements that never change
  - Placeholders without actual content
  - Sections added but never maintained

**Related Concepts**:
- **Similar**: Agile sprint retrospectives, decision records, progress reports
- **Contrast**: Fixed specifications, waterfall documentation
- **Contains**: Timestamps, evidence, rationale, attribution

**Example**:

```markdown
## Decision Log
- 2025-11-16 14:20 - Chose to use passport.js over manual OAuth2 implementation
  Rationale: Well-tested, reduces security risks, 5 minutes vs 2 hours
  Author: AI Agent (Claude)

- 2025-11-16 14:35 - Storing refresh tokens in encrypted database column
  Rationale: Enables offline access, follows security best practices
  Author: AI Agent (Claude)
```

**Sources**: [R1]

### Self-Containment Principle

**Definition**: The requirement that an ExecPlan must contain all knowledge, context, and instructions necessary for successful implementation without any external references.

**Scope**:
- **Includes**:
  - Embedded code examples instead of links
  - Defined terminology for all technical terms
  - Complete context about current system state
  - Full command sequences with expected outputs
- **Excludes**:
  - Links to external documentation as primary source
  - Assumptions about prior knowledge
  - References to undefined concepts
  - Incomplete instructions requiring outside research

**Related Concepts**:
- **Similar**: Hermetic builds, reproducible research, literate programming
- **Contrast**: Link-heavy documentation, reference manuals, tutorial series
- **Contains**: Embedded knowledge, complete context, defined terms

**Example**:

```markdown
## Context and Orientation
The application currently uses session-based authentication with Express.js.
Sessions are stored in PostgreSQL using connect-pg-simple. The auth flow:

1. User submits credentials to POST /api/login
2. Server validates against bcrypt hashes in users table
3. Session created with user_id stored
4. Session cookie sent to browser

OAuth2 will ADD to this by providing an alternative path through Google.

Technical terms:
- OAuth2: Protocol where users authenticate via Google, not our passwords
- JWT: JSON Web Token, a signed JSON object used as auth credential
- Refresh token: Long-lived token to get new access tokens without re-login
```

**Sources**: [R1]

---

## Core Patterns

### Pattern: Three-Phase Development Process

**Intent**: Separate planning, implementation, and verification into distinct AI agent sessions to maximize focus and reduce context pollution.

**Context**: When using AI agents for complex features requiring multiple hours of work across potentially multiple context windows.

**Implementation**:

```markdown
# Phase 1: Plan Only (Session 1)
User: "I need to implement real-time notifications. Create a detailed ExecPlan
       but write no code yet."
Agent: [Creates comprehensive PLANS.md with all sections]

# Phase 2: Implementation (Session 2 - Fresh Context)
User: "Execute the plan in ./plans/notifications-PLANS.md"
Agent: [Reads plan, implements systematically, updates Progress section]

# Phase 3: Verify & Refactor (Session 3 - Fresh Context)
User: "Verify the implementation matches the ExecPlan acceptance criteria"
Agent: [Runs tests, confirms behaviors, updates Outcomes section]
```

**Key Principles**:
- **Clean Context**: Each phase starts with reset context to avoid confusion
- **Plan Immutability**: During execution, only Progress/Surprises update, not the plan itself
- **Verification Independence**: Different perspective catches issues

**Trade-offs**:
- ✅ **Advantages**: Clear separation of concerns, reduced errors, better documentation
- ⚠️ **Disadvantages**: More total time, potential context switching overhead
- 💡 **Alternatives**: Single-session for simple tasks under 30 minutes

**Sources**: [R1]

### Pattern: Milestone-Based Structuring

**Intent**: Decompose complex tasks into independently verifiable milestones that incrementally build toward the goal.

**Context**: Large features that would overwhelm a single context window or require natural breaking points for validation.

**Implementation**:

```markdown
## Milestone 1: Database Schema and Models
Scope: Create tables and ORM models for notifications

Deliverables:
- Migration file: migrations/001_create_notifications.sql
- Model file: models/Notification.ts
- Test file: tests/models/Notification.test.ts

Commands to verify:
```bash
npm run migrate:up
npm test models/Notification.test.ts
```

Expected output:
```
✓ Migration 001_create_notifications.sql applied
✓ Notification model creates records
✓ Notification model validates required fields
```

## Milestone 2: WebSocket Infrastructure
Scope: Set up Socket.io for real-time connections

[Continue with same structure...]
```

**Key Principles**:
- **Independent Verification**: Each milestone produces observable results
- **Incremental Progress**: Later milestones build on earlier ones
- **Clear Boundaries**: No ambiguity about what belongs in each milestone

**Trade-offs**:
- ✅ **Advantages**: Natural checkpoints, easier debugging, partial delivery possible
- ⚠️ **Disadvantages**: Some overhead in milestone design, potential for over-engineering
- 💡 **Alternatives**: Continuous flow for smaller tasks

**Sources**: [R1]

---

## Decision Checklist

- [ ] **Self-Containment**: Plan includes all necessary knowledge without external links [R1]
  - **Verify**: No critical information requires following external URLs
  - **Impact**: AI agent fails or hallucinates if missing context
  - **Mitigation**: Embed code examples, define all terms, include full context

- [ ] **Living Sections Present**: All four mandatory sections exist and are maintained [R1]
  - **Verify**: Progress, Surprises, Decisions, Outcomes sections have real content
  - **Impact**: Lost learnings and inability to resume work
  - **Mitigation**: Update sections immediately when events occur

- [ ] **Novice-Enablement**: Someone unfamiliar with codebase can execute successfully [R1]
  - **Verify**: No assumed knowledge about project structure or conventions
  - **Impact**: AI agents make incorrect assumptions
  - **Mitigation**: Document current state, file locations, and conventions explicitly

- [ ] **Observable Outcomes**: Acceptance criteria describe user-visible behaviors [R1]
  - **Verify**: Each criterion can be demonstrated with commands and outputs
  - **Impact**: Unclear when task is actually complete
  - **Mitigation**: Replace internal descriptions with external behaviors

- [ ] **Recovery Paths**: Plan includes rollback and retry strategies [R1]
  - **Verify**: Clear instructions for handling failures and retrying
  - **Impact**: Stuck state when errors occur
  - **Mitigation**: Add "If this fails..." sections with recovery steps

---

## Anti-patterns / Pitfalls

### Anti-pattern: Link-Heavy Plans

**Symptom**: Plan contains multiple "See [URL] for details" or "Follow documentation at [link]"

**Why It Happens**: Natural tendency to reference rather than embed, especially for well-known technologies

**Impact**:
- AI agents cannot access external URLs reliably
- Context lost when links change or become unavailable
- Different agents may interpret external content differently

**Solution**: Embed the essential parts directly in the plan with attribution

**Example**:

```markdown
# ❌ Anti-pattern
Configure OAuth2 following Google's guide at:
https://developers.google.com/identity/protocols/oauth2

# ✅ Correct pattern
Configure OAuth2 with Google (based on official docs):

1. Create credentials in Google Cloud Console:
   - Go to APIs & Services > Credentials
   - Create OAuth 2.0 Client ID
   - Set redirect URI to: http://localhost:3000/auth/google/callback

2. Required scopes for basic profile:
   - openid - Required for OpenID Connect
   - email - Access to user's email
   - profile - Access to basic profile info

Code example:
[Embed actual configuration code here]
```

**Sources**: [R1]

### Anti-pattern: Static Requirements Lists

**Symptom**: Plan has requirements that never update despite discoveries during implementation

**Why It Happens**: Treating ExecPlan like traditional specifications instead of living documents

**Impact**:
- Decisions made without documentation
- No learning captured for future work
- Mismatch between plan and implementation

**Solution**: Continuously update all sections as work progresses

**Example**:

```markdown
# ❌ Anti-pattern - Never updates
## Requirements
- Must support Google OAuth2
- Must store user sessions
- Must redirect to dashboard

# ✅ Correct pattern - Living document
## Requirements (Updated)
- Must support Google OAuth2
  - 2025-11-16: Added requirement for refresh token storage
- Must store user sessions
  - 2025-11-16: Decided on PostgreSQL over Redis for persistence
- Must redirect to dashboard
  - 2025-11-16: Added /onboarding redirect for first-time users
```

**Sources**: [R1]

---

## Evaluation

### Metrics

**Self-Containment Score**: Percentage of technical decisions that can be understood without external references
- **Why It Matters**: Directly impacts AI agent success rate
- **Target**: 100% of critical decisions explained in-plan
- **Measurement**: Count external links vs embedded knowledge
- **Tools**: Automated link checker, content analysis
- **Frequency**: Before each execution phase

**Living Document Freshness**: Time since last update to living sections
- **Why It Matters**: Stale sections indicate lost learnings
- **Target**: Updated within 15 minutes of any discovery
- **Measurement**: Timestamp analysis of section updates
- **Tools**: Git history, timestamp parsing
- **Frequency**: Continuous during execution

**Sources**: [R1]

### Testing Strategies

**Unit Tests**:
- Each milestone produces verifiable outputs
- Commands in plan actually execute successfully
- File paths and names match actual structure

**Integration Tests**:
- Complete plan execution achieves stated purpose
- All acceptance criteria demonstrably met
- No undefined terms or broken references

**Performance Benchmarks**:
- Plan execution time within estimated bounds
- Token usage for AI agents remains under context limits
- Update frequency meets freshness targets

### Success Criteria

- [ ] AI agent can execute plan without asking clarifying questions
- [ ] All four living sections contain meaningful, timestamped content
- [ ] Another developer can understand what was built and why
- [ ] No critical information requires following external links
- [ ] Plan accurately reflects final implementation state

---

## Update Log

- **2025-11-16** – Initial document creation based on OpenAI Cookbook specification (Author: Claude)

---

## See Also

### Prerequisites
- [agents-md] – AI agent README format that complements ExecPlans
- [markdown-syntax] – Basic Markdown knowledge required for formatting

### Related Topics
- [task-decomposition] – Strategies for breaking down complex work
- [context-management] – Managing AI agent context windows effectively
- [ai-driven-development] – Broader patterns for AI-assisted coding

### Advanced / Platform-specific
- [codex-optimization] – OpenAI Codex-specific optimizations
- [multi-agent-coordination] – Coordinating multiple AI agents on one plan
- [plan-versioning] – Managing ExecPlan evolution over time

---

## References

- [R1] OpenAI. "Using PLANS.md for multi-hour problem solving." OpenAI Cookbook. https://cookbook.openai.com/articles/codex_exec_plans (accessed 2025-11-16)

---

**Document ID**: `docs/PLANS.md`
**Canonical URL**: `https://github.com/artificial-intelligence-first/ssot/blob/main/docs/PLANS.md`
**License**: MIT