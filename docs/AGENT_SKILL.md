---
title: Agent Skill All Model
slug: agent-skill
summary: "Agent Skill Spec"
document_type: spec
tags: [topic, ai-first, agent, skill, specification]
last_updated: 2025-11-13
---

# Topic: Agent Skill All Model - Universal Specification

## Agent Contract

- **PURPOSE**:
  - Define a vendor-neutral specification for agent skills that ensures portability across any language model and execution environment
  - Standardize skill structure, format, permissions, and execution methods
  - Enable dynamic context loading without permanent overhead
- **USE_WHEN**:
  - Implementing agent skills that need to work across multiple platforms
  - Building skill libraries for teams or organizations
  - Designing execution environments that support agent skills
  - Migrating skills from one platform to another
- **DO_NOT_USE_WHEN**:
  - Building platform-specific features (use `host_overrides` section instead)
  - Creating one-off scripts without reusability requirements
  - Implementing system-level tools that don't benefit from skill abstraction
- **PRIORITY**:
  - This specification takes precedence over platform-specific skill formats when portability is required
  - `host_overrides` can customize behavior for specific environments without breaking core compatibility
  - Breaking changes require major version increments
- **RELATED_TOPICS**:
  - tool-calling-protocols
  - function-schemas
  - execution-environments
  - progressive-disclosure
  - context-management

---

## TL;DR

- **WHAT**: A vendor-neutral specification defining agent skills as folder-based modules with `skill.yaml` manifests, implementations, and documentation
- **WHY**: Enables skill portability across different models and execution environments while minimizing context overhead (~400 tokens) and maximizing output quality
- **WHEN**: Building reusable agent capabilities for document processing, code generation, data analysis, or any task-specific domain expertise
- **HOW**: Create a directory with `skill.yaml` (manifest), implementation scripts (Python/TypeScript), and supporting documentation following the three-layer model (Specification → Adapter → Implementation)
- **WATCH_OUT**: Avoid embedding vendor-specific logic in core specification; use `host_overrides` and adapters for platform-specific needs

---

## Canonical Definitions

### Agent Skill

**Definition**: A task-specific module consisting of a machine-readable manifest (`skill.yaml`), executable implementations, and supporting documentation that can be dynamically loaded and invoked by AI agents.

**Scope**:
- **Includes**:
  - Declarative metadata (capabilities, permissions, safety constraints)
  - One or more tool definitions with JSON Schema contracts
  - Python and/or TypeScript implementations
  - Human and model-oriented documentation
  - Test cases and evaluation criteria
- **Excludes**:
  - Platform-specific UI configurations (belongs in `host_overrides`)
  - Permanent system prompt additions (skills load on-demand)
  - General-purpose libraries without agent-specific interfaces

**Related Concepts**:
- **Similar**: MCP tools, OpenAI function calling, LangChain tools
- **Contrast**: System prompts (permanent overhead), plugins (platform-locked), libraries (no declarative metadata)
- **Contains**: Tools (individual functions), runtime specifications, permission models

**Example**:

```text
pdf-processing/
├── skill.yaml           # Manifest
├── README.md            # Human documentation
├── INSTRUCTIONS.md      # Model-specific guidance
├── scripts/
│   ├── helper.py        # Python implementation
│   └── helper.ts        # TypeScript implementation
└── tests/
    └── cases.yaml       # Test definitions
```

**Sources**: [R1], [R2]

### Three-Layer Model

**Definition**: An architectural pattern separating skill specification (Layer 1), host-specific adaptation (Layer 2), and concrete implementation (Layer 3) to ensure vendor neutrality.

**Scope**:
- **Includes**:
  - **Layer 1**: `skill.yaml`, directory structure, schemas (vendor-neutral)
  - **Layer 2**: Transformation adapters in each execution environment
  - **Layer 3**: Actual code in `scripts/` and resources in `templates/`
- **Excludes**:
  - Monolithic skill implementations mixing all layers
  - Direct coupling between skill code and specific platforms

**Related Concepts**:
- **Similar**: Hexagonal architecture, adapter pattern, plugin systems
- **Contrast**: Tightly-coupled platform SDKs, hardcoded integrations
- **Contains**: Specification layer, adapter layer, implementation layer

