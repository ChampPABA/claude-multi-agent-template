# .claude/lib/ - Implementation Logic

> **Logic specifications for Main Claude orchestrator**

---

## 📁 Files

**`agent-executor.md`** - Agent retry & escalation logic
Used by `/cdev` to execute agents with automatic retry, validation, and user escalation

**`tdd-classifier.md`** - TDD classification logic
Used by `/csetup` to automatically determine which phases require TDD workflow

**`flags-updater.md`** - 🆕 Progress tracking protocol
Ensures Main Claude updates flags.json after EVERY phase completion. Provides helper functions for extracting files, tasks, and calculating duration.

**`agent-router.md`** - 🆕 Mandatory agent routing rules
Enforces strict agent boundaries. Main Claude MUST delegate implementation work to specialized agents. Includes work type detection patterns and self-check protocol.

**`validation-gates.md`** - 🆕 Validation checkpoints
Four validation gates that Main Claude MUST pass: before work, after agent responds, before reporting, and before phase start. Ensures quality and correctness at each step.

---

## 🚨 Important

These are **logic specifications** (not executable code). Main Claude reads these .md files as documentation and implements the logic when running `/cdev` and `/csetup` commands.

**Why .md files?** Claude Code has no TypeScript runtime. These files are "pseudocode specifications" that Main Claude reads and implements.

---

## 📚 See Also

- `.claude/contexts/patterns/validation-framework.md` - Agent validation checklists
- `.claude/contexts/patterns/agent-discovery.md` - Agent discovery flow
- `.claude/commands/cdev.md` - How /cdev uses agent-executor.md
- `.claude/commands/csetup.md` - How /csetup uses tdd-classifier.md
