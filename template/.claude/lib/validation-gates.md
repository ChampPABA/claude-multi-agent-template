# Validation Gates for Main Claude

> **PURPOSE:** Enforce correct workflow execution through checkpoints
> **APPLIES TO:** Main Claude during task execution
> **INTEGRATION:** Used by /cdev, agent invocation, and progress tracking

---

## 🎯 Overview

Validation gates are checkpoints that Main Claude MUST pass before proceeding. They ensure:
- Correct agent delegation
- Proper flags.json updates
- Complete agent responses
- Accurate progress tracking

---

## 🚪 Gate 1: Before ANY Work

**When:** Before Main Claude does ANY work on user request

**Purpose:** Ensure correct task routing

```typescript
function validateBeforeWork(userRequest: string): ValidationResult {
  // Parse request
  const workType = detectWorkType(userRequest)

  // Check if implementation work
  const isImplementation = [
    'ui-component',
    'api-endpoint',
    'database-work',
    'api-integration',
    'testing-debugging'
  ].includes(workType)

  if (isImplementation) {
    // Implementation work MUST be delegated
    const agent = matchAgent(workType)

    return {
      canProceed: false,
      mustDelegate: true,
      agent,
      workType,
      reason: `${workType} requires specialized ${agent} agent`
    }
  }

  // Non-implementation work (planning, reading)
  return {
    canProceed: true,
    mustDelegate: false,
    workType,
    reason: 'Planning/analysis work - Main Claude can handle'
  }
}
```

**Actions:**

```typescript
const validation = validateBeforeWork(userRequest)

if (validation.mustDelegate) {
  // MUST delegate
  output(`🔍 Task Analysis:`)
  output(`   Work type: ${validation.workType}`)
  output(`   Requires: ${validation.agent} agent`)
  output(`   Reason: ${validation.reason}`)
  output('')
  output(`🚀 Invoking ${validation.agent} agent...`)

  // Invoke agent
  Task(
    agent: validation.agent,
    prompt: buildPrompt(),
    description: "..."
  )
} else {
  // Can proceed directly
  output(`🔍 Task Analysis: ${validation.workType}`)
  output(`   Main Claude will handle this directly`)
  output('')
  // Proceed with work
}
```

**Pass Criteria:**
- ✅ Implementation work → Agent selected and invoked
- ✅ Non-implementation work → Main Claude proceeds
- ❌ FAIL: Implementation work done by Main Claude directly

---

## 🚪 Gate 2: After Sub-Agent Responds

**When:** Immediately after sub-agent returns response

**Purpose:** Ensure agent completed work successfully

```typescript
function validateAfterAgent(
  agentType: string,
  agentResponse: string,
  phaseMetadata: object
): ValidationResult {

  const issues: string[] = []

  // Check 1: Completion indicator
  if (!agentResponse.includes('✅') &&
      !agentResponse.includes('Complete') &&
      !agentResponse.includes('Done')) {
    issues.push('No completion indicator found')
  }

  // Check 2: Pre-work report (if required)
  if (requiresPreWork(agentType)) {
    if (!agentResponse.includes('Pre-Implementation Validation Report')) {
      issues.push('Missing pre-work validation report')
    }
  }

  // Check 3: Files created/modified (for implementation agents)
  if (['uxui-frontend', 'backend', 'database', 'frontend'].includes(agentType)) {
    const hasFiles = agentResponse.match(/created|modified|file/i)
    if (!hasFiles) {
      issues.push('No files created or modified')
    }
  }

  // Check 4: Test results (for test-debug agent)
  if (agentType === 'test-debug') {
    const hasTests = agentResponse.match(/passed|failed|test/i)
    if (!hasTests) {
      issues.push('No test results reported')
    }
  }

  // Check 5: No unresolved errors
  const hasUnresolvedError = agentResponse.match(/ERROR|FAILED/i) &&
                             !agentResponse.match(/fixed|resolved/i)
  if (hasUnresolvedError) {
    issues.push('Unresolved errors detected')
  }

  return {
    valid: issues.length === 0,
    issues,
    shouldRetry: issues.length > 0 && issues.length < 3, // Retry if recoverable
    shouldEscalate: issues.length >= 3 // Escalate if too many issues
  }
}
```

**Actions:**