**Example**:

```yaml
# Layer 1: Vendor-neutral specification
apiVersion: skills.v1
kind: Skill
metadata:
  id: com.example.pdf_processing
spec:
  tools:
    - name: extract_text
      input_schema: { type: object, properties: {...} }
      implementation:
        entrypoint: scripts/helper.py
        handler: extract_text
        runtime: python
```

**Sources**: [R1], [R3]

### Progressive Disclosure

**Definition**: A context optimization strategy where skill metadata loads first, with detailed instructions and auxiliary files loaded on-demand only when the skill is activated.

**Scope**:
- **Includes**:
  - Initial lightweight metadata scan (~400 tokens per skill)
  - On-demand loading of `INSTRUCTIONS.md` and templates
  - Conditional loading based on trigger matching
- **Excludes**:
  - Loading all skill content into permanent system prompt
  - Eager loading of unnecessary documentation

**Related Concepts**:
- **Similar**: Lazy loading, just-in-time compilation, context windowing
- **Contrast**: Full system prompt embedding, static context loading
- **Contains**: Metadata-first scanning, trigger-based activation, incremental context addition

**Example**:

```python
# Host implementation of progressive disclosure
def select_skills(user_message: str) -> list[Skill]:
    # Scan only metadata first (lightweight)
    candidates = [s for s in all_skills if matches_triggers(s, user_message)]
    # Load full instructions only for selected skills
    for skill in candidates:
        skill.load_instructions()  # On-demand loading
    return candidates
```

**Sources**: [R2], [R4]

### Host Overrides

**Definition**: Platform-specific customizations declared in the `host_overrides` section of `skill.yaml` that allow execution environments to adapt skill behavior without modifying the core specification.

**Scope**:
- **Includes**:
  - Tool name aliases for platform conventions
  - Additional permission models specific to the host
  - Custom timeout values or resource limits
  - Platform-specific configuration mappings
- **Excludes**:
  - Core skill logic modifications
  - Breaking changes to input/output schemas
  - Vendor-specific code in main implementation files

**Related Concepts**:
- **Similar**: Feature flags, conditional compilation, configuration overlays
- **Contrast**: Hard forks, platform-specific branches, separate codebases
- **Contains**: Host identifiers, configuration overrides, tool aliases

**Example**:

```yaml
host_overrides:
  - host: "example-ide"
    config:
      tools_aliases:
        extract_text: "pdf_text"
      permissions:
        custom_sandboxing: true
      timeouts:
        per_tool_seconds: 300
```

**Sources**: [R1]

---

## Core Patterns

### Pattern: Folder-Based Skill Module

**Intent**: Organize all skill components (manifest, code, docs, tests) in a single directory for easy discovery, distribution, and version control.

**Context**: When building reusable agent skills that need to be shared, versioned, and maintained independently across projects and environments.

**Implementation**:

```text
my-skill/
├── skill.yaml           # Required: Machine-readable manifest
├── README.md            # Recommended: Human-readable documentation
├── INSTRUCTIONS.md      # Optional: Detailed guide for models
├── prompts/             # Optional: Few-shot examples
│   └── examples.md
├── scripts/             # Optional: Executable code
│   ├── helper.py
│   └── helper.ts
├── templates/           # Optional: Output templates
│   └── template.txt
└── tests/               # Optional: Test definitions
    ├── cases.yaml
    └── fixtures/
```

**Key Principles**:
- **Single Directory = Single Skill**: All related assets bundled together for atomic versioning
- **Convention Over Configuration**: Standard file names (`skill.yaml`, `README.md`) enable automatic discovery
- **Language Agnostic**: Python and TypeScript can coexist; hosts choose appropriate runtime
- **Self-Documenting**: Human docs, model instructions, and machine specs all present

**Trade-offs**:
- ✅ **Advantages**: Easy distribution (zip/git), clear boundaries, version control friendly
- ⚠️ **Disadvantages**: Duplication if multiple skills share code (mitigate with shared libraries)
- 💡 **Alternatives**: Monorepo with shared code, package-based distribution with dependencies

**Sources**: [R1], [R2]

---

### Pattern: JSON Schema Tool Contracts

