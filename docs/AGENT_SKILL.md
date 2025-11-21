---
title: Agent Skill All Model
slug: agent-skill
summary: "Skill spec overview"
type: spec
tags: [topic, ai-first, agent, skill, specification]
last_updated: 2025-11-22
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
- **Ecosystem**: Layer 2 adapters bridge to MCP, OpenAI Actions, and LangChain Tools

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

```python
import json
from abc import ABC, abstractmethod
from typing import Any

# Layer 2: Host-specific adapter (e.g., for Claude platform)
class ClaudeSkillAdapter:
    """Adapter that transforms vendor-neutral skill to Claude-specific format"""

    def __init__(self, skill_spec: dict):
        self.spec = skill_spec
        self.runtime = self._detect_runtime()

    def transform_to_claude_tool(self) -> dict:
        """Convert skill.yaml tool definition to Claude tool format"""
        tool = self.spec['spec']['tools'][0]
        return {
            "name": tool['name'],
            "description": tool.get('description', ''),
            "input_schema": self._adapt_schema(tool['input_schema']),
            "implementation": self._create_claude_wrapper(tool)
        }

    def _adapt_schema(self, schema: dict) -> dict:
        """Adapt JSON Schema to Claude's specific requirements"""
        adapted = schema.copy()
        # Claude-specific schema adjustments
        if 'additionalProperties' not in adapted:
            adapted['additionalProperties'] = False
        return adapted

    def _create_claude_wrapper(self, tool: dict) -> callable:
        """Create platform-specific execution wrapper"""
        entrypoint = tool['implementation']['entrypoint']
        handler = tool['implementation']['handler']

        def wrapper(**kwargs):
            # Platform-specific setup (permissions, sandboxing)
            with self._setup_claude_context():
                # Import and execute the actual implementation
                module = self._load_module(entrypoint)
                func = getattr(module, handler)
                return func(**kwargs)

        return wrapper

# Layer 2: Adapter for OpenAI platform
class OpenAISkillAdapter:
    """Adapter for OpenAI function calling"""

    def transform_to_openai_function(self) -> dict:
        """Convert to OpenAI function format"""
        tool = self.spec['spec']['tools'][0]
        return {
            "type": "function",
            "function": {
                "name": tool['name'],
                "description": tool.get('description'),
                "parameters": tool['input_schema'],
                # OpenAI-specific: strict mode for structured outputs
                "strict": True
            }
        }

    def create_openai_executor(self) -> callable:
        """Create OpenAI-specific executor with their sandbox"""
        def executor(function_call):
            # OpenAI-specific execution context (host-provided sandbox)
            with create_openai_sandbox() as sandbox:
                result = sandbox.run_function(
                    function_call.name,
                    **json.loads(function_call.arguments),
                )
            return result
        return executor

class SkillAdapter(ABC):
    """Abstract base for all platform adapters"""

    @abstractmethod
    def load_skill(self, path: str) -> dict:
        """Load skill from directory"""
        pass

    @abstractmethod
    def validate_permissions(self) -> bool:
        """Check platform-specific permissions"""
        pass

    @abstractmethod
    def transform_tools(self) -> list:
        """Convert tools to platform format"""
        pass

    @abstractmethod
    def setup_runtime(self) -> Any:
        """Initialize platform-specific runtime"""
        pass
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
def select_skills(user_message: str) -> list["Skill"]:
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

### Pattern: Formal Manifest Schema

**Intent**: Define a strict, versioned structure for `skill.yaml` to ensure validation tools and IDEs can reliably parse and autocomplete skill definitions.

**Context**: As the ecosystem grows, ad-hoc YAML structures lead to fragmentation. A formal schema ensures consistency across all skills.

**Implementation**:

```yaml
apiVersion: skills.v1
kind: Skill
metadata:
  id: com.example.pdf_processing
  version: 1.0.0
spec:
  tools: [...]
permissions: [...]
secrets:    # New: Explicit secret declaration
  required: [...]
