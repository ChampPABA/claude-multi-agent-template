# Design Validator

> **Version:** 1.1.0 - Imperative Instructions (No Pseudocode)
> **Purpose:** Single Source of Truth for Design System Validation
> **Used by:** Main Claude, uxui-frontend, ux-tester

---

## Overview

This file defines **mandatory steps** for design system compliance.

```
PREVENTION (Before Implementation)
├── Main Claude: Pre-Flight Check before invoking uxui-frontend
└── uxui-frontend: STEP 0.5 - Read data.yaml, report tokens

DETECTION (After Implementation)
└── ux-tester: Step 5.5 - agent-browser style comparison
```

---

## Part 1: Design Token Locations

**Primary source (project-specific):**
```
design-system/data.yaml
```

**Fallback (universal principles):**
```
.claude/contexts/design/*.md
```

**Page-specific plan:**
```
openspec/changes/{changeId}/page-plan.md
```

---

## Part 2: Main Claude Pre-Flight Check

**เมื่อไหร่ต้องทำ:** ก่อน invoke uxui-frontend หรือ frontend agent ทุกครั้ง

**ขั้นตอนที่ต้องทำ:**

### 2.1 ตรวจสอบว่ามี design system หรือไม่

อ่านไฟล์ `design-system/data.yaml`

**ถ้ามีไฟล์:**
```
✅ Design system found: design-system/data.yaml
```
→ ไปขั้นตอน 2.2

**ถ้าไม่มีไฟล์:**
```
⚠️ WARNING: No design system found!
   Path: design-system/data.yaml (not found)

   Options:
   1. Run /designsetup first (recommended)
   2. Continue with fallback design principles

   Proceeding with fallback...
```
→ ไปขั้นตอน 2.3 แต่ใช้ fallback

### 2.2 บอก agent ให้อ่าน design system

เมื่อ invoke agent ต้องบอกในส่วน prompt ว่า:

```
MANDATORY: Read design-system/data.yaml before writing any CSS/Tailwind.
Report the tokens you loaded before starting implementation.
```

### 2.3 Verify agent compliance

หลัง agent ตอบกลับ ตรวจสอบว่ามี report นี้หรือไม่:

```
✅ Design System Loaded
   - Source: design-system/data.yaml
   - Colors: [list]
   - Spacing: [list]
   - Animation: [list]
```

**ถ้าไม่มี report:** ถาม agent ว่าอ่าน design system หรือยัง

---

## Part 3: uxui-frontend STEP 0.5 (MANDATORY)

**ขั้นตอนที่ agent ต้องทำก่อนเขียน code:**

### 3.1 อ่าน design-system/data.yaml

อ่านไฟล์ `design-system/data.yaml`

**ถ้ามีไฟล์:** จด tokens ต่อไปนี้:
- colors (primary, secondary, background, foreground, muted, accent)
- spacing scale (4, 8, 12, 16, 24, 32, 48, 64)
- animation durations (150ms, 300ms, 500ms เท่านั้น!)
- shadows (sm, md, lg, xl)
- borderRadius scale

**ถ้าไม่มีไฟล์:**
```
⚠️ Design System NOT FOUND
   - Path: design-system/data.yaml (missing)
   - Fallback: Using .claude/contexts/design/*.md
   - Recommendation: Run /designsetup to generate design system
```
→ อ่าน `.claude/contexts/design/*.md` แทน

### 3.2 Report ก่อนเริ่มเขียน code

**ต้อง report นี้ก่อนเขียน CSS/Tailwind ใดๆ:**

```
✅ Design System Loaded (STEP 0.5)
   - Source: design-system/data.yaml
   - Colors: primary=#xxx, secondary=#xxx, background=#xxx, foreground=#xxx
   - Spacing scale: 4, 8, 12, 16, 24, 32, 48, 64
   - Animation durations: 150ms, 300ms, 500ms
   - Shadows: sm, md, lg, xl
```

### 3.3 กฎการใช้ tokens

**ห้ามใช้ (NEVER):**

| ห้าม | ตัวอย่าง |
|------|---------|
| Hardcoded colors | `#3b82f6`, `rgb(59,130,246)`, `text-blue-500` |
| Arbitrary spacing | `p-5`, `gap-7`, `m-[13px]`, `p-[22px]` |
| Random duration | `duration-200`, `duration-250`, `duration-400` |
| Mixed shadow levels | ใช้ `shadow-sm` ที่หนึ่ง `shadow-xl` ที่อื่น |

**ต้องใช้ (ALWAYS):**

| ใช้ | ตัวอย่าง |
|-----|---------|
| Theme colors | `bg-primary`, `text-foreground`, `bg-muted` |
| Spacing scale | `p-4`, `p-6`, `gap-8`, `m-16` |
| Standard durations | `duration-150`, `duration-300`, `duration-500` |
| Consistent shadows | เลือก level เดียวสำหรับ cards ทั้งหมด |

### 3.4 Report หลังเขียน code เสร็จ

**ต้อง report การใช้ tokens:**