**Intent**: Declare tool inputs and outputs using JSON Schema to enable automatic validation, IDE autocomplete, and cross-platform compatibility.

**Context**: When defining skill tools that need to work across different function-calling systems (OpenAI, Anthropic, local executors).

**Implementation**:

```yaml
tools:
  - name: extract_text
    description: Extract text from a PDF file with optional page range.
    input_schema:
      type: object
      required: [path]
      properties:
        path:
          type: string
          description: "Path to the PDF file"
        page_from:
          type: integer
          minimum: 1
          description: "Starting page (1-indexed)"
        page_to:
          type: integer
          minimum: 1
          description: "Ending page (1-indexed)"
    output_schema:
      type: object
      properties:
        text:
          type: string
          description: "Extracted text content"
        page_count:
          type: integer
          description: "Total pages processed"
```

**Key Principles**:
- **Explicit Contracts**: No ambiguity about what inputs are accepted and what outputs are returned
- **Validation-Ready**: Hosts can validate arguments before execution and results after
- **Documentation-Embedded**: Descriptions serve both humans and models
- **Compatibility**: JSON Schema is universally supported across platforms

**Trade-offs**:
- ✅ **Advantages**: Type safety, automatic validation, clear contracts, IDE support
- ⚠️ **Disadvantages**: Verbosity for simple tools, schema evolution requires versioning
- 💡 **Alternatives**: TypeScript types (less portable), OpenAPI specs (heavier), informal descriptions (unsafe)

**Sources**: [R1], [R3]

---

### Pattern: Dual Runtime Implementation

**Intent**: Provide both Python and TypeScript implementations of the same tool to maximize environment compatibility.

**Context**: When skills need to run in diverse environments where Python or Node.js might be preferred or exclusively available.

**Implementation**:

```yaml
# skill.yaml
tools:
  - name: extract_text
    description: Extracts text from PDF (Python runtime).
    input_schema:
      type: object
      required: [path]
      properties:
        path: { type: string }
    output_schema:
      type: object
      properties:
        text: { type: string }
    implementation:
      entrypoint: scripts/helper.py
      handler: extract_text
      runtime: python

  - name: extract_text_ts
    description: Extracts text from PDF (TypeScript runtime).
    input_schema:
      type: object
      required: [path]
      properties:
        path: { type: string }
    output_schema:
      type: object
      properties:
        text: { type: string }
    implementation:
      entrypoint: scripts/helper.ts
      handler: extract_text
      runtime: node
```

**Key Principles**:
- **Runtime Flexibility**: Hosts choose the implementation matching their environment
- **Identical Contracts**: Both implementations honor the same input/output schemas
- **Graceful Degradation**: If one runtime unavailable, fall back to the other
- **Dependency Declaration**: Each runtime declares its own dependencies (`pip` vs `npm`)

**Trade-offs**:
- ✅ **Advantages**: Maximum compatibility, fallback options, developer choice
- ⚠️ **Disadvantages**: Maintenance burden (two codebases), potential behavioral drift
- 💡 **Alternatives**: Single runtime with cross-compilation, WASM for universal binary

**Sources**: [R1]

---

### Pattern: Least Privilege Permissions

**Intent**: Declare minimal filesystem, network, and process permissions required for safe skill execution.

**Context**: When skills need to operate in sandboxed or security-conscious environments where unrestricted access is unacceptable.

**Implementation**:

```yaml
permissions:
  filesystem:
    read:
      - "**/*.pdf"           # Only read PDF files
      - "samples/*.txt"      # Read text samples
    write:
      - "output/*.txt"       # Only write to output directory
      - "**/*_filled.pdf"    # Write filled PDFs anywhere
  network:
    outbound:
      - "api.example.com"    # Only this API endpoint
      # Empty array = no network access
  processes:
    allow_subprocess: true   # Can spawn subprocesses (e.g., poppler-utils)
```

**Key Principles**:
- **Default Deny**: Start with no permissions, add only what's necessary
- **Glob Patterns**: Use specific patterns instead of broad wildcards
- **Audit Trail**: Permissions are declarative and reviewable
- **Host Enforcement**: Execution environments enforce at OS/sandbox level

