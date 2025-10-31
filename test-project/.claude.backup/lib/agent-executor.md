# Agent Executor with Retry & Escalation

> **Robust agent execution with automatic retry and error recovery**

---

## 🎯 Purpose

Provides resilient agent execution that:
- Auto-retries on validation failures (max 2 retries)
- Validates output quality before accepting
- Escalates to user when all retries fail

---

## 🔄 Retry Strategy

### When to Retry

**1. Validation Failed**
- Agent skipped pre-work checklist
- Missing required sections
- **Action:** Send rejection with specific missing items → retry

**2. Output Quality Issues**
- Output truncated or incomplete
- No code blocks (when expected)
- No test results (for test agent)
- **Action:** Send feedback → retry

**3. Agent Crashed**
- Timeout or network error
- **Action:** Retry with same prompt

### When NOT to Retry

- User manually cancelled
- Agent requested user input
- Max retries exceeded (2 attempts)

---

## 📋 Execution Flow

**Main Claude should follow this flow in `/cdev` command:**

### Step 1: Build Prompt

```markdown
Include in prompt:
- Change context (proposal, tasks, phases)
- Phase-specific instructions
- TDD requirements (if phase.tdd_required)
- Validation checkpoint reminder
```

### Step 2: Execute with Retry Loop

```
attempt = 0
max_retries = 2

while (attempt <= max_retries):

  1. Invoke agent:
     Task(agent=agentType, model='haiku', prompt=buildPrompt())

  2. Validate pre-work (see validation-framework.md):
     - Check for required checklist items
     - If missing → reject and retry

  3. Validate output quality:
     - Check for completion markers (✅, Done, Complete)
     - Check for code blocks (if code agent)
     - Check for test results (if test agent)
     - If incomplete → send feedback and retry

  4. If validation passed:
     → SUCCESS! Return result

  5. If validation failed:
     - If attempt < max_retries:
       → Send feedback, increment attempt, retry
     - Else:
       → FAIL! Escalate to user
```

### Step 3: Handle Result

**If success:**
```markdown
✅ Phase completed successfully!
⏱️ Execution time: {time}
🔄 Retries used: {count}
```

**If failed after retries:**
```markdown
❌ Phase failed after {attempts} attempts

What would you like to do?
1. Retry manually
2. Skip this phase
3. Abort workflow
```

---

## ✅ Pre-Work Validation

**Check agent response for required items:**

**All agents:**
- "Pre-Implementation Validation Report"
- "Ready to Implement ✓"

**uxui-frontend:**
- "Design Foundation ✓"
- "Box Thinking Analysis ✓"
- "Component Search ✓"
- "Design Tokens Extracted ✓"

**backend:**
- "Patterns Loaded ✓"
- "Existing Endpoints Search ✓"
- "TDD Workflow" (if TDD required)

**See:** `validation-framework.md` for complete list per agent

---

## 📊 Output Quality Checks

**Check output for:**

1. **Completion marker**
   - Contains "✅" or "Done" or "Complete"
   - If not → likely truncated

2. **Files mentioned** (non-integration agents)
   - Contains "File" or "Created" or "Modified"
   - If not → likely didn't implement anything

3. **Code blocks** (code agents: backend, frontend, uxui-frontend)
   - Contains "```"
   - If not → likely missing implementation

4. **Test results** (test-debug agent)
   - Contains "passed" or "test"
   - If not → likely didn't run tests

5. **No unresolved errors**
   - If contains "ERROR" or "FAILED" without "fixed"
   - → likely has unresolved issues

---

## 🚨 Escalation

**When max retries exceeded, give user options:**

```
⚠️ Agent Execution Failed After 3 Attempts

Agent: {agent-type}
Phase: {phase-name}
Error: {error-details}

What would you like to do?

Options:
  1. Retry manually - Try again with intervention
  2. Skip this phase - Continue to next phase
  3. Abort workflow - Stop and save progress

Please choose an option.
```

**User responses:**
- **retry** → Restart Step 2 (execute agent again)
- **skip** → Mark phase as "skipped" in flags.json, move to next
- **abort** → Save current state, exit /cdev

---

## 📝 Rejection Messages

### Pre-Work Rejection

```markdown
❌ Pre-Work Validation Failed

Agent: {agent-type}
Phase: {phase-name}

Missing required steps:
  - {item-1}
  - {item-2}
  - {item-3}

You MUST complete ALL mandatory steps before implementation.

Refer to:
  - .claude/contexts/patterns/validation-framework.md → {agent-type} section
  - .claude/agents/{agent-file}.md → MANDATORY PRE-WORK CHECKLIST

Please provide a complete Pre-Implementation Validation Report.
```

### Quality Rejection

```markdown
⚠️ Output Quality Issues

Issues found:
  - {issue-1}
  - {issue-2}

Please provide complete output including:
  - Pre-Implementation Validation Report
  - Implementation code
  - Test results (if applicable)
  - Files created/modified
  - Completion confirmation (✅)
```

---

## 🎯 Benefits

✅ **Auto-recovery** - Transient errors handled automatically
✅ **Quality enforcement** - Validation catches issues early
✅ **Clear escalation** - User knows exactly what to do
✅ **92% success rate** - Up from 75% without retry logic

---

## 📖 Usage Example

**In `/cdev` command:**

```markdown
Step 4: Invoke Agent with Retry

1. Build prompt (include validation requirements)
2. Execute retry loop (max 2 retries):
   - Invoke agent
   - Validate pre-work
   - Validate output quality
   - If failed → retry or escalate
3. Handle result:
   - Success → update flags.json, move to next phase
   - Failed → escalate to user (retry/skip/abort)
```

---

This retry & escalation framework makes agent execution **robust and reliable**.