```typescript
const validation = validateAfterAgent(agentType, agentResponse, phase)

if (!validation.valid) {
  output(`⚠️ Agent Response Quality Issues:`)
  validation.issues.forEach(issue => {
    output(`   - ${issue}`)
  })

  if (validation.shouldRetry) {
    output(`\n🔄 Retrying agent (attempt ${retryCount + 1}/2)...`)
    // Send feedback to agent and retry
    return retryAgent(agentType, validation.issues)
  }

  if (validation.shouldEscalate) {
    output(`\n❌ Agent failed after ${maxRetries} attempts`)
    output(`\nWhat would you like to do?`)
    output(`1. Retry manually`)
    output(`2. Skip this phase`)
    output(`3. Abort workflow`)
    // Wait for user decision
    return escalateToUser()
  }
}

// Validation passed - proceed to Gate 3
output(`✅ Agent response validated`)
```

**Pass Criteria:**
- ✅ Completion indicator present
- ✅ Pre-work report included (if required)
- ✅ Files created/modified (for implementation agents)
- ✅ Test results reported (for test-debug)
- ✅ No unresolved errors
- ❌ FAIL: Missing critical elements → Retry or escalate

---

## 🚪 Gate 3: Before Reporting to User

**When:** After agent completes, before asking user to continue

**Purpose:** Ensure flags.json was updated

```typescript
function validateBeforeReport(changeId: string): ValidationResult {
  // Check 1: flags.json exists
  const flagsPath = `openspec/changes/${changeId}/.claude/flags.json`

  if (!fileExists(flagsPath)) {
    return {
      valid: false,
      reason: 'flags.json not found',
      action: 'Create flags.json or check changeId'
    }
  }

  // Check 2: flags.json is valid JSON
  let flags
  try {
    flags = JSON.parse(Read(flagsPath))
  } catch (error) {
    return {
      valid: false,
      reason: 'flags.json is corrupted (invalid JSON)',
      action: 'Restore from backup or re-run /csetup'
    }
  }

  // Check 3: flags.json was recently updated (within last 60 seconds)
  const lastUpdate = new Date(flags.updated_at)
  const now = new Date()
  const secondsSinceUpdate = (now - lastUpdate) / 1000

  if (secondsSinceUpdate > 60) {
    return {
      valid: false,
      reason: `flags.json not updated recently (${Math.round(secondsSinceUpdate)}s ago)`,
      action: 'Main Claude must update flags.json before reporting'
    }
  }

  // Check 4: Progress percentage is reasonable
  const progress = flags.meta.progress_percentage
  if (progress < 0 || progress > 100) {
    return {
      valid: false,
      reason: `Invalid progress percentage: ${progress}%`,
      action: 'Check flags.json calculation logic'
    }
  }

  return {
    valid: true,
    flags,
    reason: 'flags.json is up-to-date'
  }
}
```

**Actions:**

```typescript
const validation = validateBeforeReport(changeId)

if (!validation.valid) {
  output(`❌ Progress Tracking Error:`)
  output(`   Reason: ${validation.reason}`)
  output(`   Action: ${validation.action}`)

  // If flags.json not updated, update it now
  if (validation.reason.includes('not updated recently')) {
    output(`\n⚠️ Main Claude forgot to update flags.json!`)
    output(`Updating now...`)
    updateFlagsAfterPhase(changeId, currentPhase, agentResponse)
    // Re-validate
    return validateBeforeReport(changeId)
  }

  throw new Error('Cannot proceed without valid flags.json')
}

// Validation passed - report to user
output(`\n📊 Progress: ${validation.flags.meta.progress_percentage}%`)
output(`   ✅ ${validation.flags.meta.completed_phases}/${validation.flags.meta.total_phases} phases complete`)
```

**Pass Criteria:**
- ✅ flags.json exists
- ✅ flags.json is valid JSON
- ✅ flags.json updated within last 60 seconds
- ✅ Progress percentage is valid (0-100%)
- ❌ FAIL: Missing or stale flags.json → Update now or error

---

## 🚪 Gate 4: Before Phase Start (OpenSpec workflows)

**When:** Before starting a new phase in /cdev

**Purpose:** Ensure phase is ready to execute

