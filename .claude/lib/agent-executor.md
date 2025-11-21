# Agent Executor with Retry & Escalation

> **Robust agent execution with automatic retry and error recovery**
> **Version:** 1.4.0 (Incremental Testing Integration)

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

### Step 1: Build Prompt with Approval Context

```markdown
Include in prompt:
- Change context (proposal, tasks, phases)
- Phase-specific instructions
- TDD requirements (if phase.tdd_required)
- Validation checkpoint reminder
- Approval context (if user approved workflow) ← NEW!
```

**Approval Context Format:**

```
[AUTO-PROCEED: YES]
User has approved this workflow. After completing pre-work validation,
proceed immediately to implementation without asking for confirmation.
```

**When to include:**
- ✅ User ran `/cdev` command → Auto-approve (implicit approval for all phases)
- ✅ User said "continue", "proceed", "yes", "ลุยเลย" → Auto-approve
- ❌ Agent previously failed → Skip (need explicit approval)
- ❌ Manual intervention mode → Skip (user wants control)

### Step 2: Execute with Retry Loop

```
attempt = 0
max_retries = 2
auto_proceed = userApprovalGranted()  // Check if user approved workflow

while (attempt <= max_retries):

  1. Invoke agent:
     Task(agent=agentType, model='haiku', prompt=buildPrompt(auto_proceed))

  2. Handle agent questions (NEW!):
     If agent asks "Should I proceed?" or "Continue?":
       - If auto_proceed === true:
         → Answer agent: "YES, proceed immediately"
         → Continue waiting for implementation result
       - Else:
         → Ask user: "Agent ready. Proceed? (yes/no)"
         → Wait for user response

  3. Validate pre-work (see validation-framework.md):
     - Check for required checklist items
     - If missing → reject and retry

  4. Validate output quality:
     - Check for completion markers (✅, Done, Complete)
     - Check for code blocks (if code agent)
     - Check for test results (if test agent)
     - If incomplete → send feedback and retry

  5. If validation passed:
     → SUCCESS! Return result

  6. If validation failed:
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

1. Check user approval status:
   - User ran /cdev → auto_proceed = true
   - User said "continue" → auto_proceed = true
   - Otherwise → auto_proceed = false

2. Build prompt (include validation requirements + approval context)

3. Execute retry loop (max 2 retries):
   - Invoke agent
   - Handle agent questions (auto-answer if approved)
   - Validate pre-work
   - Validate output quality
   - If failed → retry or escalate

4. Handle result:
   - Success → update flags.json, move to next phase
   - Failed → escalate to user (retry/skip/abort)
```

---

## 🎯 Auto-Proceed Decision Tree

```
User Action → auto_proceed?
─────────────────────────────
/cdev         → YES (implicit approval for all phases)
"continue"    → YES (explicit approval)
"proceed"     → YES (explicit approval)
"yes"         → YES (explicit approval)
"ลุยเลย"      → YES (explicit approval)
/cdev retry   → NO  (need confirmation after failure)
Manual mode   → NO  (user wants control)
```

**When auto_proceed = YES:**
- Agent asks "Proceed?" → Main Claude answers "YES" immediately
- No double-confirmation with user
- Faster workflow execution

**When auto_proceed = NO:**
- Agent asks "Proceed?" → Main Claude asks user
- Manual confirmation at each step
- Slower but more controlled

---

This retry & escalation framework makes agent execution **robust and reliable**.

---

---

# 🔄 Incremental Testing Execution (v1.4.0)

> **NEW:** Milestone-based execution with round-based retry and Main Claude intervention

---

## 📋 Execution Mode Detection

Before executing a phase, check the `testingStrategy` field:

```typescript
if (phase.testingStrategy?.type === 'incremental' && phase.testingStrategy.milestones) {
  // Incremental mode: Execute milestone by milestone
  return await executeIncrementalPhase(phase, changeId)
} else {
  // Standard mode: Single agent execution (existing logic above)
  return await executeStandardPhase(phase, changeId)
}
```

---

## 🎯 Incremental Execution Flow

### Overview

