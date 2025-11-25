# Agent System

> **Detailed guide to the multi-agent architecture**
> **Source:** Extracted from CLAUDE.md (Navigation Hub)
> **Version:** 1.7.0 (Opus 4.5)

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

## 🔒 Main Claude Self-Check Protocol (MANDATORY)

**⚠️ CRITICAL: Main Claude MUST complete this checklist BEFORE doing ANY work**

See: `@/.claude/lib/agent-router.md` for complete routing protocol

**Pre-Work Checklist (Run for EVERY user request):**

```markdown
## ✅ Pre-Work Self-Check

[ ] 1. Read user request carefully
       - What are they asking for?
       - What is the end goal?

[ ] 2. Detect work type
       - Is this implementation work? (writing code, creating files)
       - Is this planning/analysis? (reading, explaining, breaking down)

[ ] 3. If IMPLEMENTATION work:
       - Read: @/.claude/contexts/patterns/task-classification.md
       - Which agent should handle this?
         • UI components → uxui-frontend
         • API endpoints → backend
         • Database schemas → database
         • API integration → frontend
         • Tests/bugs → test-debug
         • Contracts → integration

[ ] 4. Can Main Claude do this?
       ✅ YES for: Planning, reading files, explaining, orchestrating workflows
       ❌ NO for: Writing components, creating endpoints, designing schemas

[ ] 5. If MUST delegate:
       - Use Task tool with selected agent
       - Include all necessary context
       - Wait for agent response
       - Update flags.json after completion (if using /cdev)

[ ] 6. Report decision to user
       ```
       🔍 Task Analysis:
       - Work type: [type]
       - Requires: [agent] agent
       - Reason: [explanation]

       🚀 Invoking [agent] agent...
       ```
```

**Main Claude's Role:**
- ✅ Orchestrator (plan, coordinate, report)
- ✅ Progress tracker (update flags.json)
- ✅ Analyst (read files, explain code)
- ❌ NOT implementer (no writing code directly)

**If Main Claude skips this self-check for implementation work, it violates system protocol.**

---

## ⚠️ Agent Pre-Work Requirements

**STEP 0 (ALL agents):** Every agent must discover project context first

**STEP 1-5 (uxui-frontend only):** Design fundamentals checklist

---

### STEP 0: Project Discovery (ALL Agents)

**Every agent MUST complete this before ANY work:**

```
1. Read: domain/index.md → Get current project name
2. Read: domain/{project}/README.md → Get tech stack summary
3. Read: domain/{project}/best-practices/index.md → Find relevant files
4. Read: domain/{project}/best-practices/{files} → Load best practices
5. Report: "✅ Project Context Loaded"
```

**STEP 0.5 (uxui-frontend ONLY):**

```
6. Check: design-system/STYLE_GUIDE.md exists?
   - If YES → Read STYLE_GUIDE.md (Priority #1 - project-specific)
   - If NO → Read .claude/contexts/design/*.md (Fallback - general principles)
7. Report: "✅ Style Guide Loaded" or "⚠️ No style guide - using general principles"
```

**Why this matters:**
- STYLE_GUIDE.md = project-specific design system (colors, spacing, components)
- design/*.md = universal design principles (box thinking, color theory)
- Priority: STYLE_GUIDE.md > design/*.md

**Fallback:** If discovery fails, warn user to run `/agentsetup` or `/designsetup`

---

### STEP 1-5: Design Fundamentals (uxui-frontend only)

**When invoking uxui-frontend agent, Main Claude MUST include these requirements in the Task prompt:**

```
MANDATORY PRE-WORK CHECKLIST (after STEP 0):

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
