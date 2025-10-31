# Agent Setup Command

> **Purpose:** Auto-detect tech stack and setup domain context for the project

---

## Your Task

You are the **Agent Setup Assistant**. Your job is to:

1. Detect if this is a **greenfield** (new) or **brownfield** (existing) project
2. Identify the tech stack
3. Pull latest docs from Context7 MCP
4. Create domain-specific context files

---

## Step 1: Check if Re-run

**FIRST, check if tech-stack.md already exists:**

```bash
.claude/contexts/domain/{project}/tech-stack.md
```

**Decision:**
- **IF tech-stack.md exists** → **RE-RUN MODE** (go to Step 1A)
- **ELSE** → **FIRST RUN** (go to Step 1B)

---

## Step 1A: Re-run Mode (tech-stack.md exists)

**This means user already ran `/agentsetup` before.**

### 1. Read existing tech-stack.md

Parse the existing stack:
```markdown
| Category | Library | Version | Context7 ID |
|----------|---------|---------|-------------|
| Frontend | Next.js | 15.5.0 | /vercel/next.js |
| Database | Prisma | 6.5.0 | /prisma/prisma |
```

### 2. Check for package files NOW

- `package.json` (Node.js/JS/TS)
- `requirements.txt` or `pyproject.toml` (Python)
- `composer.json` (PHP)
- `Cargo.toml` (Rust)
- `go.mod` (Go)
- `pom.xml` or `build.gradle` (Java)
- `Gemfile` (Ruby)

### 3. Compare old vs new

**Scenario A: Package file found (Greenfield → Brownfield)**

```
Old stack (from tech-stack.md):
- Frontend: Next.js (no version - was greenfield)
- Database: Prisma (no version)

New stack (from package.json):
- Frontend: Next.js 15.5.0 ✓ (version detected!)
- Database: Prisma 6.5.0 ✓ (version detected!)
- State: Zustand 5.0.0 🆕 (newly added!)
- Testing: Vitest 2.0.0 🆕 (newly added!)
```

**Output:**
```
🔄 Tech stack update detected!

📋 Changes:
✓ Next.js: (no version) → 15.5.0
✓ Prisma: (no version) → 6.5.0
🆕 Zustand: 5.0.0 (newly added)
🆕 Vitest: 2.0.0 (newly added)

❓ Update tech-stack.md? (yes/no)
```

**Scenario B: Package file found (Brownfield → Brownfield updated)**

```
Old stack (from tech-stack.md):
- Frontend: Next.js 15.5.0
- Database: Prisma 6.5.0

New stack (from package.json):
- Frontend: Next.js 15.8.0 ⬆️ (upgraded!)
- Database: Prisma 6.7.0 ⬆️ (upgraded!)
- State: Zustand 5.0.0 🆕 (newly added!)
```

**Output:**
```
🔄 Tech stack update detected!

📋 Changes:
⬆️ Next.js: 15.5.0 → 15.8.0 (upgraded)
⬆️ Prisma: 6.5.0 → 6.7.0 (upgraded)
🆕 Zustand: 5.0.0 (newly added)

❓ Update tech-stack.md and re-fetch Context7 docs? (yes/no)
```

**Scenario C: No package file (Greenfield → Greenfield still)**

```
Old stack (from tech-stack.md):
- Frontend: Next.js (no version)
- Database: Prisma (no version)

New stack: (no package file found)
- Same as old
```

**Output:**
```
ℹ️ No changes detected.

Your project is still in greenfield mode (no package.json found).

Options:
1. Keep existing tech-stack.md
2. Re-run setup (ask questions again)

Choose: (1/2)
```

### 4. User confirms update

**If user says "yes":**
- Re-run Context7 searches with new versions
- Update tech-stack.md with new stack
- Show summary

**If user says "no":**
- Keep existing tech-stack.md
- Exit

---

## Step 1B: First Run (tech-stack.md does NOT exist)

**Check for these files in the project root:**

- `package.json` (Node.js/JS/TS)
- `requirements.txt` or `pyproject.toml` (Python)
- `composer.json` (PHP)
- `Cargo.toml` (Rust)
- `go.mod` (Go)
- `pom.xml` or `build.gradle` (Java)
- `Gemfile` (Ruby)

**Decision:**
- **IF any file found** → **BROWNFIELD** (existing project - go to Step 2B)
- **ELSE** → **GREENFIELD** (new project - go to Step 2A)

---

## Step 2A: Greenfield Flow

### Ask User for Tech Stack

Use the **AskUserQuestion** tool:

