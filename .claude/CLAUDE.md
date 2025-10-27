# CLAUDE.md

> **Navigation Hub for AI Agents**  
> **Template Version:** 1.0.0 - Universal Multi-Agent Template

---

## 🎯 What is This Template?

Universal, framework-agnostic template for AI-assisted development.

**What's Included:**
- ✅ 6 Specialized Agents (Orchestrator + 5 specialists)
- ✅ Universal Patterns (logging, testing, error-handling)
- ✅ Design Foundation (color theory, spacing, typography)
- ✅ Domain-Specific Support (add your business logic)

**What's NOT Included:**
- ❌ Framework patterns → Use Context7 MCP
- ❌ Package managers → Use Context7 MCP
- ❌ Spec frameworks → Optional (OpenSpec, BMAD, SpecKit)

---

## 📖 Quick Navigation

**Design/UI:**
- `@/.claude/contexts/design/index.md` (Start here)
- `@/.claude/contexts/design/box-thinking.md` (Layout analysis)
- `@/.claude/contexts/patterns/ui-component-consistency.md` (Visual consistency)

**Development:**
- `@/.claude/contexts/patterns/logging.md`
- `@/.claude/contexts/patterns/testing.md`
- `@/.claude/contexts/patterns/task-breakdown.md`
- `@/.claude/contexts/patterns/frontend-component-strategy.md`

**Framework-Specific:**
- Use Context7 MCP (Example: "React hooks best practices")

---

## 🤖 Agent System

### How It Works:

**Orchestrator (Planner) → Main Claude (Executor)**

```
1. Main Claude calls orchestrator agent
   ↓
2. Orchestrator analyzes tasks.md → Returns JSON plan
   ↓
3. Main Claude executes plan:
   - Phase 1: Sequential (uxui-frontend → test-debug → human approval)
   - Phase 2+: Parallel (frontend, backend, database)
```

### Available Agents:

| Agent | Color | Role |
|-------|-------|------|
| **orchestrator** | Gold | Analyzes tasks.md, returns execution plan (Planner) |
| **uxui-frontend** | Blue | UX/UI components with mock data |
| **test-debug** | Red | Automated testing (max 3-4 iterations) |
| **frontend** | Green | Connect components to APIs |
| **backend** | Purple | API endpoints with validation |
| **database** | Gray | Schema design and migrations |

### Usage:

**Option 1: With Orchestrator (Recommended for complex projects)**
```
User: "Analyze tasks.md and create execution plan"
Main Claude: *Calls orchestrator agent*
Orchestrator: *Returns JSON plan*
Main Claude: *Shows plan to user*
User: "Approved"
Main Claude: *Executes plan using specialist agents*
```

**Option 2: Direct Agent Invocation (For simple tasks)**
```
User: "/agents uxui-frontend"
Main Claude: *Executes agent directly*
```

---

**💡 Remember:** This template is universal. Use Context7 for framework-specific docs!
