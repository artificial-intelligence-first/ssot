---
title: AGENTS Guide
slug: agents-guide
status: living
last_updated: 2025-11-01
tags: agents, conventions, documentation, workflow, best-practices
summary: Comprehensive guide to AGENTS.md convention for AI-agent-friendly operational documentation.
authors: Naru Kijima
sources:
  - { id: R1, title: "AGENTS.md Official Website", url: "https://agents.md", accessed: "2025-10-23" }
  - { id: R2, title: "Cursor - AI-first Code Editor", url: "https://cursor.com", accessed: "2025-10-23" }
  - { id: R3, title: "Jules - Google AI Coding Agent", url: "https://jules.google", accessed: "2025-10-23" }
  - { id: R4, title: "Amp - AI Development Platform", url: "https://ampcode.com", accessed: "2025-10-23" }
  - { id: R5, title: "Factory - Autonomous Software Engineering", url: "https://factory.ai", accessed: "2025-10-23" }
  - { id: R6, title: "DeepWiki: openai/agents.md Documentation", url: "https://deepwiki.com/openai/agents.md", accessed: "2025-10-23" }
---

# AGENTS Guide

> **For Humans**: This guide explains the AGENTS.md convention for structuring AI-agent-friendly documentation in your repositories.
>
> **For AI Agents**: AGENTS.md provides machine-focused operational knowledge complementing human-facing documentation. Read this to understand project conventions, development workflows, and automation patterns.

## Overview

AGENTS.md is a Markdown convention introduced by OpenAI and partner teams to provide AI coding agents with a predictable, machine-focused playbook. The format has been adopted by **over 20,000 open-source repositories** and is recognized by major agent platforms.

### Official Partners and Contributors

The AGENTS.md specification was developed collaboratively by:

- **OpenAI** - Codex platform [R1]
- **Cursor** - AI-first code editor [R2]
- **Google** - Jules coding agent [R3]
- **Amp** - AI development platform [R4]
- **Factory** - AI software development [R5]

### Supported AI Coding Tools

Major agent platforms that recognize and consume AGENTS.md files:

- **OpenAI Codex** - Code generation and completion
- **Cursor** - AI-first code editor with native AGENTS.md support
- **Jules** (Google) - Google's AI coding agent
- **Amp** - AI-powered development workflows
- **Factory** - Autonomous software engineering
- **RooCode** - AI coding assistant
- **VS Code AI Extensions** - Growing ecosystem support
- **Custom Agents** - Extensible to bespoke implementations

**Key Purpose**: Give AI agents the operational knowledge they need to edit and validate code safely without relying solely on human-facing documentation. [R1]

## Core Principles

### 1. Placement & Scope

- Place `AGENTS.md` at the repository root
- Large monorepos may include nested `AGENTS.md` files for specific subsystems
- Agents read the closest (most specific) instructions when multiple files exist
- Explicit user prompts override file guidance [R6]

**File Specifications**: [R6]
- **File name**: Exactly `AGENTS.md` (case-sensitive)
- **Encoding**: UTF-8
- **Format**: Standard Markdown (.md)
- **Line endings**: Unix-style LF preferred

**Precedence Hierarchy** (highest to lowest): [R6]
1. Explicit user chat prompts
2. Closest AGENTS.md to edited file
3. Parent directory AGENTS.md files
4. Root project AGENTS.md

### 2. Content Structure

AGENTS.md typically includes sections covering:

- **Development environment setup** - Tools, dependencies, workspace configuration
- **Build & test commands** - How to compile, run tests, validate changes
- **Linting & formatting** - Code style enforcement, quality checks
- **Security policies** - Credential handling, secret management, security scanning
- **PR & commit policies** - Contribution workflow, review requirements

### 3. Machine-First, Human-Readable

- Write clear, imperative instructions
- Use plain language while being technically precise
- Include concrete commands and examples
- Focus on "what" and "how" over "why" (save philosophy for README.md)

## Standard Template

```markdown
# AGENTS.md

## Dev Environment Tips
- List required tools, versions, package managers
- Document workspace setup commands
- Explain how to navigate the codebase structure
- Note any non-obvious configuration requirements

## Testing Instructions
- Where to find test files and CI configuration
- Commands to run full test suite
- How to run specific test subsets
- Requirements before merging (all tests passing, coverage thresholds, etc.)
- Expectations around adding/updating tests with code changes

## Build & Deployment
- Build commands for different environments
- How to verify successful builds
- Deployment procedures (if applicable)
- Artifact locations and validation

## Linting & Code Quality
- Linter configuration and commands
- Formatting tools and auto-fix commands
- Type checking requirements
- When to run quality checks (pre-commit, pre-PR, etc.)

## PR Instructions
- PR title/description format
- Required checks before submitting
- Review process expectations
- Branch naming conventions
- Commit message guidelines

## Security & Credentials
- How to handle secrets and credentials
- Security scanning tools and requirements
- Dependency vulnerability checks
- Prohibited practices
```