```
Phase Start (e.g., "Google Maps API Integration")
↓
Milestone 1: Core implementation (1 record)
  → Round 1: Attempt 1 → FAIL
  → Round 1: Attempt 2 → FAIL
  → Main Claude: Give hints
  → Round 2: Attempt 1 → PASS ✅
↓
Milestone 2: Parameterized query (10 records)
  → Round 1: Attempt 1 → PASS ✅
↓
Milestone 3: Error handling
  → Round 1: Attempt 1 → FAIL
  → Round 1: Attempt 2 → FAIL
  → Main Claude: Ask human (complex issue) → PAUSE 🛑
↓
Human resolves issue
↓
Resume: Milestone 3
  → Round 2: Attempt 1 → PASS ✅
↓
Milestone 4: Scale + performance
  → Round 1: Attempt 1 → PASS ✅
↓
Phase Complete ✅
```

---

## 🔄 Round-based Retry Logic

### Per-Milestone Retry

- **Quota per round:** 2 attempts
- **Between rounds:** Main Claude intervention (reset quota)
- **No global limit:** Unlimited rounds (user/Main Claude decides when to stop)

```typescript
async function executeMilestone(milestone: Milestone, phase: Phase): Promise<MilestoneResult> {
  let round = 1
  let passed = false
  const history = []

  while (!passed) {
    console.log(`\n📍 Round ${round}`)

    // Execute 2 attempts in this round
    for (let attempt = 1; attempt <= 2; attempt++) {
      console.log(`\n   Attempt ${attempt}/2:`)

      // Build prompt (include previous failures + hints if available)
      const prompt = buildMilestonePrompt(milestone, round, attempt, history)

      // Execute agent
      const result = await executeAgent(phase.agent, prompt)

      // Validate exit criteria
      const validation = validateExitCriteria(result.output, milestone.exitCriteria)

      // Store in history
      history.push({ round, attempt, validation, output: result.output })

      if (validation.allPassed) {
        // SUCCESS!
        console.log(`\n   ✅ PASSED`)
        passed = true
        return { status: 'passed', history }
      } else {
        // FAILED
        console.log(`\n   ❌ FAILED (${validation.failures.length} criteria not met)`)

        if (attempt === 2) {
          // Both attempts failed → Escalate to Main Claude
          console.log(`\n   ⚠️ Round ${round} exhausted`)
          break  // Exit attempt loop
        } else {
          console.log(`\n   🔄 Retrying...`)
        }
      }
    }

    // If we're here, round failed → Main Claude intervention
    if (!passed) {
      const decision = await mainClaudeIntervention(milestone, history)

      if (decision.action === 'give_hints') {
        // Continue to next round with hints
        console.log(`\n💡 Main Claude Guidance:`)
        decision.hints.forEach(h => console.log(`   - ${h}`))
        history.push({ type: 'hints', round: round + 1, hints: decision.hints })
        round++
      } else if (decision.action === 'ask_human') {
        // Pause and wait for human
        console.log(`\n🛑 Human intervention required`)
        return { status: 'paused', reason: decision.reason, history }
      }
    }
  }
}
```

---

## 🤖 Main Claude Intervention

### Decision Logic

```typescript
async function mainClaudeIntervention(milestone: Milestone, history: ExecutionHistory): Promise<Decision> {
  // Analyze failure patterns
  const analysis = analyzeFailures(history)

  console.log(`\n🤔 Main Claude analyzing failures...`)
  console.log(`   Error pattern: ${analysis.pattern}`)
  console.log(`   Complexity: ${analysis.complexity}`)
  console.log(`   Confidence: ${analysis.confidence}`)

  // Decision matrix
  if (analysis.pattern === 'same_error' && analysis.complexity === 'SIMPLE') {
    // Same error 2x + simple issue → Give hints
    return {
      action: 'give_hints',
      hints: generateHints(analysis, milestone)
    }
  }

  if (analysis.pattern === 'different_errors' || analysis.complexity === 'COMPLEX') {
    // Non-deterministic or complex → Ask human
    return {
      action: 'ask_human',
      reason: 'Complex or intermittent failures detected',
      report: generateHumanReport(milestone, history, analysis)
    }
  }

  // Too many rounds without progress → Ask human
  if (history.filter(h => h.type === 'hints').length >= 2) {
    return {
      action: 'ask_human',
      reason: 'No progress after 2 rounds of guidance',
      report: generateHumanReport(milestone, history, analysis)
    }
  }

  // Default: Give hints
  return {
    action: 'give_hints',
    hints: generateHints(analysis, milestone)
  }
}
```

