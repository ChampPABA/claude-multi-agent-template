# CLAUDE.md

> **Navigation Hub for AI Agents**  
> **Template Version:** 1.0.0 - Universal Multi-Agent Template

---

## 🎯 What is This Template?

Universal, framework-agnostic template for AI-assisted development.

**What's Included:**
- ✅ 6 Specialized Agents (integration + 5 domain specialists)
- ✅ Universal Patterns (logging, testing, error-handling, agent selection)
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
- `@/.claude/contexts/patterns/task-classification.md` (Agent selection guide)
- `@/.claude/contexts/patterns/agent-coordination.md` (When to run agents parallel/sequential)
- `@/.claude/contexts/patterns/error-recovery.md` (How agents handle errors & escalate)
- `@/.claude/contexts/patterns/logging.md`
- `@/.claude/contexts/patterns/testing.md`
- `@/.claude/contexts/patterns/task-breakdown.md`
- `@/.claude/contexts/patterns/frontend-component-strategy.md`

**Framework-Specific:**
- Use Context7 MCP (Example: "React hooks best practices")

---

## 🤖 Agent System

### How It Works:

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

### Available Agents (6 specialists):

| Agent | Color | When to Use | Phase |
|-------|-------|-------------|-------|
| **integration** | Orange | Validate API contracts before connecting | 2.5 |
| **uxui-frontend** | Blue | Design UI components with mock data | 1 |
| **test-debug** | Red | Run tests and fix bugs (max 3-4 iterations) | 1,3,4 |
| **frontend** | Green | Connect UI to backend APIs | 3 |
| **backend** | Purple | Create API endpoints with validation | 2 |
| **database** | Pink | Design schemas, migrations, complex queries | 2 |

### Usage:

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

### ⚠️ Enforcing Design Fundamentals (CRITICAL for uxui-frontend)

**When invoking uxui-frontend agent, Main Claude MUST include these requirements in the Task prompt:**

```
MANDATORY PRE-WORK CHECKLIST:

Before writing ANY code, you MUST:

1. **Read ALL design contexts:**
   - @/.claude/contexts/design/index.md
   - @/.claude/contexts/design/box-thinking.md
   - @/.claude/contexts/design/color-theory.md
   - @/.claude/contexts/design/spacing.md
   - @/.claude/contexts/patterns/ui-component-consistency.md
   - @/.claude/contexts/patterns/frontend-component-strategy.md

2. **Do Box Thinking Analysis:**
   - Identify all boxes (parent, children, siblings)
   - Document relationships (container, adjacent, nested)
   - Plan space flow using spacing scale (8, 16, 24, 32, 40, 48px)
   - Plan responsive behavior (stack/merge/compress)

3. **Search for Existing Components:**
   - Glob: "**/*{Keyword}*.{tsx,jsx,vue}"
   - Grep: "[similar-pattern]"
   - Decision: Reuse > Compose > Extend > Create New
   - If creating new: Extract design tokens from most similar component

4. **Extract Design Tokens from Reference Component:**
   ```typescript
   const DESIGN_TOKENS = {
     spacing: { padding: '[from reference]', gap: '[from reference]' },
     colors: { bg: '[theme token]', text: '[theme token]', border: '[theme token]' },
     shadows: '[from reference - e.g., shadow-sm]',
     borderRadius: '[from reference - e.g., rounded-md]'
   }
   ```

5. **Report Pre-Implementation Analysis:**
   You MUST provide a detailed report covering steps 1-4 BEFORE writing any code.

CRITICAL RULES:
- ❌ NO hardcoded colors (text-gray-500) → ✅ Use theme tokens (text-foreground/70)
- ❌ NO arbitrary spacing (p-5) → ✅ Use spacing scale (p-4, p-6)
- ❌ NO inconsistent icons (h-5 w-5, opacity-50) → ✅ Match reference (h-4 w-4, text-foreground/70)
- ❌ NO creating duplicate components → ✅ Search and reuse first

If you skip these steps, your work will be rejected.
```

**Why this enforcement matters:**
- Prevents visual inconsistency (mismatched colors, spacing, shadows)
- Ensures component reuse (avoids duplicates)
- Maintains design system integrity
- Saves implementation time

**Example: Build Login System**
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

**💡 Remember:** This template is universal. Use Context7 for framework-specific docs!