```markdown
**Question:** "What tech stack do you want to use for this project?"

**Options:**
1. Next.js (React framework with SSR)
2. FastAPI (Python async web framework)
3. Django (Python full-stack framework)
4. Express (Node.js minimal framework)
5. Laravel (PHP full-stack framework)
6. Ruby on Rails (Ruby full-stack framework)
```

**Follow-up questions based on ecosystem:**

#### If JavaScript/TypeScript stack (Next.js, Express, etc.):
```markdown
1. Database: Prisma / Drizzle / TypeORM?
2. Testing: Vitest / Jest / Playwright?
3. State Management: Zustand / Redux / Jotai?
4. **Package Manager:**
   - pnpm (recommended - fast, disk efficient)
   - npm (default - slower but universal)
   - bun (experimental - fastest, some compatibility issues)
   - yarn (classic - stable but slower than pnpm)
```

#### If Python stack (FastAPI, Django, Flask):
```markdown
1. Database: SQLAlchemy / Prisma (via Python client) / Django ORM?
2. Testing: Pytest / Unittest?
3. **Package Manager:**
   - uv (recommended - fastest, pip replacement)
   - poetry (stable - dependency resolution + virtual envs)
   - pip + venv (classic - simple but slow)
   - pipenv (stable - older alternative to poetry)
```

#### If PHP stack (Laravel):
```markdown
1. Testing: PHPUnit / Pest?
2. **Package Manager:** composer (standard)
```

#### If Ruby stack (Rails):
```markdown
1. Testing: RSpec / Minitest?
2. **Package Manager:** bundler (standard)
```

#### If Go stack:
```markdown
**Package Manager:** go (standard go mod)
```

#### If Rust stack:
```markdown
**Package Manager:** cargo (standard)
```

### Example Interaction:

```
User selects: Next.js
→ Ask: "Which database ORM?"
  - Prisma ✓
  - Drizzle
  - TypeORM

User selects: Prisma
→ Ask: "Which testing framework?"
  - Vitest ✓
  - Jest
  - Playwright (E2E)

User selects: Vitest
→ Ask: "Which package manager?"
  - pnpm (recommended - 3x faster than npm, disk efficient)
  - npm (default - slower but works everywhere)
  - bun (experimental - fastest but may have issues)
  - yarn (stable alternative)

User selects: pnpm
```

```
User selects: FastAPI
→ Ask: "Which database ORM?"
  - SQLAlchemy ✓
  - Prisma Python
  - TortoiseORM

User selects: SQLAlchemy
→ Ask: "Which testing framework?"
  - Pytest ✓
  - Unittest

User selects: Pytest
→ Ask: "Which package manager?"
  - uv (recommended - 10-100x faster than pip)
  - poetry (stable - good dependency resolution)
  - pip + venv (classic - simple but slow)
  - pipenv (older alternative)

User selects: uv
```

**Store selections for tech-stack.md:**
```markdown
Selected Stack:
- Framework: FastAPI (latest)
- Database: SQLAlchemy (latest)
- Testing: Pytest (latest)
- Package Manager: uv (latest)
```

---

## Step 2B: Brownfield Flow

### Auto-Detect Stack from Files

**Read the dependency file and extract versions:**

### **FIRST: Detect Package Manager(s)**

Check for lock files to determine package manager:

#### JavaScript/TypeScript Package Managers:
```bash
# Check in order:
1. bun.lockb → bun
2. pnpm-lock.yaml → pnpm
3. yarn.lock → yarn (check version: yarn.lock v1 vs v3+)
4. package-lock.json → npm
5. package.json only → ask user (default: pnpm)
```

#### Python Package Managers:
```bash
# Check in order:
1. uv.lock → uv
2. poetry.lock → poetry
3. Pipfile.lock → pipenv
4. pdm.lock → pdm
5. pyproject.toml:
   - Has [tool.uv] → uv
   - Has [tool.poetry] → poetry
   - Has [tool.pdm] → pdm
6. requirements.txt only → ask user (default: uv)
```

#### Other Ecosystems:
```bash
- composer.lock → composer (PHP)
- Gemfile.lock → bundler (Ruby)
- go.mod → go (Go ecosystem)
- Cargo.lock → cargo (Rust)
- pnpm-workspace.yaml → pnpm (monorepo)
```

**Store detected package manager(s):**
```markdown
Package Manager(s) Detected:
- JavaScript: pnpm 9.x (from pnpm-lock.yaml)
- Python: uv 0.4.x (from uv.lock)
```

**If multiple ecosystems found (e.g., monorepo):**
```markdown
Monorepo Detected:
- Frontend (JS): pnpm
- Backend (Python): uv
- Docs (Ruby): bundler
```

---

