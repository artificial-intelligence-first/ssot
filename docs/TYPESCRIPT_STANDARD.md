---
title: TypeScript Standard Set
slug: typescript-standard
summary: "TypeScript configuration SSOT for all projects"
type: spec
tags: [typescript, standards, linting, testing, zod, ssot]
last_updated: 2025-11-24
---

# TypeScript Standard Set

## Agent Contract

- **PURPOSE**:
  - Define the authoritative TypeScript configuration and tooling standards for all TypeScript projects
  - Establish non-negotiable rules for type safety, linting, formatting, and runtime validation
  - Provide a canonical reference for AI agents and developers when creating or modifying TypeScript code
- **USE_WHEN**:
  - Creating new TypeScript projects or repositories
  - Configuring build pipelines and CI/CD for TypeScript projects
  - Resolving questions about TypeScript configuration standards
  - AI agents generating TypeScript code or configuration files
- **DO_NOT_USE_WHEN**:
  - Working with non-TypeScript projects (use language-specific standards)
  - Documenting project-specific business logic
  - Creating temporary prototypes or proof-of-concepts where strict typing may hinder rapid iteration
- **PRIORITY**:
  - This document takes precedence over any project-specific TypeScript configurations that conflict with these standards
  - Deviations require explicit justification and must be documented in project-specific SSOT files
- **RELATED_TOPICS**:
  - ssot-guide
  - code-quality
  - ai-first-development
  - ci-cd-standards

### Agent-Specific Behavior

- **When generating TypeScript code**:
  1. Always apply the strict tsconfig settings defined in this document
  2. Do not propose relaxing `strict` or disabling lint rules by default. If a rule must be adjusted, explain why and propose a narrow, well-scoped solution with human review
  3. Always use Zod for runtime validation at IO boundaries - never use type assertions (`as Type`) for unvalidated external data
- **When configuring new projects**:
  - Use the configurations in this document as the authoritative source, and adapt only paths or environment-specific options (e.g. `target`, `lib`, `moduleResolution`) as needed
  - Ensure all required npm scripts are present
  - Set up CI pipeline with all required gates
- **Security Protocol**:
  - Never use type assertions (`as Type`) for unvalidated external data
  - Always validate external data with Zod schemas before use
  - Treat all unvalidated external data as potentially unsafe
  - Type assertions are only allowed in documented exceptional cases (e.g. DOM APIs, third-party libraries with incorrect typings)

## 1. Overview

The TypeScript Standard Set defines the baseline configuration and tooling requirements for all TypeScript projects within our AI-First organization. This document serves as the Single Source of Truth (SSOT) for TypeScript development standards, ensuring consistency, type safety, and maintainability across all projects.

### Purpose and Scope

- **Target Audience**: All TypeScript projects including frontend applications, backend services, AI agents, CLI tools, and libraries
- **Goal**: Provide a clear, unambiguous standard that new repositories and AI agents can adopt without hesitation
- **Compatibility**: Designed to work seamlessly with AGDD (AI-Guided Driven Development), MAG-SAG patterns, and AI-First development workflows

This standard prioritizes:
- **Type safety** over convenience
- **Explicit error handling** over implicit assumptions
- **Runtime validation** at all IO boundaries
- **Automated enforcement** through CI/CD pipelines

## 2. tsconfig.base.json – Shared Compiler Baseline

All TypeScript projects must inherit from a common `tsconfig.base.json` configuration. Environment-specific settings (target, lib, module, moduleResolution) should be overridden in individual project configurations.

> **Note**: Environment-specific options such as `target`, `lib`, `module`, and `moduleResolution` MUST be set in the project's own `tsconfig.json`. The `tsconfig.base.json` is only responsible for **safety and quality** flags.

