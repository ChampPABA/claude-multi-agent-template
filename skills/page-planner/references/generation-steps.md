# Generation Steps

Complete step-by-step process for generating page plans.

---

## STEP 1: Detect Change Context

1. Determine change ID:
   - Check command argument for change ID
   - If not provided, find most recently modified change in `openspec/changes/`

2. If no change found:
   ```
   ❌ No active change found. Run after OpenSpec generates proposal.md
   ```
   → Stop

3. Set output path: `openspec/changes/{changeId}/page-plan.md`

---

## STEP 2: Read Context Files

### Required Files
- `openspec/changes/{changeId}/proposal.md`
- `openspec/changes/{changeId}/tasks.md`
- `openspec/changes/{changeId}/.claude/phases.md`
- `design-system/data.yaml`

### User Files
Extract files with `@` prefix from user message.

### Load Process
1. Read all context files
2. Join with separator
3. Store proposal, tasks, phases separately for analysis
4. Extract design tokens from data.yaml:
   - Primary color
   - Spacing scale
   - Component library
   - Shadows

---

## STEP 3: Search Existing Components

Search patterns for common components:
- Navbar/Navigation: `**/{Navbar,Navigation}*.{tsx,jsx,vue}`
- Footer: `**/{Footer}*.{tsx,jsx,vue}`
- Sidebar/Drawer: `**/{Sidebar,Drawer}*.{tsx,jsx,vue}`
- Header: `**/{Header}*.{tsx,jsx,vue}`

For each found:
- Extract component name
- Store file path
- Find exported functions

---

## STEP 4: Generate Plan Sections

### 4.1: Component Plan

**Reuse Components:**
```markdown
### 🔄 Reuse Components (Found in codebase)
- **Navbar**
  - Path: `/components/Navbar.tsx`
  - Usage: `<Navbar />`
```

**New Shared Components:**
```markdown
### ✅ Create New Components
#### Shared Components
- **Footer**
  - Purpose: Site-wide footer
  - Store at: `/components/Footer.tsx`
```

**New Specific Components:**
```markdown
#### Page-Specific Components
- **HeroSection**
  - Purpose: Landing page hero
  - Store at: `/app/landing/HeroSection.tsx`
```

### 4.2: Page Structure

```tsx
<Layout>
  <Navbar />        {/* Reuse */}
  <HeroSection />   {/* New specific */}
  <FeatureGrid />   {/* New specific */}
  <Footer />        {/* New shared */}
</Layout>
```

### 4.3: Layout Wireframe

Generate ASCII art for:
- Desktop (>1024px)
- Tablet (768-1023px)
- Mobile (<768px)

Include:
- Container sizes
- Grid columns
- Spacing values

### 4.4: Animation Blueprint

From data.yaml, define:
- Button animations (hover, active, loading)
- Card animations (hover, active)
- Input animations (focus, error)
- Navigation animations
- Modal animations

### 4.5: UI States

For each interactive component:
- Empty state (message + CTA)
- Loading state (skeleton/spinner)
- Success state (confirmation)
- Error state (message + retry)
- Disabled state (explanation)

### 4.6: Asset Checklist

**Images:**
- Filename, dimensions
- WebP format
- Responsive sizes
- Loading strategy
- Alt text

**Icons:**
- SVG format preferred
- Optimization notes

---

## STEP 5: Write Output

1. Write to `openspec/changes/{changeId}/page-plan.md`

2. Report summary:
   ```
   ✅ Page plan generated!

   📄 Output: openspec/changes/{changeId}/page-plan.md

   📊 Summary:
   - Found components: X (reuse)
   - New shared: Y
   - New specific: Z
   - Assets needed: N
   ```

3. Next steps:
   - Review page-plan.md
   - Prepare assets
   - Run /csetup