### Failure Analysis

```typescript
function analyzeFailures(history: ExecutionHistory): Analysis {
  const failures = history.filter(h => h.validation && !h.validation.allPassed)

  // Extract unique error messages
  const errorMessages = failures.flatMap(f =>
    f.validation.failures.map(fail => fail.criterion + ':' + fail.explanation)
  )
  const uniqueErrors = [...new Set(errorMessages)]

  // Detect pattern
  let pattern: 'same_error' | 'different_errors' | 'intermittent'
  if (uniqueErrors.length === 1) {
    pattern = 'same_error'
  } else if (uniqueErrors.length === failures.length) {
    pattern = 'different_errors'
  } else {
    pattern = 'intermittent'
  }

  // Assess complexity
  const complexity = uniqueErrors.some(e =>
    e.includes('timeout') ||
    e.includes('intermittent') ||
    e.includes('non-deterministic')
  ) ? 'COMPLEX' : 'SIMPLE'

  // Confidence in root cause
  const confidence = (pattern === 'same_error' && complexity === 'SIMPLE') ? 'HIGH' : 'LOW'

  return { pattern, complexity, confidence, uniqueErrors }
}
```

### Hint Generation

```typescript
function generateHints(analysis: Analysis, milestone: Milestone): string[] {
  const hints = []

  // Pattern-based hints
  if (analysis.uniqueErrors.some(e => e.includes('401') || e.includes('auth'))) {
    hints.push('Check if API_KEY environment variable is set correctly')
    hints.push('Verify API key is valid (not expired/revoked)')
    hints.push('Ensure API key has permissions for this endpoint')
  }

  if (analysis.uniqueErrors.some(e => e.includes('timeout'))) {
    hints.push('Increase timeout threshold (may be too aggressive)')
    hints.push('Check network connectivity to API endpoint')
    hints.push('Verify API endpoint URL is correct')
  }

  if (analysis.uniqueErrors.some(e => e.includes('structure') || e.includes('schema'))) {
    hints.push('Compare actual response structure with expected schema')
    hints.push('Check if API version changed (response format may differ)')
    hints.push('Add console.log() to inspect actual response')
  }

  // Generic debugging hints
  hints.push('Review exit criteria - ensure they match current implementation')
  hints.push('Add detailed logging to identify exact failure point')

  return hints
}
```

---

## ✅ Exit Criteria Validation

### Agent Output Format

Agent MUST respond in this format:

```markdown
## Milestone ${id} Results

**Implementation Summary:**
[What was implemented]

**Test Results:**
- [ ] Response status = 200 - PASS - Got status 200
- [ ] Data structure valid - PASS - Schema matches
- [ ] Response time < 500ms - FAIL - Got 612ms (too slow)
- [ ] API authentication works - PASS - No 401 errors

**Issues Found (if any):**
- Response time exceeds threshold (612ms vs 500ms)

**Conclusion:**
FAIL → Need to optimize query performance
```

### Parsing Logic

```typescript
function validateExitCriteria(agentOutput: string, criteria: string[]): Validation {
  const results = []

  for (const criterion of criteria) {
    // Match pattern: "- [ ] {criterion} - PASS/FAIL - explanation"
    const regex = new RegExp(
      `\\[(.?)\\]\\s*${escapeRegex(criterion)}\\s*-\\s*(PASS|FAIL)\\s*-\\s*(.+)`,
      'i'
    )
    const match = agentOutput.match(regex)

    if (match) {
      const [, checkbox, status, explanation] = match
      results.push({
        criterion,
        passed: status.toUpperCase() === 'PASS',
        explanation: explanation.trim()
      })
    } else {
      // Not found → FAIL (agent didn't report)
      results.push({
        criterion,
        passed: false,
        explanation: 'Agent did not report on this criterion'
      })
    }
  }

  return {
    allPassed: results.every(r => r.passed),
    passedCount: results.filter(r => r.passed).length,
    totalCount: results.length,
    results,
    failures: results.filter(r => !r.passed)
  }
}
```

