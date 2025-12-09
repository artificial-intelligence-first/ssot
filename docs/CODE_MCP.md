---
title: Code MCP
slug: code-mcp
summary: "Code MCP guide"
type: reference
tags: [topic, ai-first, agent, mcp, code, optimization]
last_updated: 2025-11-24
---

# Topic: Code MCP — Model-Agnostic Code Execution MCP Implementation Guide

## Agent Contract

- **PURPOSE**:
  - Define a vendor-neutral implementation guide for Code MCP, transforming MCP tools from direct invocations to code APIs executed in secure sandboxes
  - Achieve dramatic token consumption reduction (up to 98.7%) while maintaining security, privacy, and reproducibility
  - Enable progressive disclosure where models read only necessary tool definitions on-demand
- **USE_WHEN**:
  - Implementing MCP integrations with cost optimization requirements
  - Building agent systems that process large datasets or make many tool calls
  - Designing secure execution environments for AI-generated code
  - Migrating from direct tool invocation patterns to code-based execution
- **DO_NOT_USE_WHEN**:
  - Simple single-tool invocations where overhead exceeds benefits
  - Systems without sandboxing capabilities (security risk)
  - Real-time latency-critical applications where sandbox overhead is unacceptable
  - Environments where code generation by models is unreliable or unavailable
  - Simple single-tool invocations where overhead exceeds benefits (use direct tool calling)
  - Small-scale tasks with low frequency where infrastructure maintenance outweighs value
- **PRIORITY**:
  - This specification takes precedence over direct MCP tool invocation when token optimization is critical
  - Security requirements override cost optimization—never sacrifice isolation for performance
  - Progressive disclosure is mandatory for systems with >20 available tools
- **RELATED_TOPICS**:
  - agent-skill
  - mcp-protocol
  - progressive-disclosure
  - sandbox-execution
  - token-optimization

In this repository, recommended agents for applying this specification (such as `repo-orchestrator` and `doc-maintainer`) are defined in `AGENTS.md`.

---

## TL;DR

- **WHAT**: An implementation pattern that wraps MCP tools as typed code APIs executed in isolated sandboxes, with models generating code instead of directly invoking tools
- **WHY**: Reduces token consumption by up to 98.7% (150K→2K tokens) by keeping tool definitions and intermediate data out of model context while improving security and reproducibility
- **WHEN**: Use for MCP integrations with many tools, large data processing, or cost-sensitive deployments where sandbox overhead is acceptable
- **HOW**: Implement thin typed wrappers around MCP tools, execute agent-generated code in sandboxes, apply progressive disclosure for tool definitions, and filter/aggregate data before returning summaries to models
- **WATCH_OUT**: Requires robust sandboxing (resource limits, isolation, audit logging) and careful error handling; models must be capable of generating correct code in target language

---

## Canonical Definitions

### Code MCP

**Definition**: An architectural pattern where MCP (Model Context Protocol) tools are wrapped as typed function APIs and invoked through agent-generated code executed in secure sandboxes, rather than through direct model-to-tool invocations.

**Scope**:
- **Includes**:
  - Thin typed wrappers for each MCP tool (Python/TypeScript)
  - Sandbox execution environment with resource limits
  - MCP client handling JSON-RPC communication
  - Progressive disclosure of tool definitions
  - In-sandbox data filtering and aggregation
- **Excludes**:
  - Direct function calling without sandboxing (security risk)
  - Pre-loading all tool definitions into system prompt
  - Exposing raw large datasets to model context

**Related Concepts**:
- **Similar**: Code interpreter patterns, Jupyter-style execution, E2B sandboxes
- **Contrast**: Direct tool invocation (OpenAI function calling), prompt-based tool use
- **Contains**: Code wrappers, sandbox runner, MCP client, progressive disclosure

**Example**:

```typescript
// Instead of model calling tools directly:
// ❌ model → tool("google_drive__get_document", {id: "abc"})

// Model generates code executed in sandbox:
// ✅ model → code → sandbox executes:
import { getDocument } from "./servers/google-drive";
const doc = await getDocument({ documentId: "abc" });
const summary = extractKeyPoints(doc.content); // 10K lines → 200 words
console.log(summary); // Only summary to model
```

**Sources**: [R1]

### Code Wrapper (Code API)

**Definition**: A thin typed function that wraps a single MCP tool, providing language-native interface (TypeScript/Python) with type annotations, docstrings, and standardized error handling.

**Scope**:
- **Includes**:
  - Type-safe input/output interfaces (TypedDict, interface)
  - Inline documentation (docstrings, JSDoc comments)
  - Call to underlying `callMCPTool` client function
  - Standard naming convention: `<server>__<tool>` identifier
- **Excludes**:
  - Business logic or data transformation (belongs in skills)
  - Direct MCP protocol handling (delegated to client)
  - Authentication/authorization logic (handled by MCP server)

**Related Concepts**:
- **Similar**: SDK wrappers, API clients, adapter functions
- **Contrast**: Raw JSON-RPC calls, untyped dynamic invocations
- **Contains**: Type definitions, client invocation, error propagation

**Example**:

```python
# servers/google_drive/get_document.py
from typing import TypedDict
from client.mcp_client import call_mcp_tool

class GetDocumentInput(TypedDict):
    documentId: str

class GetDocumentResponse(TypedDict):
    content: str

async def get_document(input: GetDocumentInput) -> GetDocumentResponse:
    """Read a document from Google Drive"""
    return await call_mcp_tool("google_drive__get_document", input)
```

**Sources**: [R1]

### Progressive Disclosure

**Definition**: A context optimization strategy where tool definitions are loaded on-demand rather than pre-loaded, with granular detail levels (name-only, name+description, full-schema) based on agent needs.

**Scope**:
- **Includes**:
  - On-demand file reading via `readFile` tool
  - Tiered detail levels for tool discovery
  - Lazy loading of schemas only when needed
  - Caching of loaded definitions within session
- **Excludes**:
  - Eager loading of all tool definitions at session start
  - Exposing full schemas when names suffice
  - Permanent embedding in system prompts

**Related Concepts**:
- **Similar**: Lazy loading, just-in-time compilation, demand paging
- **Contrast**: Pre-loading, static context, full schema enumeration
- **Contains**: Search tools API, detail levels, file-based definitions

**Example**:

```typescript
// Phase 1: Model searches with name-only
const tools = await searchTools({ query: "google drive", detail: "name" });
// Returns: ["google_drive__get_document", "google_drive__update_document"]

// Phase 2: Model reads only the needed definition
const def = await readFile("servers/google-drive/getDocument.ts");
// Only this one tool's schema loaded into context

// Phase 3: Model generates code using that tool
const code = `
  import { getDocument } from "./servers/google-drive";
  const doc = await getDocument({ documentId: "abc123" });
`;
```

**Sources**: [R1], [R3]

### Sandbox Execution Layer

**Definition**: An isolated execution environment for running agent-generated code with enforced resource limits, process isolation, network restrictions, and comprehensive audit logging.

**Scope**:
- **Includes**:
  - Process isolation (namespaces, seccomp, cgroups)
  - Resource limits (CPU, memory, time, disk, FDs, threads)
  - Network access control (domain allowlists, CIDR blocks)
  - Audit logging (invocations, data flow, output sizes)
  - Filesystem restrictions (read/write boundaries)
