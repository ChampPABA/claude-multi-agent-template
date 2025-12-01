---
name: Change Status
description: Quick progress status for a change (with project context)
category: Multi-Agent
tags: [status, progress, quick]
---

## Usage

```bash
/cstatus {change-id}
/cstatus                # Shows project status only (no change-id)
```

## What It Does

Shows quick progress summary:
- **Project context** (from PROJECT_STATUS.yml if exists)
- Progress percentage with bar
- Current phase
- Time spent/remaining
- Quick stats

---

## Step 1: Show Project Context (v2.1.0)

```typescript
const projectStatusPath = 'PROJECT_STATUS.yml'

if (fileExists(projectStatusPath)) {
  const projectStatus = parseYaml(Read(projectStatusPath))

  output(`
📊 Project Status
├─ Focus: ${projectStatus.current_focus?.description || 'Not set'}
├─ Active change: ${projectStatus.current_focus?.active_change || 'None'}
├─ Blockers: ${projectStatus.blockers?.length || 0}
├─ Infra: ${summarizeInfraStatus(projectStatus.infrastructure)}
└─ Updated: ${projectStatus.last_updated}
`)

  // Show blockers if any
  if (projectStatus.blockers?.length > 0) {
    output(`
🚧 Active Blockers:
${projectStatus.blockers.map(b => `   - ${b.id}: ${b.description}`).join('\n')}
`)
  }
}

// If no change-id provided, stop here
if (!changeId) {
  output(`
Commands:
→ Update project status: /pstatus
→ View change status: /cstatus {change-id}
`)
  return
}
```

---

## Step 2: Show Change Status

```typescript
// Read change flags
const flagsPath = `openspec/changes/${changeId}/.claude/flags.json`

if (!fileExists(flagsPath)) {
  return output(`❌ Change ${changeId} not found or not set up. Run /csetup ${changeId} first.`)
}

const flags = JSON.parse(Read(flagsPath))
```

## Output Format

```
📊 Project Status
├─ Focus: Building authentication system
├─ Active change: auth-system
├─ Blockers: 1
├─ Infra: DB ✅ | API ✅ | Tunnel ⏳
└─ Updated: 2025-11-30

🚧 Active Blockers:
   - domain-config: Need domain for Cloudflare public routes

─────────────────────────────────────────

📦 CHANGE-{id}: {type} | {template}

Progress: [████████░░] 64% (7/11 phases)

Current Phase: #8 Refactor (test-debug)
├─ Started: 14:15 (15 minutes ago)
├─ Estimated: 20 minutes
└─ Status: in_progress

✅ Completed: 7 phases
🔄 In Progress: 1 phase
⏳ Remaining: 3 phases

⏱️ Time:
├─ Spent: 2h 55min (estimated: 3h 15min)
├─ Remaining: ~35 minutes
└─ Efficiency: 111% (ahead of estimate)

📈 Stats:
├─ Tests: 12 passed, 0 failed (75% coverage)
├─ Issues: 2 found, 2 fixed, 0 remaining
└─ Files: 4 created, 2 modified

🎯 Next Steps:
1. Complete refactoring (20 min)
2. Test coverage report (5 min)
3. Documentation (15 min)

Commands:
→ Update project status: /pstatus
→ Detailed view: /cview {change-id}
→ Continue dev: /cdev {change-id}
```

---

## Helper: summarizeInfraStatus()

```typescript
function summarizeInfraStatus(infrastructure) {
  if (!infrastructure) return 'Not configured'

  return Object.entries(infrastructure)
    .map(([service, info]) => {
      const icon = info.status === 'healthy' ? '✅' :
                   info.status === 'degraded' ? '⚠️' :
                   info.status === 'down' ? '❌' :
                   info.status === 'waiting' ? '⏳' : '❓'
      return `${service} ${icon}`
    })
    .join(' | ')
}
```

---

## Implementation Notes

1. **Always show project status first** (if PROJECT_STATUS.yml exists)
2. **Then show change status** (if change-id provided)
3. **Include /pstatus in commands** to encourage keeping status updated
