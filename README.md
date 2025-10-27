# Claude Multi-Agent Template

> Reusable multi-agent system for spec-driven development with automatic Context7 integration.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 What is this?

A **production-ready template** for building software with AI agents that:

- ✅ **Coordinate complex tasks** - Orchestrator delegates to specialists
- ✅ **Always up-to-date** - Uses Context7 MCP for latest framework docs
- ✅ **Zero maintenance** - No tech stack docs to update (Context7 handles it)
- ✅ **Reusable** - Works for Next.js, FastAPI, Vue, Django, or any stack
- ✅ **Incremental** - 4-phase methodology (MVT → Complexity → Scale → Deploy)

---

## 🚀 Quick Start

### 1. Clone Template

```bash
git clone https://github.com/ChampPABA/claude-multi-agent-template.git my-project
cd my-project
rm -rf .git
git init
```

### 2. Setup MCP (Context7)

Add to your MCP settings:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp"]
    }
  }
}
```

### 3. Start Building

**Option A: Manual**
```bash
/agents orchestrator
# Describe your task, agent coordinates implementation
```

**Option B: With tasks.md**
```markdown
<!-- tasks.md -->
# Feature: User Authentication

## Tech Stack
- Frontend: Next.js 15
- Backend: Next.js API Routes
- Database: Prisma + PostgreSQL

## Tasks
### Phase 1: UX-UI
- Task 1.1: Create login form (mock data)
- Task 1.2: Test with Vitest
- Task 1.3: Human approval

### Phase 2: Frontend
- Task 2.1: Connect to API
- Task 2.2: Add state management (Zustand)

### Phase 3: Backend
- Task 3.1: POST /api/auth/login
- Task 3.2: JWT token generation

### Phase 4: Database
- Task 4.1: User model (email, password, name)
```

Then:
```
User: "Execute tasks.md"
→ Orchestrator reads tasks → Detects Next.js/Prisma → Delegates to agents
```

---

## 🤖 Agents

### **Orchestrator** (Sonnet 4.5)
Coordinates multi-step tasks, detects tech stack, delegates to specialists.

### **UX-UI Frontend** (Haiku 4.5)
Creates components with mock data, follows design foundation.

### **Test-Debug** (Haiku 4.5)
Runs tests, fixes bugs automatically (max 3-4 iterations, then escalates).

### **Frontend** (Haiku 4.5)
Connects components to real APIs, implements state management.

### **Backend** (Haiku 4.5)
Builds API endpoints with validation (FastAPI, Express, Next.js API Routes).

### **Database** (Haiku 4.5)
Designs schemas, writes migrations (Prisma, SQLAlchemy, TypeORM).

---

## 📁 Structure

```
.claude/
├── CLAUDE.md                    # Navigation guide
├── agents/                      # 6 agents (Orchestrator + 5 specialists)
│   ├── 01-orchestrator.md
│   ├── 02-uxui-frontend.md
│   ├── 03-test-debug.md
│   ├── 04-frontend.md
│   ├── 05-backend.md
│   └── 06-database.md
│
└── contexts/
    ├── patterns/                # Universal patterns (static)
    │   ├── logging.md
    │   ├── testing.md
    │   ├── error-handling.md
    │   ├── task-breakdown.md
    │   ├── development-principles.md
    │   ├── code-standards.md
    │   ├── state-management.md
    │   ├── package-management.md
    │   └── specification.md
    │
    ├── design/                  # Design foundation (static)
    │   ├── index.md
    │   ├── color-theory.md
    │   ├── typography.md
    │   ├── spacing.md
    │   ├── shadows.md
    │   ├── layout.md
    │   ├── responsive.md
    │   ├── box-thinking.md
    │   └── accessibility.md
    │
    └── domain/                  # Project-specific (you create)
        └── README.md
```

---

## 🎨 Design System

Template includes **universal design foundation**:

- **Color Theory** - Harmony, WCAG AAA contrast, shade generation
- **Typography** - Font scales, hierarchy, readability
- **Spacing** - 8px grid system
- **Shadows** - 4-level elevation system
- **Layout** - Grid, flexbox, responsive patterns
- **Accessibility** - ARIA, keyboard nav, screen readers

**Project-specific colors:** Define in `.claude/contexts/domain/{project}/design-tokens.md`

---

## 🧪 Testing Philosophy

### TDD for Critical Paths (Required)
- Business logic (calculations, transformations)
- API endpoints (validation, error handling)
- External service integrations
- Data transformations

### Test-Alongside for Simple Code
- CRUD operations
- UI components (presentational)
- Configuration files

**Test-Debug agent** runs tests automatically, fixes bugs (max 3-4 iterations).

---

## 📊 Logging & Observability

**Every significant action must be logged** (structured JSON):

```typescript
logger.info('api_route_entry', { route, method, requestId })
logger.info('db_operation_success', { operation, table, duration })
logger.error('api_route_error', { route, error, stack, requestId })
```

See: `.claude/contexts/patterns/logging.md`

---

## 🔧 Tech Stack Support

### Automatically Detected via Context7

**Frontend:**
- Next.js, React, Vue, Svelte, Angular

**Backend:**
- FastAPI, Express, NestJS, Django, Flask

**Database:**
- Prisma, SQLAlchemy, TypeORM, Drizzle

**Testing:**
- Vitest, Jest, Pytest, Playwright

Agents search Context7 MCP for latest docs automatically.

---

## 📖 Examples

### Example 1: Next.js + Prisma

```bash
# Your project
package.json: { "dependencies": { "next": "15.5.0", "@prisma/client": "6.5.0" } }

# Orchestrator detects:
Frontend = Next.js 15
Database = Prisma
→ Agents use Context7: Next.js App Router docs + Prisma docs
```

### Example 2: FastAPI + SQLAlchemy

```bash
# Your project
requirements.txt: fastapi, sqlalchemy

# Orchestrator detects:
Backend = FastAPI
Database = SQLAlchemy
→ Agents use Context7: FastAPI docs + SQLAlchemy docs
```

---

## 🎯 Customization

### Add Domain-Specific Context

```bash
mkdir -p .claude/contexts/domain/myproject
```

Example (E-commerce):
```markdown
<!-- .claude/contexts/domain/ecommerce/checkout-flow.md -->
# Checkout Flow

## Steps
1. Cart review
2. Shipping address
3. Payment method
4. Order confirmation

## Business Rules
- Free shipping > $50
- Tax calculation by state
- Inventory check before payment
```

Agents will load these patterns automatically.

---

## 🤝 Contributing

This is a template repo. Fork and customize for your needs!

**Improvements welcome:**
- Additional patterns (caching, rate limiting, etc.)
- More design foundation content
- Example projects
- Documentation improvements

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Credits

Built with:
- [Claude Code](https://claude.com/claude-code) - AI-powered coding assistant
- [Context7 MCP](https://context7.com) - Always up-to-date library documentation
- [OpenSpec](https://openspec.dev) - Spec-driven development framework (optional)

---

**Ready to build?** Clone this template and start creating! 🚀
