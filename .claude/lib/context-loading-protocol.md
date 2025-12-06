# Context Loading Protocol

> **Unified context loading strategy for all agents**
> **Version:** 2.0.0 (Claude 4.5 Optimized)
> **Purpose:** Consistent context loading across 6 agents (DRY principle)

---

## 📋 Overview

This protocol defines how agents discover and load context before starting work.

**Why this exists:**
- ✅ Single source of truth (DRY principle)
- ✅ Consistent behavior across all agents
- ✅ Easier maintenance (update once, applies everywhere)
- ✅ Package manager safety (prevent wrong tool usage)

**Who uses this:**
- All 6 agents (integration, uxui-frontend, test-debug, frontend, backend, database)
- Commands that need tech stack info (/csetup, /cdev)

---

## 📦 Level 0: Package Manager Discovery

**Before running install/run commands, detect the package manager.**

### Why This Matters:

Using the correct package manager:
- ✅ Prevents duplicate lock files (package-lock.json + pnpm-lock.yaml conflicts)
- ✅ Installs to correct location (node_modules vs .venv)
- ✅ Maintains CI/CD compatibility
- ✅ Avoids version conflicts

### Protocol:

**Step 1: Check if tech-stack.md exists**

```bash
# Read this file FIRST:
.claude/contexts/domain/{project-name}/tech-stack.md
```

**Step 2: Extract package manager**

```markdown
## Package Manager
### JavaScript/TypeScript
- Tool: pnpm
- Install: pnpm install <package>
- Run: pnpm run <script>

### Python
- Tool: uv
- Install: uv pip install <package>
- Run: uv run <script>
```

**Step 3: Store for all subsequent commands**

```
✅ Package Manager Detected:
   - JavaScript: pnpm
   - Python: uv

🎯 Will use these tools for all install/run commands
```

### What to Extract:

From tech-stack.md, extract:

1. **Framework** (Next.js, FastAPI, Vue, Django, Express)
   - Use for: Context7 queries
   - Example: "/vercel/next.js", "/fastapi/fastapi"

2. **Package Manager** (pnpm, npm, bun, uv, poetry, pip)
   - Use for: ALL install/run commands
   - Always use detected PM to prevent lock file conflicts

3. **ORM/Database Tool** (Prisma, SQLAlchemy, TypeORM, Drizzle)
   - Use for: Database agents
   - Example: Prisma → use `prisma` CLI

4. **Testing Framework** (Vitest, Jest, Pytest, Playwright)
   - Use for: test-debug agent
   - Example: Vitest → use `vitest` command

### If tech-stack.md Doesn't Exist:

```
⚠️ tech-stack.md not found!
💡 User should run: /csetup

FALLBACK (use ONLY if absolutely necessary):
- Detect from package.json (JavaScript)
- Detect from pyproject.toml (Python)
- Warn user about missing tech-stack.md
```

---

## 📚 Level 1: Universal Patterns (All Agents Load)

These patterns apply to ALL agents regardless of role:

**Core Patterns (ALWAYS load):**
- `@.claude/contexts/patterns/error-handling.md` (how to handle errors)
- `@.claude/contexts/patterns/logging.md` (logging standards)
- `@.claude/contexts/patterns/testing.md` (test conventions)
- `@.claude/contexts/patterns/code-standards.md` (coding style)

**Why load these:**
- Ensures consistent error messages across codebase
- Prevents random logging formats
- Enforces test naming conventions
- Maintains code quality standards

**Example report:**
```
✅ Universal Patterns Loaded:
   - Error Handling ✓
   - Logging ✓
   - Testing ✓
   - Code Standards ✓
```

---

## 🎯 Level 2: Framework-Specific Patterns (Context7)

Based on tech-stack.md, query Context7 for latest framework docs.

### Decision Tree:

**IF Backend Framework (FastAPI, Express, Django):**

