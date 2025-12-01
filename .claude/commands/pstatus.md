---
name: Project Status
description: Update PROJECT_STATUS.yml for cross-session context
category: Multi-Agent
tags: [status, context, cross-session]
---

## Usage

```bash
/pstatus
/pstatus quick     # Quick update (outdated sections only)
/pstatus full      # Full review (all sections)
/pstatus blockers  # Update blockers section only
```

## What It Does

Interactive update of `PROJECT_STATUS.yml` - the cross-session context file that helps Claude understand project state in new sessions.

**WHY this exists:** New Claude sessions lose context about infrastructure, blockers, and priorities. This command helps maintain that context.

---

## Step 1: Check File Exists

```typescript
const statusPath = 'PROJECT_STATUS.yml'

if (!fileExists(statusPath)) {
  output(`
📊 PROJECT_STATUS.yml not found

This file provides cross-session context for Claude.
It helps new sessions understand:
- Infrastructure state (DB, API, tunnels)
- Blockers (waiting for domain, API keys)
- Completed work & next priorities

Create it now? (yes/no)
  `)

  const answer = await askUser()
  if (answer === 'yes') {
    // Copy from template
    copy('.claude/templates/PROJECT_STATUS.template.yml', statusPath)
    output('✅ Created PROJECT_STATUS.yml - please fill in your project details')
    return
  } else {
    return output('Skipped. Run /pstatus again when ready.')
  }
}
```

---

## Step 2: Read Current Status

```typescript
const status = parseYaml(Read(statusPath))
const lastUpdated = new Date(status.last_updated)
const daysSinceUpdate = Math.floor((Date.now() - lastUpdated) / (1000 * 60 * 60 * 24))

output(`
📊 PROJECT_STATUS.yml

Last updated: ${status.last_updated} (${daysSinceUpdate} days ago)
Current focus: ${status.current_focus?.description || 'Not set'}
Active change: ${status.current_focus?.active_change || 'None'}
Blockers: ${status.blockers?.length || 0}
Completed changes: ${status.completed_changes?.length || 0}
`)
```

---

## Step 3: Select Update Mode

```typescript
// If mode provided via argument, use it
// Otherwise, ask user

const mode = args[0] || await askUserQuestion({
  questions: [{
    question: 'What would you like to update?',
    header: 'Mode',
    options: [
      { label: 'Quick Update', description: 'Only sections that seem outdated' },
      { label: 'Full Review', description: 'Walk through all sections' },
      { label: 'Specific Section', description: 'Update one section only' }
    ],
    multiSelect: false
  }]
})
```

---

## Step 4: Section-by-Section Updates

### 4.1 Update `last_updated`

```typescript
// Always update timestamp
status.last_updated = new Date().toISOString().split('T')[0]
```

### 4.2 Update `current_focus`

```typescript
output(`
📍 Current Focus
   Description: "${status.current_focus?.description || 'Not set'}"
   Active change: ${status.current_focus?.active_change || 'None'}
`)

const updateFocus = await askUserQuestion({
  questions: [{
    question: 'Update current focus?',
    header: 'Focus',
    options: [
      { label: 'Keep as is', description: 'No changes needed' },
      { label: 'Update description', description: 'Change what you are working on' },
      { label: 'Set active change', description: 'Link to OpenSpec change' },
      { label: 'Clear active change', description: 'Not working on a change' }
    ],
    multiSelect: false
  }]
})

// Handle user selection...
```

### 4.3 Update `completed_changes`

```typescript
output(`
✅ Completed Changes (${status.completed_changes?.length || 0})
${status.completed_changes?.map(c => `   - ${c.id} (${c.date}): ${c.summary}`).join('\n') || '   (none)'}
`)

// Auto-detect archived changes not in list
const archivedChanges = listFiles('openspec/changes/archive/')
const missingChanges = archivedChanges.filter(dir => {
  const id = path.basename(dir)
  return !status.completed_changes?.some(c => c.id === id)
})

if (missingChanges.length > 0) {
  output(`
📦 Found ${missingChanges.length} archived change(s) not in completed_changes:
${missingChanges.map(c => `   - ${path.basename(c)}`).join('\n')}

Add them? (yes/no)
  `)

  const addMissing = await askUser()
  if (addMissing) {
    for (const changePath of missingChanges) {
      const id = path.basename(changePath)
      // Try to read proposal.md for summary
      const proposalPath = `${changePath}/proposal.md`
      let summary = 'No summary available'
      if (fileExists(proposalPath)) {
        const proposal = Read(proposalPath)
        // Extract first sentence or title
        summary = extractSummary(proposal)
      }

      status.completed_changes = status.completed_changes || []
      status.completed_changes.push({
        id,
        date: new Date().toISOString().split('T')[0],
        summary
      })
      output(`   ✅ Added: ${id}`)
    }
  }
}
```

### 4.4 Update `infrastructure`