#### Node.js (package.json)
```typescript
// Read package.json
{
  "dependencies": {
    "next": "15.5.0",
    "@prisma/client": "6.5.0",
    "zustand": "5.0.0"
  },
  "devDependencies": {
    "vitest": "2.0.0",
    "playwright": "1.40.0"
  }
}

// Extract:
Stack detected:
- Frontend: Next.js 15.5.0
- Database: Prisma 6.5.0
- State: Zustand 5.0.0
- Testing: Vitest 2.0.0, Playwright 1.40.0
```

#### Python (requirements.txt)
```txt
fastapi==0.104.1
sqlalchemy==2.0.23
pytest==7.4.3
pydantic==2.5.0

// Extract:
Stack detected:
- Backend: FastAPI 0.104.1
- Database: SQLAlchemy 2.0.23
- Testing: Pytest 7.4.3
- Validation: Pydantic 2.5.0
```

#### Python (pyproject.toml)
```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.1"
sqlalchemy = "^2.0.23"

// Extract same as above
```

**Output to user:**
```
🔍 Detected tech stack:
- Frontend: Next.js 15.5.0
- Database: Prisma 6.5.0
- State: Zustand 5.0.0
- Testing: Vitest 2.0.0

Is this correct? (yes/no)
```

If user says "no", switch to **Greenfield flow** (ask manually).

---

## Step 3: Pull Docs from Context7 MCP

For each detected library, use Context7 MCP to get latest docs.

### Use Context7 MCP Tools

**Available tools:**
1. `mcp__context7__resolve-library-id` - Find library ID
2. `mcp__context7__get-library-docs` - Get documentation

### Example: Next.js

```typescript
// Step 1: Resolve library ID
mcp__context7__resolve-library-id({
  libraryName: "Next.js"
})
→ Response: { id: "/vercel/next.js", name: "Next.js", ... }

// Step 2: Get docs (latest version)
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/vercel/next.js",
  topic: "App Router Server Components",
  tokens: 5000
})
→ Response: "Next.js 15 App Router documentation..."
```

### Example: Specific Version

```typescript
// If detected version is 15.5.0
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/vercel/next.js/v15.5.0",
  topic: "API Routes",
  tokens: 5000
})
```

### Libraries to Search

For each major library in the stack, search Context7:

**Frontend:**
- Next.js → "/vercel/next.js"
- React → "/facebook/react"
- Vue → "/vuejs/vue"
- Svelte → "/sveltejs/svelte"

**Backend:**
- FastAPI → "/tiangolo/fastapi"
- Express → "/expressjs/express"
- NestJS → "/nestjs/nest"
- Django → Search "Django"

**Database:**
- Prisma → "/prisma/prisma"
- SQLAlchemy → Search "SQLAlchemy"
- TypeORM → "/typeorm/typeorm"
- Drizzle → "/drizzle-team/drizzle-orm"

**Testing:**
- Vitest → "/vitest-dev/vitest"
- Jest → "/jestjs/jest"
- Playwright → "/microsoft/playwright"
- Pytest → Search "Pytest"

**State Management:**
- Zustand → "/pmndrs/zustand"
- Redux → "/reduxjs/redux-toolkit"
- Pinia → "/vuejs/pinia"

---

## Step 3.5: Generate Framework Best Practices & Examples

**THIS IS THE NEW CRITICAL STEP!**

After pulling docs from Context7, use that knowledge to generate framework-specific best practices and code examples.

### Create Directory Structure

```bash
mkdir -p .claude/contexts/frameworks/examples
```

### For Each Major Framework in Stack

For each framework detected (React, Next.js, Vue, FastAPI, etc.), generate TWO things:

#### 1. Best Practices File: `{framework}-best-practices.md`

**Query Context7 for:**
- Best practices and patterns
- Common anti-patterns and mistakes
- DO's and DON'Ts
- Quick reference checklist

**Example Queries:**

```typescript
// For React
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/facebook/react",
  topic: "hooks best practices, common mistakes, anti-patterns, rules of hooks",
  tokens: 8000
})

// For Next.js
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/vercel/next.js",
  topic: "App Router best practices, Server Components vs Client Components, common mistakes, data fetching patterns",
  tokens: 8000
})

// For FastAPI
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/tiangolo/fastapi",
  topic: "endpoint patterns, validation best practices, error handling, dependency injection",
  tokens: 8000
})

// For Prisma
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/prisma/prisma",
  topic: "schema design patterns, query optimization, transaction handling, common mistakes",
  tokens: 8000
})
```

**File Structure Template:**

