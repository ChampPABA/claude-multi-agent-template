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

#### ขั้นตอนที่ 1: อ่าน flags.json

อ่านไฟล์ `openspec/changes/{change-id}/.claude/flags.json`

จดข้อมูลต่อไปนี้:
- `current_phase`: ชื่อ phase ปัจจุบัน
- `phases[current_phase].status`: สถานะของ phase
- `phases[current_phase].agent`: agent ที่ต้องใช้

---

#### ขั้นตอนที่ 2: ตรวจสอบสถานะ phase

**ถ้า status = "completed":**
- หา phase ถัดไปจาก phases.md
- อัพเดต current_phase เป็น phase ถัดไป

**ถ้า status = "pending" หรือ "in_progress":**
- ใช้ phase ปัจจุบัน

---

#### ขั้นตอนที่ 3: Report สถานะ

```
📍 Current Phase: {phase_number} - {phase_name}
   Agent: {agent}
   Status: {status}
```

---

### Step 3: Check Phase Type

---

#### ตรวจสอบว่า phase ต้องการ manual action หรือไม่

**ถ้า agent = "user":**
```
🛑 Phase {phase_number} requires manual action

Instructions:
{instructions from phases.md}

When done: /cdev {change-id} --continue
```
→ หยุดทำงาน รอ user ทำเสร็จแล้ว run /cdev ใหม่

---

#### ตรวจสอบว่ามี agent หลายตัวหรือไม่

**ถ้า agent มีเครื่องหมาย "+" (เช่น "backend + database"):**
- แยก agents ออกมาเป็น list
- Invoke agents พร้อมกัน (parallel)
- รอทุก agent เสร็จก่อนไปต่อ

**ถ้ามี agent ตัวเดียว:**
- Invoke agent ตัวนั้น
- รอเสร็จแล้วไป Step 4

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

**เมื่อไหร่ต้องทำ:** ก่อน invoke uxui-frontend หรือ frontend agent ทุกครั้ง

---

#### ขั้นตอนที่ 1: ตรวจสอบว่าเป็น visual agent หรือไม่

ดู phase.agent ว่าเป็น `uxui-frontend` หรือ `frontend` หรือไม่

**ถ้าไม่ใช่:** ข้าม Step 4.0 ไปเลย

**ถ้าใช่:** ทำขั้นตอนถัดไป

---

#### ขั้นตอนที่ 2: ตรวจสอบว่ามี design system หรือไม่

อ่านไฟล์ `design-system/data.yaml`

**ถ้ามีไฟล์:**
```
✅ Design system found: design-system/data.yaml
```
→ ไปขั้นตอนที่ 3

**ถ้าไม่มีไฟล์:**
```
⚠️ WARNING: No design system found!
   Path: design-system/data.yaml (not found)

   Options:
   1. Run /designsetup first (recommended)
   2. Continue with fallback design principles

   Proceeding with fallback...
```
→ ไปขั้นตอนที่ 4 โดยไม่ inject instruction

---

#### ขั้นตอนที่ 3: บอก agent ให้อ่าน design system

เมื่อ invoke agent ต้องบอกใน prompt ว่า:

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

#### ขั้นตอนที่ 4: Verify agent compliance หลัง agent ตอบกลับ

ตรวจสอบว่า agent output มี report นี้หรือไม่:

```
✅ Design System Loaded (STEP 0.5)
   - Source: design-system/data.yaml
   - Colors: [list]
   - Spacing: [list]
   - Animation: [list]
```

**ถ้ามี report:** ผ่าน ไปต่อได้

**ถ้าไม่มี report:** ถาม agent ว่าอ่าน design system หรือยัง

---

### Step 4.1: Build Agent Prompt

**สร้าง prompt สำหรับ agent โดยประกอบด้วย:**

---

#### ส่วนที่ 1: Change Context

ประกอบข้อมูลจาก:
- `proposal.md` - What we're building and why
- `tasks.md` - Tasks for this phase
- `design.md` - Design decisions (if exists)
- `phases.md` - Phase instructions

---

#### ส่วนที่ 2: Library Requirements (v2.1.2)

