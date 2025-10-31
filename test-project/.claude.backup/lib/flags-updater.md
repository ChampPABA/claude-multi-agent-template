# Flags.json Update Protocol

> **WHO:** Main Claude (orchestrator)
> **WHEN:** Immediately after sub-agent completes phase
> **HOW:** Follow this exact flow
> **PURPOSE:** Ensure real-time progress tracking for users

---

## 🎯 Core Principle

**Main Claude is ALWAYS responsible for updating flags.json**

- ❌ NOT sub-agents (they don't have direct access)
- ❌ NOT user (they shouldn't have to)
- ✅ Main Claude after EVERY phase completion

---

## 🔄 Update Flow

```
Step 1: Sub-agent responds with completion message
   ↓
Step 2: Main Claude validates response quality
   ↓
Step 3: Main Claude updates flags.json (MANDATORY - THIS STEP!)
   ↓
Step 4: Main Claude reports progress to user
   ↓
Step 5: Main Claude asks to continue (or auto-continue)
```

**⚠️ CRITICAL:** Step 3 CANNOT be skipped. Ever.

---

## 📝 Update Implementation

### Function Specification

```typescript
/**
 * Updates flags.json after a phase completes
 *
 * WHEN TO CALL: Immediately after sub-agent responds successfully
 * WHERE: In /cdev command, Step 5 (Post-Execution)
 */
function updateFlagsAfterPhase(
  changeId: string,
  phaseName: string,
  agentResponse: string
): void {

  // 1. Read current flags
  const flagsPath = `openspec/changes/${changeId}/.claude/flags.json`

  if (!fileExists(flagsPath)) {
    throw new Error(`flags.json not found at ${flagsPath}`)
  }

  const flags = JSON.parse(Read(flagsPath))

  // 2. Extract information from agent response
  const filesCreated = extractFilesCreated(agentResponse)
  const filesModified = extractFilesModified(agentResponse)
  const tasksCompleted = extractTaskIds(agentResponse)
  const notes = extractSummary(agentResponse)

  // Calculate duration
  const startedAt = flags.phases[phaseName].started_at
  const completedAt = new Date().toISOString()
  const actualMinutes = calculateMinutes(startedAt, completedAt)

  // 3. Update phase status
  flags.phases[phaseName] = {
    ...flags.phases[phaseName],
    status: 'completed',
    completed_at: completedAt,
    actual_minutes: actualMinutes,
    files_created: filesCreated,
    files_modified: filesModified,
    tasks_completed: tasksCompleted,
    notes: notes.substring(0, 200) // Limit to 200 chars
  }

  // 4. Update meta statistics
  flags.meta.completed_phases++
  flags.meta.pending_phases--
  flags.meta.in_progress_phases = 0 // Reset in-progress
  flags.meta.progress_percentage = Math.round(
    (flags.meta.completed_phases / flags.meta.total_phases) * 100
  )
  flags.meta.total_actual_minutes += actualMinutes
  flags.meta.time_remaining_estimate = calculateTimeRemaining(flags)

  // Update file counts
  flags.meta.files_created += filesCreated.length
  flags.meta.files_modified += filesModified.length

  // 5. Move to next phase
  const nextPhase = getNextPhaseName(flags)
  flags.current_phase = nextPhase

  if (nextPhase && flags.phases[nextPhase]) {
    flags.phases[nextPhase].status = 'pending'
  }

  // 6. Check if all complete
  if (flags.meta.completed_phases === flags.meta.total_phases) {
    flags.ready_to_archive = true
  }

  // 7. Update timestamp
  flags.updated_at = new Date().toISOString()

  // 8. Add to history
  flags.history.push({
    timestamp: completedAt,
    action: 'phase_completed',
    phase: phaseName,
    duration_minutes: actualMinutes
  })

  // 9. Write back to file
  Write(flagsPath, JSON.stringify(flags, null, 2))

  // 10. Report success (to terminal, visible to user)
  output(`\n📊 Progress Updated:`)
  output(`   ✅ Phase "${phaseName}" marked complete`)
  output(`   ⏱️  Duration: ${actualMinutes} min (estimated: ${flags.phases[phaseName].estimated_minutes} min)`)
  output(`   📁 Files: ${filesCreated.length} created, ${filesModified.length} modified`)
  output(`   📈 Progress: ${flags.meta.progress_percentage}% (${flags.meta.completed_phases}/${flags.meta.total_phases})`)
}
```

---

## 🔍 Helper Functions

### extractFilesCreated()

```typescript
function extractFilesCreated(response: string): string[] {
  const patterns = [
    /(?:Created|created|Created:)\s*(.+)/gi,
    /📁\s*(?:Created|created):\s*(.+)/gi,
    /✅\s*Created\s+file:\s*(.+)/gi,
    /new file:\s*(.+)/gi
  ]

  const files: string[] = []

  for (const pattern of patterns) {
    const matches = response.matchAll(pattern)
    for (const match of matches) {
      // Extract file paths (one per line or comma-separated)
      const paths = match[1].split(/[,\n]/).map(p => p.trim())
      files.push(...paths.filter(p => p.length > 0))
    }
  }

  // Remove duplicates
  return [...new Set(files)]
}
```

### extractFilesModified()

```typescript
function extractFilesModified(response: string): string[] {
  const patterns = [
    /(?:Modified|modified|Updated|updated):\s*(.+)/gi,
    /📝\s*(?:Modified|updated):\s*(.+)/gi,
    /✏️\s*Updated\s+file:\s*(.+)/gi
  ]

  const files: string[] = []

  for (const pattern of patterns) {
    const matches = response.matchAll(pattern)
    for (const match of matches) {
      const paths = match[1].split(/[,\n]/).map(p => p.trim())
      files.push(...paths.filter(p => p.length > 0))
    }
  }

  return [...new Set(files)]
}
```

### extractTaskIds()

```typescript
function extractTaskIds(response: string): string[] {
  // Look for task IDs like "1.1", "1.2", "2.1"
  const pattern = /(?:task|Task)\s*(?:ID|id)?:?\s*([\d\.]+)/gi
  const matches = response.matchAll(pattern)

  const taskIds: string[] = []
  for (const match of matches) {
    taskIds.push(match[1])
  }

  return taskIds
}
```

### extractSummary()

```typescript
function extractSummary(response: string): string {
  // Look for summary section
  const summaryPatterns = [
    /(?:Summary|SUMMARY):\s*(.+?)(?:\n\n|\n#|$)/si,
    /(?:Notes|NOTES):\s*(.+?)(?:\n\n|\n#|$)/si,
    /(?:Completed|COMPLETED):\s*(.+?)(?:\n\n|\n#|$)/si
  ]

  for (const pattern of summaryPatterns) {
    const match = response.match(pattern)
    if (match) {
      return match[1].trim()
    }
  }

  // Fallback: First 200 chars of response
  return response.substring(0, 200).trim()
}
```

### calculateMinutes()

```typescript
function calculateMinutes(startISO: string, endISO: string): number {
  const start = new Date(startISO)
  const end = new Date(endISO)
  const diffMs = end - start
  return Math.round(diffMs / 1000 / 60) // Convert to minutes
}
```

### getNextPhaseName()

```typescript
function getNextPhaseName(flags: Flags): string | null {
  // Get all phase names in order
  const phaseNames = Object.keys(flags.phases).sort((a, b) => {
    return flags.phases[a].phase_number - flags.phases[b].phase_number
  })

  // Find first pending phase
  for (const name of phaseNames) {
    if (flags.phases[name].status === 'pending') {
      return name
    }
  }

  // All phases complete
  return null
}
```

### calculateTimeRemaining()

```typescript
function calculateTimeRemaining(flags: Flags): number {
  let remaining = 0

  for (const [name, phase] of Object.entries(flags.phases)) {
    if (phase.status === 'pending' || phase.status === 'in_progress') {
      remaining += phase.estimated_minutes || 0
    }
  }

  return remaining
}
```

---

## ⚠️ CRITICAL RULES

### Rule 1: NEVER Skip This Step

```markdown
❌ WRONG:
Sub-agent completes → Main Claude asks user to continue
(flags.json not updated)

✅ CORRECT:
Sub-agent completes → Main Claude updates flags.json → Main Claude reports progress → Main Claude asks user to continue
```

### Rule 2: Update IMMEDIATELY After Sub-Agent Responds

```markdown
Don't wait for:
- ❌ User confirmation
- ❌ Next phase to start
- ❌ Batch multiple updates

Update:
- ✅ As soon as sub-agent returns success
- ✅ Before asking user anything
- ✅ After EACH individual phase
```

### Rule 3: Validate Before Update

```typescript
// Check 1: flags.json exists
if (!fileExists(flagsPath)) {
  output(`❌ Error: flags.json not found`)
  output(`Run: /csetup ${changeId}`)
  return
}

// Check 2: Phase exists in flags
if (!flags.phases[phaseName]) {
  output(`❌ Error: Phase "${phaseName}" not found in flags.json`)
  return
}

// Check 3: Sub-agent actually completed work
if (!agentResponse.includes('✅') && !agentResponse.includes('Complete')) {
  output(`⚠️ Warning: Agent response does not confirm completion`)
  output(`Proceed with caution`)
}
```

### Rule 4: Always Report to User

```markdown
After updating flags.json, ALWAYS show:

📊 Progress Updated:
   ✅ Phase "frontend-mockup" marked complete
   ⏱️  Duration: 95 min (estimated: 90 min)
   📁 Files: 4 created, 0 modified
   📈 Progress: 9% (1/11)
```

---

## 🐛 Error Handling

### Scenario 1: flags.json Not Found

```typescript
if (!fileExists(flagsPath)) {
  output(`❌ Error: flags.json not found`)
  output(`Expected at: ${flagsPath}`)
  output(`\nPlease run: /csetup ${changeId}`)
  throw new Error('flags.json not found')
}
```

### Scenario 2: Invalid JSON

```typescript
try {
  const flags = JSON.parse(Read(flagsPath))
} catch (error) {
  output(`❌ Error: flags.json is corrupted (invalid JSON)`)
  output(`\nOptions:`)
  output(`1. Restore from backup`)
  output(`2. Re-run: /csetup ${changeId} (will overwrite)`)
  throw new Error('Invalid flags.json')
}
```

### Scenario 3: Phase Not Found

```typescript
if (!flags.phases[phaseName]) {
  output(`❌ Error: Phase "${phaseName}" not found in flags.json`)
  output(`\nAvailable phases:`)
  Object.keys(flags.phases).forEach(name => {
    output(`  - ${name}`)
  })
  throw new Error('Phase not found')
}
```

### Scenario 4: Cannot Extract Files

```typescript
const filesCreated = extractFilesCreated(agentResponse)

if (filesCreated.length === 0) {
  output(`⚠️ Warning: Could not extract created files from agent response`)
  output(`\nPlease manually specify files (comma-separated, or press Enter to skip):`)
  const userInput = await getUserInput()
  if (userInput.trim()) {
    filesCreated = userInput.split(',').map(f => f.trim())
  }
}
```

---

## 📊 Success Indicators

After implementing this protocol, you should see:

1. **100% Update Rate**
   - Every phase completion → flags.json updated
   - No manual intervention needed

2. **Real-Time Progress**
   - User sees progress after every phase
   - `/cstatus` shows accurate data

3. **Accurate Time Tracking**
   - Actual vs estimated time recorded
   - Efficiency metrics available

4. **Complete Audit Trail**
   - History log in flags.json
   - Can reconstruct entire workflow

---

## 🔗 Integration Points

**This protocol is used by:**
- `/cdev` command (Step 5: Post-Execution)
- `/cstatus` command (reads updated flags)
- `/cview` command (reads updated flags)

**This protocol depends on:**
- `flags-template.json` (initial structure)
- `/csetup` command (creates flags.json)
- Sub-agents (provide completion responses)

---

## 🎯 Quick Reference

**Main Claude, after sub-agent completes:**

```typescript
// 1. Validate response
if (!validateAgentResponse(agentResponse)) {
  // Handle retry or escalation
}

// 2. Update flags.json (MANDATORY)
updateFlagsAfterPhase(changeId, currentPhase, agentResponse)

// 3. Read updated flags
const flags = JSON.parse(Read(`openspec/changes/${changeId}/.claude/flags.json`))

// 4. Report to user
output(`\n📊 Progress: ${flags.meta.progress_percentage}%`)

// 5. Ask to continue
if (flags.ready_to_archive) {
  output('✅ All phases complete!')
} else {
  output(`\n📍 Next: Phase ${flags.phases[flags.current_phase].phase_number}`)
  output('Continue? (yes/no)')
}
```

---

**💡 Remember:** Main Claude updates flags.json. Always. No exceptions.