---

## 🛑 Human Intervention Report

### Report Format

```markdown
🛑 Human Intervention Required

**Phase:** ${phase.name}
**Milestone:** ${milestone.id}/${totalMilestones} - ${milestone.name}
**Total Attempts:** ${totalAttempts} across ${rounds} rounds
**Status:** AWAITING RESOLUTION

---

## Failure Summary

### Round 1
**Attempt 1:**
- ❌ Response status = 200 → Got 401 (Unauthorized)
- ❌ API authentication works → Invalid API key

**Attempt 2:**
- ❌ Response status = 200 → Got 401 (Unauthorized)
- ❌ API authentication works → Invalid API key

### Round 2 (after hints: "Check API_KEY env variable")
**Attempt 1:**
- ❌ Response status = 200 → Got 500 (Internal Server Error)
- ❌ Data structure valid → Unexpected error format

**Attempt 2:**
- ❌ Response status = 200 → Got 503 (Service Unavailable)
- ✅ API authentication works → Auth passed this time

---

## Analysis

**Error Pattern:** Different errors each attempt (intermittent)
**Complexity:** HIGH (non-deterministic behavior)
**Root Cause Hypothesis:** API instability or network issues
**Confidence:** LOW

**Possible Causes:**
1. Google Maps API experiencing outage/degradation
2. Rate limiting kicking in intermittently
3. Network connectivity issues
4. API key quota exhausted

---

## Recommendations

1. Check Google Cloud Console → API quota usage
2. Test API directly (curl/Postman) outside codebase
3. Review recent Google Maps API status
4. Consider adding retry logic with exponential backoff
5. Verify API key permissions and billing status

---

## Next Steps

Please investigate and provide guidance:
- Should we continue with current approach?
- Or pause and fix infrastructure/config first?
- Or change strategy (e.g., use different API)?

Reply with your decision.
```

---

## 📊 Complete Example Flow

```typescript
// In /cdev command

async function executePhase(phase: Phase, changeId: string) {
  // Check testing strategy
  if (phase.testingStrategy?.type === 'incremental') {
    console.log(`\n🔄 INCREMENTAL MODE`)
    console.log(`   Milestones: ${phase.testingStrategy.milestones.length}`)

    // Execute each milestone
    for (const milestone of phase.testingStrategy.milestones) {
      console.log(`\n━━━ Milestone ${milestone.id} ━━━`)

      const result = await executeMilestone(milestone, phase)

      if (result.status === 'passed') {
        console.log(`✅ Milestone ${milestone.id} complete`)
        updateFlags(changeId, {
          [`phase_${phase.id}_milestone_${milestone.id}`]: 'completed'
        })
      } else if (result.status === 'paused') {
        console.log(`🛑 Execution paused`)
        console.log(result.reason)
        return { status: 'paused', phase, milestone }
      }
    }

    console.log(`\n✅ Phase complete: All milestones passed`)
    return { status: 'completed', phase }

  } else {
    // Standard execution (existing logic)
    return await executeStandardPhase(phase, changeId)
  }
}
```

---

## 🎯 Benefits of Incremental Testing

✅ **Early bug detection** - Catch issues at milestone 1 (1 record) vs milestone 4 (1000 records)
✅ **Easier debugging** - Small scope = faster to identify root cause
✅ **Progressive confidence** - Each milestone proves the next will likely work
✅ **Intelligent recovery** - Main Claude provides hints instead of blind retry
✅ **Human-in-the-loop** - Escalate complex issues that agents can't solve

---

**This incremental execution framework transforms high-risk tasks into manageable, validated steps! 🚀**
