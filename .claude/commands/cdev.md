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

---

#### Step 2.1: Read flags.json

1. Read the file `openspec/changes/{change-id}/.claude/flags.json`
2. Extract and note these values:
   - `current_phase` - The current phase name
   - `phases[current_phase].status` - The phase status
   - `phases[current_phase].agent` - The assigned agent

---

#### Step 2.2: Check Phase Status

**If status equals "completed":**
1. Look up the next phase in phases.md
2. Update current_phase to the next phase name

**If status equals "pending" or "in_progress":**
1. Keep using the current phase (no change)

---

#### Step 2.3: Report Status

Display this information:
```
📍 Current Phase: {phase_number} - {phase_name}
   Agent: {agent}
   Status: {status}
```

---

### Step 3: Check Phase Type

---

#### Step 3.1: Check for Manual Action

**If the agent value equals "user":**
1. Display this message:
   ```
   🛑 Phase {phase_number} requires manual action

   Instructions:
   {instructions from phases.md}

   When done: /cdev {change-id} --continue
   ```
2. Stop execution and wait for user to complete the task
3. Wait for user to run /cdev again

---

#### Step 3.2: Check for Multiple Agents

**If the agent value contains "+" (example: "backend + database"):**
1. Split the agent string by "+" into a list of individual agents
2. Invoke all agents in parallel
3. Wait for all agents to complete before proceeding

**If there is only a single agent:**
1. Invoke that single agent
2. Wait for completion then proceed to Step 4

### Step 4: Invoke Agent with Retry & Validation

**This step now uses the enhanced agent-executor framework!**

See: `.claude/lib/agent-executor.md` for full implementation

**High-Level Flow:**

1. **Calculate Context Size** (for model selection)
2. **Select Model** (haiku vs sonnet based on complexity)
3. **Pre-Flight Design Check** (for visual agents) ← NEW v3.3.0
4. **Execute Agent with Retry** (automatic retry on failure)
5. **Validate Pre-Work** (enforce mandatory checklist)
6. **Validate Output Quality** (check completeness)
7. **Handle Errors** (retry or escalate)

### Step 4.0: Pre-Flight Design Check (v3.3.0)

→ **Full Protocol:** `.claude/lib/design-validator.md` (Part 2)

**When to execute:** Before invoking uxui-frontend or frontend agent

---

#### Step 4.0.1: Check if Visual Agent

1. Look at the phase.agent value
2. Check if it equals `uxui-frontend` or `frontend`

**If NOT a visual agent:**
- Skip Step 4.0 entirely and proceed to Step 4.1

**If it IS a visual agent:**
- Proceed to next step

---

#### Step 4.0.2: Check for Design System

1. Attempt to read the file `design-system/data.yaml`

**If the file exists:**
1. Display this message:
   ```
   ✅ Design system found: design-system/data.yaml
   ```
2. Proceed to Step 4.0.3

**If the file does NOT exist:**
1. Display this warning:
   ```
   ⚠️ WARNING: No design system found!
      Path: design-system/data.yaml (not found)

      Options:
      1. Run /designsetup first (recommended)
      2. Continue with fallback design principles

      Proceeding with fallback...
   ```
2. Skip to Step 4.1 without injecting design system instructions

---

#### Step 4.0.3: Inject Design System Instructions

When building the agent prompt, include this text:

```
MANDATORY: Read design-system/data.yaml before writing any CSS/Tailwind.
Report the tokens you loaded before starting implementation.

You must report:
- Colors: primary=#xxx, secondary=#xxx, etc.
- Spacing scale: 4, 8, 12, 16, 24, 32, 48, 64
- Animation durations: 150ms, 300ms, 500ms ONLY

DO NOT use:
- Hardcoded colors (#3b82f6, rgb())
- Arbitrary spacing (p-5, gap-7)
- Random durations (duration-200, duration-250)
```

---

#### Step 4.0.4: Verify Agent Compliance

After the agent responds, check the output for this report:

```
✅ Design System Loaded (STEP 0.5)
   - Source: design-system/data.yaml
   - Colors: [list]
   - Spacing: [list]
   - Animation: [list]
```

**If the report is present:**
- Validation passed, proceed