### Standard Configuration

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,
    "useUnknownInCatchVariables": true,
    "esModuleInterop": true,
    "resolveJsonModule": true
  }
}
```

### Key Compiler Options Explained

- **`strict: true`**: Enables all strict type-checking options including `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, etc. This is non-negotiable for type safety.
- **`noUnusedLocals` & `noUnusedParameters`**: Detects unused variables and parameters at compile time, preventing dead code accumulation.
- **`noImplicitReturns`**: Ensures all code paths in functions explicitly return a value when expected.
- **`noFallthroughCasesInSwitch`**: Prevents accidental fallthrough in switch statements, a common source of bugs.
- **`forceConsistentCasingInFileNames`**: Prevents cross-platform issues with case-sensitive file systems.
- **`useUnknownInCatchVariables`**: Changes catch clause variables from `any` to `unknown`, forcing explicit type checking of errors.
- **`esModuleInterop`**: Essential for modern ES module interoperability with CommonJS modules.
- **`resolveJsonModule`**: Allows importing JSON files with type inference, standard in modern TypeScript projects.

### Additional Compiler Options to Consider

- **`noEmitOnError: true`**: Prevents JavaScript emission when type errors exist. Strongly recommended for production builds.
- **`skipLibCheck`**: We default to `false` for library correctness, but large monorepos MAY use `true` as an explicit, documented exception to improve build performance.
- **`isolatedModules: true`**: Required when using transpile-only tools (Vite, SWC, esbuild). Recommended for all new projects.

### Progressive Enhancement Options (Appendix A)

The following options provide additional type safety but may require code changes in existing projects:

**Recommended for new projects:**
- **`noImplicitOverride: true`**: Ensures `override` keyword is used when overriding base class methods
- **`exactOptionalPropertyTypes: true`**: Distinguishes between `undefined` and missing properties

**Consider for maximum safety (breaking changes likely):**
- **`noUncheckedIndexedAccess: true`**: Adds `undefined` to index signature access (e.g., `arr[i]` becomes `T | undefined`)
- **`noPropertyAccessFromIndexSignature: true`**: Requires bracket notation for index signatures

Adopt these progressively based on project maturity and team readiness.

## 3. ESLint + TypeScript-ESLint + Prettier – Linting and Formatting

The standard combines ESLint for static analysis, TypeScript-ESLint for TypeScript-specific rules, and Prettier for consistent formatting.

### Standard ESLint Configuration

```javascript
// .eslintrc.cjs (example)
module.exports = {
  parser: "@typescript-eslint/parser",
  parserOptions: {
    project: "./tsconfig.json",
    sourceType: "module"
  },
  plugins: ["@typescript-eslint"],
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking",
    "prettier"
  ],
  rules: {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-non-null-assertion": "error",
    "@typescript-eslint/ban-ts-comment": [
      "error",
      { "ts-ignore": true, "ts-nocheck": true }
    ],
    "@typescript-eslint/no-unsafe-assignment": "error",
    "@typescript-eslint/no-unsafe-member-access": "error",
    "@typescript-eslint/no-unsafe-call": "error",
    "@typescript-eslint/no-unsafe-return": "error",
    "@typescript-eslint/no-floating-promises": "error",
    "@typescript-eslint/require-await": "error"
  }
};
```

### Rule Rationale

- **`no-explicit-any`**: Prohibits the use of `any` type, maintaining type safety throughout the codebase. If truly needed, use `unknown` and narrow the type.
- **`no-non-null-assertion`**: Bans the non-null assertion operator (`!`), preventing runtime errors from incorrect null/undefined assumptions.
- **`ban-ts-comment`**: Prohibits `@ts-ignore` and `@ts-nocheck` comments that suppress type errors, ensuring all type issues are properly addressed.
- **`no-unsafe-*` rules**: Detect and prevent dangerous operations stemming from `any` types, catching potential runtime errors at lint time.
- **`no-floating-promises`**: Ensures promises are properly handled with await, `.then()`, or `.catch()`, preventing unhandled rejections.
- **`require-await`**: Flags `async` functions that don't use `await`, indicating unnecessary async overhead or missing await statements.

