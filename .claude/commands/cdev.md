---
name: Change Develop
description: Start/continue multi-agent development for a change
category: Multi-Agent
tags: [dev, orchestration, agents]
---

## Usage

```bash
/cdev {change-id}
/cdev {change-id} --continue
/cdev {change-id} --retry
```

## What It Does

Orchestrates agent execution for change development:
1. Read current phase from flags.json
2. Get agent assignment from phases.md
3. Invoke appropriate agent(s)
4. Update progress
5. Continue or pause for user action

## Steps

### Step 1: Load Change Context

```bash
# Check prerequisites
ls openspec/changes/{change-id}/.claude/flags.json
ls openspec/changes/{change-id}/.claude/phases.md
```

If not found:
```
❌ Change not set up
Run: /csetup {change-id}
```

### Step 2: Read Current Phase

```typescript
const flags = JSON.parse(Read('openspec/changes/{change-id}/.claude/flags.json'))
const currentPhase = flags.current_phase
const phaseData = flags.phases[currentPhase]

if (phaseData.status === 'completed') {
  // Move to next phase
  currentPhase = getNextPhase(flags)
}
```

### Step 3: Check Phase Type

```typescript
const agent = phaseData.agent

if (agent === 'user') {
  // Manual action required
  output(`🛑 Phase ${phaseData.phase_number} requires manual action`)
  output(`Instructions: ${getInstructions(currentPhase)}`)
  output(`When done: /cdev ${changeId} --continue`)
  return
}

if (agent.includes('+')) {
  // Multiple agents (parallel)
  agents = agent.split('+').map(a => a.trim())
  invokeMultipleAgents(agents, changeId, currentPhase)
} else {
  // Single agent
  invokeAgent(agent, changeId, currentPhase)
}
```

### Step 4: Invoke Agent with Retry & Validation

**This step now uses the enhanced agent-executor framework!**

See: `.claude/lib/agent-executor.md` for full implementation

**High-Level Flow:**

1. **Calculate Context Size** (for model selection)
2. **Select Model** (haiku vs sonnet based on complexity)
3. **Execute Agent with Retry** (automatic retry on failure)
4. **Validate Pre-Work** (enforce mandatory checklist)
5. **Validate Output Quality** (check completeness)
6. **Handle Errors** (retry or escalate)

**Implementation:**

```typescript
// Step 4: Invoke Agent with Retry & Validation

// 4.1: Build agent prompt
const prompt = buildAgentPrompt(phase, changeContext)

// 4.2: Execute agent with retry & validation
output(`\n🚀 Invoking ${phase.agent} agent (model: haiku)...`)

const result = await executeAgentWithRetry(
  phase.agent,
  phase,
  changeContext,
  {
    max_retries: 2,
    retry_delay: 5000,
    timeout: 600000,  // 10 minutes
    validate_output: true
  }
)

// 4.3: Handle result
if (result.success) {
  output(`\n✅ Phase ${phase.phase_number} completed successfully!`)
  output(`⏱️ Execution time: ${(result.execution_time / 1000).toFixed(1)}s`)
  output(`🔄 Retries used: ${result.retries_used}`)
  output(`✅ Validation: ${result.validation_passed ? 'PASSED' : 'SKIPPED'}`)

  // Continue to Step 5: Post-Execution
} else {
  output(`\n❌ Phase ${phase.phase_number} failed`)
  output(`Error: ${result.error}`)
  output(`Retries used: ${result.retries_used}`)

  // Escalate to user
  const action = await escalateToUser(phase.agent, phase, result)

  switch (action) {
    case 'retry':
      output(`Retrying Phase ${phase.phase_number}...`)
      // Restart Step 4
      return executePhaseAgain(changeId, phase)

    case 'skip':
      output(`⚠️ Skipping Phase ${phase.phase_number}`)
      await markPhaseAsSkipped(changeId, phase, result.error)
      // Continue to next phase
      break

    case 'abort':
      output(`🛑 Workflow aborted`)
      output(`Resume with: /cdev ${changeId}`)
      return
  }
}
```

**Helper Functions Used:**

1. **buildAgentPrompt()**: See `.claude/lib/agent-executor.md`
2. **executeAgentWithRetry()**: See `.claude/lib/agent-executor.md`
3. **escalateToUser()**: See `.claude/lib/agent-executor.md`

**Model Strategy:**
- All agents use `model: haiku` (fixed)
- Haiku performs excellently with detailed context
- 12-20x cheaper than sonnet
- Quality maintained through comprehensive validation framework

---

### Step 4.5: Validation Details

**Validation is handled automatically inside executeAgentWithRetry():**

See `.claude/lib/agent-executor.md` for complete validation flow including:
- Pre-work validation (checks required checklist items)
- Output quality checks (completion markers, code blocks, test results)
- Retry logic (max 2 retries with feedback)
- Escalation (user options on failure)

**Agent-specific validation requirements:**

See `.claude/contexts/patterns/validation-framework.md` for complete checklist per agent:
- uxui-frontend: Design Foundation, Box Thinking, Component Search, Design Tokens
- backend: Patterns Loaded, Endpoint Search, TDD Workflow (if required), Error Handling
- database: Schema Analysis, Migration Strategy, Existing Schemas Search
- frontend: API Contract Verification, State Management, Error Handling
- test-debug: Test Infrastructure, Coverage Targets, Test Plan
- integration: Contract Collection, Schema Validation, Data Flow Analysis

---

### Step 5: Post-Execution

After agent completes:

1. **Read updated flags.json**
2. **Check next phase:**

```typescript
if (flags.ready_to_archive) {
  output('✅ All phases complete! Ready to archive.')
} else if (nextPhaseRequiresUser) {
  output('🛑 Next phase requires your action')
  output(`When done: /cdev ${changeId} --continue`)
} else {
  output(`📍 Next: Phase ${nextNumber}: ${nextName}`)
  output('Continue? (yes/no)')
}
```

---

## Example Session

```bash
$ /cdev CHANGE-003

✅ Reading change context...
📁 Change: CHANGE-003 Create Landing Page
📊 Template: frontend-only (11 phases)
📍 Current: Phase 1/11 Frontend Mockup

Invoking uxui-frontend agent...

[Agent executes Phase 1...]

✅ Phase 1 completed! (95 minutes)

📁 Files created:
   - src/app/page.tsx
   - src/components/landing/hero-section.tsx
   - src/components/landing/features-section.tsx
   - src/components/landing/cta-section.tsx

📍 Next: Phase 2 Accessibility Test (test-debug)

Continue? (yes/no)
> yes

[Continues...]

🛑 Phase 3 requires manual testing.
Test visual consistency using Chrome DevTools MCP.
When done: /cdev CHANGE-003 --continue

$ [User tests]

$ /cdev CHANGE-003 --continue

Updating flags → Phase 3 marked completed
📍 Next: Phase 4 Business Logic Validation
Continue? (yes/no)
> yes

[Continues until complete...]

✅ All phases completed! (11/11)
Ready to archive!
```

---

## Flags

- `--continue`: Skip to next phase (after manual action)
- `--retry`: Retry current phase if blocked

---

## Error Handling

**If phase blocked:**
```
❌ Phase blocked: {error}
Suggestions: {suggestions}
Retry: /cdev {change-id} --retry
```
