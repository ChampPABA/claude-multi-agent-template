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

**Follow-up questions:**
- Database: Prisma / SQLAlchemy / TypeORM / Eloquent / ActiveRecord?
- Testing: Vitest / Jest / Pytest / PHPUnit / RSpec?
- State Management (if frontend): Zustand / Redux / Pinia / Vuex?

### Example Interaction:

```
User selects: Next.js
→ Ask: "Which database ORM?"
  - Prisma
  - Drizzle
  - TypeORM

User selects: Prisma
→ Ask: "Which testing framework?"
  - Vitest
  - Jest
  - Playwright (E2E)
```

---

## Step 2B: Brownfield Flow

### Auto-Detect Stack from Files

**Read the dependency file and extract versions:**

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

## Step 4: Create Domain Context Files

Create directory structure:
```bash
mkdir -p .claude/contexts/domain/{project-name}
```

### File 1: tech-stack.md

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

## Installation Commands

\`\`\`bash
# Node.js
pnpm install

# Python
pip install -r requirements.txt

# PHP
composer install
\`\`\`

## Key Patterns (from Context7)

### Next.js 15 App Router
- Server Components by default
- Use 'use client' for interactivity
- File-based routing in app/ directory

### Prisma 6
- Use \`prisma generate\` after schema changes
- Connection pooling with \`?pool_timeout=0\`
- Use transactions for multi-step operations

### Zustand 5
- Create stores with \`create()\`
- Use \`persist\` middleware for localStorage
- TypeScript support with generics

### Vitest 2
- Use \`describe\` and \`it\` for tests
- Mock with \`vi.fn()\` and \`vi.mock()\`
- Run tests with \`vitest\` or \`vitest --run\`
```

### File 2: architecture.md (Optional)

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

🛠️ Tech Stack Detected:
- Frontend: Next.js 15.5.0
- Database: Prisma 6.5.0
- State: Zustand 5.0.0
- Testing: Vitest 2.0.0

📁 Domain Context Created:
- .claude/contexts/domain/{project}/tech-stack.md
- .claude/contexts/domain/{project}/architecture.md (if applicable)
- .claude/contexts/domain/{project}/business-rules.md (if applicable)
- .claude/contexts/domain/{project}/design-tokens.md (if applicable)

📚 Context7 Docs Retrieved:
- Next.js 15 App Router (5000 tokens)
- Prisma 6 Best Practices (5000 tokens)
- Zustand 5 TypeScript (3000 tokens)
- Vitest 2 Testing (3000 tokens)

🚀 Ready to start! Use:
- /agents orchestrator → Coordinate complex tasks
- /agents frontend → Build UI components
- /agents backend → Create API endpoints
- /agents database → Design schemas
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
2. **ALWAYS create tech-stack.md** (mandatory)
3. **ONLY create architecture/business-rules/design-tokens** if spec provides info
4. **NEVER guess versions** - read from package files or ask user
5. **ALWAYS confirm detected stack** with user before proceeding
6. **Store Context7 library IDs** in tech-stack.md for future reference

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