## Best Practices

### For Repository Maintainers

1. **Keep it updated** - AGENTS.md should reflect current practices
2. **Be specific** - Include exact commands, not just concepts
3. **Test instructions** - Verify that agents can successfully follow the guidance
4. **Link to details** - Reference deeper documentation when needed
5. **Version control** - Track changes to understand evolution of practices
6. **Use imperative language** - Write direct commands ("Run test", "Check file") rather than suggestions ("You might want to...") [R6]
7. **Focus on actionable steps** - Provide concrete procedures over conceptual explanations [R6]
8. **Include context switching** - For monorepos, specify navigation commands between packages [R6]

### For AI Agents Reading This

1. **Prioritize AGENTS.md** over general documentation when performing coding tasks
2. **Check for nested files** in subdirectories of large projects
3. **Follow instructions literally** unless explicitly overridden by the user
4. **Report ambiguities** back to users rather than guessing
5. **Reference specific sections** when explaining your actions
6. **Execute commands as specified** - When testing commands are listed, run them automatically [R6]
7. **Respect precedence hierarchy** - User prompts override file instructions [R6]

### Anti-Patterns to Avoid

**❌ Overly verbose explanations**: [R6]
- Agents need concise, actionable instructions, not educational content
- Save detailed "why" explanations for README.md

**❌ Outdated command references**:
- Ensure commands reference current package managers and tools
- Stale instructions reduce agent effectiveness

**❌ Human-centric language**:
- Avoid: "Please remember to run tests"
- Prefer: "Run `npm test` before committing"

**❌ Missing monorepo context**:
- Include workspace navigation commands
- Specify package filtering (e.g., `--filter <package-name>`)

## Sample Workflow: pnpm + Turborepo + Vite

```markdown
## Dev Environment Tips
- Use `pnpm dlx turbo run where <project_name>` to jump to a package instead of scanning with `ls`.
- Run `pnpm install --filter <project_name>` to add the package to your workspace so Vite, ESLint, and TypeScript can see it.
- Use `pnpm create vite@latest <project_name> -- --template react-ts` to spin up a new React + Vite package with TypeScript checks ready.
- Check the name field inside each package's package.json to confirm the right name—skip the top-level one.

## Testing Instructions
- Find the CI plan in the .github/workflows folder.
- Run `pnpm turbo run test --filter <project_name>` to run every check defined for that package.
- From the package root you can just call `pnpm test`. The commit should pass all tests before you merge.
- To focus on one step, add the Vitest pattern: `pnpm vitest run -t "<test name>"`.
- Fix any test or type errors until the whole suite is green.
- After moving files or changing imports, run `pnpm lint --filter <project_name>` to be sure ESLint and TypeScript rules still pass.
- Add or update tests for the code you change, even if nobody asked.

## PR Instructions
- Title format: [<project_name>] <Title>
- Always run `pnpm lint` and `pnpm test` before committing.
- Once tests pass, run `pnpm lint` from the repo root in case there's shared tooling.
- List every change in your PR description with checkboxes, calling out the tests you ran plus any follow-up work.
- Ask for review by tagging your team's Slack or GitHub handle. Include context for risky changes (e.g., migrations, rewrites).
- Don't merge when CI is red. Leave review feedback in the PR so others know the current status.
- Update documentation and changelog entries as necessary.
```

> **Note**: Treat this as a sample. Replace commands, tooling, and review policies with the specifics of your repository.

## Integration with Other Conventions

### AGENTS.md + SSOT.md

- Use AGENTS.md for operational procedures
- Use SSOT.md for canonical data definitions and terminology
- Cross-reference when procedural steps depend on canonical definitions

### AGENTS.md + CHANGELOG.md

- AGENTS.md explains *how* to contribute
- CHANGELOG.md tracks *what* was contributed
- Keep PR instructions in AGENTS.md aligned with changelog update requirements

### AGENTS.md + PLANS.md (ExecPlans)

- AGENTS.md provides standing procedures
- ExecPlans document specific multi-step initiatives
- ExecPlans should reference relevant AGENTS.md sections for standard practices

## Tool Support

### OpenAI Code Generation Models
The latest OpenAI code generation models (e.g., GPT-4.1 Code, GPT-4.1 Mini) can rely on AGENTS.md to understand repository-specific procedures. Review each model's documentation to confirm the most recent behavior. [R1]

### Cursor
Cursor treats AGENTS.md as the project-specific workflow guide with native format support. [R2]

### Jules (Google)
Google's Jules coding agent natively consumes AGENTS.md for project-specific context. [R3]

### Amp
Amp integrates AGENTS.md into its AI-powered development workflows. [R4]

### Factory
Factory's autonomous software engineering platform uses AGENTS.md for operational guidance. [R5]