- **Excludes**:
  - Unrestricted host access
  - Persistent state across sessions (unless explicitly managed)
  - Direct access to production credentials

**Related Concepts**:
- **Similar**: Docker containers, Firecracker microVMs, gVisor, E2B sandboxes
- **Contrast**: Direct host execution, unsandboxed code interpreters
- **Contains**: Runtime environment, resource governor, network policy, audit subsystem

**Example**:

```yaml
# Sandbox configuration
sandbox:
  cpu_limit: "1.0"           # 1 CPU core
  memory_limit: "512Mi"      # 512 MiB
  timeout_seconds: 300       # 5 minutes max
  network:
    allowed_domains:
      - "api.google.com"
      - "api.salesforce.com"
  filesystem:
    read_only: ["/usr", "/lib"]
    writable: ["/workspace"]
  audit:
    log_level: "INFO"
    redact_pii: true
```

**Sources**: [R1]

### Code Skill

**Definition**: A reusable composition of multiple code wrappers that abstracts a high-level task, packaged with documentation (SKILL.md) describing purpose, inputs, outputs, and prerequisites.

**Scope**:
- **Includes**:
  - Main implementation file (`main.py` / `main.ts`)
  - SKILL.md documentation (purpose, I/O, examples)
  - Composition of multiple tool wrappers
  - Intermediate data handling and state management
  - Error handling and retry logic
- **Excludes**:
  - Low-level MCP protocol details
  - Direct tool invocations (uses wrappers)
  - Single-tool operations (use wrappers directly)

**Related Concepts**:
- **Similar**: Agent skills (as defined in agent-skill specification), workflows, procedures
- **Contrast**: Individual tool wrappers, raw tool invocations
- **Contains**: Multiple wrapper calls, orchestration logic, documentation

**Example**:

```typescript
// skills/save-sheet-as-csv/main.ts
import * as gdrive from "../../servers/google-drive";
import * as fs from "node:fs/promises";

/**
 * Exports a Google Sheet as CSV file in workspace
 *
 * Input: { sheetId: string }
 * Output: { path: string } - Path to saved CSV
 */
export async function saveSheetAsCsv(sheetId: string): Promise<string> {
  const data = await gdrive.getSheet({ sheetId });
  const csv = data.map((row: any[]) => row.join(",")).join("\n");
  const path = `./workspace/sheet-${sheetId}.csv`;
  await fs.writeFile(path, csv);
  return path;
}
```

**Sources**: [R1]

---

## Core Patterns

### Pattern: Code Wrapper Generation

**Intent**: Create thin typed wrappers around MCP tools that provide language-native interfaces with type safety and inline documentation.

**Context**: When exposing MCP tools to agent-generated code in a type-safe, discoverable manner.

**Implementation**:

```python
# Template for Python wrapper generation
from typing import TypedDict
from client.mcp_client import call_mcp_tool

class {ToolName}Input(TypedDict):
    {input_fields}

class {ToolName}Response(TypedDict):
    {response_fields}

async def {tool_function_name}(
    input: {ToolName}Input
) -> {ToolName}Response:
    """{tool_description}"""
    return await call_mcp_tool(
        "{server}__{tool}",
        input
    )
```

**Key Principles**:
- **One wrapper per tool**: Clear 1:1 mapping between MCP tools and wrapper functions
- **Type annotations required**: Enable IDE autocomplete and static analysis
- **Naming convention**: `<server>__<tool>` for identifiers, `verb_object` for function names
- **Minimal logic**: Wrappers only handle invocation, no business logic

**Trade-offs**:
- ✅ **Advantages**: Type safety, discoverability, consistent interface, IDE support
- ⚠️ **Disadvantages**: Code generation overhead, maintenance burden with schema changes
- 💡 **Alternatives**: Dynamic proxies (less type-safe), manual implementation (slower), codegen from schemas (recommended)

**Sources**: [R1]

---

### Pattern: Sandbox-Based Execution

**Intent**: Execute agent-generated code in isolated environments with strict resource limits and comprehensive audit logging.

**Context**: When running untrusted code generated by language models that invokes external APIs or processes sensitive data.

**Implementation**:

```typescript
// Sandbox runner interface
interface SandboxConfig {
  cpuLimit: string;
  memoryLimit: string;
  timeoutSeconds: number;
  network: { allowedDomains: string[] };
  filesystem: { readOnly: string[]; writable: string[] };
}

async function executeSandboxed(
  code: string,
  config: SandboxConfig
): Promise<{ stdout: string; stderr: string; exitCode: number }> {
  const sandbox = await createIsolatedEnv(config);
  try {
    const result = await sandbox.execute(code);
    await auditLog({
      code_hash: hash(code),
      duration_ms: result.duration,
      exit_code: result.exitCode,
      tools_invoked: result.toolCalls
    });
    return result;
  } finally {
    await sandbox.cleanup();
  }
}
```

**Key Principles**:
- **Process isolation**: Use namespaces, cgroups, seccomp for containment
- **Resource limits**: Enforce CPU, memory, time, disk, FD, thread limits
- **Network control**: Allowlist domains/IPs, block sensitive destinations
- **Audit everything**: Log invocations, data flow, output sizes with tamper protection

**Trade-offs**:
- ✅ **Advantages**: Security, reproducibility, resource control, compliance-ready
- ⚠️ **Disadvantages**: Latency overhead (~100-500ms), complexity, infrastructure requirements
- 💡 **Alternatives**: Unrestricted execution (unsafe), VM-based (heavier), WASM (limited capabilities)