**If the report is missing:**
- Ask the agent whether they read the design system

---

### Step 4.1: Build Agent Prompt

Build the agent prompt by assembling these sections:

---

#### Section 1: Change Context

Include information from these files:
1. Read `proposal.md` - What we're building and why
2. Read `tasks.md` - Tasks for this phase
3. Read `design.md` - Design decisions (if the file exists)
4. Read `phases.md` - Phase instructions

Combine this information into the prompt context.

---

#### Section 2: Library Requirements (v2.1.2)

Add these instructions to the agent prompt:
1. Scan tasks.md for patterns like: "Install X", "Configure X"
2. Scan design.md for: "D1: Use X Library", "Decision: Use X"
3. Use the specified libraries, not custom implementations
4. Implement according to design spec, not library defaults

---

#### Section 3: Development Principles (v3.1.0 - ALL agents)

**If the file `.claude/contexts/patterns/development-principles.md` exists:**

Add this section to the prompt:
```
## 🏛️ Development Principles (Level 1 - ALL Agents)

REQUIRED READING: @.claude/contexts/patterns/development-principles.md

Quick Reference:
| Principle | Summary |
|-----------|---------|
| KISS | Choose simple solutions |
| YAGNI | Build only what you need now |
| SRP | One responsibility per module |
| DRY | Single source of truth |
| Fail Fast | Detect errors immediately |
```

---

#### Section 4: Best Practices (agent-specific)

**If the directory `.claude/contexts/domain/project/best-practices/` exists:**

1. Determine which best-practices files match the current agent:

   | Agent | Relevant Topics |
   |-------|-----------------|
   | uxui-frontend | react, nextjs, vue, tailwind |
   | frontend | react, nextjs, vue, typescript |
   | backend | express, fastapi, django, prisma, drizzle |
   | database | prisma, drizzle, postgres, mongodb |
   | test-debug | vitest, jest, playwright |
   | integration | typescript |
   | ux-tester | (none) |

2. Add this section to the prompt with the relevant file names:
   ```
   ## 📚 Best Practices (STEP 0)

   Read these files before implementation:
   - Read: .claude/contexts/domain/project/best-practices/{relevant-file}.md
   ```

---

#### Section 5: Design System (uxui-frontend only)

**If the agent equals uxui-frontend:**

1. Check if `design-system/data.yaml` exists

   **If the file exists:**
   Add this section to the prompt:
   ```
   ## 🎨 Design System (STEP 0.5)

   Files to read:
   - design-system/data.yaml

   Style Guidelines:
   | Instead of | Use |
   |------------|-----|
   | text-gray-500, #64748b | text-foreground, bg-muted |
   | p-5, gap-7 | p-4, p-6, gap-8 |
   | mixing shadow-sm/lg | consistent shadow-md |
   ```

   **If the file does NOT exist:**
   Add this warning to the prompt:
   ```
   ⚠️ WARNING: No design system found!
   Using fallback: .claude/contexts/design/*.md
   ```

---

#### Section 6: Report Format Enforcement (ux-tester only)

**If agent equals ux-tester:**

Add this section to the prompt:

```
⚠️ MANDATORY REPORT FORMAT ENFORCEMENT

You MUST follow the EXACT report format from your agent definition file.

HARD LIMITS:
- MAX 150 lines total (count before submitting)
- Use TABLES ONLY (no paragraphs for personas/issues)
- 1 row per persona, 1 row per issue
- MAX 10 steps in Human Testing Guide

VIOLATIONS THAT WILL BE REJECTED:
- Verbose persona backgrounds/stories
- Paragraph descriptions instead of tables
- Report exceeding 150 lines
- Duplicate information across sections

Reference: .claude/agents/07-ux-tester.md → "Report Format" section

Before generating report, count lines. If > 150, cut non-essential details.
```

---

### Step 4.2: Execute Agent with Retry

---

#### Step 4.2.1: Invoke the Agent

1. Display this message before invoking:
   ```
   🚀 Invoking {agent} agent (model: opus)...
   ```

2. Invoke the agent with these settings:
   - Model: opus (fixed)
   - Timeout: 10 minutes
   - Max retries: 2 attempts

---