### RooCode
RooCode AI coding assistant supports AGENTS.md format for project instructions. [R6]

### VS Code AI Extensions
AI-assisted extensions for VS Code increasingly ingest AGENTS.md as contextual guidance.

### Custom Agents
For bespoke agents, implement an AGENTS.md parser so they inherit standard operating procedures.

> **Support Note**: Compatibility may change—review each tool's release notes regularly.

## Real-World Examples

The AGENTS.md format has been adopted across diverse technology stacks and project types. Notable implementations include: [R6]

### Notable Open-Source Projects

**openai/codex** (Rust) [R6]
- General-purpose CLI tooling for AI coding agents
- Cargo commands, clippy rules, and Rust-specific workflows

**apache/airflow** (Python) [R6]
- Platform to programmatically author, schedule, and monitor workflows
- pip install procedures, pytest patterns, mypy configuration

**temporalio/sdk-java** (Java) [R6]
- Java SDK for Temporal workflow orchestration
- Maven/Gradle setup, JUnit testing patterns

**PlutoLang/Pluto** (C++) [R6]
- Superset of Lua 5.4 focused on general-purpose programming
- CMake build system, compiler flag specifications

### Adoption Patterns

Projects using AGENTS.md span:
- **Monorepo architectures** with nested configuration
- **Single-package applications** with focused instructions
- **Library/SDK projects** with API usage examples
- **Infrastructure tools** with deployment workflows

## Conflict Resolution

When guidance conflicts arise:

1. **Most specific wins** - Nested AGENTS.md overrides root AGENTS.md
2. **User commands override** - Explicit user instructions take precedence over file guidance
3. **Newer over older** - Within the same file, later sections clarify earlier ones
4. **Explicit over implicit** - Direct commands override general principles

## Frequently Asked Questions

### Are there required fields?

No. AGENTS.md uses standard Markdown without mandatory structure. The format is intentionally flexible—use sections that make sense for your project. [R6]

### What if instructions conflict?

The system uses proximity-based precedence: [R6]
- File closest to edited code wins
- User prompts override all file-based instructions
- Nested AGENTS.md files override parent directory files

### Will the agent run testing commands automatically?

Yes, when commands are explicitly listed in AGENTS.md (e.g., "Run `npm test` before committing"), agents will typically execute them as part of their workflow. [R6]

### Can I update it later?

Absolutely. Treat AGENTS.md as **living documentation** that evolves with your project. Update it whenever workflows change, new tools are adopted, or best practices are refined. [R6]

### How do I migrate existing docs to AGENTS.md?

For backward compatibility, create a symbolic link: [R6]

```bash
mv DEVELOPMENT.md AGENTS.md
ln -s AGENTS.md DEVELOPMENT.md
```

This preserves existing references while adopting the standard format.

### What about monorepos?

Use nested AGENTS.md files for each package or subsystem. Agents will prioritize the closest file to the code they're editing. [R6]

## Adoption Checklist

- [ ] Create `AGENTS.md` at repository root
- [ ] Document development environment setup
- [ ] Specify test execution and validation procedures
- [ ] Define PR and commit requirements
- [ ] Include linting and code quality standards
- [ ] Add security and credential handling policies
- [ ] Review and update with team
- [ ] Link from README.md for human discoverability
- [ ] Test with AI agents to verify clarity
- [ ] Establish regular review cadence (e.g., quarterly)

## Community & Standards

- **Specification**: Maintained openly on GitHub (MIT License)
- **Discussion**: Active community feedback on scope and evolution
- **Vendor Neutrality**: Designed to work across AI platforms
- **Evolution**: Ongoing refinement based on real-world usage

## Further Resources

- [OpenAI AGENTS.md Specification](https://agents.md)
- [GitHub Repository](https://github.com/openai/agents.md)
- [DeepWiki Documentation](https://deepwiki.com/openai/agents.md)
- Growing collection of community examples
- Industry coverage and adoption case studies

## References

- [R1] [OpenAI AGENTS.md Official Website](https://agents.md) - Official specification and documentation
- [R2] [Cursor](https://cursor.com) - AI-first code editor with native AGENTS.md support
- [R3] [Jules - Google](https://jules.google) - Google's AI coding agent platform
- [R4] [Amp](https://ampcode.com) - AI-powered development platform
- [R5] [Factory](https://factory.ai) - Autonomous software engineering platform
- [R6] [DeepWiki: openai/agents.md](https://deepwiki.com/openai/agents.md) - Comprehensive community documentation and implementation examples (Accessed: 2025-10-23)

## Update Log

- 2025-10-23: Added comprehensive information from DeepWiki including official partners, 20k+ repository adoption statistics, real-world examples, FAQ section, and detailed file specifications.
- 2025-10-20: Published the initial edition (reassembled from community practices and the public specification).

---

**Remember**: AGENTS.md is about making AI agents effective collaborators. Keep instructions clear, commands concrete, and guidance current.