### Separation of Concerns

- **ESLint**: Focuses on detecting bugs, dangerous patterns, and logical errors
- **Prettier**: Handles all code formatting (indentation, line breaks, semicolons)
- **Integration**: Use `eslint-config-prettier` to disable ESLint formatting rules that conflict with Prettier

### Monorepo and Performance Considerations

For monorepo setups using pnpm workspaces or similar:

```javascript
// Root .eslintrc.cjs for monorepo
module.exports = {
  root: true,
  parser: "@typescript-eslint/parser",
  parserOptions: {
    tsconfigRootDir: __dirname,
    project: ["./packages/*/tsconfig.json"],
    sourceType: "module"
  },
  // ... rest of config
  overrides: [
    {
      files: ["*.config.js", "*.config.ts", "scripts/**/*"],
      parserOptions: {
        project: null // Skip type-aware linting for config files
      }
    }
  ]
};
```

**Performance tips:**
- Use `tsconfigRootDir: __dirname` to prevent ESLint from searching parent directories
- For large codebases, consider running ESLint per package rather than from root
- Use `--cache` flag in CI: `eslint --cache --cache-location .eslintcache`

### Handling Exceptional Cases

When you must disable a rule, use the narrowest scope possible:

```typescript
// ❌ Avoid this:
// @ts-ignore
someCall();

// ✅ Prefer this:
// eslint-disable-next-line @typescript-eslint/no-explicit-any -- Third-party lib has incorrect typings, see issue #123
const unsafeValue: any = thirdPartyCall();
```

## 3.5. Allowed Exceptional Uses of `any` and Type Assertions

This standard is strict by default, but there are explicitly allowed escape hatches:

- `as const` for literal inference
- Narrowing DOM APIs where TypeScript typings are intentionally generic (e.g., `document.querySelector('#root') as HTMLDivElement | null`)
- Working around incorrect or incomplete third-party type definitions
- React ref handling and similar framework-specific patterns

**Rules for exceptions:**
- Never use `as` or `any` for **external data** (API responses, webhooks, LLM JSON, database queries)
- Every exceptional use MUST:
  - Be as local as possible
  - Include a short comment explaining why the assertion is safe
  - Prefer `unknown` + type guards over `any` when possible
  - Use `eslint-disable-next-line` rather than broader disables

## 4. Runtime Validation with Zod – IO Boundaries

All external data entering the system must be validated using Zod schemas. This includes API responses, database queries, webhook payloads, LLM-generated JSON, and any other external data sources.

### Standard Pattern

```typescript
import { z } from "zod";

// Define schema
export const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email().optional()
});

// Derive TypeScript type from schema
export type User = z.infer<typeof UserSchema>;

// Validate external data
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json();

  // Never use 'as User' - always validate
  return UserSchema.parse(data);
}

// Safe parsing with error handling
async function fetchUserSafe(id: string): Promise<User | null> {
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json();

  const result = UserSchema.safeParse(data);
  if (result.success) {
    return result.data;
  } else {
    console.error('Validation failed:', result.error);
    return null;
  }
}
```

### Key Principles

- **Never use type assertions** (`as SomeType`) for external data - always validate through schemas
- **Validate at IO boundaries** (API layer, DB adapters, message queues, LLM calls), not at every internal function call
- **Single Source of Truth**: TypeScript types are derived from Zod schemas using `z.infer`, not defined separately
- **Fail fast**: Use `.parse()` for critical paths where invalid data should throw
- **Graceful degradation**: Use `.safeParse()` when you need to handle validation failures explicitly
- Once data is validated at the boundary, it can be passed as regular TypeScript types internally

### Performance and Architecture Guidelines

