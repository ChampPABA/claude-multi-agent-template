---
name: Change View
description: View detailed progress for a change
category: Multi-Agent
tags: [progress, view, status]
---

## Usage

```bash
/cview {change-id}
/cview {change-id} --json
```

## What It Does

Shows detailed phase-by-phase breakdown with:
- All phases (completed, in-progress, pending)
- Time tracking per phase
- Agent assignments
- Issues and notes
- Files touched
- Statistics

## Steps

### Step 1: Check if Change Exists

```bash
ls openspec/changes/{change-id}/.claude/flags.json
```

If not found:
```
❌ Error: Change {change-id} not set up
Run: /csetup {change-id}
```

### Step 2: Read flags.json

```typescript
const flags = JSON.parse(
  Read('openspec/changes/{change-id}/.claude/flags.json')
)
```

### Step 3: Format Output

**If `--json` flag:**
```json
{
  "change_id": "CHANGE-003",
  "template": "frontend-only",
  "progress_percentage": 64,
  "current_phase": "refactor",
  "phases": { ... },
  "meta": { ... }
}
```

**Otherwise, format human-readable:**

```
════════════════════════════════════════════════════════════
📋 {CHANGE_ID}: {Change Title} ({template})
════════════════════════════════════════════════════════════

📊 Overall Progress: {percentage}% ({completed}/{total} phases complete)

⏱️  Time Tracking:
    Total Spent:      {spent}h {min}m
    Total Estimated:  {estimated}h {min}m
    Efficiency:       {efficiency}% {ahead/behind} schedule
    Remaining:        ~{remaining}h {min}m

════════════════════════════════════════════════════════════
✅ COMPLETED PHASES ({count})
════════════════════════════════════════════════════════════

[{number}] {Phase Name} ({agent})
    ⏱️  {start_time} → {end_time} ({duration} min, estimated {estimated} min)
    📁 Created: {count} files
       - {file-path-1}
       - {file-path-2}
    ✓ Tasks: {task-ids}
    📝 {notes}

{repeat for all completed phases}

════════════════════════════════════════════════════════════
🔄 IN PROGRESS ({count})
════════════════════════════════════════════════════════════

[{number}] {Phase Name} ({agent}) ← CURRENT
    ⏱️  Started: {start_time} ({minutes_ago} minutes ago)
    ⏱️  Estimated: {remaining} minutes remaining
    📝 {notes}

════════════════════════════════════════════════════════════
⏳ PENDING ({count})
════════════════════════════════════════════════════════════

[{number}] {Phase Name} ({agent})
    ⏱️  Estimated: {estimated} minutes
    📋 {brief-description}

{repeat for all pending phases}

════════════════════════════════════════════════════════════
📈 STATISTICS
════════════════════════════════════════════════════════════

Tests:      {passed} passed, {failed} failed ({pass_rate}% pass rate)
Coverage:   {coverage}% (target: {target}% {✓/✗})
Issues:     {found} found, {fixed} fixed, {remaining} remaining
Files:      {created} created, {modified} modified
Approvals:  {approval_status}

════════════════════════════════════════════════════════════
🎯 NEXT STEPS
════════════════════════════════════════════════════════════

{if in_progress}
Current phase in progress. Wait for completion.

{else if next_phase === user}
Next phase requires your action:
→ Phase {number}: {Phase Name}
→ {action_required}

When done: /cdev {change-id} --continue

{else if next_phase === automated}
Continue development:
→ /cdev {change-id}

{else if all_complete}
✅ All phases complete!

Review and archive:
1. Update tasks.md (mark all [x])
2. Review report: openspec/changes/{change-id}/.claude/report.md
3. Archive: openspec archive {change-id}

{else if blocked}
⚠️ Change is blocked: {blocking_reason}
Fix issues before continuing.
```

---

## Formatting Helpers

### Progress Bar

```typescript
function generateProgressBar(percentage: number, width: number = 20): string {
  const filled = Math.floor(percentage * width / 100)
  const empty = width - filled
  return `[${'█'.repeat(filled)}${'░'.repeat(empty)}] ${percentage}%`
}

// Example: generateProgressBar(64, 20)
// Output: [████████████░░░░░░░░] 64%
```

### Time Formatting

```typescript
function formatDuration(minutes: number): string {
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  if (hours > 0) {
    return `${hours}h ${mins}m`
  }
  return `${mins} min`
}
```

### Time Ago

```typescript
function timeAgo(timestamp: string): string {
  const now = new Date()
  const then = new Date(timestamp)
  const diffMinutes = Math.floor((now - then) / 1000 / 60)

  if (diffMinutes < 60) return `${diffMinutes} minutes ago`
  const hours = Math.floor(diffMinutes / 60)
  if (hours < 24) return `${hours} hours ago`
  const days = Math.floor(hours / 24)
  return `${days} days ago`
}
```

### Efficiency Calculation