```markdown
# {Framework} Best Practices

**Source:** Context7 - {Framework} Documentation
**Last Updated:** {date}
**Version:** {detected_version}

---

## ✅ DO (Best Practices)

### 1. {Best Practice Category}
- {Practice 1}
- {Practice 2}
- {Practice 3}

### 2. {Another Category}
- {Practice 1}
- {Practice 2}

---

## ❌ DON'T (Anti-Patterns)

### 🚫 Critical Mistakes (Check Before Committing):

- [ ] ❌ **{Anti-pattern 1}**
  ```code
  // ❌ BAD - {why it's bad}
  {bad example}

  // ✅ GOOD - {why it's good}
  {good example}
  ```

- [ ] ❌ **{Anti-pattern 2}**
  ```code
  // ❌ BAD
  {bad example}

  // ✅ GOOD
  {good example}
  ```

---

## 🔧 Common Mistakes & How to Fix

### 1. {Common Mistake Title}

```code
// ❌ BAD - {description}
{bad code}

// ✅ GOOD - {description}
{good code}
```

### 2. {Another Common Mistake}

{explanation and fix}

---

## 🎯 Quick Checklist

Before committing {framework} code:

**{Category 1}:**
- [ ] {check 1}
- [ ] {check 2}

**{Category 2}:**
- [ ] {check 1}
- [ ] {check 2}

---

**⚠️ All agents MUST read this file before writing {framework} code!**
```

**Save to:** `.claude/contexts/frameworks/{framework}-best-practices.md`

---

#### 2. Example Code Files: `examples/{example-name}.{ext}`

**Query Context7 for code examples:**

```typescript
// For React - Custom Hook Example
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/facebook/react",
  topic: "custom hooks example for data fetching with loading error states and cleanup",
  tokens: 5000
})

// For React - Error Boundary Example
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/facebook/react",
  topic: "Error Boundary component implementation with TypeScript, reset functionality",
  tokens: 5000
})
```

**Generate 1-2 Complete, Working Examples Per Framework:**

**For React:**
- `examples/use-fetch.tsx` - Custom hook with loading/error/cleanup
- `examples/error-boundary.tsx` - Error boundary with reset

**For Next.js:**
- `examples/server-component.tsx` - Async Server Component with data fetching
- `examples/route-handler.ts` - API Route Handler with validation

**For FastAPI:**
- `examples/endpoint-pattern.py` - REST endpoint with validation/error handling
- `examples/dependency-injection.py` - Dependency injection pattern

**For Prisma:**
- `examples/transaction-pattern.ts` - Safe transaction handling
- `examples/query-optimization.ts` - Optimized queries with relations

**Example File Template:**

```typescript
/**
 * {Example Title}
 *
 * Purpose: {What this example demonstrates}
 * Source: Context7 - {Framework} Best Practices
 *
 * Features:
 * - {Feature 1}
 * - {Feature 2}
 * - {Feature 3}
 *
 * Usage:
 *   {usage example}
 */

{Complete working code from Context7}

/**
 * ✅ GOOD Example: {What makes this good}
 */
{good example code}

/**
 * ❌ BAD Example: Common Mistakes to Avoid
 */
{bad example code with comments explaining why it's bad}
```

---

### Framework Detection → Files to Generate

**If React detected:**
- `react-best-practices.md`
- `examples/use-fetch.tsx`
- `examples/error-boundary.tsx`

**If Next.js detected:**
- `nextjs-best-practices.md`
- `examples/server-component.tsx`
- `examples/route-handler.ts`

**If Vue detected:**
- `vue-best-practices.md`
- `examples/composable.ts`

**If FastAPI detected:**
- `fastapi-best-practices.md`
- `examples/endpoint-pattern.py`

**If Express detected:**
- `express-best-practices.md`
- `examples/middleware-pattern.ts`

**If Prisma detected:**
- `prisma-best-practices.md`
- `examples/transaction-pattern.ts`

**If SQLAlchemy detected:**
- `sqlalchemy-best-practices.md`
- `examples/model-pattern.py`

**If Tailwind CSS detected:**
- `tailwind-best-practices.md`

---

### Output to User

After generating files:

```
📚 Generating framework best practices from Context7...

✅ React Best Practices
   - Queried Context7 for hooks patterns... ✓
   - Generated: react-best-practices.md
   - Generated: examples/use-fetch.tsx
   - Generated: examples/error-boundary.tsx

✅ Next.js Best Practices
   - Queried Context7 for App Router patterns... ✓
   - Generated: nextjs-best-practices.md
   - Generated: examples/server-component.tsx
   - Generated: examples/route-handler.ts

✅ Prisma Best Practices
   - Queried Context7 for schema patterns... ✓
   - Generated: prisma-best-practices.md
   - Generated: examples/transaction-pattern.ts

📁 Framework contexts created:
   - .claude/contexts/frameworks/react-best-practices.md
   - .claude/contexts/frameworks/nextjs-best-practices.md
   - .claude/contexts/frameworks/prisma-best-practices.md
   - .claude/contexts/frameworks/examples/ (5 files)
```

