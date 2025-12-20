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

1. Check if `PROJECT_STATUS.yml` exists in project root

**If file does NOT exist:**

2. Display message:
```
📊 PROJECT_STATUS.yml not found

This file provides cross-session context for Claude.
It helps new sessions understand:
- Infrastructure state (DB, API, tunnels)
- Blockers (waiting for domain, API keys)
- Completed work & next priorities

Create it now? (yes/no)
```

3. Ask user to confirm creation

**If user says "yes":**
- Copy `.claude/templates/PROJECT_STATUS.template.yml` to project root as `PROJECT_STATUS.yml`
- Display: `✅ Created PROJECT_STATUS.yml - please fill in your project details`
- Stop execution (user needs to fill template first)

**If user says "no":**
- Display: `Skipped. Run /pstatus again when ready.`
- Stop execution

**If file EXISTS:**
- Continue to Step 2

---

## Step 2: Read Current Status

1. Read `PROJECT_STATUS.yml` and parse as YAML

2. Extract `last_updated` field

3. Calculate days since update:
   - Parse `last_updated` as date
   - Calculate difference between today and last_updated in days
   - Round down to whole number

4. Display status summary:
```
📊 PROJECT_STATUS.yml

Last updated: [YYYY-MM-DD] ([N] days ago)
Current focus: [description or 'Not set']
Active change: [change-id or 'None']
Blockers: [count]
Completed changes: [count]
```

**Example:**
```
📊 PROJECT_STATUS.yml

Last updated: 2025-11-25 (6 days ago)
Current focus: Building authentication system
Active change: auth-system
Blockers: 1
Completed changes: 3
```

---

## Step 3: Select Update Mode

1. Check if mode was provided as argument:
   - `/pstatus quick` → mode = "quick"
   - `/pstatus full` → mode = "full"
   - `/pstatus blockers` → mode = "blockers" (or any specific section)
   - `/pstatus` (no args) → ask user

**If no mode specified:**

2. Ask user: "What would you like to update?"

Display options:
- **Quick Update** - Only sections that seem outdated
- **Full Review** - Walk through all sections
- **Specific Section** - Update one section only

3. Store selected mode for Step 4

---

## Step 4: Section-by-Section Updates

### 4.1 Update `last_updated`

Always update timestamp to today's date in YYYY-MM-DD format.

**Example:** `2025-12-20`

### 4.2 Update `current_focus`

1. Display current focus:
```
📍 Current Focus
   Description: "[description or 'Not set']"
   Active change: [change-id or 'None']
```

2. Ask user: "Update current focus?"

Display options:
- **Keep as is** - No changes needed
- **Update description** - Change what you are working on
- **Set active change** - Link to OpenSpec change
- **Clear active change** - Not working on a change

**If user selects "Update description":**
- Ask: "What are you working on?"
- Update `current_focus.description` with user's answer

**If user selects "Set active change":**
- Ask: "Which change ID?"
- Update `current_focus.active_change` with change ID

**If user selects "Clear active change":**
- Set `current_focus.active_change` to null

**If user selects "Keep as is":**
- Skip to next section

### 4.3 Update `completed_changes`

1. Display completed changes:
```
✅ Completed Changes ([count])
   - [id] ([date]): [summary]
   - ...
   (or "none" if empty)
```

2. Auto-detect archived changes not in list:
   - List all directories in `openspec/changes/archive/`
   - For each archived change, check if its ID exists in `completed_changes`
   - Collect missing changes

**If missing changes found:**

3. Display:
```
📦 Found [N] archived change(s) not in completed_changes:
   - [change-id-1]
   - [change-id-2]
   ...

Add them? (yes/no)
```

4. Ask user to confirm

**If user says "yes":**

For each missing change:
- Extract change ID from directory name
- Try to read `{change-path}/proposal.md`
- Extract summary from proposal (first H1 title or first sentence)
- If proposal not found, use "No summary available"
- Add to `completed_changes`:
  ```yaml
  - id: change-id
    date: YYYY-MM-DD (today)
    summary: extracted summary
  ```
- Display: `✅ Added: {change-id}`

**If user says "no":**
- Skip to next section

### 4.4 Update `infrastructure`

1. Display infrastructure status:
```
🏗️ Infrastructure Status
   [service]: [status] (waiting: [reason]) - [notes]
   ...
   (or "none configured" if empty)
```

2. Ask user: "Update infrastructure status?"

Display options:
- **Keep as is** - No changes needed
- **Update status** - Change service status
- **Add service** - Track new infrastructure
- **Remove service** - Stop tracking a service

**If user selects "Update status":**

For each service in infrastructure:

3. Display current status:
```
[service]: Currently "[status]"
```

