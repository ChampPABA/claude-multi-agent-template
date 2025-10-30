# .claude/lib/ - Implementation Logic

> **Logic specifications for Main Claude orchestrator**

---

## 📁 Files

**`agent-executor.md`** - Agent retry & escalation logic
Used by `/cdev` to execute agents with automatic retry, validation, and user escalation

**`tdd-classifier.md`** - TDD classification logic
Used by `/csetup` to automatically determine which phases require TDD workflow

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
