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

### 1.1: Read Project Status

1. Check if `PROJECT_STATUS.yml` exists in project root
2. If file exists, read and parse YAML content

**Output format:**
```
📊 Project Status
├─ Focus: [current_focus.description or "Not set"]
├─ Active change: [current_focus.active_change or "None"]
├─ Blockers: [count of blockers or 0]
├─ Infra: [infrastructure summary - see Step 1.2]
└─ Updated: [last_updated date]
```

### 1.2: Summarize Infrastructure Status

**For each service in `infrastructure` section:**

1. Check `status` field value
2. Map to icon:
   - `healthy` → ✅
   - `degraded` → ⚠️
   - `down` → ❌
   - `waiting` → ⏳
   - Other → ❓
3. Format as: `{service-name} {icon}`
4. Join all services with ` | `

**Example output:** `DB ✅ | API ✅ | Tunnel ⏳`

**If no infrastructure configured:** Display `Not configured`

### 1.3: Show Active Blockers

**If `blockers` array exists and has items:**

```
🚧 Active Blockers:
   - [blocker-1-id]: [description]
   - [blocker-2-id]: [description]
```

**If no blockers:** Skip this section

### 1.4: Handle No Change ID

**If no change-id provided in command:**

Display:
```
Commands:
→ Update project status: /pstatus
→ View change status: /cstatus {change-id}
```

Then STOP (do not proceed to Step 2)

---

## Step 2: Show Change Status

### 2.1: Validate Change Exists

1. Build path: `openspec/changes/{changeId}/.claude/flags.json`
2. Check if file exists

**If file does NOT exist:**
```
❌ Change {changeId} not found or not set up. Run /csetup {changeId} first.
```
Then STOP.

### 2.2: Read Change Flags

1. Read `flags.json` file
2. Parse JSON content
3. Extract progress data for output (see Output Format below)

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

## Implementation Notes

1. **Always show project status first** (if PROJECT_STATUS.yml exists)
2. **Then show change status** (if change-id provided)
3. **Include /pstatus in commands** to encourage keeping status updated