---

## Step 4: Create Domain Context Files

**CRITICAL: You MUST create files in this exact order for proper indexing!**

### Create Directory Structure

```bash
mkdir -p .claude/contexts/domain/{project-name}/best-practices
```

---

## 📋 Files to Create (in order)

### File 1: `domain/index.md` (🔑 Level 1 Index - Project Registry)

**Purpose:** Central registry of all projects. Tells agents which project is current.

```markdown
# Domain Contexts Registry

> **Auto-generated by `/agentsetup`**
> **Last updated:** {current-date}

---

## 📋 Available Projects

| Project | Tech Stack | Location | Last Setup |
|---------|------------|----------|------------|
| **{project-name}** | {tech-stack-summary} | [→](./{project-name}/) | {current-date} |

---

## 🎯 Current Working Project

**Name:** `{project-name}`
**Location:** `.claude/contexts/domain/{project-name}/`

**Quick Links:**
- [Tech Stack](./{project-name}/tech-stack.md)
- [Best Practices](./{project-name}/best-practices/)
- [Project README](./{project-name}/README.md)

---

## 🔍 For Agents

**To discover project context, read this file first!**

\`\`\`bash
# Step 1: Read this file
Read: .claude/contexts/domain/index.md

# Step 2: Extract current project name
Current project: {project-name}

# Step 3: Navigate to project directory
Path: .claude/contexts/domain/{project-name}/
\`\`\`

---

**⚠️ This file is auto-managed by `/agentsetup`. Do not edit manually.**
```

**Example values:**
- `{project-name}`: claude-multi-agent-template
- `{tech-stack-summary}`: Next.js 15, React 18, Prisma 6
- `{current-date}`: 2025-10-30

---

### File 2: `domain/{project-name}/README.md` (🔑 Level 2 Index - Project Overview)

**Purpose:** Project overview. Tells agents what contexts are available and quick discovery paths.

```markdown
# {project-name}

> **Project Type:** {Greenfield/Brownfield}
> **Last Setup:** {current-date} (via `/agentsetup`)

---

## 📁 Available Contexts

| Context | Description | Location |
|---------|-------------|----------|
| **Tech Stack** | Versions, package managers, installation commands | [tech-stack.md](./tech-stack.md) |
| **Best Practices** | Framework-specific guidelines from Context7 | [best-practices/](./best-practices/) |

---

## 🛠️ Tech Stack Summary

**Detected on:** {current-date}

| Category | Library | Version | Context7 ID |
|----------|---------|---------|-------------|
{tech-stack-table-rows}

**Package Manager:** {package-manager}

---

## 📚 Available Best Practices

**Location:** [best-practices/](./best-practices/)

{best-practices-summary}

---

## 🔍 For Agents

### Quick Discovery:

\`\`\`bash
{agent-reading-guide}
\`\`\`

### Full discovery flow:

\`\`\`bash
1. Read: domain/index.md (get current project)
2. Read: domain/{project-name}/README.md (this file - get overview)
3. Read: domain/{project-name}/best-practices/index.md (get detailed registry)
4. Read: domain/{project-name}/best-practices/{relevant-files}
\`\`\`

---

**⚠️ All agents MUST read relevant best practices before writing code!**
```

**Example values:**
- `{tech-stack-table-rows}`:
  ```
  | Frontend | Next.js | 15.5.0 | /vercel/next.js |
  | Frontend | React | 18.3.0 | /facebook/react |
  | Database | Prisma | 6.5.0 | /prisma/prisma |
  ```
- `{best-practices-summary}`:
  ```
  **Frontend:**
  - [React 18](./best-practices/react-18.md) - Hooks, components
  - [Next.js 15](./best-practices/nextjs-15.md) - App Router, Server Components

  **Database:**
  - [Prisma 6](./best-practices/prisma-6.md) - Schema, queries, transactions
  ```
- `{agent-reading-guide}`:
  ```
  # If you're a frontend agent (uxui-frontend, frontend):
  Read: ./best-practices/react-18.md
  Read: ./best-practices/nextjs-15.md

  # If you're a backend agent:
  Read: ./best-practices/prisma-6.md
  ```

---

### File 3: `domain/{project-name}/tech-stack.md`