เพิ่มคำสั่งให้ agent:
1. Scan tasks.md หา patterns: "Install X", "Configure X"
2. Scan design.md หา: "D1: Use X Library", "Decision: Use X"
3. ใช้ libraries ที่ระบุ ไม่ใช่ custom implementation
4. Implement ตาม design spec ไม่ใช่ library defaults

---

#### ส่วนที่ 3: Development Principles (v3.1.0 - ALL agents)

**ถ้ามีไฟล์** `.claude/contexts/patterns/development-principles.md`:

เพิ่มใน prompt:
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

#### ส่วนที่ 4: Best Practices (agent-specific)

**ถ้ามี directory** `.claude/contexts/domain/project/best-practices/`:

หา best-practices files ที่ตรงกับ agent:

| Agent | Relevant Topics |
|-------|-----------------|
| uxui-frontend | react, nextjs, vue, tailwind |
| frontend | react, nextjs, vue, typescript |
| backend | express, fastapi, django, prisma, drizzle |
| database | prisma, drizzle, postgres, mongodb |
| test-debug | vitest, jest, playwright |
| integration | typescript |
| ux-tester | (none) |

เพิ่มใน prompt:
```
## 📚 Best Practices (STEP 0)

Read these files before implementation:
- Read: .claude/contexts/domain/project/best-practices/{relevant-file}.md
```

---

#### ส่วนที่ 5: Design System (uxui-frontend only)

**ถ้า agent = uxui-frontend:**

**ถ้ามี** `design-system/data.yaml`:
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

**ถ้าไม่มี:**
```
⚠️ WARNING: No design system found!
Using fallback: .claude/contexts/design/*.md
```

---

### Step 4.2: Execute Agent with Retry

---

#### การ invoke agent

Report ก่อน invoke:
```
🚀 Invoking {agent} agent (model: opus)...
```

Invoke agent ด้วย:
- Model: opus (fixed)
- Timeout: 10 นาที
- Max retries: 2 ครั้ง

---

#### Handle Result

**ถ้าสำเร็จ:**
```
✅ Phase {phase_number} completed successfully!
⏱️ Execution time: {time}s
🔄 Retries used: {retries}
✅ Validation: PASSED
```
→ ไป Step 5

**ถ้าล้มเหลว:**
```
❌ Phase {phase_number} failed
Error: {error}
Retries used: {retries}
```

ถาม user:
```
Options:
[retry] - ลองใหม่
[skip]  - ข้าม phase นี้
[abort] - หยุดทำงาน
```

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

**สำหรับ phases ที่มี** `requires_approval: true` (เช่น ux-tester Phase 1.5)

---

#### ขั้นตอนที่ 1: ตรวจสอบว่า phase ต้องการ approval หรือไม่

ดูใน phases.md ว่า phase ปัจจุบันมี:
- `requires_approval: true`
- หรือ metadata มีคำว่า `approval-gate`

**ถ้าไม่ต้องการ approval:** ข้าม Step 4.6 ไปเลย

**ถ้าต้องการ approval:** ทำขั้นตอนถัดไป

---

#### ขั้นตอนที่ 2: แสดงผลและรอ user ตัดสินใจ

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧪 {phase_name} Complete - Awaiting Approval
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{result_summary}

📄 Full report: openspec/changes/{change-id}/ux-test-report.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

กรุณาตัดสินใจ:

✅ "approve" → ไป Phase ถัดไป
❌ "reject [feedback]" → กลับแก้ไข Phase ก่อนหน้า

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

→ หยุดรอ user ตอบ

---

#### ขั้นตอนที่ 3: Handle user response

**ถ้า user ตอบ approve:**
- คำที่ยอมรับ: approve, approved, ok, yes, ใช่, อนุมัติ, ผ่าน, ลุย, ได้, ดี
- Output: `✅ {phase_name} approved! Continuing to next phase...`
- อัพเดต flags.json: status = "approved"
- ไป Step 5