#### Step 4.2.2: Handle Result

**If execution succeeded:**
1. Display this success message:
   ```
   ✅ Phase {phase_number} completed successfully!
   ⏱️ Execution time: {time}s
   🔄 Retries used: {retries}
   ✅ Validation: PASSED
   ```
2. Proceed to Step 5

**If execution failed:**
1. Display this error message:
   ```
   ❌ Phase {phase_number} failed
   Error: {error}
   Retries used: {retries}
   ```

2. Ask the user for their choice:
   ```
   Options:
   [retry] - Try again
   [skip]  - Skip this phase
   [abort] - Stop execution
   ```

3. Wait for user response and act accordingly

---

**Helper Functions:**

See `.claude/lib/agent-executor.md` for:
- buildAgentPrompt()
- executeAgentWithRetry()
- escalateToUser()

**Model Strategy:**
- All agents use `model: opus` (fixed)
- Opus 4.5 is the latest Claude model with best performance

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
- ux-tester: Personas Generated, Dev Server Found, Chrome DevTools Connected

---

### Step 4.6: Approval Gate Handling (v2.7.0)

**For phases with** `requires_approval: true` (example: ux-tester Phase 1.5)

---

#### Step 4.6.1: Check if Approval Required

1. Look in phases.md at the current phase
2. Check if it has:
   - `requires_approval: true`
   - OR metadata contains the word `approval-gate`

**If approval is NOT required:**
- Skip Step 4.6 entirely

**If approval IS required:**
- Proceed to next step

---

#### Step 4.6.2: Display Results and Wait for Decision

Display this message:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧪 {phase_name} Complete - Awaiting Approval
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{result_summary}

📄 Full report: openspec/changes/{change-id}/ux-test-report.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please decide:

✅ "approve" → Continue to next phase
❌ "reject [feedback]" → Go back and fix previous phase

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Wait for user response.

---

#### Step 4.6.3: Handle User Response

**If user approves:**
1. Recognize these words as approval: approve, approved, ok, yes, ใช่, อนุมัติ, ผ่าน, ลุย, ได้, ดี
2. Display: `✅ {phase_name} approved! Continuing to next phase...`
3. Update flags.json: set status = "approved"
4. Proceed to Step 5

**If user rejects:**
1. Recognize these words as rejection: reject, ไม่, แก้, no (followed by feedback)
2. Extract the feedback text from the user's message
3. Identify which phase needs to be fixed (uxui-frontend)
4. Display:
   ```
   🔄 {phase_name} rejected

   📝 Feedback: {feedback}
   🔙 Looping back to: Phase {X} - {phase_name}

   {agent} agent will receive this feedback for fixes
   ```
5. Update flags.json: set status = "rejected"
6. Return to run the phase that needs fixing

**If response is unclear:**
1. Display:
   ```
   ⚠️ Response unclear. Please answer "approve" or "reject [feedback]"
   ```
2. Ask the user again

---

**See:** `.claude/lib/agent-executor.md` → "Approval Gate Execution" section for complete flow

---

### Step 4.7: Validate Page Plan Compliance (uxui-frontend only)

**Only for uxui-frontend agent when page-plan.md exists**

**Purpose:** Verify that agent implemented all sections from page-plan.md

---

#### Step 4.7.1: Check Prerequisites

**If agent is NOT uxui-frontend OR page-plan.md does NOT exist:**
1. Display:
   ```
   ℹ️ Page plan validation: N/A (agent: {agent}, has plan: {true/false})
   ```
2. Skip Step 4.7 entirely

**If agent equals uxui-frontend AND page-plan.md exists:**
- Proceed to next step

---

#### Step 4.7.2: Analyze page-plan.md

1. Read `openspec/changes/{change-id}/page-plan.md`
2. Find Section 2 (Page Structure)
3. Count the components:
   - Look for JSX elements starting with uppercase (example: `<HeroSection>`, `<PricingTable>`)
   - Do NOT count Layout, div (wrapper elements)
   - Remove duplicates

4. Display:
   ```
   📋 Page Plan Analysis:
      Expected sections: {count}
      Components: {list}
   ```

---

#### Step 4.7.3: Ask User for Confirmation