4. Ask user to select new status:
   - **healthy** - Working normally
   - **degraded** - Working with issues
   - **down** - Not working
   - **waiting** - Pending external action
   - **Keep current** - Stay as "[current status]"

5. Handle status change:

**If new status = "healthy":**
- Update `infrastructure[service].status` to "healthy"
- Clear `infrastructure[service].waiting_for` (set to null)

**If new status = "waiting":**
- Update `infrastructure[service].status` to "waiting"
- Ask: "What is it waiting for?"
- Update `infrastructure[service].waiting_for` with user's answer

**If new status = "degraded" or "down":**
- Update `infrastructure[service].status` to selected value

**If user selects "Keep current":**
- Skip this service

**If user selects "Add service":**
- Ask: "Service name?"
- Ask: "Status?" (healthy/degraded/down/waiting)
- If waiting, ask: "Waiting for what?"
- Add new service to `infrastructure`

**If user selects "Remove service":**
- Ask: "Which service to remove?"
- Remove service from `infrastructure`

**If user selects "Keep as is":**
- Skip to next section

### 4.5 Update `blockers`

1. Display blockers:
```
🚧 Blockers ([count])
   - [id]: [description] (blocks: [what it blocks])
   ...
   (or "none" if empty)
```

2. Ask user: "Update blockers?"

Display options:
- **Keep as is** - No changes needed
- **Add blocker** - New external dependency
- **Remove blocker** - Blocker resolved
- **Update blocker** - Change existing blocker

**If user selects "Add blocker":**
- Ask: "Blocker ID?" (e.g., "domain-config")
- Ask: "What's blocked?" (description)
- Ask: "What does it block?" (e.g., "production-launch")
- Add new blocker:
  ```yaml
  - id: blocker-id
    description: user's description
    blocks: [what-it-blocks]
  ```

**If user selects "Remove blocker":**
- Display list of current blockers with numbers
- Ask: "Which blocker to remove?" (user selects by number or ID)
- Remove blocker from list

**If user selects "Update blocker":**
- Display list of current blockers with numbers
- Ask: "Which blocker to update?" (user selects by number or ID)
- Ask: "Update description? (yes/no)"
  - If yes, ask for new description
- Ask: "Update what it blocks? (yes/no)"
  - If yes, ask for new value

**If user selects "Keep as is":**
- Skip to next section

### 4.6 Update `next_priorities`

1. Display priorities (in order):
```
🎯 Next Priorities
   1. [id]: [reason]
   2. [id]: [reason]
   ...
   (or "none set" if empty)
```

2. Ask user: "Update priorities?"

Display options:
- **Keep as is** - No changes needed
- **Add priority** - New item to work on
- **Remove priority** - Completed or deprioritized
- **Reorder** - Change priority order

**If user selects "Add priority":**
- Ask: "Priority ID?" (e.g., "auth-system")
- Ask: "Why is this a priority?" (reason)
- Ask: "Add at position?" (1 = highest priority, or append to end)
- Insert new priority at specified position:
  ```yaml
  - id: priority-id
    reason: user's reason
  ```

**If user selects "Remove priority":**
- Display numbered list of priorities
- Ask: "Which priority to remove?" (user selects by number)
- Remove priority from list

**If user selects "Reorder":**
- Display numbered list of priorities
- Ask: "Which priority to move?" (user selects by number)
- Ask: "New position?" (1 = highest)
- Move priority to new position

**If user selects "Keep as is":**
- Skip to next section

### 4.7 Update `notes`

1. Display notes:
```
📝 Notes
[notes content or "(empty)"]
```

2. Ask user: "Update notes?"

Display options:
- **Keep as is** - No changes needed
- **Replace** - Replace all notes
- **Append** - Add to existing notes
- **Clear** - Remove all notes

**If user selects "Replace":**
- Ask: "New notes?"
- Replace entire `notes` field with user's input

**If user selects "Append":**
- Ask: "What to add?"
- Append user's input to existing notes (add newline separator)

**If user selects "Clear":**
- Set `notes` to empty string or null

**If user selects "Keep as is":**
- Continue to Step 5

---

## Step 5: Write Changes

1. Generate diff between original and updated status

2. Display changes summary:
```
📝 Changes to be written:

+ completed_changes: [new items]
~ current_focus: [old] → [new]
- blockers: [removed items]
...
```

3. Ask user: "Save changes?"

Display options:
- **Yes** - Write changes to PROJECT_STATUS.yml
- **No** - Discard changes

**If user selects "Yes":**

4. Convert updated status object to YAML format

5. Write to `PROJECT_STATUS.yml` (overwrite entire file)

6. Display confirmation:
```
✅ PROJECT_STATUS.yml updated!

Last updated: [YYYY-MM-DD]
Changes saved: [N] section(s)
```

**If user selects "No":**
- Display: `Changes discarded.`
- Do not modify file

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
