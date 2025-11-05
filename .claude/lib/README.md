# .claude/lib/ - Implementation Logic

> **Logic specifications for Main Claude orchestrator**
> **Version:** 1.4.0 - Context Optimization & DRY Consolidation

---

## 📁 Core Logic Files

**`agent-executor.md`** - Agent retry & escalation logic
Used by `/cdev` to execute agents with automatic retry, validation, and user escalation

**`tdd-classifier.md`** - TDD classification logic
Used by `/csetup` to automatically determine which phases require TDD workflow

**`flags-updater.md`** - Progress tracking protocol
Ensures Main Claude updates flags.json after EVERY phase completion. Provides helper functions for extracting files, tasks, and calculating duration.

**`agent-router.md`** - Mandatory agent routing rules
Enforces strict agent boundaries. Main Claude MUST delegate implementation work to specialized agents. Includes work type detection patterns and self-check protocol.

**`validation-gates.md`** - Validation checkpoints
Four validation gates that Main Claude MUST pass: before work, after agent responds, before reporting, and before phase start. Ensures quality and correctness at each step.

**`task-analyzer.md`** - TaskMaster-style task analysis (v1.3.0)
Used by `/csetup` to analyze tasks with 6 dimensions: complexity, dependencies, risk, research, subtasks, priority. Generates intelligent phases.md with time buffers and metadata.

---

## 📁 Shared Documentation (v1.4.0 - NEW!)

**`context-loading-protocol.md`** - Universal context loading strategy
Consolidated protocol used by ALL agents (STEP 0). Includes package manager discovery, framework detection via Context7, and best practices loading.

**`handoff-protocol.md`** - Agent handoff templates
Standardized handoff formats for agent-to-agent communication. Includes all 15 handoff paths with clear templates.

**`tdd-workflow.md`** - TDD workflow examples
Complete TDD implementation examples (Stripe integration, user auth). Used by frontend, backend, database agents.

**`document-loader.md`** - Token-efficient document loading
Unified pattern for loading design system files. 3-tier strategy: STYLE_TOKENS.json → design-context.md → STYLE_GUIDE.md.

---

## 📁 Detailed Guides (v1.4.0 - NEW!)

**`detailed-guides/best-practices-system.md`** - How best practices work
Complete guide to auto-generated best practices via Context7 MCP. Covers `/agentsetup`, 3-level indexing, and agent discovery flow.

**`detailed-guides/context-optimization.md`** - Token optimization strategy
Details the 70% token reduction in design system loading. Explains 3-tier loading, before/after comparisons, and benefits.

**`detailed-guides/page-planning.md`** - /pageplan command guide
Complete guide to page planning system. Covers component reuse, content drafting, asset preparation, and 25% speed improvement.

**`detailed-guides/taskmaster-analysis.md`** - 6-dimension task analysis
Detailed explanation of TaskMaster-style analysis. Covers complexity scoring, dependency detection, risk assessment, research requirements, subtask breakdown, priority ranking.

**`detailed-guides/design-system.md`** - Style guide generation
How `/designsetup` works. Covers 3 smart paths (reference → brownfield → greenfield), 17-section output, and agent discovery.

**`detailed-guides/agent-system.md`** - Agent overview & workflow
Complete agent system guide. Covers 6 specialist agents, Main Claude's role, self-check protocol, and pre-work requirements.

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