**Critical Security Note**:
Language-level sandboxes (like Python's `restricted_imports` example below) are **insufficient** for production security. They must **always** be wrapped in OS-level isolation (Docker, Firecracker, gVisor) to prevent container escapes and resource exhaustion.

**Optimization Note**:
To mitigate container startup latency (Cold Start), implement a **Warm Pool** strategy where a set of initialized containers are kept ready for immediate execution.

**Concrete Implementation Examples**:

```dockerfile
# Dockerfile for Python sandbox environment
FROM python:3.11-slim

# Create non-root user for execution
RUN useradd -m -s /bin/bash sandbox && \
    mkdir -p /workspace /tmp/sandbox

# Install security tools
RUN apt-get update && apt-get install -y \
    libseccomp2 \
    libcap2-bin \
    && rm -rf /var/lib/apt/lists/*

# Copy MCP tools wrapper
COPY --chown=sandbox:sandbox mcp_wrapper.py /app/mcp_wrapper.py
COPY --chown=sandbox:sandbox requirements.txt /app/requirements.txt

# Install Python dependencies in virtual environment
USER sandbox
WORKDIR /app
RUN python -m venv /home/sandbox/venv && \
    /home/sandbox/venv/bin/pip install --no-cache-dir -r requirements.txt

# Set up security constraints
USER root
RUN setcap -r /usr/local/bin/python3.11 2>/dev/null || true

# Switch to sandbox user
USER sandbox
ENV PATH="/home/sandbox/venv/bin:$PATH"

# Entry point with security flags
ENTRYPOINT ["python", "-u", "-B", "/app/mcp_wrapper.py"]
```

```python
# mcp_wrapper.py - Secure execution wrapper
import os
import sys
import json
import resource
import signal
from typing import Dict, Any
from contextlib import contextmanager

class SecureSandbox:
    """Secure execution environment for MCP code"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._setup_resource_limits()
        self._setup_signal_handlers()

    def _setup_resource_limits(self):
        """Apply resource constraints"""
        # CPU time limit (seconds)
        resource.setrlimit(resource.RLIMIT_CPU,
            (self.config.get('cpu_seconds', 30),
             self.config.get('cpu_seconds', 30)))

        # Memory limit (bytes)
        memory_mb = self.config.get('memory_mb', 512)
        resource.setrlimit(resource.RLIMIT_AS,
            (memory_mb * 1024 * 1024, memory_mb * 1024 * 1024))

        # File descriptor limit
        resource.setrlimit(resource.RLIMIT_NOFILE,
            (self.config.get('max_fds', 100),
             self.config.get('max_fds', 100)))

        # Process limit (prevent fork bombs)
        resource.setrlimit(resource.RLIMIT_NPROC,
            (self.config.get('max_processes', 1),
             self.config.get('max_processes', 1)))

    def _setup_signal_handlers(self):
        """Setup timeout handler"""
        def timeout_handler(signum, frame):
            raise TimeoutError("Execution timeout exceeded")

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(self.config.get('timeout_seconds', 60))

    @contextmanager
    def restricted_imports(self):
        """Restrict dangerous imports"""
        original_import = __builtins__.__import__

        def safe_import(name, *args, **kwargs):
            blocked = ['subprocess', 'os.system', 'eval', 'exec',
                      'compile', '__import__', 'open']
            if any(b in str(name) for b in blocked):
                raise ImportError(f"Import of '{name}' is not allowed")
            return original_import(name, *args, **kwargs)

        __builtins__.__import__ = safe_import
        try:
            yield
        finally:
            __builtins__.__import__ = original_import

    def execute(self, code: str) -> Dict[str, Any]:
        """Execute code with all security constraints"""
        with self.restricted_imports():
            # Create restricted namespace
            namespace = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'str': str,
                    'int': int,
                    'float': float,
                    'dict': dict,
                    'list': list,
                    'tuple': tuple,
                    'set': set,
                    'bool': bool,
                    'type': type,
                    'isinstance': isinstance,
                    'hasattr': hasattr,
                    'getattr': getattr,
                    'setattr': setattr,
                    'min': min,
                    'max': max,
                    'sum': sum,
                    'sorted': sorted,
                    'enumerate': enumerate,
                    'zip': zip,
                    'map': map,
                    'filter': filter,
                    # Explicitly exclude dangerous functions
                    # 'eval': None, 'exec': None, 'open': None
                },
                'mcp_tools': self._get_safe_mcp_tools()
            }

            # Execute with timeout
            exec(code, namespace)

            # Extract results
            return {
                'success': True,
                'output': namespace.get('result', None),
                'metrics': self._get_execution_metrics()
            }

    def _get_safe_mcp_tools(self):
        """Return sandboxed MCP tool wrappers"""
        # Import actual MCP tools with safety wrappers
        from mcp_safe_wrappers import (
            safe_read_file,
            safe_write_file,
            safe_list_files,
            safe_search_files
        )

        return {
            'read_file': safe_read_file,
            'write_file': safe_write_file,
            'list_files': safe_list_files,
            'search_files': safe_search_files
        }

# Docker Compose configuration for orchestration
```

```yaml
# docker-compose.yml - Multi-sandbox orchestration
version: '3.8'

services:
  sandbox-python:
    build:
      context: ./sandboxes/python
      dockerfile: Dockerfile
    restart: unless-stopped
    read_only: true
    tmpfs:
      - /tmp
      - /var/tmp
    security_opt:
      - no-new-privileges:true
      - seccomp:seccomp-profile.json
    cap_drop:
      - ALL
    cap_add:
      - DAC_OVERRIDE  # For file operations within allowed paths
    mem_limit: 512m
    cpus: "0.5"
    networks:
      - sandbox-net
    volumes:
      - ./workspace:/workspace:ro
      - ./outputs:/outputs:rw

  sandbox-nodejs:
    build:
      context: ./sandboxes/nodejs
      dockerfile: Dockerfile
    restart: unless-stopped
    read_only: true
    tmpfs:
      - /tmp
    security_opt:
      - no-new-privileges:true
      - seccomp:seccomp-profile.json
    cap_drop:
      - ALL
    mem_limit: 512m
    cpus: "0.5"
    networks:
      - sandbox-net
    volumes:
      - ./workspace:/workspace:ro
      - ./outputs:/outputs:rw

  sandbox-manager:
    build:
      context: ./manager
      dockerfile: Dockerfile
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - MAX_CONCURRENT_SANDBOXES=10
      - DEFAULT_TIMEOUT_SECONDS=60
    networks:
      - sandbox-net
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./audit-logs:/logs:rw

networks:
  sandbox-net:
    driver: bridge
    internal: true  # No external network access by default
```

```json
// seccomp-profile.json - Syscall filtering
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": [
        "read", "write", "open", "close", "stat", "fstat",
        "lstat", "poll", "lseek", "mmap", "mprotect",
        "munmap", "brk", "rt_sigaction", "rt_sigprocmask",
        "ioctl", "pread64", "pwrite64", "readv", "writev",
        "access", "pipe", "select", "sched_yield", "mremap",
        "msync", "mincore", "madvise", "shmget", "shmat",
        "shmctl", "dup", "dup2", "pause", "nanosleep",
        "getitimer", "alarm", "setitimer", "getpid",
        "sendfile", "socket", "connect", "accept"
      ],
      "action": "SCMP_ACT_ALLOW"
    },
    {
      "names": ["execve", "execveat"],
      "action": "SCMP_ACT_ERRNO"
    },
    {
      "names": ["fork", "vfork", "clone"],
      "action": "SCMP_ACT_ERRNO"
    },
    {
      "names": ["ptrace"],
      "action": "SCMP_ACT_ERRNO"
    }
  ]
}
```

**Sources**: [R1]

---

### Pattern: Progressive Tool Discovery

**Intent**: Load tool definitions on-demand with tiered detail levels, minimizing context overhead while maintaining discoverability.

**Context**: When working with large MCP servers offering dozens or hundreds of tools where pre-loading all definitions would exhaust context.

**Implementation**:

```typescript
// Tiered discovery API
interface SearchToolsOptions {
  query?: string;        // Optional keyword filter
  server?: string;       // Optional server filter
  detail: "name" | "name+description" | "full-schema";
}

async function searchTools(opts: SearchToolsOptions): Promise<ToolInfo[]> {
  const tools = await mcpClient.listTools({ server: opts.server });

  return tools
    .filter(t => !opts.query || t.name.includes(opts.query))
    .map(t => {
      if (opts.detail === "name") {
        return { name: t.name };
      } else if (opts.detail === "name+description") {
        return { name: t.name, description: t.description };
      } else {
        // Read full schema from file only when requested
        return {
          name: t.name,
          description: t.description,
          schema: readToolSchema(t.name)
        };
      }
    });
}
```

**Key Principles**:
- **Lazy loading**: Load schemas only when agent explicitly requests them
- **Tiered detail**: Provide minimal information first, expand on demand
- **Caching**: Memoize loaded definitions within session
- **File-based**: Store definitions in readable files for `readFile` tool access

**Trade-offs**:
- ✅ **Advantages**: Massive token savings (98.7% reduction), scalable to hundreds of tools
- ⚠️ **Disadvantages**: Multi-step discovery process, potential latency from file I/O
- 💡 **Alternatives**: Pre-load all (context explosion), embedding-based retrieval (complex)

**Sources**: [R1], [R3]

---

### Pattern: In-Sandbox Data Filtering

**Intent**: Process large datasets within the sandbox and expose only filtered/aggregated results to the model context.

**Context**: When working with tools that return large responses (thousands of records, large documents) where full data in context would be wasteful.

**Implementation**:

```python
# Data filtering within sandbox
import servers.google_drive as gdrive
import servers.salesforce as sf

# Fetch large dataset (stays in sandbox)
all_leads = await sf.query({
    "query": "SELECT * FROM Lead WHERE CreatedDate = THIS_MONTH"
})
print(f"Processing {len(all_leads)} leads...")  # Count to model

# Filter/aggregate in sandbox (not exposed to model)
high_value = [l for l in all_leads if l["AnnualRevenue"] > 1_000_000]
by_region = group_by(high_value, "Region")
stats = {region: len(leads) for region, leads in by_region.items()}

# Only summary to model
print(f"High-value leads by region: {stats}")
print(f"Top 5 leads: {high_value[:5]}")  # Sample only
```

**Key Principles**:
- **Keep data in sandbox**: Full datasets never leave execution environment
- **Expose summaries only**: Counts, aggregates, samples, statistics
- **Process before showing**: Filter, transform, deduplicate in sandbox
- **Sample intelligently**: First N, random sample, top K by score

**Trade-offs**:
- ✅ **Advantages**: Massive token savings, privacy protection, cost reduction
- ⚠️ **Disadvantages**: Model doesn't see raw data (may miss edge cases), requires careful summarization
- 💡 **Alternatives**: Streaming with incremental summaries, hierarchical aggregation, database queries

**Sources**: [R1]

---

### Pattern: Skill Composition

**Intent**: Combine multiple tool wrappers into reusable skills that abstract high-level workflows with clear documentation and error handling.

**Context**: When certain multi-tool sequences are repeatedly needed and can be packaged for reuse across different agent tasks.

**Implementation**:

```typescript
// skills/sync-drive-to-crm/main.ts
import * as gdrive from "../../servers/google-drive";
import * as salesforce from "../../servers/salesforce";

/**
 * Syncs Google Drive documents to Salesforce CRM
 *
 * Prerequisites:
 * - Google Drive access with read permissions
 * - Salesforce write access to ContentDocument
 *
 * Input: { folderId: string, accountId: string }
 * Output: { synced: number, errors: string[] }
 */
export async function syncDriveToCRM(
  folderId: string,
  accountId: string
): Promise<{ synced: number; errors: string[] }> {
  const docs = await gdrive.listFiles({ folderId });
  const errors: string[] = [];
  let synced = 0;

  for (const doc of docs) {
    try {
      const content = await gdrive.getDocument({ documentId: doc.id });
      await salesforce.createRecord({
        objectType: "ContentDocument",
        data: {
          Title: doc.name,
          Content: content.content,
          LinkedEntityId: accountId
        }
      });
      synced++;
    } catch (e) {
      errors.push(`${doc.name}: ${e.message}`);
    }
  }

  return { synced, errors };
}
```

**Key Principles**:
- **High-level abstraction**: Skills represent business logic, not low-level tool calls
- **Documentation required**: SKILL.md with purpose, I/O, prerequisites, examples
- **Error handling**: Graceful degradation, structured error reporting
- **State management**: Use workspace for intermediate artifacts

**Trade-offs**:
- ✅ **Advantages**: Reusability, maintainability, clearer abstractions, reduced model complexity
- ⚠️ **Disadvantages**: Additional abstraction layer, potential inflexibility for edge cases
- 💡 **Alternatives**: Direct tool composition (verbose), prompt-based procedures (fragile)

**Sources**: [R1]

---

### Pattern: Automatic Stub Generation

**Intent**: Auto-generate wrapper code from MCP tool schemas to reduce manual implementation burden and ensure schema consistency.

**Context**: When onboarding new MCP servers or updating existing ones with schema changes.

**Implementation**:

```python
# codegen/generate_wrappers.py
import json
from pathlib import Path
from typing import Dict, Any

WRAPPER_TEMPLATE = '''
from typing import TypedDict
from client.mcp_client import call_mcp_tool

class {input_class}(TypedDict):
{input_fields}

class {output_class}(TypedDict):
{output_fields}

async def {function_name}(
    input: {input_class}
) -> {output_class}:
    """{description}"""
    return await call_mcp_tool("{tool_id}", input)
'''

def generate_wrapper(tool_schema: Dict[str, Any]) -> str:
    input_fields = generate_typed_dict_fields(tool_schema["parameters"])
    output_fields = generate_typed_dict_fields(tool_schema["returns"])

    return WRAPPER_TEMPLATE.format(
        input_class=f"{to_pascal_case(tool_schema['name'])}Input",
        output_class=f"{to_pascal_case(tool_schema['name'])}Response",
        input_fields=input_fields,
        output_fields=output_fields,
        function_name=to_snake_case(tool_schema['name']),
        description=tool_schema['description'],
        tool_id=tool_schema['id']
    )

# Usage:
for tool in mcp_server.list_tools():
    schema = mcp_server.get_tool_schema(tool.name)
    wrapper_code = generate_wrapper(schema)
    output_path = Path(f"servers/{tool.server}/{tool.name}.py")
    output_path.write_text(wrapper_code)
```

**Key Principles**:
- **Schema-driven**: Single source of truth in MCP tool definitions
- **Type safety**: Generate language-native types from JSON Schema
- **Versioning**: Track schema versions, regenerate on changes
- **Validation**: Verify generated code compiles/passes type checking

**Trade-offs**:
- ✅ **Advantages**: Consistency, reduced manual work, automatic updates, fewer errors
- ⚠️ **Disadvantages**: Requires schema availability, generated code may need customization
- 💡 **Alternatives**: Manual implementation (error-prone), dynamic proxies (no type safety)

**TypeScript Implementation**:

```typescript
// codegen/generate-ts-wrappers.ts
import * as fs from 'fs';
import * as path from 'path';
import { JSONSchema7 } from 'json-schema';

interface ToolSchema {
  id: string;
  name: string;
  description: string;
  parameters: JSONSchema7;
  returns: JSONSchema7;
}

class TypeScriptWrapperGenerator {
  private readonly outputDir: string;

  constructor(outputDir: string) {
    this.outputDir = outputDir;
  }

  generateWrapper(schema: ToolSchema): string {
    const inputInterface = this.generateInterface(
      `${this.toPascalCase(schema.name)}Input`,
      schema.parameters
    );

    const outputInterface = this.generateInterface(
      `${this.toPascalCase(schema.name)}Output`,
      schema.returns
    );

    const functionName = this.toCamelCase(schema.name);

    return `
// Auto-generated from MCP schema - DO NOT EDIT MANUALLY
import { MCPClient } from '../client/mcp-client';

${inputInterface}

${outputInterface}

/**
 * ${schema.description}
 * @param input The input parameters for ${schema.name}
 * @returns Promise resolving to the tool output
 */
export async function ${functionName}(
  input: ${this.toPascalCase(schema.name)}Input
): Promise<${this.toPascalCase(schema.name)}Output> {
  return await MCPClient.callTool<
    ${this.toPascalCase(schema.name)}Input,
    ${this.toPascalCase(schema.name)}Output
  >('${schema.id}', input);
}

// Type guard for runtime validation
export function is${this.toPascalCase(schema.name)}Output(
  value: unknown
): value is ${this.toPascalCase(schema.name)}Output {
  return (
    typeof value === 'object' &&
    value !== null &&
    ${this.generateTypeGuard(schema.returns)}
  );
}
`.trim();
  }

  private generateInterface(name: string, schema: JSONSchema7): string {
    const properties = schema.properties || {};
    const required = new Set(schema.required || []);

    const fields = Object.entries(properties).map(([key, prop]) => {
      const optional = !required.has(key) ? '?' : '';
      const type = this.jsonSchemaToTypeScript(prop as JSONSchema7);
      const description = (prop as any).description;

      let field = `  ${key}${optional}: ${type};`;
      if (description) {
        field = `  /** ${description} */\n${field}`;
      }
      return field;
    }).join('\n');

    return `export interface ${name} {\n${fields}\n}`;
  }

  private jsonSchemaToTypeScript(schema: JSONSchema7): string {
    switch (schema.type) {
      case 'string':
        if (schema.enum) {
          return schema.enum.map(v => `'${v}'`).join(' | ');
        }
        return 'string';
      case 'number':
      case 'integer':
        return 'number';
      case 'boolean':
        return 'boolean';
      case 'array':
        if (schema.items) {
          const itemType = this.jsonSchemaToTypeScript(
            schema.items as JSONSchema7
          );
          return `${itemType}[]`;
        }
        return 'any[]';
      case 'object':
        if (schema.properties) {
          const props = Object.entries(schema.properties)
            .map(([k, v]) => `${k}: ${this.jsonSchemaToTypeScript(v as JSONSchema7)}`)
            .join('; ');
          return `{ ${props} }`;
        }
        if (schema.additionalProperties) {
          const valueType = typeof schema.additionalProperties === 'object'
            ? this.jsonSchemaToTypeScript(schema.additionalProperties)
            : 'any';
          return `Record<string, ${valueType}>`;
        }
        return 'object';
      case 'null':
        return 'null';
      default:
        // Handle union types
        if (Array.isArray(schema.type)) {
          return schema.type.map(t =>
            this.jsonSchemaToTypeScript({ ...schema, type: t })
          ).join(' | ');
        }
        return 'any';
    }
  }

  private generateTypeGuard(schema: JSONSchema7): string {
    const properties = schema.properties || {};
    const required = schema.required || [];

    const checks = required.map(prop =>
      `'${prop}' in value`
    );

    Object.entries(properties).forEach(([key, prop]) => {
      const propSchema = prop as JSONSchema7;
      if (propSchema.type === 'string') {
        checks.push(`typeof (value as any).${key} === 'string'`);
      } else if (propSchema.type === 'number') {
        checks.push(`typeof (value as any).${key} === 'number'`);
      } else if (propSchema.type === 'boolean') {
        checks.push(`typeof (value as any).${key} === 'boolean'`);
      }
    });

    return checks.join(' &&\n    ');
  }

  async generateAllWrappers(schemas: ToolSchema[]): Promise<void> {
    // Ensure output directory exists
    await fs.promises.mkdir(this.outputDir, { recursive: true });

    // Generate index file
    const indexContent: string[] = [
      '// Auto-generated barrel export - DO NOT EDIT MANUALLY',
      ''
    ];

    for (const schema of schemas) {
      // Generate wrapper for each tool
      const wrapperCode = this.generateWrapper(schema);
      const fileName = `${this.toKebabCase(schema.name)}.ts`;
      const filePath = path.join(this.outputDir, fileName);

      await fs.promises.writeFile(filePath, wrapperCode, 'utf-8');
      console.log(`Generated: ${filePath}`);

      // Add to index exports
      const functionName = this.toCamelCase(schema.name);
      indexContent.push(
        `export { ${functionName}, ` +
        `${this.toPascalCase(schema.name)}Input, ` +
        `${this.toPascalCase(schema.name)}Output, ` +
        `is${this.toPascalCase(schema.name)}Output } from './${fileName.replace('.ts', '')}';`
      );
    }

    // Write index file
    const indexPath = path.join(this.outputDir, 'index.ts');
    await fs.promises.writeFile(
      indexPath,
      indexContent.join('\n'),
      'utf-8'
    );
    console.log(`Generated index: ${indexPath}`);
  }

  // Utility methods for case conversion
  private toPascalCase(str: string): string {
    return str
      .split(/[-_]/)
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join('');
  }

  private toCamelCase(str: string): string {
    const pascal = this.toPascalCase(str);
    return pascal.charAt(0).toLowerCase() + pascal.slice(1);
  }

  private toKebabCase(str: string): string {
    return str.replace(/([A-Z])/g, '-$1').toLowerCase().replace(/^-/, '');
  }
}

// CLI usage
async function main() {
  const generator = new TypeScriptWrapperGenerator('./generated/mcp-wrappers');

  // Load schemas from MCP server
  const schemas = await loadSchemasFromMCPServer();

  // Generate all wrappers
  await generator.generateAllWrappers(schemas);

  // Run TypeScript compiler to verify generated code
  const { exec } = require('child_process');
  exec('npx tsc --noEmit ./generated/mcp-wrappers/*.ts', (error, stdout, stderr) => {
    if (error) {
      console.error('Type checking failed:', stderr);
      process.exit(1);
    }
    console.log('All wrappers generated and type-checked successfully!');
  });
}

if (require.main === module) {
  main().catch(console.error);
}
```

```json
// tsconfig.json for generated code
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./generated"
  },
  "include": ["generated/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**Sources**: [R1]

---

### Pattern: System Prompt Design

**Intent**: Configure the model to act as a code-generating agent that discovers and uses tools via sandboxed execution, rather than expecting direct tool invocation.

**Context**: When initializing the agent session and defining its operational boundaries.

**Implementation**:

```markdown
# System Prompt Template

You are an expert AI agent with access to a secure code execution environment.
Your goal is to solve tasks by writing Python/TypeScript code.

## Capabilities
- **No Direct Tool Calls**: You cannot call tools directly. Instead, you must write code to import and use them.
- **Tool Access**: Tools are available in the `mcp_tools` module or via standard imports.
- **Discovery**:
  1. Search for tools: `await mcp_tools.search_tools({ query: "..." })`
  2. Read definitions: `await mcp_tools.read_file("servers/...")`
- **Execution**: Write complete, executable scripts.

## Workflow
1. **Search**: Find relevant tools for the task.
2. **Inspect**: Read tool schemas if you are unsure of arguments.
3. **Plan**: Outline your approach.
4. **Code**: Write a complete script to execute the plan.
5. **Review**: Analyze the execution output and refine if necessary.

## Constraints
- **Data Handling**: Do not output raw data > 50 lines. Summarize it in code.
- **Error Handling**: Handle errors gracefully with try/catch blocks.
- **Imports**: Use only allowed libraries.
```

**Key Principles**:
- **Role Definition**: Explicitly shift model from "tool caller" to "coder".
- **Discovery Instructions**: Teach the model how to find tools (Progressive Disclosure).
- **Output Constraints**: Enforce summarization to save tokens.
- **One-Shot Examples**: Include at least one example of the Search -> Read -> Code loop.

**Trade-offs**:
- ✅ **Advantages**: Clear expectations, reduced hallucinations, standardized behavior
- ⚠️ **Disadvantages**: Consumes system prompt tokens (though less than full tool definitions)
- 💡 **Alternatives**: Fine-tuning (expensive), hardcoded logic (inflexible)

---

### Pattern: Self-Correction Loop

**Intent**: Automatically recover from execution errors by analyzing stack traces and rewriting code, with strict iteration limits to prevent infinite loops.

**Context**: When the sandboxed execution returns a non-zero exit code or exception.

**Implementation**:

```python
# Agent execution loop with self-correction
MAX_RETRIES = 3

async def run_agent_task(task: str):
    context = initialize_context(task)
    attempts = 0

    while attempts < MAX_RETRIES:
        # 1. Generate Code
        code = await model.generate_code(context)

        # 2. Execute in Sandbox
        result = await sandbox.execute(code)

        if result.success:
            return result.output

        # 3. Analyze Error
        attempts += 1
        error_msg = f"Execution failed (Attempt {attempts}/{MAX_RETRIES}):\n{result.stderr}"

        # 4. Update Context with Error
        context.append({
            "role": "user",
            "content": f"The code failed with this error:\n{error_msg}\n"
                       f"Please fix the code and try again."
        })

    # Fallback after max retries
    raise AgentError("Failed to complete task after multiple attempts.")
```

**Key Principles**:
- **Feedback Loop**: Feed stderr/exceptions back to the model as context.
- **Iteration Limit**: Hard limit (e.g., 3 retries) to prevent infinite token consumption.
- **State Preservation**: Maintain conversation history so the model knows what failed previously.
- **Human Handoff**: Escalate to human or return structured error after max retries.

**Trade-offs**:
- ✅ **Advantages**: Robustness, ability to fix minor syntax/logic errors, higher success rate
- ⚠️ **Disadvantages**: Increased latency and token cost per task
- 💡 **Alternatives**: Single-shot (fragile), human-in-the-loop (slow)

**Sources**: [R1]

---

## Decision Checklist

- [ ] **Sandbox environment configured with resource limits**: CPU, memory, time, disk, FD, thread limits enforced [R1]
  - **Verify**: Test sandbox with resource-intensive code, confirm limits trigger
  - **Impact**: Without limits, malicious/buggy code can DoS host system
  - **Mitigation**: Use proven sandboxing (Docker, Firecracker, gVisor) with preset profiles

- [ ] **OS-level isolation is mandatory**: Language-level sandboxes (e.g., Python `restricted_imports`) are used ONLY as a secondary defense layer [R1]
  - **Verify**: Confirm Docker/Firecracker/gVisor is wrapping the execution runtime
  - **Impact**: Container escape, host system compromise
  - **Mitigation**: Deploy with `gvisor-runsc` or similar secure runtime

- [ ] **Warm pools implemented for latency sensitivity**: Idle containers kept ready [R1]
  - **Verify**: Measure start-up latency; should be <500ms
  - **Impact**: Poor user experience due to cold start delays (1-3s)
  - **Mitigation**: Maintain a pool of 2-5 warm sandboxes

- [ ] **Network access restricted to required domains**: Allowlist configured, sensitive destinations blocked [R1]
  - **Verify**: Attempt connections to non-allowed domains, confirm blocks
  - **Impact**: Unrestricted network access enables data exfiltration
  - **Mitigation**: Default-deny network policy with explicit allowlist per tool

- [ ] **Audit logging captures all tool invocations**: Logs include tool, input hash, output size, duration, trace_id [R1]
  - **Verify**: Review audit logs for completeness and tamper resistance
  - **Impact**: Compliance violations, inability to debug/reproduce issues
  - **Mitigation**: Implement structured logging with retention policies

- [ ] **Progressive disclosure reduces context by >90%**: Token usage measured before/after migration [R1]
  - **Verify**: Count tokens in pre-load vs. on-demand approaches
  - **Impact**: Context window exhaustion, high costs, slow responses
  - **Mitigation**: Implement tiered discovery API with lazy loading

- [ ] **All wrappers have type annotations**: Python TypedDict, TypeScript interfaces complete [R1]
  - **Verify**: Run type checkers (mypy, tsc --noEmit), confirm 0 errors
  - **Impact**: Runtime errors, poor IDE support, fragile generated code
  - **Mitigation**: Use code generation from schemas with validation

- [ ] **PII/PHI data masked in logs and model output**: Redaction rules tested [R1]
  - **Verify**: Process test data with sensitive fields, confirm masking
  - **Impact**: Regulatory violations (GDPR, HIPAA), privacy breaches
  - **Mitigation**: Automatic masking in sandbox output, structured redaction rules

- [ ] **Error handling includes retries with exponential backoff**: Transient failures handled gracefully [R1]
  - **Verify**: Simulate network failures, confirm retry behavior
  - **Impact**: Task failures from transient issues, poor user experience
  - **Mitigation**: Implement retry decorator with jitter, circuit breakers

- [ ] **Self-correction loop has hard limits**: Max retries set (e.g., 3) to prevent infinite loops [R1]
  - **Verify**: Test with permanently failing code, confirm loop terminates
  - **Impact**: Infinite token consumption, stuck processes
  - **Mitigation**: Counter in execution loop

- [ ] **Debug replay capability**: System stores inputs/seeds to reproduce failures [R1]
  - **Verify**: Re-run a past job ID and confirm identical execution path
  - **Impact**: Inability to diagnose complex agent failures
  - **Mitigation**: Store full context, seeds, and code in immutable logs

- [ ] **Secrets managed via secure storage (Vault, env vars)**: No hardcoded credentials [R1]
  - **Verify**: Scan codebase for secrets, confirm environment-based loading
  - **Impact**: Credential leakage, unauthorized access
  - **Mitigation**: Use secret management systems, rotate keys regularly

- [ ] **Tool wrappers follow naming convention**: `<server>__<tool>` identifier, `verb_object` function [R1]
  - **Verify**: Review wrapper file names and function signatures
  - **Impact**: Inconsistency, discoverability issues, namespace collisions
  - **Mitigation**: Enforce naming in code generation templates and linters

- [ ] **Skills documented with SKILL.md**: Purpose, I/O, prerequisites, examples present [R1]
  - **Verify**: Check each skill directory for complete documentation
  - **Impact**: Unclear usage, maintenance difficulty, poor discoverability
  - **Mitigation**: Template-based skill creation with required fields

---

## Anti-patterns / Pitfalls

### Anti-pattern: Pre-loading All Tool Definitions

**Symptom**: System prompt or initial context contains full schemas for all available MCP tools (dozens to hundreds), causing context window exhaustion or massive token costs.

**Why It Happens**: Simplest implementation approach; mimics traditional function calling patterns where all functions are declared upfront.

**Impact**:
- Context window consumed by tool definitions instead of task data
- Token costs 50-100x higher than necessary
- Cannot scale beyond ~20-30 tools before hitting limits
- Reduced quality due to less room for examples and reasoning

**Solution**: Implement progressive disclosure with tiered detail levels (name → name+description → full-schema) and on-demand loading.

**Example**:

```typescript
// ❌ Anti-pattern: Pre-load everything
const systemPrompt = `
You have access to these tools:
${allTools.map(t => JSON.stringify(t.schema)).join('\n')}
`;  // 150,000 tokens consumed

// ✅ Correct pattern: On-demand loading
const systemPrompt = `
You can search for tools using searchTools({query, detail: "name"|"name+description"|"full-schema"}).
Read tool definitions from files as needed.
`;  // 200 tokens, load specifics later
```

**Sources**: [R1]

### Anti-pattern: Exposing Large Datasets to Model Context

**Symptom**: Sandbox returns thousands of records or multi-megabyte documents directly to model, causing context bloat and high costs.

**Why It Happens**: Direct translation of tool output without considering context efficiency; treating sandbox like external API.

**Impact**:
- Token costs 10-100x higher than necessary
- Context window filled with raw data instead of insights
- Model struggles to process large unstructured data
- Privacy risks from exposing all data to model logs

**Solution**: Filter, aggregate, and summarize data within sandbox; expose only insights, statistics, and samples to model.

**Example**:

```python
# ❌ Anti-pattern: Expose all data
all_records = await db.query("SELECT * FROM transactions")
print(all_records)  # 50,000 records → 2M tokens to model

# ✅ Correct pattern: Filter and summarize
all_records = await db.query("SELECT * FROM transactions")
high_value = [r for r in all_records if r["amount"] > 10000]
stats = {
    "total": len(all_records),
    "high_value_count": len(high_value),
    "total_amount": sum(r["amount"] for r in all_records)
}
print(f"Transaction summary: {stats}")  # 100 tokens
print(f"Top 5 high-value: {high_value[:5]}")  # 500 tokens
```

**Sources**: [R1]

### Anti-pattern: Unsandboxed Code Execution

**Symptom**: Agent-generated code runs directly on host system without isolation, resource limits, or audit logging.

**Why It Happens**: Sandbox complexity perceived as unnecessary overhead; trust in model-generated code.

**Impact**:
- Security vulnerabilities (arbitrary code execution)
- Resource exhaustion (infinite loops, memory leaks)
- No audit trail for compliance
- Cannot enforce least privilege per tool

**Solution**: Always execute agent code in isolated sandboxes with enforced resource limits, network restrictions, and comprehensive audit logging.

**Example**:

```typescript
// ❌ Anti-pattern: Direct execution
const code = await model.generateCode(task);
eval(code);  // Runs on host, no limits, huge security risk

// ✅ Correct pattern: Sandboxed execution
const code = await model.generateCode(task);
const result = await sandbox.execute(code, {
  cpuLimit: "1.0",
  memoryLimit: "512Mi",
  timeoutSeconds: 300,
  network: { allowedDomains: ["api.example.com"] },
  audit: true
});
```

**Sources**: [R1]

### Anti-pattern: Missing Type Annotations in Wrappers

**Symptom**: Tool wrappers use untyped dictionaries or `any` types, providing no compile-time safety or IDE support.

**Why It Happens**: Perceived as faster to write; underestimating value of type safety for agent-generated code.

**Impact**:
- Runtime errors from schema mismatches
- Poor IDE autocomplete for developers and models
- Difficult to detect breaking changes
- Fragile code generation by models

**Solution**: Always use strict type annotations (TypedDict in Python, interfaces in TypeScript) with complete field definitions.

**Example**:

```python
# ❌ Anti-pattern: No types
async def get_document(input):  # What fields? What types?
    return await call_mcp_tool("google_drive__get_document", input)

# ✅ Correct pattern: Full type annotations
from typing import TypedDict

class GetDocumentInput(TypedDict):
    documentId: str

class GetDocumentResponse(TypedDict):
    content: str
    title: str
    mimeType: str

async def get_document(input: GetDocumentInput) -> GetDocumentResponse:
    """Read a document from Google Drive"""
    return await call_mcp_tool("google_drive__get_document", input)
```

**Sources**: [R1]

### Anti-pattern: No Error Handling or Retries

**Symptom**: Tool calls fail permanently on transient network issues; no retry logic or circuit breakers implemented.

**Why It Happens**: Happy-path focus during development; underestimating frequency of transient failures.

**Impact**:
- Tasks fail unnecessarily from temporary issues
- Poor user experience with brittle workflows
- Cascading failures in multi-tool sequences
- No graceful degradation

**Solution**: Implement retry logic with exponential backoff and jitter; use circuit breakers for failing services; structure errors for model understanding.

**Example**:

```typescript
// ❌ Anti-pattern: No retry logic
async function callMCPTool(tool: string, input: any) {
  return await transport.invoke(tool, input);
  // Fails permanently on network blip
}

// ✅ Correct pattern: Retries with backoff
async function callMCPTool(tool: string, input: any, opts?: CallOptions) {
  const maxRetries = opts?.maxRetries ?? 3;
  let lastError: Error;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await transport.invoke(tool, input);
    } catch (e) {
      lastError = e;
      if (!isRetryable(e) || attempt === maxRetries - 1) throw e;

      const delay = Math.min(1000 * 2 ** attempt, 10000);
      const jitter = Math.random() * 1000;
      await sleep(delay + jitter);
    }
  }

  throw lastError;
}
```

**Sources**: [R1]

### Anti-pattern: Language-Level Sandboxing Only

**Symptom**: Relying solely on Python's `restricted_imports` or Node.js `vm` module for security.

**Why It Happens**: Easier to implement than Docker/Firecracker; misconception that it is "good enough".

**Impact**:
- Trivial to bypass (e.g., via introspection, segfaults, or logic bombs)
- False sense of security
- No resource isolation (CPU/Memory bombs still work)

**Solution**: Always wrap language runtimes in OS-level virtualization (Containers, MicroVMs). Language-level restrictions are only a defense-in-depth measure.

### Anti-pattern: Infinite Correction Loops

**Symptom**: Agent keeps trying to fix code that fails with the same error, consuming infinite tokens until timeout.

**Why It Happens**: Missing iteration counter in the agent loop; assuming the model will eventually "get it right".

**Impact**:
- Massive token waste
- System hangs
- User frustration

**Solution**: Implement a strict `MAX_RETRIES` counter. If code fails N times, abort with a structured error or request human intervention.

---

## Evaluation

### Metrics

**Token Reduction Rate**: Percentage reduction in tokens consumed compared to pre-loading all tool definitions.
- **Why It Matters**: Primary cost optimization metric; directly impacts operating costs and context availability
- **Target**: >90% reduction (e.g., 150K → <15K tokens)
- **Measurement**: Compare token counts before/after migration using tokenizer (tiktoken, transformers)
- **Tools**: Token counters, cost tracking dashboards, A/B testing
- **Frequency**: Continuous monitoring with weekly cost reports

**Tool Call Success Rate**: Percentage of tool invocations that succeed (including retries).
- **Why It Matters**: Reliability indicator; low success rate indicates infrastructure or error handling issues
- **Target**: >98% success after retries
- **Measurement**: Ratio of successful completions to total attempts in audit logs
- **Tools**: Observability platforms (Datadog, Grafana), audit log analyzers
- **Frequency**: Real-time monitoring with alerts for drops below threshold

**Sandbox Overhead Latency**: Additional time required for sandboxed execution vs. direct execution.
- **Why It Matters**: Determines feasibility for latency-sensitive applications
- **Target**: <500ms P95 overhead for typical workloads
- **Measurement**: Compare execution time with/without sandboxing
- **Tools**: Performance profilers, distributed tracing (Jaeger, Tempo)
- **Frequency**: Load testing before deployment, continuous monitoring in production

**Data Exposure Ratio**: Percentage of intermediate data kept in sandbox vs. exposed to model.
- **Why It Matters**: Privacy and token optimization metric; lower is better
- **Target**: <5% of raw data exposed (95%+ filtered in sandbox)
- **Measurement**: Compare sizes of tool outputs vs. model-visible outputs
- **Tools**: Custom analyzers, audit log parsers
- **Frequency**: Weekly sampling audits

**Sources**: [R1]

### Testing Strategies

**Unit Tests**:
- Each wrapper tested with valid/invalid inputs against schema
- MCP client tested with mocked transport layer
- Error handling tested (timeouts, malformed responses, rate limits)
- Type annotations verified with static analysis (mypy, tsc)

**Integration Tests**:
- Full sandbox lifecycle: code generation → execution → result parsing
- Multi-tool workflows tested end-to-end
- Progressive disclosure tested (search → load → invoke)
- Skill compositions tested with real MCP servers

**Performance Benchmarks**:
- Token consumption measured across representative workloads
- Sandbox startup and execution time profiled
- Memory footprint during large data processing
- Concurrent execution capacity tested

**Security Tests**:
- Sandbox escape attempts (privilege escalation, file traversal)
- Resource exhaustion attacks (fork bombs, memory leaks)
- Network policy violations (blocked domains, data exfiltration)
- Secret leakage scans (logs, outputs, error messages)

### Success Criteria

- [ ] Token consumption reduced by >90% compared to pre-loading baseline
- [ ] All tool wrappers have complete type annotations passing static analysis
- [ ] Sandbox resource limits enforced (CPU, memory, time, network, FDs)
- [ ] Audit logs capture 100% of tool invocations with tamper protection
- [ ] Tool call success rate >98% including retry logic
- [ ] Progressive disclosure implemented with tiered detail levels
- [ ] Data filtering reduces model-visible data to <5% of raw outputs
- [ ] PII/PHI redaction rules tested and enforced
- [ ] Error handling includes retries with exponential backoff
- [ ] Security review passed (sandbox isolation, secret management, audit completeness)

---

## Practical Examples

### 16.1 Document Processing Workflow

**Requirement**: Retrieve meeting transcript, summarize, and update CRM

```ts
import * as gdrive from "../servers/google-drive";
import * as salesforce from "../servers/salesforce";

