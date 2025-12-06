# Page Planning System

> **Detailed guide to /pageplan command**
> **Source:** Extracted from CLAUDE.md (Navigation Hub)
> **Version:** 1.4.0

---

## 📋 What is /pageplan?

**Problem it solves:**
- ❌ Before: Agent creates UI without knowing existing components → duplicates Navbar 3 times
- ❌ Before: Agent uses random colors, spacing → Landing page `#0d7276`, Dashboard `#4f46e5` (inconsistent!)
- ❌ Before: Agent uses lorem ipsum → No real content

**Solution: /pageplan command**
- ✅ Searches existing components BEFORE implementing
- ✅ Generates component reuse plan (Navbar ✅ reuse, HeroSection ❌ create)
- ✅ AI drafts real content from PRD (headlines, descriptions)
- ✅ Creates asset checklist for user to prepare (images, icons)

---

## How It Works

```bash
# Step 1: OpenSpec generates proposal
User: "Build landing page"
→ proposal.md + tasks.md

# Step 2: Generate page plan
User: /pageplan @prd.md @project_brief.md

Main Claude:
1. Reads user-specified files (@prd.md, @brief.md)
2. Reads proposal.md (technical architecture)
3. Reads data.yaml (design tokens)
4. Searches existing components (Glob/Grep)
5. Generates: openspec/changes/{id}/page-plan.md
   - 🔄 Reuse: Navbar, Footer (found)
   - ✅ New: HeroSection, FeatureGrid (create)
   - 📝 Content draft (AI-generated from PRD)
   - 📦 Asset checklist (user prepares)

# Step 3: User reviews & prepares
→ Edit content draft
→ Prepare assets (images, icons)
→ Approve page-plan.md

# Step 4: Setup & implement
User: /csetup landing-page
User: /cdev landing-page

→ uxui-frontend agent:
  - STEP 0.5: Reads page-plan.md ✅
  - STEP 3: SKIP component search (page-plan did it!) ⚡
  - Implements: Reuse Navbar, create HeroSection
  - Uses: Real content from page-plan
  - References: Assets user prepared
```

---

## page-plan.md Structure

```markdown
# Page Plan: Landing Page

## 1. Component Plan
🔄 Reuse: Navbar, Footer (found in codebase)
✅ New Shared: (none)
✅ New Specific: HeroSection, FeatureGrid, TestimonialCarousel

## 2. Page Structure
<Layout>
  <Navbar /> {/* Reuse */}
  <HeroSection /> {/* New - content below */}
  <FeatureGrid /> {/* New - content below */}
  <Footer /> {/* Reuse */}
</Layout>

## 3. Assets to Prepare (คุณต้องเตรียม)
- [ ] hero-image.jpg (1920x1080)
- [ ] logo.svg (200x60)
- [ ] feature-icons (3x 24x24 SVG)

## 4. Content Draft (AI-Generated - กรุณา Review & Edit)
**Headline:** "Master TOEIC with AI-Powered Tests"
**Subheadline:** "Experience exam-quality questions..."
**CTA:** "Start Free Test"
...
```

---

## Benefits

| Before (No page-plan) | After (With page-plan) |
|----------------------|------------------------|
| ❌ Agent guesses structure | ✅ Clear structure defined |
| ❌ Duplicate components | ✅ Reuse existing components |
| ❌ Inconsistent design | ✅ Sync with data.yaml |
| ❌ Lorem ipsum content | ✅ Real content from PRD |
| ❌ Missing assets | ✅ Asset checklist prepared |
| ❌ Agent wastes time searching | ✅ Search done once upfront (25% faster) |

---

## When to Use

```
✅ Use /pageplan for:
- Landing pages
- Dashboards
- Multi-section UI pages
- Any task with multiple components

❌ Skip /pageplan for:
- Backend API endpoints
- Database schemas
- Simple single-component tasks
- Non-UI work
```

---

## Integration with data.yaml

```
data.yaml      → Design tokens (colors, spacing, shadows, psychology)
page-plan.md   → Content structure (sections, components, assets)

uxui-frontend agent combines both:
- Colors from data.yaml (#0d7276)
- Content from page-plan ("Master TOEIC...")
- Result: Consistent + Real content
```

---

## 🔗 See Also

- `../../commands/pageplan.md` - /pageplan command implementation
- `../../commands/designsetup.md` - /designsetup command (generates data.yaml + README.md)
- `../../contexts/patterns/ui-component-consistency.md` - Component reuse patterns
- `../../contexts/patterns/frontend-component-strategy.md` - When to create vs reuse
- `../document-loader.md` - Token-efficient loading patterns