**Trade-offs**:
- ✅ **Advantages**: Security, auditability, user trust, safe execution
- ⚠️ **Disadvantages**: Requires careful planning, may need iteration, host support varies
- 💡 **Alternatives**: Full sandbox (heavier), trust-based (riskier), no restrictions (unsafe)

**Sources**: [R1]

---

### Pattern: Trigger-Based Skill Selection

**Intent**: Enable automatic skill selection by matching user intent against declared triggers (mentions, file types, intents).

**Context**: When building agent systems that need to autonomously select relevant skills from a large library without explicit user commands.

**Implementation**:

```yaml
when_to_use:
  triggers:
    mentions:
      - "PDF"
      - "form"
      - "OCR"
      - "scan"
      - "document extraction"
    file_types:
      - ".pdf"
      - ".djvu"
    intents:
      - "document_extraction"
      - "form_filling"
      - "text_extraction"
```

**Key Principles**:
- **Multi-Modal Matching**: Combine keyword mentions, file extensions, and semantic intents
- **Explicit Declaration**: Skill authors know best when their skill is relevant
- **Ranking Support**: Hosts can rank skills by match strength
- **Override Support**: Manual invocation via `command` always takes precedence

**Trade-offs**:
- ✅ **Advantages**: Autonomous operation, reduced user burden, context-aware selection
- ⚠️ **Disadvantages**: Potential false positives, requires good trigger design, ambiguity resolution needed
- 💡 **Alternatives**: Always manual invocation, embedding-based similarity, LLM-based selection

**Sources**: [R1], [R2]

---

### Pattern: Progressive Context Loading

**Intent**: Minimize permanent context overhead by loading skill metadata first, then instructions only when activated.

**Context**: When managing large skill libraries where loading all documentation into context would exceed token budgets or waste resources.

**Implementation**:

```yaml
# Lightweight metadata (always loaded)
metadata:
  id: com.example.pdf_processing
  name: pdf-processing
  version: 1.0.0
  tags: [pdf, extraction]
spec:
  summary: >
    Extract text/tables from PDFs with optional OCR.
  when_to_use:
    triggers:
      mentions: ["PDF", "OCR"]
  # Instructions loaded on-demand
  instructions:
    system: |
      You are a PDF Processing Skill...
    readme: "README.md"  # File loaded only when skill activated
```

**Key Principles**:
- **Metadata-First**: Scan all skills with minimal token cost (~400 tokens each)
- **Activation-Triggered**: Load full instructions (`INSTRUCTIONS.md`, templates) only when skill selected
- **Lazy References**: Use file paths instead of inline content for large documentation
- **Quality Over Quantity**: Target the right altitude—encourage critical thinking without excessive detail

**Trade-offs**:
- ✅ **Advantages**: Scalable to hundreds of skills, reduced context waste, faster initial load
- ⚠️ **Disadvantages**: Two-phase loading complexity, file I/O on activation
- 💡 **Alternatives**: Embedding-based retrieval, pre-filtered subsets, full eager loading (limited scale)

**Sources**: [R2], [R4], [R5]

---

## Decision Checklist

- [ ] **Skill follows folder-based structure**: Directory contains `skill.yaml` + implementations + docs [R1]
  - **Verify**: Check for `skill.yaml` at directory root
  - **Impact**: Skills without manifests cannot be discovered or validated
  - **Mitigation**: Generate `skill.yaml` from existing documentation or code

- [ ] **All tools have JSON Schema contracts**: `input_schema` and `output_schema` defined [R1]
  - **Verify**: Parse schemas and validate they are valid JSON Schema
  - **Impact**: Missing schemas prevent validation and break type safety
  - **Mitigation**: Generate schemas from code signatures or API docs

- [ ] **Permissions follow least privilege**: Only necessary filesystem/network/process access declared [R1]
  - **Verify**: Review `permissions` block against actual tool behavior
  - **Impact**: Overly broad permissions create security risks
  - **Mitigation**: Test skill in restricted sandbox and expand permissions incrementally

- [ ] **Skill loads in <500 tokens (metadata only)**: Progressive disclosure enabled [R4], [R5]
  - **Verify**: Count tokens in `metadata` + `spec.summary` + `when_to_use`
  - **Impact**: Heavy metadata prevents scaling to large skill libraries
  - **Mitigation**: Move detailed guidance to `INSTRUCTIONS.md`, use file references