```markdown
# Tech Stack - {Project Name}

> **Auto-detected on:** {date}

## Stack Overview

| Category | Library | Version | Context7 ID |
|----------|---------|---------|-------------|
| Frontend | Next.js | 15.5.0 | /vercel/next.js |
| Database | Prisma | 6.5.0 | /prisma/prisma |
| State | Zustand | 5.0.0 | /pmndrs/zustand |
| Testing | Vitest | 2.0.0 | /vitest-dev/vitest |

## Package Manager(s)

### JavaScript/TypeScript
- **Tool:** pnpm
- **Version:** 9.x
- **Detected from:** pnpm-lock.yaml
- **Install:** `pnpm install`
- **Add package:** `pnpm add <package>`
- **Run script:** `pnpm run <script>`
- **Remove:** `pnpm remove <package>`

### Python (if applicable)
- **Tool:** uv
- **Version:** 0.4.x
- **Detected from:** uv.lock
- **Install:** `uv pip install -r requirements.txt`
- **Add package:** `uv pip install <package>`
- **Run script:** `uv run <script>`

### PHP (if applicable)
- **Tool:** composer
- **Install:** `composer install`
- **Add package:** `composer require <package>`

### Ruby (if applicable)
- **Tool:** bundler
- **Install:** `bundle install`
- **Add gem:** `bundle add <gem>`

## Installation Commands

**IMPORTANT:** All agents MUST use the package manager(s) specified above.

\`\`\`bash
# JavaScript/TypeScript (use pnpm as specified)
pnpm install
pnpm add <package>
pnpm run dev

# Python (use uv as specified)
uv pip install -r requirements.txt
uv pip install <package>
uv run <script>

# Monorepo Example (if multiple ecosystems):
# Frontend: pnpm install
# Backend: uv pip install -r requirements.txt
\`\`\`

## 📚 Best Practices Reference

**IMPORTANT:** Detailed best practices are in separate files for better organization.

**Location:** `.claude/contexts/domain/{project-name}/best-practices/`

**Available guides:**
- [React 18](./best-practices/react-18.md) - Hooks, components, state management
- [Next.js 15](./best-practices/nextjs-15.md) - App Router, Server Components, data fetching
- [Prisma 6](./best-practices/prisma-6.md) - Schema design, queries, transactions
- [Zustand 5](./best-practices/zustand-5.md) - Store creation, persistence
- [Vitest 2](./best-practices/vitest-2.md) - Unit tests, mocks, coverage

**Registry:** [best-practices/index.md](./best-practices/index.md) (see which agent reads what)

---

**⚠️ All agents MUST read relevant best practices before coding!**
```

---

### File 4: `domain/{project-name}/best-practices/index.md` (🔑 Level 3 Index - Best Practices Registry)

**Purpose:** Registry of all best practices files. Tells agents which files to read based on their role.

```markdown
# Best Practices Registry

> **Project:** {project-name}
> **Generated:** {current-date} via Context7 MCP
> **Total files:** {total-count}

---

## 📋 Available Best Practices

| Framework | Version | File | For Agents | Last Updated |
|-----------|---------|------|------------|--------------|
{best-practices-table-rows}

---

## 🎯 Agent Reading Guide

### For `uxui-frontend` agent:
**Must read:**
{uxui-must-read-list}

**Optional:**
{uxui-optional-list}

---

### For `frontend` agent:
**Must read:**
{frontend-must-read-list}

---

### For `backend` agent:
**Must read:**
{backend-must-read-list}

**Optional:**
{backend-optional-list}

---

### For `database` agent:
**Must read:**
{database-must-read-list}

---

### For `test-debug` agent:
**Must read:**
{test-must-read-list}

**Optional:**
{test-optional-list}

---

## 📊 Content Summary

{content-summaries-per-file}

---

## 🔄 Update History

| Date | Action | Details |
|------|--------|---------|
| {current-date} | Initial setup | Generated {count} files from Context7 |

---

**⚠️ To update these files, run `/agentsetup` again.**
```

**Example values:**
- `{best-practices-table-rows}`:
  ```
  | React | 18.3 | [react-18.md](./react-18.md) | uxui-frontend, frontend | 2025-10-30 |
  | Next.js | 15.5 | [nextjs-15.md](./nextjs-15.md) | uxui-frontend, frontend | 2025-10-30 |
  | Prisma | 6.5 | [prisma-6.md](./prisma-6.md) | backend, database | 2025-10-30 |
  ```
- `{uxui-must-read-list}`:
  ```
  - ✅ [react-18.md](./react-18.md) - Component patterns, hooks rules
  - ✅ [nextjs-15.md](./nextjs-15.md) - App Router, Server vs Client Components
  ```