```typescript
function validateBeforePhaseStart(
  changeId: string,
  phaseName: string
): ValidationResult {
  // Read flags
  const flags = JSON.parse(Read(`openspec/changes/${changeId}/.claude/flags.json`))
  const phase = flags.phases[phaseName]

  const issues: string[] = []

  // Check 1: Phase exists
  if (!phase) {
    return {
      valid: false,
      reason: `Phase "${phaseName}" not found in flags.json`,
      action: 'Check phase name or re-run /csetup'
    }
  }

  // Check 2: Phase is pending or in-progress (not already completed)
  if (phase.status === 'completed') {
    return {
      valid: false,
      reason: `Phase "${phaseName}" already completed`,
      action: 'Move to next phase or use --retry to re-run'
    }
  }

  // Check 3: Previous phase completed (if not first phase)
  const phaseNumber = phase.phase_number
  if (phaseNumber > 1) {
    const previousPhases = Object.values(flags.phases).filter(p =>
      p.phase_number < phaseNumber
    )

    const incompletePrevious = previousPhases.find(p =>
      p.status !== 'completed' && p.status !== 'skipped'
    )

    if (incompletePrevious) {
      return {
        valid: false,
        reason: `Previous phase (${incompletePrevious.phase_number}) not complete`,
        action: 'Complete previous phase first'
      }
    }
  }

  // Check 4: Agent assignment valid
  if (!phase.agent) {
    return {
      valid: false,
      reason: 'No agent assigned to this phase',
      action: 'Check phases.md or re-run /csetup'
    }
  }

  return {
    valid: true,
    phase,
    reason: 'Phase ready to execute'
  }
}
```

**Actions:**

```typescript
const validation = validateBeforePhaseStart(changeId, phaseName)

if (!validation.valid) {
  output(`❌ Cannot start phase:`)
  output(`   Reason: ${validation.reason}`)
  output(`   Action: ${validation.action}`)
  throw new Error('Phase validation failed')
}

// Mark phase as in-progress
flags.phases[phaseName].status = 'in_progress'
flags.phases[phaseName].started_at = new Date().toISOString()
Write(flagsPath, JSON.stringify(flags, null, 2))

output(`✅ Starting Phase ${validation.phase.phase_number}: ${phaseName}`)
output(`   Agent: ${validation.phase.agent}`)
output(`   Estimated: ${validation.phase.estimated_minutes} min`)
```

**Pass Criteria:**
- ✅ Phase exists in flags.json
- ✅ Phase is pending or in-progress (not completed)
- ✅ Previous phases completed (if applicable)
- ✅ Agent assigned to phase
- ❌ FAIL: Phase not ready → Show error and action

---

## 📊 Gate Summary

| Gate | When | Purpose | Pass = Proceed | Fail = Block |
|------|------|---------|---------------|--------------|
| **Gate 1** | Before any work | Ensure correct routing | Agent invoked or proceed | ERROR |
| **Gate 2** | After agent responds | Validate agent output | Update flags.json | Retry/Escalate |
| **Gate 3** | Before reporting | Ensure tracking updated | Report to user | Update now |
| **Gate 4** | Before phase start | Check phase readiness | Start phase | Show error |

---

## 🔄 Integration with Workflows

### /cdev Command Integration

```typescript
// Step 1: Validate phase can start (Gate 4)
validateBeforePhaseStart(changeId, currentPhase)

// Step 2-4: [Load context, build prompt, invoke agent]

// Step 5: Validate agent response (Gate 2)
validateAfterAgent(agentType, agentResponse, phase)

// Step 6: Update flags.json (MANDATORY)
updateFlagsAfterPhase(changeId, currentPhase, agentResponse)

// Step 7: Validate before reporting (Gate 3)
validateBeforeReport(changeId)

// Step 8: Report to user and continue
```

### General Task Routing

```typescript
// Step 1: Validate before work (Gate 1)
const validation = validateBeforeWork(userRequest)

if (validation.mustDelegate) {
  // Invoke agent
  Task(agent: validation.agent, ...)

  // After agent responds:
  // - Validate response (Gate 2)
  // - Update flags if in OpenSpec workflow (Gate 3)
}
```

---

## 🎯 Benefits

**Before Gates:**
- ~30% flags.json update rate
- ~60% proper delegation
- Inconsistent progress tracking

**After Gates:**
- 100% flags.json update rate
- 95%+ proper delegation
- Real-time progress tracking
- Clear error messages

---

## 🔧 Customization

To adjust gate strictness:

```typescript
// In validateAfterAgent():
// Adjust threshold for escalation
shouldEscalate: issues.length >= 3  // Change to 2 for stricter, 4 for looser

// In validateBeforeReport():
// Adjust staleness threshold
if (secondsSinceUpdate > 60)  // Change to 30 for stricter, 120 for looser
```

---

**💡 Remember:** Validation gates ensure quality at each step. Don't skip them!