```
📊 Design Token Usage Report
   Colors used: text-foreground, bg-primary, bg-muted, border-border
   Spacing used: p-4, p-6, p-8, gap-4, gap-8
   Animations: duration-150, duration-300
   Shadows: shadow-md (consistent)

   ✅ All tokens from data.yaml
```

**ถ้ามี non-standard values:**

```
📊 Design Token Usage Report
   ...
   ⚠️ Non-standard values used:
      - p-5 (reason: needed odd spacing for alignment)
      - #custom-color (reason: brand requirement not in data.yaml)
```

---

## Part 4: ux-tester Step 5.5 Design Compliance Check

**เมื่อไหร่ต้องทำ:** หลัง persona testing (Step 5) ก่อน generate final report (Step 6)

### 4.1 ตรวจสอบว่ามี data.yaml หรือไม่

อ่านไฟล์ `design-system/data.yaml`

**ถ้าไม่มี:**
```
ℹ️ Skipping design compliance check (no data.yaml)
```
→ ข้าม Step 5.5 ไปเลย

**ถ้ามี:** ทำขั้นตอนถัดไป

### 4.2 Load expected tokens จาก data.yaml

จดค่าที่คาดหวัง:
- Colors ทั้งหมด (พร้อม hex values)
- Animation durations: 150ms, 300ms, 500ms
- Spacing scale

### 4.3 ใช้ agent-browser ตรวจสอบ

**ขั้นตอน:**

1. Navigate ไปหน้าที่ต้องการตรวจ:
   ```bash
   agent-browser open http://localhost:xxxx
   ```

2. Take snapshot เพื่อดู DOM และ elements:
   ```bash
   agent-browser snapshot -i
   ```

3. ดู elements หลักๆ:
   - buttons (สี, padding, transition)
   - headings (font-size, color)
   - cards (shadow, border-radius, padding)
   - links (color, hover states)

4. เปรียบเทียบกับ tokens ที่คาดหวัง

### 4.4 บันทึก violations ที่พบ

**ตัวอย่าง violations:**

| Element | Property | Actual | Expected |
|---------|----------|--------|----------|
| button.cta | background-color | #3b82f6 | primary: #2563eb |
| .card | transition-duration | 200ms | 150ms หรือ 300ms หรือ 500ms |
| h1.hero | font-size | 52px | 48px (max in scale) |

### 4.5 เพิ่มใน ux-test-report.md

**เพิ่ม section นี้ใน report:**

```markdown
---

## 📐 Design Compliance Check

> Validated against: design-system/data.yaml

### Summary

| Category | Compliant | Violations | Status |
|----------|-----------|------------|--------|
| Colors | 15 | 2 | ⚠️ |
| Spacing | 20 | 0 | ✅ |
| Animation | 5 | 3 | ❌ |

### Violations Found

| Element | Property | Actual | Expected |
|---------|----------|--------|----------|
| button.cta | background | #3b82f6 | #2563eb (primary) |
| .card | duration | 200ms | 150/300/500ms |

### Quick Fixes

1. **button.cta**
   - เปลี่ยนจาก `bg-blue-500` → `bg-primary`

2. **.card transition**
   - เปลี่ยนจาก `duration-200` → `duration-150`

---
```

---

## Part 5: Quick Reference Checklist

### For Main Claude

Before invoking uxui-frontend or frontend:

- [ ] Check if `design-system/data.yaml` exists
- [ ] If exists: Tell agent to read it and report tokens
- [ ] If not exists: Warn user, suggest /designsetup
- [ ] After agent responds: Verify token report exists

### For uxui-frontend

Before writing any CSS/Tailwind:

- [ ] Read `design-system/data.yaml`
- [ ] Report loaded tokens (colors, spacing, animation, shadows)
- [ ] Use ONLY tokens from data.yaml
- [ ] NO hardcoded colors (#xxx)
- [ ] NO arbitrary spacing (p-5, gap-7)
- [ ] NO random durations (only 150/300/500ms)

After implementation:

- [ ] Report token usage
- [ ] List any non-standard values with reasons

### For ux-tester

After persona testing:

- [ ] Check if `design-system/data.yaml` exists
- [ ] If exists: Load expected tokens
- [ ] Use agent-browser to check computed styles
- [ ] Compare actual vs expected
- [ ] Add compliance section to ux-test-report.md

---

## Common Violations and Fixes

| Violation | Bad | Good |
|-----------|-----|------|
| Hardcoded color | `bg-blue-500`, `#3b82f6` | `bg-primary` |
| Arbitrary spacing | `p-5`, `gap-7` | `p-4`, `p-6`, `gap-8` |
| Wrong duration | `duration-200` | `duration-150` or `duration-300` |
| Inconsistent shadow | `shadow-sm` here, `shadow-xl` there | `shadow-md` everywhere |
| Non-scale font | `text-[52px]` | `text-5xl` (48px) |

---

## See Also

- `.claude/agents/02-uxui-frontend.md` - Agent file (STEP 0.5)
- `.claude/agents/07-ux-tester.md` - Agent file (Step 5.5)
- `.claude/commands/cdev.md` - Main Claude workflow
- `design-system/data.yaml` - Design tokens source