**ถ้า user ตอบ reject:**
- คำที่ยอมรับ: reject, ไม่, แก้, no (ตามด้วย feedback)
- ดึง feedback จาก message
- หา phase ที่ต้องกลับไปแก้ (uxui-frontend)
- Output:
```
🔄 {phase_name} rejected

📝 Feedback: {feedback}
🔙 Looping back to: Phase {X} - {phase_name}

{agent} agent จะได้รับ feedback นี้เพื่อแก้ไข
```
- อัพเดต flags.json: status = "rejected"
- กลับไป run phase ที่ต้องแก้ไข

**ถ้าไม่เข้าใจคำตอบ:**
```
⚠️ ไม่เข้าใจคำตอบ กรุณาตอบ "approve" หรือ "reject [feedback]"
```
→ ถาม user อีกครั้ง

---

**See:** `.claude/lib/agent-executor.md` → "Approval Gate Execution" section for complete flow

---

### Step 4.7: Validate Page Plan Compliance (uxui-frontend only)

**เฉพาะ uxui-frontend agent เมื่อมี page-plan.md**

**Purpose:** ตรวจสอบว่า agent implement ครบทุก section ตาม page-plan.md

---

#### ขั้นตอนที่ 1: ตรวจสอบเงื่อนไข

**ถ้า agent ไม่ใช่ uxui-frontend หรือไม่มี page-plan.md:**
```
ℹ️ Page plan validation: N/A (agent: {agent}, has plan: {true/false})
```
→ ข้าม Step 4.7 ไปเลย

**ถ้า agent = uxui-frontend และมี page-plan.md:**
→ ทำขั้นตอนถัดไป

---

#### ขั้นตอนที่ 2: วิเคราะห์ page-plan.md

อ่าน `openspec/changes/{change-id}/page-plan.md`

หา Section 2 (Page Structure) และนับจำนวน components:
- ดู JSX elements ที่ขึ้นต้นด้วยตัวใหญ่ (เช่น `<HeroSection>`, `<PricingTable>`)
- ไม่นับ Layout, div (wrapper elements)
- Remove duplicates

Report:
```
📋 Page Plan Analysis:
   Expected sections: {count}
   Components: {list}
```

---

#### ขั้นตอนที่ 3: ถาม user ยืนยัน

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

---

#### ขั้นตอนที่ 4: Handle user response

**ถ้า user ตอบ yes:**
```
✅ Page plan compliance confirmed
   All {count} sections implemented
```
→ ไป Step 5

**ถ้า user ตอบ retry:**
```
🔄 Retrying phase with enhanced enforcement...
Agent will be explicitly instructed to implement all {count} sections
```
→ กลับไป run phase อีกครั้งพร้อม enhanced prompt

**ถ้า user ตอบ skip:**
```
⚠️ Skipping validation - proceed with caution
   This may result in incomplete implementation
```
→ ไป Step 5

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

**Main Claude อัพเดต flags.json หลังจบแต่ละ phase**

→ See: `.claude/lib/flags-updater.md` for complete protocol

WHY: Immediate updates ensure /cstatus shows accurate progress.

---

#### ขั้นตอนที่ 1: อัพเดต flags.json

```
🔄 Updating progress tracking...
```

อัพเดตข้อมูลต่อไปนี้:
- Mark phase as completed
- Record actual duration
- Extract files created/modified
- Update meta statistics (progress %, time remaining)
- Move current_phase to next phase

---

#### ขั้นตอนที่ 2: Report Progress

```
📊 Progress Update:
   ✅ {completed}/{total} phases complete
   📈 {percentage}% progress
   ⏱️  {time_spent} spent
   ⏱️  {time_remaining} remaining
```

---

#### ขั้นตอนที่ 3: Check next phase

**ถ้าทุก phases เสร็จหมดแล้ว (ready_to_archive):**

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

**ถ้ายังมี phases ที่ยังไม่เสร็จ:**

```
📍 Next: Phase {X}: {phase_name}
   Agent: {agent}
   Estimated: {X} min
```

**ถ้า next phase ต้องการ manual action:**
```
🛑 Next phase requires your action
When done: /cdev {change-id} --continue
```

**ถ้า next phase เป็น agent:**
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