Display this prompt:
```
⚠️ VALIDATION REQUIRED:

Did the agent implement ALL {count} sections?

Please verify the implementation includes:
   - {Component1}
   - {Component2}
   - ...

Options:
  [yes]   - All sections implemented ✓
  [retry] - Agent skipped sections, retry with strict enforcement
  [skip]  - Skip validation (not recommended)
```

Wait for user response.

---

#### Step 4.7.4: Handle User Response

**If user answers yes:**
1. Display:
   ```
   ✅ Page plan compliance confirmed
      All {count} sections implemented
   ```
2. Proceed to Step 5

**If user answers retry:**
1. Display:
   ```
   🔄 Retrying phase with enhanced enforcement...
   Agent will be explicitly instructed to implement all {count} sections
   ```
2. Return to run the phase again with enhanced prompt

**If user answers skip:**
1. Display:
   ```
   ⚠️ Skipping validation - proceed with caution
      This may result in incomplete implementation
   ```
2. Proceed to Step 5

---

**When to use:**
- Agent: uxui-frontend
- page-plan.md exists
- Phase completed successfully

**Common issues caught:**
- Agent implemented 5/10 sections (missing ProblemSection, ComparisonTable, etc.)
- Agent followed tasks.md ("4-5 components") instead of page-plan.md (10 sections)
- Agent skipped sections they thought were "optional"

---

### Step 5: Post-Execution (Flags Update)

**Main Claude updates flags.json after each phase**

→ See: `.claude/lib/flags-updater.md` for complete protocol

WHY: Immediate updates ensure /cstatus shows accurate progress.

---

#### Step 5.1: Update flags.json

1. Display:
   ```
   🔄 Updating progress tracking...
   ```

2. Update these fields in flags.json:
   - Mark the phase as completed
   - Record actual duration
   - Extract files created/modified
   - Update meta statistics (progress %, time remaining)
   - Move current_phase to next phase

---

#### Step 5.2: Report Progress

Display this progress summary:
```
📊 Progress Update:
   ✅ {completed}/{total} phases complete
   📈 {percentage}% progress
   ⏱️  {time_spent} spent
   ⏱️  {time_remaining} remaining
```

---

#### Step 5.3: Check Next Phase

**If all phases are complete (ready_to_archive equals true):**

Display this completion report:
```
╔════════════════════════════════════════════════════════════╗
║           ✅ CHANGE COMPLETED SUCCESSFULLY                 ║
╚════════════════════════════════════════════════════════════╝

📦 Change: {change-id}
📋 Template: {template} ({total_phases} phases)

═══════════════════════════════════════════════════════════════
📊 EXECUTION SUMMARY
═══════════════════════════════════════════════════════════════

⏱️  Time:
   • Estimated: {estimated}
   • Actual:    {actual}
   • Variance:  {variance}

📈 Phases Completed: {completed}/{total}
   ✅ 1. phase-name (Xm)
   ✅ 2. phase-name (Xm)
   ...

═══════════════════════════════════════════════════════════════
📁 FILES CREATED/MODIFIED
═══════════════════════════════════════════════════════════════

✨ Created ({count}):
   • {file1}
   • {file2}

📝 Modified ({count}):
   • {file1}
   • {file2}

═══════════════════════════════════════════════════════════════
🚀 NEXT STEPS
═══════════════════════════════════════════════════════════════

1. Review changes:  /cview {change-id}
2. Test manually:   Verify the implementation works
3. Mark complete:   Update tasks.md (mark all [x])
4. Archive:         openspec archive {change-id}
```

**If there are still incomplete phases:**

Display the next phase information:
```
📍 Next: Phase {X}: {phase_name}
   Agent: {agent}
   Estimated: {X} min
```

**If the next phase requires manual action:**
Display:
```
🛑 Next phase requires your action
When done: /cdev {change-id} --continue
```

**If the next phase is an agent:**
Ask the user:
```
Continue? (yes/no)
```

---

**Key points:**
- Main Claude updates flags.json (sub-agents don't have access)
- Update happens immediately after sub-agent responds
- Update happens before asking user to continue

**Correct flow:**
```
Agent completes → Update flags.json → Report progress → Ask user to continue
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