- [ ] **Host-specific logic isolated in `host_overrides`**: Core spec remains vendor-neutral [R1]
  - **Verify**: Grep for platform-specific code/config in main spec sections
  - **Impact**: Vendor lock-in, reduced portability
  - **Mitigation**: Extract platform-specific settings to `host_overrides` array

- [ ] **Semantic versioning used**: Breaking changes increment major version [R1]
  - **Verify**: Check `metadata.version` matches semantic versioning format
  - **Impact**: Breaking changes without major version increment break dependents
  - **Mitigation**: Implement `CHANGELOG.md` and version validation in CI

- [ ] **Safety constraints declared**: PII handling, overwrite confirmations, redaction policies set [R1]
  - **Verify**: Review `spec.safety` section completeness
  - **Impact**: Uncontrolled data handling creates compliance risks
  - **Mitigation**: Add safety defaults in host adapter if skill omits them

- [ ] **Smoke tests defined**: At least one test in `evaluation.smoke_tests` [R1]
  - **Verify**: Parse `spec.evaluation.smoke_tests` array
  - **Impact**: No automated validation of skill functionality
  - **Mitigation**: Generate basic test from tool examples or manual testing

- [ ] **Dependencies explicitly declared**: All `pip`/`npm`/`system` requirements listed [R1]
  - **Verify**: Cross-reference `runtime.dependencies` with actual imports
  - **Impact**: Runtime errors from missing dependencies
  - **Mitigation**: Use dependency scanning tools or containerization

- [ ] **Documentation exists for both humans and models**: `README.md` and optional `INSTRUCTIONS.md` [R1]
  - **Verify**: Check file existence and non-empty content
  - **Impact**: Poor discoverability, unclear usage for humans and models
  - **Mitigation**: Generate README from `skill.yaml` metadata as starting point

---

## Anti-patterns / Pitfalls

### Anti-pattern: Embedding Full Documentation in System Prompt

**Symptom**: All skill instructions permanently loaded in system prompt, causing token bloat and context waste.

**Why It Happens**: Simple to implement initially; developers don't plan for scale beyond 5-10 skills.

**Impact**:
- Context window exhaustion with large skill libraries
- Increased latency and cost from processing unused instructions
- Reduced space for actual task context and conversation history

**Solution**: Implement progressive disclosure—load metadata first, instructions on activation.

**Example**:

```yaml
# ❌ Anti-pattern: Inline everything
spec:
  instructions:
    system: |
      [5000 tokens of detailed procedures, examples, edge cases...]

# ✅ Correct pattern: Reference on-demand files
spec:
  summary: "Extract text/tables from PDFs with optional OCR."
  instructions:
    system: |
      You are a PDF Processing Skill. Follow procedures in INSTRUCTIONS.md.
    readme: "README.md"           # Loaded only when activated
    detailed: "INSTRUCTIONS.md"   # Loaded only when activated
```

**Sources**: [R2], [R4]

---

### Anti-pattern: Vendor-Specific Logic in Core Specification

**Symptom**: `skill.yaml` contains conditionals, platform-specific paths, or tool names tied to one execution environment.

**Why It Happens**: Skill developed against single platform; portability not considered initially.

**Impact**:
- Skill fails when moved to different environment
- Forks multiply, maintenance burden increases
- Violates vendor-neutral design principle

**Solution**: Extract platform-specific settings to `host_overrides`, use generic paths and tool names in core spec.

**Example**:

```yaml
# ❌ Anti-pattern: Platform-specific in core spec
spec:
  tools:
    - name: claude_code_extract_text  # Platform-specific name
      implementation:
        entrypoint: /usr/local/claude/scripts/helper.py  # Absolute path

# ✅ Correct pattern: Generic core + host overrides
spec:
  tools:
    - name: extract_text  # Generic name
      implementation:
        entrypoint: scripts/helper.py  # Relative path
host_overrides:
  - host: "claude-code"
    config:
      tools_aliases:
        extract_text: "claude_code_extract_text"
```

