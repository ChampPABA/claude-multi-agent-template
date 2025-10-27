# Claude Multi-Agent Template

Reusable multi-agent system for spec-driven development with Context7 integration.

---

## 📚 Navigation

### Universal Contexts (Static - Reusable)
- **Patterns:** `@.claude/contexts/patterns/` - Development principles, logging, testing, error handling
- **Design Foundation:** `@.claude/contexts/design/` - Color theory, typography, spacing, shadows, accessibility
- **Agents:** `@.claude/agents/` - 6 specialized agents (Orchestrator + 5 specialists)

### Tech Stack Contexts (Dynamic - Context7 MCP)
Agents automatically search Context7 for latest documentation:
- Next.js, React, Vue, Svelte (Frontend)
- FastAPI, Express, Django (Backend)
- Prisma, SQLAlchemy, TypeORM (Database)

### Domain Contexts (Project-specific)
- **Create your domain:** `.claude/contexts/domain/{project-name}/`
- Example: `domain/ielts/`, `domain/ecommerce/`, `domain/crm/`

---

## 🤖 Available Agents

### Orchestrator (Sonnet 4.5)
**When to use:** Complex multi-step tasks requiring coordination

**Invoke:** `/agents orchestrator` or automatically when user provides `tasks.md`

**Role:** Reads tasks.md → Detects tech stack → Delegates to specialist agents

---

### Specialist Agents (Haiku 4.5)

| Agent | Role | Invoke |
|-------|------|--------|
| **uxui-frontend** | UX/UI components with mock data | `/agents uxui-frontend` |
| **test-debug** | Automated testing (max 3-4 iterations) | `/agents test-debug` |
| **frontend** | Connect components to APIs | `/agents frontend` |
| **backend** | API endpoints with validation | `/agents backend` |
| **database** | Schema design and migrations | `/agents database` |

---

## 🚀 Quick Start

### 1. Clone Template
```bash
git clone https://github.com/ChampPABA/claude-multi-agent-template.git
cd your-project
```

### 2. Create Domain Context (Optional)
```bash
mkdir -p .claude/contexts/domain/myproject
# Add project-specific patterns (design tokens, business rules, etc.)
```

### 3. Use Agents

**Manual:**
```bash
/agents orchestrator
```

**Automatic (Proactive):**
```
User: "Execute tasks in tasks.md"
→ Main Claude invokes orchestrator automatically
→ Orchestrator delegates to specialists
```

---

## 📖 How It Works

### Hybrid Context System
- **Static contexts** (patterns, design) → Always available, reusable
- **Dynamic contexts** (tech stack) → Context7 MCP searches latest docs
- **Domain contexts** (project) → Your custom business logic

### Agent Workflow
```
tasks.md (with Phase 1-4)
   ↓
Orchestrator (Sonnet 4.5)
├─ Detects tech stack (package.json, requirements.txt)
├─ Loads contexts (patterns/ + design/ + domain/)
├─ Routes tasks:
│  ├─ Phase 1: UX-UI → /agents uxui-frontend → /agents test-debug → Human approval
│  ├─ Phase 2-4: Parallel execution (frontend, backend, database)
│  └─ Merge outputs + validate integration
└─ Return complete implementation
```

---

## 🎯 Core Principles

- **KISS** - Keep it simple
- **YAGNI** - You aren't gonna need it
- **Observability First** - Log everything that matters
- **TDD for Critical Paths** - Test business logic first
- **Context7 for Latest Docs** - Always up-to-date framework patterns

---

## 📚 Learn More

- **Patterns:** See `.claude/contexts/patterns/` for detailed guides
- **Design:** See `.claude/contexts/design/` for design system foundation
- **Agents:** See `.claude/agents/` for agent prompts and capabilities

---

**Remember:** This is a template. Customize for your project's needs!