```typescript
function calculateEfficiency(actual: number, estimated: number): {
  percentage: number
  status: 'ahead' | 'on track' | 'behind'
} {
  const percentage = Math.round((estimated / actual) * 100)
  let status: 'ahead' | 'on track' | 'behind'

  if (percentage > 110) status = 'ahead'
  else if (percentage >= 90) status = 'on track'
  else status = 'behind'

  return { percentage, status }
}
```

---

## Example Output

```bash
$ /cview CHANGE-003

════════════════════════════════════════════════════════════
📋 CHANGE-003: Create Landing Page (frontend-only)
════════════════════════════════════════════════════════════

📊 Overall Progress: [████████████░░░░░░░░] 64% (7/11 phases complete)

⏱️  Time Tracking:
    Total Spent:      2h 55min
    Total Estimated:  3h 15min
    Efficiency:       111% (ahead of schedule)
    Remaining:        ~35 minutes

════════════════════════════════════════════════════════════
✅ COMPLETED PHASES (7)
════════════════════════════════════════════════════════════

[1] Frontend Mockup (uxui-frontend)
    ⏱️  2025-10-30 10:00 → 11:35 (95 min, estimated 90 min)
    📁 Created: 4 files
       - src/app/page.tsx
       - src/components/landing/hero-section.tsx
       - src/components/landing/features-section.tsx
       - src/components/landing/cta-section.tsx
    ✓ Tasks: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3
    📝 All landing page sections created. Responsive design implemented.

[2] Accessibility Test (test-debug)
    ⏱️  2025-10-30 11:35 → 11:43 (8 min, estimated 10 min)
    🎯 Lighthouse: 98/100
    ✓ Contrast ratio: Pass
    ✓ ARIA labels: Complete
    📝 Minor contrast adjustment made to CTA button.

[3] Manual UX Test (user)
    ⏱️  2025-10-30 11:43 → 12:03 (20 min, estimated 15 min)
    🐛 Issues: 2 found, 2 fixed
       - Spacing issue in mobile view (fixed)
       - Hero headline too small on tablet (fixed)

[4] Business Logic Validation (integration)
    ⏱️  2025-10-30 12:03 → 12:10 (7 min, estimated 10 min)
    ✓ Requirements: 9/9 passed
    ✓ No discrepancies

[5] User Approval (user)
    ⏱️  2025-10-30 12:10 → 12:15 (5 min, estimated 5 min)
    ✅ Approved

[6] Component Tests (test-debug)
    ⏱️  2025-10-30 12:15 → 12:40 (25 min, estimated 20 min)
    ✓ Tests: 12 passed, 0 failed
    📊 Coverage: 75% (target: 70%)

[7] Responsive Test (user)
    ⏱️  2025-10-30 14:00 → 14:15 (15 min, estimated 15 min)
    ✓ Breakpoints: 1920x1080, 768x1024, 375x667
    ✓ No issues found

════════════════════════════════════════════════════════════
🔄 IN PROGRESS (1)
════════════════════════════════════════════════════════════

[8] Refactor (test-debug) ← CURRENT
    ⏱️  Started: 2025-10-30 14:15 (15 minutes ago)
    ⏱️  Estimated: 20 minutes total (~5 minutes remaining)
    📝 Extracting reusable button component. Optimizing CSS classes.

════════════════════════════════════════════════════════════
⏳ PENDING (3)
════════════════════════════════════════════════════════════

[9] Test Coverage Report (test-debug)
    ⏱️  Estimated: 5 minutes
    📋 Generate final coverage report

[10] Documentation (integration)
     ⏱️  Estimated: 15 minutes
     📋 Update README, add JSDoc comments

[11] Final Report (integration)
     ⏱️  Estimated: 10 minutes
     📋 Generate verbose report for archive

════════════════════════════════════════════════════════════
📈 STATISTICS
════════════════════════════════════════════════════════════

Tests:      12 passed, 0 failed (100% pass rate)
Coverage:   75% (target: 70% ✓)
Issues:     2 found, 2 fixed, 0 remaining
Files:      4 created, 2 modified
Approvals:  ✅ User approved (phase 5)

════════════════════════════════════════════════════════════
🎯 NEXT STEPS
════════════════════════════════════════════════════════════

Current phase in progress. Wait for completion or check status:
→ /cstatus CHANGE-003

To continue after current phase completes:
→ /cdev CHANGE-003

To view raw JSON data:
→ /cview CHANGE-003 --json
```

---

## Error Handling

**If change not found:**
```
❌ Error: Change CHANGE-003 not found or not set up

Please check:
1. Change ID is correct
2. Change has been set up: /csetup CHANGE-003
```

**If flags.json is corrupted:**
```
❌ Error: Cannot parse flags.json (invalid JSON)

This may indicate corruption. Try:
1. Check file: openspec/changes/{change-id}/.claude/flags.json
2. Restore from backup if available
3. Re-run setup: /csetup {change-id} (will overwrite!)
```

---

## Quick Commands Reference

```bash
# Detailed view
/cview CHANGE-003

# JSON output
/cview CHANGE-003 --json

# Combined with other commands
/cview CHANGE-003 && /cdev CHANGE-003
```