**Sources**: [R1]

---

### Anti-pattern: Overly Broad Permissions

**Symptom**: Skill declares `filesystem.read: ["**/*"]` or `network.outbound: ["*"]` when only narrow access needed.

**Why It Happens**: Developer wants skill to "just work" without thinking through actual requirements.

**Impact**:
- Security teams block skill deployment
- Users distrust and disable skill
- Actual compromise risk if skill has vulnerability

**Solution**: Start with minimal permissions, use glob patterns for specific file types/directories, expand only as needed.

**Example**:

```yaml
# ❌ Anti-pattern: Broad permissions
permissions:
  filesystem:
    read: ["**/*"]                 # Reads everything
    write: ["**/*"]                # Writes anywhere
  network:
    outbound: ["*"]                # Any external connection

# ✅ Correct pattern: Least privilege
permissions:
  filesystem:
    read: ["**/*.pdf", "samples/"]  # Only PDFs and samples
    write: ["output/", "**/*_processed.pdf"]  # Only output dir
  network:
    outbound: ["api.ocr-service.com"]  # Only specific API
```

**Sources**: [R1]

---

### Anti-pattern: Missing or Weak Input Validation

**Symptom**: Tool implementations accept arbitrary inputs without schema validation, leading to runtime errors or security issues.

**Why It Happens**: Developer trusts model to always provide correct inputs; validation seen as unnecessary overhead.

**Impact**:
- Tool crashes with cryptic errors confusing the model
- Path traversal vulnerabilities (e.g., `../../etc/passwd`)
- Type errors causing incorrect results silently

**Solution**: Define strict JSON Schemas, validate in host adapter before calling handler, sanitize file paths and user inputs.

**Example**:

```python
# ❌ Anti-pattern: No validation
def extract_text(args, ctx):
    path = args["path"]  # Could be missing or malicious
    return {"text": open(path).read()}  # Path traversal risk

# ✅ Correct pattern: Validated and sanitized
def extract_text(args: dict, ctx: RunContext) -> dict:
    # Host already validated against input_schema
    path = pathlib.Path(args["path"]).expanduser().resolve()
    # Ensure path within allowed boundaries
    if not path.is_relative_to(ctx.cwd):
        raise ValueError(f"Path {path} outside working directory")
    if not path.suffix.lower() == ".pdf":
        raise ValueError(f"Expected .pdf file, got {path.suffix}")
    # Now safe to process
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages)
    return {"text": text, "page_count": len(pdf.pages)}
```

**Sources**: [R1], [R3]

---

### Anti-pattern: Ignoring Skill Versioning

**Symptom**: `metadata.version` never incremented, breaking changes deployed without communication, no CHANGELOG.

**Why It Happens**: Small team, informal process, "we'll remember what changed."

**Impact**:
- Dependents break silently when skill updates
- No rollback path when issues discovered
- Trust erosion, users pin to old versions indefinitely

**Solution**: Adopt semantic versioning, increment major for breaking changes, maintain CHANGELOG.md, communicate updates.

**Example**:

```yaml
# ❌ Anti-pattern: Version stagnation
metadata:
  version: 1.0.0  # Never changes despite breaking schema updates

# ✅ Correct pattern: Semantic versioning
metadata:
  version: 2.0.0  # Major bump for breaking change
# CHANGELOG.md:
# 2.0.0 (2025-11-13)
# BREAKING: Renamed `extract_text` to `extract_pdf_text`
# BREAKING: Changed output schema to include `page_count`
# 1.1.0 (2025-10-20)
# ADDED: OCR fallback for scanned PDFs
```

**Sources**: [R1]

---

## Evaluation

### Metrics

**Skill Activation Accuracy**: Percentage of times the correct skill is selected for a given task.
- **Why It Matters**: Poor selection wastes tokens loading wrong skills, confuses users, reduces task success rate
- **Target**: >95% precision, >90% recall for skills with well-defined triggers
- **Measurement**: Log ratio of (correct activations) / (total activations) in production
- **Tools**: Analytics dashboard, A/B testing framework
- **Frequency**: Continuous monitoring with weekly reviews