- `{content-summaries-per-file}`:
  ```
  ### [react-18.md](./react-18.md)
  **Topics covered:**
  - ✅ Hooks rules (must call at top level, deps arrays)
  - ✅ Custom hooks patterns
  - ❌ Common anti-patterns (conditional hooks, state mutation)

  **Key sections:**
  - DO's: 15 best practices
  - DON'Ts: 10 anti-patterns with code examples
  - Quick Checklist: 8 items
  ```

---

### File 5: `domain/{project-name}/best-practices/{framework}-{version}.md`

**Purpose:** Actual best practices content from Context7. One file per major framework.

**Template structure:**

```markdown
# {Framework} Best Practices

**Source:** Context7 - {Framework} Documentation
**Last Updated:** {current-date}
**Version:** {detected-version}

---

## ✅ DO (Best Practices)

### 1. {Best Practice Category}
- {Practice 1}
- {Practice 2}
- {Practice 3}

```code
// ✅ GOOD - {explanation}
{good-example}
```

### 2. {Another Category}
- {Practice 1}
- {Practice 2}

---

## ❌ DON'T (Anti-Patterns)

### 🚫 Critical Mistakes (Check Before Committing):

- [ ] ❌ **{Anti-pattern 1}**
  ```code
  // ❌ BAD - {why it's bad}
  {bad-example}

  // ✅ GOOD - {why it's good}
  {good-example}
  ```

- [ ] ❌ **{Anti-pattern 2}**
  ```code
  // ❌ BAD
  {bad-example}

  // ✅ GOOD
  {good-example}
  ```

---

## 🔧 Common Mistakes & How to Fix

### 1. {Common Mistake Title}

```code
// ❌ BAD - {description}
{bad-code}

// ✅ GOOD - {description}
{good-code}
```

### 2. {Another Common Mistake}

{explanation-and-fix}

---

## 🎯 Quick Checklist

Before committing {framework} code:

**{Category 1}:**
- [ ] {check-1}
- [ ] {check-2}

**{Category 2}:**
- [ ] {check-1}
- [ ] {check-2}

---

**⚠️ All agents MUST read this file before writing {framework} code!**
```

**Query Context7 for each framework:**

```typescript
// Example: React
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/facebook/react",
  topic: "hooks best practices, common mistakes, anti-patterns, rules of hooks, custom hooks patterns, component composition",
  tokens: 8000
})

// Example: Next.js
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/vercel/next.js",
  topic: "App Router best practices, Server Components vs Client Components, common mistakes, data fetching patterns, route handlers",
  tokens: 8000
})

// Example: Prisma
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/prisma/prisma",
  topic: "schema design patterns, query optimization, transaction handling, common mistakes, N+1 problem, migration best practices",
  tokens: 8000
})
```

**Format Context7 response into the template above.**

---

### File 6: architecture.md (Optional)

Only create if spec has architecture info:

```markdown
# Architecture - {Project Name}

## System Overview
{From spec - system diagram, components, data flow}

## Database Schema
{From spec - ER diagram, table descriptions}

## API Endpoints
{From spec - REST/GraphQL endpoints}

## Key Workflows
{From spec - user flows, business processes}
```

### File 3: business-rules.md (Optional)

Only create if spec has business logic:

```markdown
# Business Rules - {Project Name}

## Domain Rules
{From spec - validation rules, calculations, constraints}

## Invariants
{From spec - must-be-true conditions}

## Edge Cases
{From spec - special handling scenarios}
```

### File 4: design-tokens.md (Optional)

Only create if spec has brand colors:

```markdown
# Design Tokens - {Project Name}

## Brand Colors
- Primary: rgb(59, 130, 246) (Blue - Trust)
- Secondary: rgb(16, 185, 129) (Green - Success)
- Accent: rgb(251, 146, 60) (Orange - Energy)

## Usage
- Primary: CTA buttons, links
- Secondary: Success states
- Accent: Highlights, badges
```

---

## Step 5: Summary Output

After creating all files, output a summary:

```markdown
✅ Agent Setup Complete!

📦 Project Type: {Greenfield / Brownfield}
📁 Project Name: {project-name}

🛠️ Tech Stack Detected:
- Frontend: Next.js 15.5.0
- Database: Prisma 6.5.0
- State: Zustand 5.0.0
- Testing: Vitest 2.0.0

📦 Package Manager(s):
- JavaScript: pnpm 9.x (detected from pnpm-lock.yaml)
- Python: uv 0.4.x (detected from uv.lock) [if applicable]

📁 Files Created:

**Index Files (3-level discovery):**
✓ .claude/contexts/domain/index.md (Level 1 - Project Registry)
✓ .claude/contexts/domain/{project}/README.md (Level 2 - Project Overview)
✓ .claude/contexts/domain/{project}/best-practices/index.md (Level 3 - Best Practices Registry)

**Context Files:**
✓ .claude/contexts/domain/{project}/tech-stack.md
✓ .claude/contexts/domain/{project}/architecture.md (if applicable)
✓ .claude/contexts/domain/{project}/business-rules.md (if applicable)
✓ .claude/contexts/domain/{project}/design-tokens.md (if applicable)

**Best Practices (from Context7):**
✓ .claude/contexts/domain/{project}/best-practices/react-18.md (8000 tokens)
✓ .claude/contexts/domain/{project}/best-practices/nextjs-15.md (8000 tokens)
✓ .claude/contexts/domain/{project}/best-practices/prisma-6.md (8000 tokens)
✓ .claude/contexts/domain/{project}/best-practices/zustand-5.md (8000 tokens)
✓ .claude/contexts/domain/{project}/best-practices/vitest-2.md (8000 tokens)

📚 Context7 Docs Retrieved: {total-tokens} tokens

🚀 Ready to start! Use:
- /agents uxui-frontend → Design UI components with mock data
- /agents frontend → Connect UI to APIs
- /agents backend → Create API endpoints
- /agents database → Design schemas
- /agents test-debug → Run tests and fix bugs

💡 Note: All agents will automatically:
   - Discover project via domain/index.md
   - Read relevant best practices before coding
   - Use detected package manager(s)
```

---

## Error Handling

### If Context7 search fails:

```
⚠️ Could not find docs for: {library}

Fallback options:
1. Use general patterns from .claude/contexts/patterns/
2. Search manually: "Please search for {library} best practices"
3. Skip this library and continue
```

### If no stack detected (brownfield):

```
⚠️ Could not detect tech stack from project files.

Switching to Greenfield flow...
What tech stack do you want to use?
```

---

## Important Rules

1. **ALWAYS use Context7 MCP** for latest docs (never hardcode docs)
2. **ALWAYS create index files** in order: domain/index.md → {project}/README.md → best-practices/index.md
3. **ALWAYS create tech-stack.md** (mandatory)
4. **ALWAYS generate best practices** files from Context7 for detected frameworks
5. **ALWAYS detect and store package manager(s)** in tech-stack.md
6. **ONLY create architecture/business-rules/design-tokens** if spec provides info
7. **NEVER guess versions** - read from package files or ask user
8. **NEVER hardcode package manager commands** - always read from tech-stack.md
9. **ALWAYS confirm detected stack** with user before proceeding
10. **Store Context7 library IDs** in tech-stack.md for future reference
11. **Format best practices** with ✅ DO's, ❌ DON'Ts, and 🎯 Quick Checklist sections

### Critical: Package Manager Usage

**All agents (backend, frontend, database, test-debug) MUST:**
1. Read `.claude/contexts/domain/{project}/tech-stack.md` BEFORE running any install/run commands
2. Use the package manager specified in tech-stack.md
3. Never assume npm/pip - always check tech-stack.md first

**Example:**
```
Agent reads tech-stack.md:
- Package Manager: pnpm

Agent runs:
✅ pnpm add fastapi  (correct)
❌ npm install fastapi  (wrong - ignored tech-stack.md!)
```

**For monorepo projects:**
```
Agent reads tech-stack.md:
- JavaScript: pnpm
- Python: uv

Agent working on backend (Python):
✅ uv pip install fastapi  (correct - uses Python package manager)
❌ pnpm add fastapi  (wrong - fastapi is Python, not JS!)
```

---

## Example Full Flow (Brownfield - Next.js)

```
1. User runs: /agentsetup

2. Read package.json:
   {
     "dependencies": {
       "next": "15.5.0",
       "@prisma/client": "6.5.0"
     }
   }

3. Output:
   🔍 Detected: Next.js 15.5.0, Prisma 6.5.0
   Is this correct? (yes/no)

4. User: yes

5. Search Context7:
   - resolve-library-id("Next.js") → "/vercel/next.js"
   - get-library-docs("/vercel/next.js/v15.5.0", "App Router")
   - resolve-library-id("Prisma") → "/prisma/prisma"
   - get-library-docs("/prisma/prisma/v6.5.0", "Client API")

6. Create files:
   - .claude/contexts/domain/myproject/tech-stack.md

7. Output summary:
   ✅ Setup complete! Ready to build.
```

---

**Now execute this workflow!**