```javascript
// FastAPI (Python)
mcp__context7__get-library-docs("/fastapi/fastapi", {
  topic: "routing, dependency injection, pydantic validation, async",
  tokens: 3000
})

// Express (Node.js)
mcp__context7__get-library-docs("/expressjs/express", {
  topic: "routing, middleware, error handling",
  tokens: 2000
})

// Django
mcp__context7__get-library-docs("/django/django", {
  topic: "views, urls, models, middleware",
  tokens: 3000
})
```

**IF Frontend Framework (React, Next.js, Vue):**

```javascript
// Next.js
mcp__context7__get-library-docs("/vercel/next.js", {
  topic: "app router, server components, api routes, routing",
  tokens: 3000
})

// React
mcp__context7__get-library-docs("/facebook/react", {
  topic: "hooks, components, state management",
  tokens: 2000
})

// Vue
mcp__context7__get-library-docs("/vuejs/core", {
  topic: "composition api, components, reactivity",
  tokens: 2000
})
```

**IF ORM/Database (Prisma, SQLAlchemy, TypeORM):**

```javascript
// Prisma
mcp__context7__get-library-docs("/prisma/prisma", {
  topic: "schema, migrations, queries, relations",
  tokens: 3000
})

// SQLAlchemy
mcp__context7__get-library-docs("/sqlalchemy/sqlalchemy", {
  topic: "models, sessions, queries, relationships",
  tokens: 3000
})

// TypeORM
mcp__context7__get-library-docs("/typeorm/typeorm", {
  topic: "entities, migrations, queries",
  tokens: 2000
})
```

**IF Testing Framework (Vitest, Jest, Pytest, Playwright):**

```javascript
// Vitest
mcp__context7__get-library-docs("/vitest-dev/vitest", {
  topic: "testing, mocking, coverage",
  tokens: 2000
})

// Pytest
mcp__context7__get-library-docs("/pytest-dev/pytest", {
  topic: "fixtures, parametrize, mocking",
  tokens: 2000
})

// Playwright
mcp__context7__get-library-docs("/microsoft/playwright", {
  topic: "browser testing, selectors, assertions",
  tokens: 2000
})
```

**Example report:**
```
✅ Framework Docs Loaded (Context7):
   - Next.js 15 ✓ (app router, server components)
   - React 19 ✓ (hooks, components)
   - Prisma 6 ✓ (schema, queries)
   - Vitest 2 ✓ (testing, mocking)
```

---

## 🎨 Level 3: Agent-Specific Contexts

Each agent loads additional contexts based on their role.

### uxui-frontend Agent:

**Additional contexts:**
- `@.claude/contexts/design/index.md` (design principles)
- `@.claude/contexts/design/box-thinking.md` (layout analysis)
- `@.claude/contexts/design/color-theory.md` (color usage)
- `@.claude/contexts/design/spacing.md` (spacing scale)
- `@.claude/contexts/design/shadows.md` (elevation)
- `@.claude/contexts/patterns/ui-component-consistency.md` (component reuse)
- `@.claude/contexts/patterns/frontend-component-strategy.md` (when to create vs reuse)

**Project-specific (if exists):**
- `design-system/data.yaml` (tokens + psychology, ~500 tokens)
- `design-system/README.md` (human-readable summary, ~100 tokens)
- `openspec/changes/{change-id}/page-plan.md` (from /pageplan command)

**Loading strategy:**
```
1. Load data.yaml (contains all design tokens)
2. Fall back to design/*.md if no data.yaml
```

### backend Agent:

**Additional contexts:**
- API security patterns
- Request validation patterns
- Authentication/authorization patterns

**ORM-specific:**
- Load ORM docs from Context7 (Prisma, SQLAlchemy, etc.)

### database Agent:

**Additional contexts:**
- Schema design patterns
- Migration patterns
- Query optimization patterns

**ORM-specific:**
- Load ORM docs from Context7
- Focus on: schema, migrations, relationships

### frontend Agent:

**Additional contexts:**
- State management patterns (Zustand, Redux)
- API integration patterns
- Form handling patterns

### integration Agent:

