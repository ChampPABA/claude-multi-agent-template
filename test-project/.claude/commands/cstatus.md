---
name: Change Status
description: Quick progress status for a change
category: Multi-Agent
tags: [status, progress, quick]
---

## Usage

```bash
/cstatus {change-id}
```

## What It Does

Shows quick progress summary:
- Progress percentage with bar
- Current phase
- Time spent/remaining
- Quick stats

## Output Format

```
📊 CHANGE-{id}: {type} | {template}

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
→ Detailed view: /cview {change-id}
→ Continue dev: /cdev {change-id}
```

## Implementation

Read `openspec/changes/{change-id}/.claude/flags.json` and format output using helper functions.
