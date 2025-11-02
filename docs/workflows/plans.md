---
title: Plans
slug: plans
status: living
last_updated: 2025-11-01
tags: [plans, execplans, project-management, documentation, workflow]
summary: "ExecPlan workflow for documenting and tracking complex, multi-step development initiatives."
authors: []
sources:
  - { id: R1, title: "OpenAI Cookbook - Exec Plans", url: "https://cookbook.openai.com/articles/codex_exec_plans", accessed: "2025-10-23" }
  - { id: R2, title: "Agile User Stories - Mountain Goat Software", url: "https://www.mountaingoatsoftware.com/agile/user-stories", accessed: "2025-10-23" }
  - { id: R3, title: "Architecture Decision Records (ADR)", url: "https://adr.github.io/", accessed: "2025-10-23" }
---

# Plans

> **For Humans**: This guide explains the ExecPlan workflow for documenting multi-step initiatives, inspired by OpenAI Cookbook patterns.
>
> **For AI Agents**: ExecPlans are execution specifications that keep multi-hour coding tasks aligned. Maintain these documents throughout work execution, updating progress, decisions, and discoveries in real-time.

## Overview

ExecPlans are living documents that guide complex, multi-step development work. They combine project planning, technical specifications, and real-time progress tracking into a single, evolving document that both humans and AI agents can follow.

## Format Specification

### Basic Structure

```markdown
# PROJECT_NAME ExecPlan

## Objective
Clear statement of what will be accomplished.

## Context
- Background information
- Current state
- Constraints and requirements

## Success Criteria
- [ ] Measurable outcome 1
- [ ] Measurable outcome 2
- [ ] Measurable outcome 3

## Technical Approach
High-level strategy and key technical decisions.

## Execution Steps
1. [ ] Step with clear action
2. [ ] Next step building on previous
3. [ ] Final validation step

## Progress Log
### YYYY-MM-DD HH:MM
- Completed: What was done
- Decision: Key choice made
- Discovery: New information found
- Blocker: Issue encountered

## Open Questions
- [ ] Question needing resolution
- [ ] Another uncertainty

## Results
Summary of what was delivered and lessons learned.
```

## Core Patterns

### Pattern: Progressive Elaboration

Start high-level, add detail as you learn:

```markdown
## Execution Steps (Initial)
1. [ ] Implement authentication
2. [ ] Add user management
3. [ ] Deploy to production

## Execution Steps (Refined)
1. [ ] Implement authentication
   - [ ] Set up OAuth provider
   - [ ] Create login endpoints
   - [ ] Add session management
2. [ ] Add user management
   - [ ] Design user schema
   - [ ] Create CRUD operations
   - [ ] Add role-based access
3. [ ] Deploy to production
   - [ ] Configure environment
   - [ ] Set up CI/CD
   - [ ] Perform smoke tests
```

### Pattern: Decision Recording

Document choices inline:

```markdown
## Progress Log
### 2025-11-01 10:30
- **Decision**: Chose PostgreSQL over MySQL
  - Reason: Better JSON support for our use case
  - Trade-off: Slightly higher operational complexity
  - Reference: [SSOT Guide – Data Contracts](../core/ssot-guide.md#data-contracts)
```

### Pattern: Blocker Management

Track and resolve impediments:

```markdown
## Open Questions
- [x] ~~Which authentication provider?~~ → Resolved: Auth0
- [ ] How to handle rate limiting? → **BLOCKER**
  - Option A: Client-side retry
  - Option B: Queue-based approach
  - Need: Performance requirements from product
```

## Workflow

### 1. Initiation

```markdown
# Feature X ExecPlan

## Objective
Implement user notification system with email and SMS channels.

## Context
- Current: No notification system
- Users: 10K daily active
- SLA: 99.9% delivery rate

## Success Criteria
- [ ] Email notifications working
- [ ] SMS notifications working
- [ ] User preferences honored
- [ ] Analytics dashboard updated
```

### 2. Execution

Update in real-time as work progresses:

```markdown
## Execution Steps
1. [x] Design notification schema
2. [x] Implement email service
3. [ ] **IN PROGRESS** Implement SMS service
   - [x] Research providers
   - [x] Select Twilio
   - [ ] Integration development ← CURRENT
4. [ ] Add user preferences
5. [ ] Update analytics
```