**Additional contexts:**
- API contract validation patterns
- OpenAPI/Swagger patterns

### test-debug Agent:

**Additional contexts:**
- Test framework docs from Context7
- Debugging patterns
- Coverage patterns

---

## 📊 Complete Loading Flow Example

**Example: uxui-frontend agent starting work**

```
🔄 Starting Context Loading Protocol...

📦 Level 0: Package Manager Discovery
   → Reading: .claude/contexts/domain/my-app/tech-stack.md
   ✅ Detected:
      - Framework: Next.js 15
      - Package Manager: pnpm
      - Testing: Vitest 2

📚 Level 1: Universal Patterns
   → Loading: error-handling.md ✓
   → Loading: logging.md ✓
   → Loading: testing.md ✓
   → Loading: code-standards.md ✓
   ✅ Universal patterns loaded

🎯 Level 2: Framework-Specific (Context7)
   → Query: /vercel/next.js (app router, server components)
   → Query: /facebook/react (hooks, components)
   ✅ Framework docs loaded

🎨 Level 3: Agent-Specific (uxui-frontend)
   → Loading: design/*.md ✓
   → Loading: patterns/ui-component-consistency.md ✓
   → Loading: design-system/data.yaml ✓
   → Loading: openspec/changes/landing-page/page-plan.md ✓
   ✅ Design contexts loaded

✅ Context Loading Complete!

📁 Project: my-app
🛠️ Stack: Next.js 15 + React 19
📦 Package Manager: pnpm
🎨 Style Guide: ✓ (17 sections)
📋 Page Plan: ✓ (3 reuse, 2 new)

🎯 Ready to start work!
```

---

## 📋 Package Manager Guidelines

### Use Detected Package Manager

| If Detected | Install Command | Run Command |
|-------------|-----------------|-------------|
| pnpm | `pnpm install lodash` | `pnpm run dev` |
| npm | `npm install lodash` | `npm run dev` |
| uv | `uv pip install requests` | `uv run app.py` |
| poetry | `poetry add requests` | `poetry run python app.py` |

WHY: Using the detected PM prevents lock file conflicts and maintains CI/CD compatibility.

### Error Handling:

**If package manager command fails:**

```
❌ Error: pnpm command failed

Troubleshooting:
1. Check tech-stack.md is accurate
2. Verify package manager is installed
3. Try: npm install -g pnpm
4. Update tech-stack.md if wrong
```

**If tech-stack.md is outdated:**

```
⚠️ Warning: tech-stack.md shows pnpm, but pnpm-lock.yaml not found

Suggestion:
- Run: /csetup (regenerate tech-stack.md)
- Or manually update tech-stack.md
```

---

## 🔄 When to Re-load Context

**Re-load Level 0-2 when:**
- ✅ User runs `/csetup` (tech stack changed)
- ✅ Framework version upgraded
- ✅ New dependencies added

**Don't re-load when:**
- ❌ Working on same project continuously
- ❌ Context already loaded this session
- ❌ Only code changes (no new dependencies)

---

## 📝 Quick Reference

### Checklist for Agents:

```markdown
Before starting ANY work:

[ ] Level 0: Read tech-stack.md
    - Extract package manager
    - Extract framework
    - Store for subsequent commands

[ ] Level 1: Load universal patterns
    - error-handling.md
    - logging.md
    - testing.md
    - code-standards.md

[ ] Level 2: Query Context7
    - Framework docs
    - ORM docs (if applicable)
    - Testing docs (if applicable)

[ ] Level 3: Load agent-specific contexts
    - See agent-specific sections above

[ ] Report context loading complete
    - Show package manager
    - Show frameworks loaded
    - Show contexts loaded
```

---

## 🔗 See Also

- `agent-discovery.md` - Project discovery flow (STEP 0)
- `validation-framework.md` - Pre-work validation requirements
- `agent-router.md` - Agent routing rules
- `contexts/domain/{project}/tech-stack.md` - Tech stack source of truth
