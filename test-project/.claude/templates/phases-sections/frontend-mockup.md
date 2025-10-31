# Phase: Frontend Mockup

**Agent:** `uxui-frontend`
**Metadata:** `| design-work | TDD | mockup |`
**Estimated time:** 90 minutes

## 📚 Context Loading Strategy

**Tier 1 - Critical (Always Load):**
- ✅ `tech-stack.md` → Package manager, React/Next.js versions
- ✅ `project.md` (Code Conventions, Testing Strategy sections)
- ✅ `ui-component-consistency.md` → Visual consistency patterns

**Tier 2 - Conditional (Metadata: design-work):**
- ✅ `design/index.md` → Design system overview
- ✅ `design/box-thinking.md` → Layout analysis
- ✅ `design/color-theory.md` → Color usage
- ✅ `design/spacing.md` → Spacing scale (8, 16, 24, 32, 40, 48px)

**Tier 3 - Skip (Not Needed):**
- ❌ `error-handling.md` → Not needed for mockup (no real API)
- ❌ `logging.md` → Not production code yet

**Token estimate:** ~7,000 tokens (vs 15,000 without filtering)

## 🎯 Purpose

Create UI components with mockup data. Focus on visual design, layout, and user experience without backend integration.

## 📝 Agent-Specific Instructions

**MANDATORY PRE-WORK (STEP 0-5 from CLAUDE.md):**

1. **Project Discovery:**
   - Read: `domain/index.md` → Get project name
   - Read: `domain/project/README.md` → Get core stack
   - Read: `domain/project/best-practices/index.md` → Get relevant practices
   - Read relevant best practices files

2. **Change Context:**
   - Read: `../proposal.md` → Business requirements
   - Read: `../.claude/context.md` → Change-specific tech

3. **Design Contexts (design-work flag):**
   - Read ALL design contexts (listed in Tier 2 above)

4. **Box Thinking Analysis:**
   - Identify boxes: containers, children, siblings
   - Document relationships: nested, adjacent
   - Plan space flow: spacing scale
   - Plan responsive: stack/merge/compress

5. **Search for Existing Components:**
   ```bash
   Glob: "**/*{Keyword}*.{tsx,jsx,vue}"
   Grep: "[similar-pattern]"
   ```
   - Decision: Reuse > Compose > Extend > Create New
   - Extract design tokens from similar components

6. **Report Pre-Implementation:**
   Provide detailed report covering steps 1-5 BEFORE writing code.

**IMPLEMENTATION:**

- Use **mockup data** for all dynamic content
- Follow TDD if applicable (see testing.md)
- Visual consistency: match existing components
- Loading states: skeleton loaders
- Error states: user-friendly messages (mockup errors)
- Responsive design: test 3 breakpoints minimum

**CRITICAL RULES:**
- ❌ NO hardcoded colors → ✅ Use theme tokens
- ❌ NO arbitrary spacing → ✅ Use spacing scale
- ❌ NO inconsistent icons → ✅ Match reference components
- ❌ NO creating duplicate components → ✅ Search and reuse first

## ✅ Success Criteria

- [ ] UI components created with mockup data
- [ ] Responsive design implemented (3 breakpoints)
- [ ] Visual consistency matches design system
- [ ] Component reuses existing UI primitives
- [ ] No hardcoded colors or spacing values
- [ ] Pre-implementation analysis completed

## 📤 Output

**Files created/modified:**
- List all component files created
- List all files modified

**Update flags.json:**
```json
{
  "phases": {
    "frontend_mockup": {
      "status": "completed",
      "completed_at": "{ISO-timestamp}",
      "actual_minutes": {duration},
      "tasks_completed": ["{task-ids}"],
      "files_created": ["{file-paths}"],
      "notes": "Summary of work done"
    }
  }
}
```

**Report to user:**
```
✅ Phase 1: Frontend Mockup completed!

⏱️ Time: {actual} minutes (estimated: 90)

📁 Files created:
{list-of-files}

✓ Tasks completed:
{list-of-task-ids}

📍 Next phase: #2 Accessibility Test (test-debug agent)
```
