# Agent System

> **Detailed guide to the multi-agent architecture**
> **Source:** Extracted from CLAUDE.md (Navigation Hub)
> **Version:** 2.0.0 (Claude 4.5 Optimized)

---

## 🤖 How It Works

**Main Claude analyzes tasks → Invokes specialist agents directly**

```
1. User provides task (e.g., "Build login system")
   ↓
2. Main Claude reads @task-classification.md
   ↓
3. Main Claude selects appropriate agent(s)
   ↓
4. Execute in proper sequence:
   - Phase 1: uxui-frontend (UI with mock data)
   - Phase 2: backend + database (parallel)
   - Phase 2.5: integration (validate contracts)
   - Phase 3: frontend (connect UI to API)
   - Phase 4: test-debug (tests & bug fixes)
```

---

## Available Agents (6 specialists)

**All agents use Opus 4.5** for best-in-class reasoning and code quality.

| Agent | Color | Model | When to Use | Phase |
|-------|-------|-------|-------------|-------|
| **integration** | Orange | opus | Validate API contracts before connecting | 2.5 |
| **uxui-frontend** | Blue | opus | Design UI components with mock data | 1 |
| **test-debug** | Red | opus | Run tests and fix bugs (max 3-4 iterations) | 1,3,4 |
| **frontend** | Green | opus | Connect UI to backend APIs | 3 |
| **backend** | Cyan | opus | Create API endpoints with validation | 2 |
| **database** | Pink | opus | Design schemas, migrations, complex queries | 2 |

---

## Usage

**For any task, Main Claude will:**
1. Read `@/.claude/contexts/patterns/task-classification.md`
2. Determine which agent(s) to use
3. Invoke agents in proper sequence
4. Coordinate between agents

**You can also invoke agents directly:**
```
User: "/agents uxui-frontend"
Main Claude: *Executes uxui-frontend agent directly*
```

---

## 🔒 Main Claude Self-Check Protocol

**Before starting work, Main Claude routes tasks appropriately.**

→ See: `@/.claude/lib/agent-router.md` for complete routing protocol

**Quick Routing Table:**

| Task Type | Route To |
|-----------|----------|
| UI components | uxui-frontend |
| API endpoints | backend |
| Database schemas | database |
| API integration | frontend |
| Tests/bugs | test-debug |
| Contracts | integration |
| Planning, reading, explaining | Main Claude (direct) |

**Main Claude's Role:**
- Orchestrator (plan, coordinate, report)
- Progress tracker (update flags.json)
- Analyst (read files, explain code)

WHY routing matters: Specialist agents have domain-specific validation (design tokens, TDD patterns, error handling) that ensures higher quality output.

---

## 📋 Agent Pre-Work Requirements

→ See: `.claude/agents/_shared/pre-work-checklist.md` for detailed checklist

### STEP 0: Project Discovery (All Agents)

```
1. Read: domain/index.md → Get current project name
2. Read: domain/{project}/README.md → Get tech stack summary
3. Read: domain/{project}/best-practices/index.md → Find relevant files
4. Read: domain/{project}/best-practices/{files} → Load best practices
5. Report: "✅ Project Context Loaded"
```

### STEP 0.5: Design Context (uxui-frontend only)

```
6. Check: design-system/STYLE_GUIDE.md exists?
   - If YES → Read STYLE_GUIDE.md (project-specific)
   - If NO → Read .claude/contexts/design/*.md (fallback)
7. Report: "✅ Style Guide Loaded"
```

WHY: STYLE_GUIDE.md has project-specific tokens. design/*.md has universal principles.

**Fallback:** If discovery fails, suggest `/agentsetup` or `/designsetup`

---

### STEP 1-5: Design Fundamentals (uxui-frontend only)

→ See: `.claude/agents/02-uxui-frontend.md` for complete checklist

**Summary:**
1. Read design contexts (box-thinking, color-theory, spacing)
2. Do Box Thinking Analysis (identify boxes, relationships, spacing)
3. Search for existing components (Reuse > Compose > Extend > Create)
4. Extract design tokens from reference component
5. Report pre-implementation analysis

**Style Guidelines:**

| Instead of | Use | WHY |
|------------|-----|-----|
| text-gray-500 | text-foreground/70 | Theme-aware |
| p-5 | p-4 or p-6 | Spacing scale |
| h-5 w-5, opacity-50 | h-4 w-4, text-foreground/70 | Consistency |

WHY these steps matter: Prevents visual inconsistency, ensures component reuse, maintains design system integrity.

---

## Example: Build Login System

```
User: "Build a login system"
Main Claude analyzes → Breaks into phases:
  Phase 1: /agents uxui-frontend (create login form UI)
  Phase 2: /agents backend (create POST /api/login)
          /agents database (create User model) [parallel]
  Phase 2.5: /agents integration (verify contracts)
  Phase 3: /agents frontend (connect form to API)
  Phase 4: /agents test-debug (test everything)
```

---

## 🔗 See Also

- `../agent-router.md` - Mandatory agent routing rules (enforcement)
- `../agent-executor.md` - Agent retry & escalation logic (used by /cdev)
- `../../contexts/patterns/task-classification.md` - Agent selection guide
- `../../contexts/patterns/agent-coordination.md` - When to run agents parallel/sequential
- `../../contexts/patterns/agent-discovery.md` - Shared agent discovery flow