**High-frequency API paths:**
- Consider caching parsed schemas for hot paths
- Use `z.preprocess()` for lightweight transformations before validation
- For database schemas, consider tools like Prisma or Drizzle that generate both DB schema and Zod validators

**Error handling policy:**
```typescript
const result = schema.safeParse(data);
if (!result.success) {
  logger.error('Validation failed', {
    errors: result.error.flatten(),
    endpoint: request.url,
    timestamp: new Date().toISOString()
  });
  // Return 400 for user input, 500 for internal data corruption
  return response.status(isUserInput ? 400 : 500).json({
    error: 'Validation failed',
    details: production ? undefined : result.error.flatten()
  });
}
```

## 5. NPM Scripts – lint, typecheck, test

Every TypeScript project must include these standard npm scripts in `package.json`:

```json
{
  "scripts": {
    "lint": "eslint \"src/**/*.{ts,tsx,js,jsx}\"",
    "typecheck": "tsc --noEmit",
    "test": "vitest"
  }
}
```

### Script Purposes

- **`lint`**: Runs ESLint on all source files to catch bugs and enforce code quality
- **`typecheck`**: Verifies TypeScript compilation without emitting files, ensuring type safety
- **`test`**: Runs the test suite using Vitest (preferred) or Jest

### Test Runner Preference

**Vitest** is the preferred test runner for new projects due to:
- Native TypeScript support without additional configuration
- Faster execution through worker threads
- Compatible Jest API for easy migration
- Built-in ESM support

For legacy projects, Jest remains acceptable but should migrate to Vitest when feasible.

### Additional Development Scripts

```json
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "lint:fix": "eslint \"src/**/*.{ts,tsx,js,jsx}\" --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,js,jsx}\"",
    "format:check": "prettier --check \"src/**/*.{ts,tsx,js,jsx}\"",
    "test:watch": "vitest watch",
    "test:coverage": "vitest run --coverage"
  }
}
```

**For pnpm workspaces:**
```json
{
  "scripts": {
    "lint": "pnpm -r run lint",
    "typecheck": "pnpm -r run typecheck",
    "test": "pnpm -r run test"
  }
}
```

## 6. CI Pipeline – Required Gates

All TypeScript projects must implement CI pipelines that enforce these standards. The following jobs must pass before merging to the main branch:

### Required CI Jobs

1. **Lint Check**: Ensures code quality standards are met
2. **Type Check**: Verifies TypeScript compilation succeeds
3. **Test Suite**: Runs all tests and ensures they pass
4. **Format Check**: Verifies code formatting consistency (optional but recommended)

### Sample GitHub Actions Workflow

```yaml
# .github/workflows/typescript-ci.yml
name: TypeScript CI
# Note: This example shows separate jobs for clarity.
# In production, consider using job dependencies (`needs`) or
# matrix strategies to optimize execution time and reduce duplication.

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run typecheck

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run test

  format-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run format:check
```

### Merge Protection Rules

Configure branch protection rules to require all CI checks to pass before merging:
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Include administrators in these restrictions

## 7. Usage Guidelines – How New Repos Apply This Standard

### Package Manager Preference

> **Note**: We prefer `pnpm` for new projects due to its efficiency and disk space optimization. Examples in this document use `npm` for readability, but should be adapted to the chosen package manager (pnpm/yarn/npm).

Follow these steps to apply the TypeScript Standard Set to new repositories:

### Step 1: Initialize TypeScript Configuration

1. Create `tsconfig.base.json` in the repository root with the standard configuration
2. Create `tsconfig.json` extending the base:

**Option A: Include tests in type checking (recommended)**

