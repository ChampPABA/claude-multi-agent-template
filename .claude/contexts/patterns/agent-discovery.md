# Agent Discovery Pattern

> **Standard 5-level project context discovery for ALL agents**

---

## 🎯 Purpose

Every agent MUST discover project context before ANY work. This ensures agents have all necessary context loaded.

---

## 📋 Discovery Sequence

### Level 1: Find Current Project

```bash
Read: .claude/contexts/domain/index.md
```

**Extract:**
- Current project name
- Project location path

**If not found:** → Go to [Fallback Strategy](#fallback-strategy)

---

### Level 2: Load Project Overview

```bash
Read: .claude/contexts/domain/{project}/README.md
```

**Extract:**
- Tech stack summary (frameworks, versions)
- Package manager
- Available best practices files

**If not found:** → Go to [Fallback Strategy](#fallback-strategy)

---

### Level 3: Check Best Practices Index

```bash
Read: .claude/contexts/domain/{project}/best-practices/index.md
```

**Find section:** "For `{your-agent-type}` agent"

**Extract:** List of must-read files for your role

**If not found:** → Go to [Fallback Strategy](#fallback-strategy)

---

### Level 4: Load Relevant Best Practices

**Based on Level 3 index, read agent-specific best practices:**

```bash
# Example for backend agent:
Read: .claude/contexts/domain/{project}/best-practices/fastapi-*.md
Read: .claude/contexts/domain/{project}/best-practices/express-*.md

# Example for frontend agent:
Read: .claude/contexts/domain/{project}/best-practices/react-*.md
Read: .claude/contexts/domain/{project}/best-practices/nextjs-*.md
```

**Use glob to find files:**
```bash
Glob: ".claude/contexts/domain/{project}/best-practices/*.md"
```

---

### Level 5: Change Context (If Working on OpenSpec Change)

**Check if change-specific context exists:**

```bash
ls openspec/changes/{change-id}/.claude/
```

**If exists, read change context:**

1. **Change-specific tech & patterns:**
   ```bash
   Read: openspec/changes/{change-id}/.claude/context.md
   ```

2. **Current progress:**
   ```bash
   Read: openspec/changes/{change-id}/.claude/flags.json
   ```

3. **Current phase instructions:**
   ```bash
   Read: openspec/changes/{change-id}/.claude/phases.md
   ```
   Find current phase section only (based on flags.json)

4. **OpenSpec files:**
   ```bash
   Read: openspec/changes/{change-id}/proposal.md   # WHY - goals, scope
   Read: openspec/changes/{change-id}/tasks.md      # WHAT - checklist
   Read: openspec/changes/{change-id}/design.md     # HOW - technical architecture (if exists)
   ```

   > **Note:** `design.md` = Technical/Architecture decisions (API structure, data flow)
   > This is DIFFERENT from `STYLE_GUIDE.md` which is Visual Design (colors, fonts)
   > See CLAUDE.md "File Naming Conventions" for details.

**If change context doesn't exist:**
- Skip Level 5 (working on general task, not OpenSpec change)

---

## ✅ Discovery Complete - Report

**After completing Levels 1-4, output:**

```
✅ Project Context Loaded

📁 Project: {project-name}
🛠️ Stack: {tech-stack-summary}
📚 Best Practices Loaded:
   - {framework-1} ✓
   - {framework-2} ✓

🎯 Ready to proceed!
```

---

## 🚨 Fallback Strategy

**If any level fails:**

1. **Try Glob Search:**
   ```bash
   Glob: ".claude/contexts/domain/*/README.md"
   ```
   - **Found 1:** Use it
   - **Found multiple:** Ask user which project
   - **Found 0:** Go to step 2

2. **Warn User:**
   ```
   ⚠️ No project context found!

   It looks like you haven't run `/agentsetup` yet.

   Options:
   1. Run `/agentsetup` now (recommended)
   2. Continue without best practices (universal patterns only)

   Which would you like?
   ```

3. **If user chooses option 2:**
   - Continue with universal patterns from `.claude/contexts/patterns/`
   - Warn that code may not follow project-specific conventions

---

## 📖 Usage in Agent Files

**In each agent .md file, replace entire STEP 0 with:**

```markdown
## STEP 0: Discover Project Context (MANDATORY - DO THIS FIRST!)

**Follow standard agent discovery:**
→ See `.claude/contexts/patterns/agent-discovery.md`

**Report when complete:**
✅ Project Context Loaded
```

---

This pattern ensures ALL agents follow the same discovery flow consistently.