host_overrides: [...]
```

**Key Principles**:
- **Versioning**: `apiVersion` allows the schema to evolve without breaking existing skills
- **Root Validation**: Top-level keys are fixed; no arbitrary fields allowed
- **Type Safety**: Each section enforces specific types (e.g., `permissions` must be an object)

**Trade-offs**:
- ✅ **Advantages**: Enables linting, validation, and reliable parsing
- ⚠️ **Disadvantages**: Slightly more verbose boilerplate
- 💡 **Alternatives**: Schemaless YAML (flexible but fragile)

**Sources**: [R1]

---

### Pattern: Declarative Secrets

**Intent**: Explicitly declare required credentials (API keys, tokens) without embedding them in code or configuration files.

**Context**: Skills often need external services (OCR, Database, APIs) but should never store secrets in the repository.

**Implementation**:

```yaml
secrets:
  required:
    - name: OCR_SERVICE_API_KEY
      description: "API key for the external OCR provider"
      usage: env  # Injected as environment variable
    - name: DATABASE_URL
      description: "Connection string for results storage"
      optional: true
```

**Key Principles**:
- **Declaration Only**: Skill defines *what* it needs, Host decides *how* to provide it
- **Environment Injection**: Secrets are typically exposed as environment variables to the runtime
- **Validation**: Host checks for presence of required secrets before starting the skill

**Trade-offs**:
- ✅ **Advantages**: Security, separation of concerns, no hardcoded secrets
- ⚠️ **Disadvantages**: Requires host support to manage and inject secrets
- 💡 **Alternatives**: `.env` files (hard to manage in production), hardcoding (insecure)

**Sources**: [R1]

---

### Pattern: Standardized Runtime Protocol

**Intent**: Define standard behavior for errors, cancellations, and asynchronous operations to ensure consistent host handling.

**Context**: Different hosts handle errors differently. A standard protocol ensures the model understands failures regardless of the environment.

**Implementation**:

```python
# Standardized Error Response
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Upstream service rate limit hit. Retry in 60s.",
    "retry_after": 60,
    "retriable": true
  }
}

# Async Job Response
{
  "status": "async",
  "job_id": "job_12345",
  "message": "Processing started. Poll status with get_job_status."
}
```

**Key Principles**:
- **Structured Errors**: Machine-readable error codes enable intelligent retries by the Agent
- **Async Support**: Protocol anticipates long-running tasks via job IDs
- **Cancellation**: Hosts can signal cancellation via standard signals (SIGTERM)

**Trade-offs**:
- ✅ **Advantages**: Predictable behavior, better error recovery, support for long tasks
- ⚠️ **Disadvantages**: Implementation complexity for simple scripts
- 💡 **Alternatives**: Throwing raw exceptions (confusing to models)

**Sources**: [R1]

---

### Pattern: Host-Mediated Composition

**Intent**: Allow skills to utilize other skills' capabilities only through the Host, preventing direct coupling and "dependency hell."

**Context**: A complex skill (e.g., "Research") might need a simpler skill (e.g., "Web Search"). Direct imports create tight coupling.

**Implementation**:

```python
# ❌ Anti-pattern: Direct import
from my_other_skill import search  # Hard dependency

# ✅ Correct pattern: Host-mediated
def research_topic(topic, ctx):
    # Request host to execute another tool
    results = ctx.host.execute_tool("web_search", {"query": topic})
    return summarize(results)
```

**Key Principles**:
- **Loose Coupling**: Skills remain independent units
- **Host Control**: Host maintains visibility and control over the call stack
- **Mockability**: Easier to test skills in isolation by mocking the host

**Trade-offs**:
- ✅ **Advantages**: Modularity, easier testing, no circular dependencies
- ⚠️ **Disadvantages**: Higher latency (IPC overhead), complex host interface
- 💡 **Alternatives**: Shared libraries (good for utility code, bad for full skills)

**Sources**: [R1]

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

- [ ] **Secrets declared in manifest**: No hardcoded credentials in code [R1]
  - **Verify**: Check `secrets.required` vs code usage of `os.environ`
  - **Impact**: Security leaks, deployment failures
  - **Mitigation**: Scan code for high-entropy strings and move to `secrets`

- [ ] **Skill Composition via Host**: No direct imports of other skills [R1]
  - **Verify**: Check imports for references to other skill directories
  - **Impact**: Tight coupling, broken portability
  - **Mitigation**: Refactor to use `ctx.host.execute_tool()`

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

```yaml
# tests/cases.yaml - Test definition format
version: 1.0
tests:
  - name: test_extract_text_valid_input
    tool: extract_text
    input:
      path: "fixtures/sample.pdf"
      page_from: 1
      page_to: 2
    expected:
      text: contains("Sample PDF content")
      page_count: 2
    tags: [smoke, unit]

  - name: test_extract_text_invalid_path
    tool: extract_text
    input:
      path: "nonexistent.pdf"
    expected_error:
      type: FileNotFoundError
      message: contains("not found")
    tags: [unit, error-handling]

  - name: test_permission_boundary
    tool: extract_text
    input:
      path: "/etc/passwd"  # Outside allowed paths
    expected_error:
      type: PermissionError
      message: contains("Access denied")
    tags: [security, unit]