// Retrieve large document
const transcript = (await gdrive.getDocument({
  documentId: "abc123"
})).content;

// Process within sandbox (not exposed to model)
const notes = summarize(transcript);  // 10,000 lines → 500 words

// Update CRM with summary
await salesforce.updateRecord({
  objectType: "SalesMeeting",
  recordId: "00Q5f000001abcXYZ",
  data: { Notes: notes }
});

// Only this summary goes to model
console.log("✓ CRM updated with summarized notes");
```

### 16.2 Data Analysis Pipeline

```python
import servers.sheets as sheets
import servers.analytics as analytics

# Fetch large dataset
data = await sheets.get_all_rows({"sheetId": "quarterly"})
print(f"Processing {len(data)} records...")  # Model sees count

# Heavy processing in sandbox
metrics = calculate_metrics(data)
anomalies = detect_anomalies(data)

# Only send insights to model
print(f"Key insights: {metrics['summary']}")
print(f"Anomalies detected: {len(anomalies)}")

# Store detailed results
await analytics.save_report({
  "reportId": "Q4-2024",
  "metrics": metrics,
  "anomalies": anomalies[:10]  # Limit exposure
})
```

---

## Update Log

- **2025-11-24** – Fixed Update Log date inconsistencies. (Author: AI-First)
- **2025-11-22** – Updated based on peer review: added System Prompt Design and Self-Correction Loop patterns, clarified OS-level sandbox requirements, added warm pool and debug replay checklists. (Author: AI-First)
- **2025-11-19** – Enhanced Sandbox-Based Execution pattern with complete Docker implementation, security profiles, and Python wrapper. Added TypeScript stub generation implementation with full type mapping and CLI tooling. (Author: AI-First)
- **2025-11-14** – Added Practical Examples section with document processing and data analysis pipeline examples. Updated metadata. (Author: AI-First)
- **2025-11-13** – Initial specification created covering Code MCP architecture, implementation patterns, progressive disclosure, sandbox execution, security practices, and cost optimization strategies. (Author: AI-First)

---

## See Also

### Prerequisites
- [mcp-protocol](https://modelcontextprotocol.io/) – Understanding MCP specification is essential for implementing Code MCP
- [sandbox-security](https://en.wikipedia.org/wiki/Sandbox_(computer_security)) – Foundational concepts for safe code execution
- [json-schema](https://json-schema.org/) – Required for type generation and validation

### Related Topics
- [UNIVERSAL_AGENT_SKILL.md](./UNIVERSAL_AGENT_SKILL.md) – Complementary specification for agent skill packaging and distribution
- [EXEC_PLAN.md](./EXEC_PLAN.md) – Task planning methodology for AI-driven development
- [SSOT.md](./SSOT.md) – Governance guide for Single Source of Truth
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) – Alternative approaches and comparison points
- [gVisor](https://gvisor.dev/) – Deep dive into sandboxing technologies and configurations

### Advanced / Platform-specific
- [docker-sandboxing](https://docs.docker.com/) – Docker-based sandbox implementation
- [firecracker-microvm](https://firecracker-microvm.github.io/) – Lightweight VM-based sandboxing
- [gvisor](https://gvisor.dev/) – Application kernel for container sandboxing
- [e2b-sandboxes](https://e2b.dev/) – Managed sandbox service for agent execution

---

## References

- [R1] Anthropic. "Code execution with MCP: building more efficient AI agents." Anthropic Engineering Blog. https://www.anthropic.com/engineering/code-execution-with-mcp (accessed 2025-11-13)
- [R2] Model Context Protocol. "MCP Specification." Official Documentation. https://modelcontextprotocol.io (accessed 2025-11-13)
- [R3] Research on Progressive Disclosure. "Dynamic context loading strategies in AI systems." (multiple academic and industry sources)

---

**Document ID**: `docs/CODE_MCP.md`
**Canonical URL**: `https://github.com/artificial-intelligence-first/ssot/blob/main/docs/CODE_MCP.md`
**License**: MIT
