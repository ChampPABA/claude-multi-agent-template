# Phase: UX Testing (Persona-Based)

**Agent:** `ux-tester`
**Metadata:** `| approval-gate | user-testing | persona-based |`
**Estimated time:** 30 minutes
**Requires Approval:** YES (blocks until user approves/rejects)

## 🎯 Purpose

ทดสอบ UI จากมุมมอง User จริง ก่อนที่จะไป Phase ถัดไป (Backend)
- Auto-generate personas จาก product context
- Test แต่ละ persona ผ่าน agent-browser
- คำนวณ weighted conversion prediction
- รอ User approve หรือ reject

## 📋 Pre-Requisites

- ✅ Phase 1 (Frontend Mockup) completed
- ✅ Dev server running (localhost:3000 or similar)
- ✅ agent-browser installed (`npx skills add vercel-labs/agent-browser`)

## 🔄 Process

### Step 1: Load Context
```bash
Read: openspec/changes/{change-id}/proposal.md
Read: openspec/changes/{change-id}/page-plan.md (if exists)
Read: openspec/changes/{change-id}/tasks.md
Read: design-system/data.yaml (if exists)
```

### Step 2: Auto-Generate Personas
- Analyze product/service from context
- Generate 3-5 personas with % breakdown
- Explain reasoning

### Step 3: Find Dev Server
- Auto-detect running server (3000, 3001, 5173, 8080)
- Error if no server found

### Step 4: Test Each Persona
For each persona:
1. Navigate to page
2. Take screenshot + snapshot
3. First impression (3 seconds)
4. Test main flow (click through)
5. Test mobile (resize to 375px)
6. Would buy? Why/why not?

### Step 5: Calculate Weighted Score
- Weight each persona's decision by their %
- Calculate total conversion prediction
- Calculate potential after fixes

### Step 6: Output Report (Inline)
Output ทุกอย่างใน response โดยตรง (ไม่สร้างไฟล์)

## ✅ Success Criteria

- [ ] Personas generated with % breakdown
- [ ] Each persona tested (desktop + mobile)
- [ ] Conversion prediction calculated
- [ ] Critical issues identified
- [ ] Recommendations with impact %
- [ ] Report generated

## 📤 Output

**Output:** Inline response (ไม่สร้างไฟล์)

**Update flags.json:**
```json
{
  "phases": {
    "ux_testing": {
      "status": "awaiting_approval",
      "completed_at": "{ISO-timestamp}",
      "actual_minutes": {duration},
      "personas_tested": {count},
      "conversion_prediction": "{percentage}",
      "critical_issues": {count}
    }
  }
}
```

## 🛑 Approval Gate

**After report generated, PAUSE and ask user:**

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧪 UX Testing Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Summary:
- Personas tested: {count}
- Conversion prediction: {percentage}%
- Critical issues: {count}
- Potential after fixes: {percentage}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

กรุณา:
1. Review report ด้านบน
2. ทดสอบ {dev-url} ด้วยตัวเอง
3. ตัดสินใจ:

✅ "approve" → ไป Phase 2 (Backend)
❌ "reject [feedback]" → กลับ Phase 1 แก้ไข

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🔄 Rejection Loop

**If user rejects:**

1. Parse feedback from rejection
2. Update flags.json:
   ```json
   {
     "phases": {
       "ux_testing": {
         "status": "rejected",
         "rejection_feedback": "{user feedback}",
         "rejection_count": 1
       },
       "frontend_mockup": {
         "status": "pending",
         "rerun_reason": "UX testing rejected: {feedback}"
       }
     }
   }
   ```
3. Loop back to Phase 1 (uxui-frontend)
4. After Phase 1 completes → Re-run Phase 1.5 (ux-testing)

## 📊 Report to User

**After approval:**
```
✅ Phase 1.5: UX Testing approved!

⏱️ Time: {actual} minutes
🧪 Personas: {count} tested
📈 Conversion: {percentage}%

📍 Next phase: Phase 2 - Backend API
```

**After rejection:**
```
🔄 Phase 1.5: UX Testing rejected

📝 Feedback: {user feedback}
🔙 Returning to: Phase 1 - Frontend Mockup

uxui-frontend agent จะได้รับ feedback นี้เพื่อแก้ไข
```