```

**Integration Tests**:
- Full skill lifecycle: discovery → selection → activation → execution → result
- Multi-skill scenarios (skill A calls skill B, shared resources)
- Host adapter compatibility (test on 2+ execution environments)
- Dependency installation and runtime setup

```python
# tests/runner.py - Universal test runner
import yaml
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List

class SkillTestRunner:
    """Universal test runner for agent skills"""

    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.skill_spec = self._load_skill_spec()
        self.test_cases = self._load_test_cases()

    def _load_skill_spec(self) -> dict:
        """Load and validate skill.yaml"""
        with open(self.skill_path / "skill.yaml") as f:
            spec = yaml.safe_load(f)
        self._validate_spec(spec)
        return spec

    def _load_test_cases(self) -> List[dict]:
        """Load test cases from tests/cases.yaml"""
        test_file = self.skill_path / "tests" / "cases.yaml"
        if not test_file.exists():
            return []
        with open(test_file) as f:
            return yaml.safe_load(f).get("tests", [])

    def run_smoke_tests(self) -> bool:
        """Run only smoke tests for quick validation"""
        smoke_tests = [t for t in self.test_cases if "smoke" in t.get("tags", [])]
        results = []
        for test in smoke_tests:
            result = self._execute_test(test)
            results.append(result)
            print(f"✓ {test['name']}" if result else f"✗ {test['name']}")
        return all(results)

    def run_all_tests(self, verbose: bool = False) -> Dict[str, Any]:
        """Run complete test suite with detailed reporting"""
        results = {
            "total": len(self.test_cases),
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "details": []
        }

        for test in self.test_cases:
            try:
                success = self._execute_test(test)
                if success:
                    results["passed"] += 1
                else:
                    results["failed"] += 1

                results["details"].append({
                    "name": test["name"],
                    "status": "passed" if success else "failed",
                    "tags": test.get("tags", [])
                })

                if verbose:
                    self._print_test_result(test, success)

            except Exception as e:
                results["failed"] += 1
                results["details"].append({
                    "name": test["name"],
                    "status": "error",
                    "error": str(e)
                })

        return results

    def _execute_test(self, test: dict) -> bool:
        """Execute a single test case"""
        tool_name = test["tool"]
        tool = self._find_tool(tool_name)

        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found in skill")

        # Determine runtime and execute
        runtime = tool["implementation"]["runtime"]
        if runtime == "python":
            return self._execute_python_test(test, tool)
        elif runtime == "typescript":
            return self._execute_typescript_test(test, tool)
        else:
            raise ValueError(f"Unsupported runtime: {runtime}")

    def _execute_python_test(self, test: dict, tool: dict) -> bool:
        """Execute Python tool with test inputs"""
        import importlib.util

        # Load the module
        script_path = self.skill_path / tool["implementation"]["entrypoint"]
        spec = importlib.util.spec_from_file_location("skill_module", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Get the handler function
        handler_name = tool["implementation"]["handler"]
        handler = getattr(module, handler_name)

        # Execute with test inputs
        try:
            result = handler(**test["input"])
            return self._validate_output(result, test.get("expected"))
        except Exception as e:
            if "expected_error" in test:
                return self._validate_error(e, test["expected_error"])
            raise

    def _execute_typescript_test(self, test: dict, tool: dict) -> bool:
        """Execute TypeScript tool with test inputs"""
        # Use Node.js subprocess to run TypeScript
        script_path = self.skill_path / tool["implementation"]["entrypoint"]
        handler_name = tool["implementation"]["handler"]

        # Create test runner script
        runner_script = f"""
        const {{ {handler_name} }} = require('./{script_path}');
        const input = {json.dumps(test["input"])};
        {handler_name}(input).then(result => {{
            console.log(JSON.stringify(result));
        }}).catch(err => {{
            console.error(JSON.stringify({{error: err.message}}));
            process.exit(1);
        }});
        """

        # Execute via Node.js
        result = subprocess.run(
            ["node", "-e", runner_script],
            cwd=self.skill_path,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            output = json.loads(result.stdout)
            return self._validate_output(output, test.get("expected"))
        else:
            error = json.loads(result.stderr)
            if "expected_error" in test:
                return self._validate_error(error, test["expected_error"])
            return False

# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run skill tests")
    parser.add_argument("skill_path", help="Path to skill directory")
    parser.add_argument("--smoke", action="store_true", help="Run only smoke tests")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--json", action="store_true", help="Output JSON report")

    args = parser.parse_args()

    runner = SkillTestRunner(args.skill_path)

    if args.smoke:
        success = runner.run_smoke_tests()
        exit(0 if success else 1)
    else:
        results = runner.run_all_tests(verbose=args.verbose)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"\nTest Results: {results['passed']}/{results['total']} passed")
        exit(0 if results['failed'] == 0 else 1)
```

**Performance Benchmarks**:
- Skill selection latency (<100ms for metadata scan)
- Tool execution time against realistic workloads
- Memory footprint during execution
- Context token usage across typical workflows

```bash
# Automated test execution via CI/CD
# .github/workflows/skill-tests.yml
name: Skill Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install test runner
        run: pip install pyyaml jsonschema

      - name: Run smoke tests
        run: python tests/runner.py . --smoke

      - name: Run full test suite
        run: python tests/runner.py . --verbose --json > test-report.json

      - name: Upload test results
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: test-report.json
```

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

## Practical Skill Examples

### 19.1 Frontend Development Skills

The **web-artifacts-builder** skill demonstrates how skills can dramatically improve frontend output quality while minimizing context overhead. Key characteristics:

- **Modern tooling integration**: React, Tailwind CSS, shadcn/ui components
- **Embedded scripts** for bootstrapping repositories and bundling with Parcel
- **Design guidance** addressing typography, themes, motion, and backgrounds
- **Progressive enhancement** supporting iterative refinement

Frontend skills should address specific design dimensions:
- **Typography**: Distinctive font choices with high contrast pairings
- **Themes**: Cultural aesthetics and cohesive color palettes
- **Motion**: Orchestrated animations and CSS-only solutions
- **Backgrounds**: Layered gradients and patterns for atmospheric depth

> Any domain where models produce generic outputs despite having more expansive understanding is a candidate for skill development. Skills enable teams to encode company design systems and component patterns into reusable modules. ([Improving frontend design through skills](https://claude.com/blog/improving-frontend-design-through-skills))

### 19.2 Document Processing Skills

Pre-configured skills for document generation (presentations/spreadsheets/documents/PDFs) demonstrate the pattern of combining:
- Declarative capabilities in `skill.yaml`
- Executable scripts for automation
- Templates for consistent output formatting

---

## Update Log

- **2024-11-19** – Added concrete Layer 2 (Adapter) implementation examples for Claude and OpenAI platforms. Enhanced testing strategies with detailed test runner implementation and CI/CD integration examples. (Author: AI-First)
- **2025-11-22** – Refined specification based on multi-agent review. Added Formal Manifest Schema, Declarative Secrets, Standardized Runtime Protocol, and Host-Mediated Composition patterns. Clarified MCP relationship. (Author: AI-First)
- **2025-11-14** – Added Practical Skill Examples section with frontend and document processing examples. Updated metadata. (Author: AI-First)
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

**Document ID**: `docs/AGENT_SKILL.md`
**Canonical URL**: `https://github.com/artificial-intelligence-first/ssot/blob/main/docs/AGENT_SKILL.md`
**License**: MIT