```typescript
output(`
🏗️ Infrastructure Status
${Object.entries(status.infrastructure || {}).map(([service, info]) =>
  `   ${service}: ${info.status}${info.waiting_for ? ` (waiting: ${info.waiting_for})` : ''}${info.notes ? ` - ${info.notes}` : ''}`
).join('\n') || '   (none configured)'}
`)

const updateInfra = await askUserQuestion({
  questions: [{
    question: 'Update infrastructure status?',
    header: 'Infra',
    options: [
      { label: 'Keep as is', description: 'No changes needed' },
      { label: 'Update status', description: 'Change service status' },
      { label: 'Add service', description: 'Track new infrastructure' },
      { label: 'Remove service', description: 'Stop tracking a service' }
    ],
    multiSelect: false
  }]
})

// Handle user selection...
// For status update, walk through each service:
if (updateInfra === 'Update status') {
  for (const [service, info] of Object.entries(status.infrastructure || {})) {
    output(`\n${service}: Currently "${info.status}"`)
    const newStatus = await askUserQuestion({
      questions: [{
        question: `Update ${service} status?`,
        header: service,
        options: [
          { label: 'healthy', description: 'Working normally' },
          { label: 'degraded', description: 'Working with issues' },
          { label: 'down', description: 'Not working' },
          { label: 'waiting', description: 'Pending external action' },
          { label: 'Keep current', description: `Stay as "${info.status}"` }
        ],
        multiSelect: false
      }]
    })

    if (newStatus !== 'Keep current') {
      status.infrastructure[service].status = newStatus

      // If changed to healthy, clear waiting_for
      if (newStatus === 'healthy') {
        status.infrastructure[service].waiting_for = null
      }

      // If changed to waiting, ask what for
      if (newStatus === 'waiting') {
        output('What is it waiting for?')
        status.infrastructure[service].waiting_for = await askUser()
      }
    }
  }
}
```

### 4.5 Update `blockers`

```typescript
output(`
🚧 Blockers (${status.blockers?.length || 0})
${status.blockers?.map(b => `   - ${b.id}: ${b.description} (blocks: ${b.blocks?.join(', ') || 'nothing specified'})`).join('\n') || '   (none)'}
`)

const updateBlockers = await askUserQuestion({
  questions: [{
    question: 'Update blockers?',
    header: 'Blockers',
    options: [
      { label: 'Keep as is', description: 'No changes needed' },
      { label: 'Add blocker', description: 'New external dependency' },
      { label: 'Remove blocker', description: 'Blocker resolved' },
      { label: 'Update blocker', description: 'Change existing blocker' }
    ],
    multiSelect: false
  }]
})

// Handle user selection...
```

### 4.6 Update `next_priorities`

```typescript
output(`
🎯 Next Priorities
${status.next_priorities?.map((p, i) => `   ${i + 1}. ${p.id}: ${p.reason}`).join('\n') || '   (none set)'}
`)

const updatePriorities = await askUserQuestion({
  questions: [{
    question: 'Update priorities?',
    header: 'Priorities',
    options: [
      { label: 'Keep as is', description: 'No changes needed' },
      { label: 'Add priority', description: 'New item to work on' },
      { label: 'Remove priority', description: 'Completed or deprioritized' },
      { label: 'Reorder', description: 'Change priority order' }
    ],
    multiSelect: false
  }]
})

// Handle user selection...
```

### 4.7 Update `notes`

```typescript
output(`
📝 Notes
${status.notes || '   (empty)'}
`)

const updateNotes = await askUserQuestion({
  questions: [{
    question: 'Update notes?',
    header: 'Notes',
    options: [
      { label: 'Keep as is', description: 'No changes needed' },
      { label: 'Replace', description: 'Replace all notes' },
      { label: 'Append', description: 'Add to existing notes' },
      { label: 'Clear', description: 'Remove all notes' }
    ],
    multiSelect: false
  }]
})

// Handle user selection...
```

---

## Step 5: Write Changes

```typescript
// Show diff
output(`
📝 Changes to be written:

${generateYamlDiff(originalStatus, status)}
`)

const confirm = await askUserQuestion({
  questions: [{
    question: 'Save changes?',
    header: 'Confirm',
    options: [
      { label: 'Yes', description: 'Write changes to PROJECT_STATUS.yml' },
      { label: 'No', description: 'Discard changes' }
    ],
    multiSelect: false
  }]
})

if (confirm === 'Yes') {
  Write(statusPath, toYaml(status))
  output(`
✅ PROJECT_STATUS.yml updated!

Last updated: ${status.last_updated}
Changes saved: ${countChanges(originalStatus, status)} section(s)
  `)
} else {
  output('Changes discarded.')
}
```

---

## Quick Mode Behavior

When `/pstatus quick` is used:

1. Check `last_updated` - if > 7 days, suggest full review
2. Auto-detect archived changes not in `completed_changes`
3. Show current blockers - ask if any resolved
4. Skip unchanged sections
5. Update timestamp and save

---

## Output Example

```
📊 PROJECT_STATUS.yml Review

Last updated: 2025-11-25 (6 days ago)
Current focus: "Building authentication system"
Active change: auth-system

📦 Found 1 archived change not in completed_changes:
   - infrastructure-cicd

Add it? (yes)
   ✅ Added: infrastructure-cicd

🚧 Blockers (1)
   - domain-config: Need domain for Cloudflare (blocks: production-launch)

Any blockers resolved? (no)

🎯 Priorities look current.

📝 Changes to be written:
   + completed_changes: infrastructure-cicd
   ~ last_updated: 2025-11-25 → 2025-12-01

Save changes? (yes)

✅ PROJECT_STATUS.yml updated!
```

---

## Integration with Other Commands

| Command | Integration |
|---------|-------------|
| `/csetup` | Reads PROJECT_STATUS.yml for context, updates `current_focus.active_change` |
| `/cstatus` | Shows both change status AND project status summary |
| `/openspec:archive` | Prompts to add to `completed_changes` |

---

## Blocker Detection Patterns

Main Claude should recognize these phrases and suggest adding blockers:

| Pattern | Example |
|---------|---------|
| "waiting for..." | "waiting for domain configuration" |
| "need X from..." | "need API key from client" |
| "blocked by..." | "blocked by DevOps team" |
| "pending..." | "pending approval" |
| "can't proceed until..." | "can't proceed until payment gateway ready" |

When detected, prompt:
```
This sounds like an external blocker. Add to PROJECT_STATUS.yml?
- id: {suggested-id}
- description: {extracted-description}
- blocks: [{related-work}]
```