```json
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*", "tests/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**Option B: Separate test configuration (for performance-sensitive projects)**

Main `tsconfig.json`:
```json
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts", "**/*.spec.ts"]
}
```

Test `tsconfig.test.json`:
```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "noEmit": true,
    "types": ["vitest/globals", "node"]
  },
  "include": ["src/**/*.test.ts", "src/**/*.spec.ts", "tests/**/*"]
}
```

Then update your `typecheck` script: `"typecheck": "tsc --noEmit && tsc -p tsconfig.test.json"`

### Step 2: Setup Linting and Formatting

1. Install dependencies:
```bash
npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-config-prettier prettier
```

2. Copy the standard `.eslintrc.cjs` configuration
3. Create `.prettierrc`:
```json
{
  "semi": true,
  "trailingComma": "all",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

### Step 3: Implement Zod Validation

1. Install Zod:
```bash
npm install zod
```

2. Create schemas for all external data interfaces:
```typescript
// src/schemas/api.ts
import { z } from 'zod';

export const ApiResponseSchema = z.object({
  success: z.boolean(),
  data: z.unknown(), // Further refine based on endpoint
  error: z.string().optional()
});
```

3. Apply validation at all IO boundaries:
```typescript
// src/api/client.ts
import { ApiResponseSchema } from '../schemas/api';

export async function apiCall(endpoint: string) {
  const response = await fetch(endpoint);
  const json = await response.json();
  return ApiResponseSchema.parse(json);
}
```

### Step 4: Configure CI Pipeline

1. Copy the sample GitHub Actions workflow to `.github/workflows/typescript-ci.yml`
2. Ensure all npm scripts are defined in `package.json`
3. Enable branch protection rules in GitHub repository settings

### Step 5: AI Agent Configuration

When configuring AI agents or writing prompts, include these directives:

```markdown
## TypeScript Development Standards

- Follow the TypeScript Standard Set defined in `docs/TYPESCRIPT_STANDARD.md` (this document)
- Do not propose relaxing tsconfig strict settings or disabling ESLint rules without justification
- If you believe a rule must be disabled or relaxed, explain why and propose:
  - A narrow, local `eslint-disable-next-line` with a justification comment, or
  - A small, well-scoped rule tweak reviewed by humans
- Never use type assertions (as Type) for unvalidated external data - always use Zod validation
- Always validate external data at IO boundaries using Zod schemas
- Ensure all code passes lint, typecheck, and test before considering a task complete
```

Include in AGENTS configuration:
```yaml
standards:
  - typescript: strict
  - validation: zod-required
  - no-any: true
  - no-type-assertions: true
```

## 8. Document Quality Gates

This document itself must pass the following quality checks:

### Required Validation

1. **TypeScript Compilation**: All code examples must compile with the strict settings defined in this document
2. **ESLint Compliance**: All TypeScript examples must pass the ESLint configuration specified
3. **Zod Schema Validation**: All Zod examples must be syntactically correct and properly typed
4. **CI Workflow Validation**: GitHub Actions workflow must be valid YAML and use current action versions

### Document Review Checklist

Before any updates to this document are merged:

- [ ] All code examples have been tested in an actual TypeScript project
- [ ] Configuration files are valid JSON/YAML with proper syntax
- [ ] No conflicting rules between tsconfig, ESLint, and Prettier configurations
- [ ] Examples follow the exceptional use cases defined in Section 3.5
- [ ] Package versions in examples are current and actively maintained
- [ ] CI workflow steps execute successfully in a test repository

### Automated Validation

```yaml
# .github/workflows/validate-typescript-standard.yml
name: Validate TypeScript Standard Document

on:
  pull_request:
    paths:
      - 'docs/TYPESCRIPT_STANDARD.md'

jobs:
  validate-examples:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Extract and validate code examples
        run: |
          # Extract TypeScript code blocks
          grep -Pzo '(?s)```typescript\n\K.*?(?=\n```)' docs/TYPESCRIPT_STANDARD.md > examples.ts || true

          # Create temporary project with our strict config
          npm init -y
          npm install -D typescript @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint eslint-config-prettier zod

          # Copy our standard tsconfig
          cat > tsconfig.json << 'EOF'
          {
            "compilerOptions": {
              "strict": true,
              "noUnusedLocals": true,
              "noUnusedParameters": true,
              "noImplicitReturns": true,
              "noFallthroughCasesInSwitch": true,
              "forceConsistentCasingInFileNames": true,
              "useUnknownInCatchVariables": true,
              "esModuleInterop": true,
              "resolveJsonModule": true,
              "noEmit": true,
              "lib": ["ES2022"],
              "target": "ES2022",
              "module": "NodeNext",
              "moduleResolution": "NodeNext"
            }
          }
          EOF

          # Copy our standard ESLint config
          cat > .eslintrc.cjs << 'EOF'
          module.exports = {
            parser: "@typescript-eslint/parser",
            parserOptions: {
              project: "./tsconfig.json",
              sourceType: "module"
            },
            plugins: ["@typescript-eslint"],
            extends: [
              "eslint:recommended",
              "plugin:@typescript-eslint/recommended",
              "plugin:@typescript-eslint/recommended-requiring-type-checking",
              "prettier"
            ],
            rules: {
              "@typescript-eslint/no-explicit-any": "error",
              "@typescript-eslint/no-non-null-assertion": "error",
              "@typescript-eslint/no-unsafe-assignment": "error",
              "@typescript-eslint/no-unsafe-member-access": "error",
              "@typescript-eslint/no-unsafe-call": "error",
              "@typescript-eslint/no-unsafe-return": "error",
              "@typescript-eslint/no-floating-promises": "error",
              "@typescript-eslint/require-await": "error"
            }
          };
          EOF

          # Type check examples (allow fragments but fail on actual errors)
          if [ -s examples.ts ]; then
            npx tsc --noEmit examples.ts 2>&1 | grep -v "Cannot find module" || true
            npx eslint examples.ts 2>&1 | grep -v "Parsing error" || true
          fi

      - name: Validate JSON/YAML configs
        run: |
          # Validate JSON code blocks (skip JSONC with comments)
          grep -Pzo '(?s)```json\n\K.*?(?=\n```)' docs/TYPESCRIPT_STANDARD.md | \
          while IFS= read -r -d '' json; do
            if [ -n "$json" ]; then
              echo "$json" | jq empty || { echo "JSON validation failed"; exit 1; }
            fi
          done

          # Validate YAML workflow
          grep -Pzo '(?s)```yaml\n.*?workflows.*?\K.*?(?=\n```)' docs/TYPESCRIPT_STANDARD.md > workflow.yml || true
          if [ -s workflow.yml ]; then
            npm install -g js-yaml
            js-yaml workflow.yml || { echo "YAML validation failed"; exit 1; }
          fi
```

### Update Protocol

1. **Minor Updates** (typos, clarifications):
   - Require one reviewer approval
   - Must pass automated validation

2. **Rule Changes** (modifying standards):
   - Require engineering team review
   - Must include migration guide for existing projects
   - Update `last_updated` field

3. **Breaking Changes** (incompatible updates):
   - Require major version bump in document
   - Provide deprecation period with clear timeline
   - Update all dependent repositories before enforcement

## 9. References

### Official Documentation

- **TypeScript Handbook & TSConfig Reference**
  https://www.typescriptlang.org/docs/
  https://www.typescriptlang.org/tsconfig

- **ESLint Documentation**
  https://eslint.org/docs/latest/
  https://eslint.org/docs/latest/use/configure

- **TypeScript-ESLint**
  https://typescript-eslint.io/
  https://typescript-eslint.io/rules/

- **Prettier**
  https://prettier.io/docs/en/

- **Zod**
  https://zod.dev/
  https://github.com/colinhacks/zod

- **Vitest**
  https://vitest.dev/guide/

- **Jest**
  https://jestjs.io/docs/getting-started

---

*This document represents the canonical TypeScript configuration for all projects in our AI-First organization. Deviations from these standards require explicit justification and approval from the engineering team.*