### 3. Completion

Summarize outcomes:

```markdown
## Results

### Delivered
- Email and SMS notification channels
- User preference management
- Real-time analytics integration

### Metrics
- Delivery rate: 99.94% (exceeds SLA)
- Average latency: 1.2 seconds
- Cost per message: $0.012

### Lessons Learned
1. Twilio's retry mechanism conflicts with our queue
2. Batch sending reduces costs by 40%
3. User preferences need versioning for compliance
```

## Anti-patterns

### Over-Planning
❌ **Wrong**: 50+ detailed steps before starting
✅ **Right**: 5-10 high-level steps, refined progressively

### Silent Updates
❌ **Wrong**: Changing plan without documenting why
✅ **Right**: Progress log entry for each change

### Abandoned Plans
❌ **Wrong**: Plan becomes stale after day 1
✅ **Right**: Living document updated throughout

## Evaluation

### Quality Metrics

- **Clarity**: Objective understood in < 30 seconds
- **Completeness**: All decisions documented
- **Currency**: Last update within 24 hours of work
- **Traceability**: Can reconstruct decision path
- **Actionability**: Next step always clear

### Review Checklist

- [ ] Objective matches delivered result
- [ ] Success criteria measurable
- [ ] All blockers resolved or documented
- [ ] Decisions include rationale
- [ ] Lessons learned captured

## Platform Integration

### GitHub Integration

```yaml
# .github/ISSUE_TEMPLATE/execplan.yml
name: ExecPlan
description: Create an execution plan
labels: [execplan]
body:
  - type: textarea
    id: objective
    label: Objective
    required: true
  - type: textarea
    id: success-criteria
    label: Success Criteria
    value: |
      - [ ] Criterion 1
      - [ ] Criterion 2
```

### AI Agent Usage

```python
# AI agent reading execplan
def load_execplan(path):
    with open(path) as f:
        plan = parse_markdown(f.read())

    return {
        'objective': plan.get('## Objective'),
        'current_step': find_in_progress(plan),
        'blockers': extract_blockers(plan),
        'decisions': extract_decisions(plan)
    }

# AI agent updating progress
def update_progress(plan_path, update):
    plan = load_execplan(plan_path)

    # Add to progress log
    timestamp = datetime.now().isoformat()
    log_entry = f"### {timestamp}\n{update}\n"

    append_to_section(plan_path, '## Progress Log', log_entry)
```

## Examples

### Feature Development

```markdown
# Dark Mode Feature ExecPlan

## Objective
Add dark mode support across web application.

## Success Criteria
- [ ] Theme toggle in settings
- [ ] Persistent user preference
- [ ] All components support both themes
- [ ] No accessibility regressions

## Execution Steps
1. [x] Create theme context
2. [x] Design color palette
3. [ ] Update components
   - [x] Navigation
   - [ ] Forms ← CURRENT
   - [ ] Tables
4. [ ] Add toggle UI
5. [ ] Test accessibility
```

### Bug Investigation

```markdown
# Memory Leak Investigation ExecPlan

## Objective
Identify and fix memory leak in production API.

## Context
- Symptom: Memory usage grows 100MB/hour
- Started: After v2.3.0 deployment
- Impact: Daily restarts required

## Technical Approach
Binary search through recent commits, profile suspicious code.

## Progress Log
### 2025-11-01 14:00
- Discovery: Leak correlates with WebSocket connections
- Test: Disabled WebSocket pooling
- Result: Leak stopped

### 2025-11-01 15:30
- Root cause: Event listeners not removed on disconnect
- Fix: Added cleanup in connection handler
- Verification: Memory stable over 4 hours
```

## See Also

- [Changelog Guide](./changelog.md)
- [AGENTS.md](../../AGENTS.md) - AI agent operational documentation
- [Contributing Guide](../governance/contributing.md)

## References

- [R1] OpenAI Cookbook - Exec Plans. https://cookbook.openai.com/articles/codex_exec_plans (accessed 2025-10-23)
- [R2] Agile User Stories - Mountain Goat Software. https://www.mountaingoatsoftware.com/agile/user-stories (accessed 2025-10-23)
- [R3] Architecture Decision Records (ADR). https://adr.github.io/ (accessed 2025-10-23)