**Context Overhead per Skill**: Average token count for skill metadata (excluding on-demand content).
- **Why It Matters**: Determines maximum skill library size before context exhaustion
- **Target**: <500 tokens for metadata, <2000 tokens total when activated
- **Measurement**: Token counter on `metadata` + `spec.summary` + `when_to_use`
- **Tools**: Tokenizer (tiktoken, transformers), CI validation script
- **Frequency**: Every commit with automated checks

**Permission Violation Rate**: Frequency of skills attempting operations outside declared permissions.
- **Why It Matters**: Indicates security risks, need for tighter sandboxing, or permission spec errors
- **Target**: 0% violations in production (all caught in testing)
- **Measurement**: Sandbox violation logs, security audit trails
- **Tools**: OS-level sandboxing (seccomp, AppArmor), runtime monitors
- **Frequency**: Real-time alerts, monthly security audits

**Sources**: [R1], [R4], [R5]

### Testing Strategies

**Unit Tests**:
- Each tool handler tested independently with valid/invalid inputs
- Schema validation tested for all input/output combinations
- Permission checks tested (file access, network calls, subprocess spawning)
- Error handling tested (missing files, malformed inputs, timeouts)

**Integration Tests**:
- Full skill lifecycle: discovery → selection → activation → execution → result
- Multi-skill scenarios (skill A calls skill B, shared resources)
- Host adapter compatibility (test on 2+ execution environments)
- Dependency installation and runtime setup

**Performance Benchmarks**:
- Skill selection latency (<100ms for metadata scan)
- Tool execution time against realistic workloads
- Memory footprint during execution
- Context token usage across typical workflows

### Success Criteria

- [ ] Skill passes JSON Schema validation for `skill.yaml`
- [ ] All declared tools execute successfully in smoke tests
- [ ] Permission boundaries enforced (no unauthorized file/network/process access)
- [ ] Metadata loads in <500 tokens, full activation in <2000 tokens
- [ ] README.md and INSTRUCTIONS.md exist and are non-empty
- [ ] At least one runtime implementation (Python or TypeScript) present
- [ ] Version follows semantic versioning (X.Y.Z format)
- [ ] Dependencies install successfully in clean environment
- [ ] Host adapter can transform schemas to native function-calling format
- [ ] Skill selection triggers match intended use cases (>90% accuracy in testing)

---

## Update Log

- **2025-11-13** – Initial specification created covering manifest structure, three-layer model, permissions, safety, progressive disclosure, and dual runtime support. (Author: AI-First)

---

## See Also

### Prerequisites
- [json-schema](https://json-schema.org/) – Understanding JSON Schema is essential for defining tool contracts
- [semantic-versioning](https://semver.org/) – Version management principles applied in this specification

### Related Topics
- [tool-calling-protocols] – How models invoke tools and interpret results
- [function-schemas] – Best practices for designing function signatures
- [progressive-disclosure] – Context optimization strategies for AI systems
- [execution-sandboxing] – Security models for running untrusted code
- [context-management] – Techniques for optimizing token usage in AI systems

### Advanced / Platform-specific
- [claude-code-skills](https://code.claude.com/docs/en/skills) – Claude Code implementation of this specification
- [mcp-protocol] – Model Context Protocol as alternative integration approach
- [langchain-tools] – LangChain's tool abstraction and integration patterns

---

## References

- [R1] Anthropic. "Claude Code Skills Documentation." Claude Code Official Docs. https://code.claude.com/docs/en/skills (accessed 2025-11-13)
- [R2] Anthropic. "Agent Skills Quickstart." Claude Documentation. https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart (accessed 2025-11-13)
- [R3] Anthropic. "Agent Skills Overview." Claude Documentation. https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview (accessed 2025-11-13)
- [R4] Anthropic. "Improving Frontend Design Through Skills." Claude Blog. https://claude.com/blog/improving-frontend-design-through-skills (accessed 2025-11-13)
- [R5] Anthropic. "Skills Repository and Examples." GitHub. https://github.com/anthropics/skills (accessed 2025-11-13)

---

**Document ID**: `ssot/AGENT_SKILL.md`
**Canonical URL**: `https://github.com/artificial-intelligence-first/ssot/blob/main/AGENT_SKILL.md`
**License**: MIT
