# Generation Steps

After user confirms selections, generate the design system files.

---

## STEP 5.5: Generate data.yaml

### Build Tokens Data Structure

**1. Meta:**
```yaml
meta:
  generated_at: "{ISO timestamp}"
  source_site: "{selectedStyle.site}"
  style: "{selectedStyle.style}"
  theme: "{selectedTheme.name}"
```

**2. Style:**
```yaml
style:
  name: "{selectedStyle.style}"
  confidence: {confidence}
  characteristics: [list]
  feel: "{feel}"
  source_site: "{site}"
```

**3. Theme:**
```yaml
theme:
  name: "{selectedTheme.name}"
  description: "{description}"
  feeling: "{feeling}"
  decorative_elements:
    use: [list of elements to use]
    avoid: [list of elements to avoid]
  icons_suggestion: [Lucide icon names]
```

**4. Animations:**
```yaml
animations:
  enabled: true/false
  libraries: [list]
  selected_patterns: [user selections]
  scroll_animations:
    enabled: true/false
    patterns: [list]
  component_animations:
    button_hover: "{effect}"
    card_hover: "{effect}"
    input_focus: "ring"
  duration:
    fast: "150ms"
    normal: "200ms"
    slow: "300ms"
  easing:
    default: "ease-in-out"
    bounce: "cubic-bezier(0.68, -0.55, 0.265, 1.55)"
```

**5. Colors:**
```yaml
colors:
  primary:
    DEFAULT: "{hex}"
    foreground: "#ffffff"
    hover: "{darkened hex}"
  secondary:
    DEFAULT: "{hex}"
    foreground: "#ffffff"
  background:
    DEFAULT: "#ffffff"
    muted: "#f1f5f9"
    subtle: "#f8fafc"
  foreground:
    DEFAULT: "#0a0a0a"
    muted: "#64748b"
  semantic:
    success: "#10b981"
    warning: "#f59e0b"
    error: "#ef4444"
    info: "#3b82f6"
```

**6. Typography:**
```yaml
typography:
  font_family:
    sans: "{font from extraction}"
    mono: "'Fira Code', monospace"
  font_size:
    xs: "12px"
    sm: "14px"
    base: "16px"
    lg: "18px"
    xl: "20px"
    2xl: "24px"
  font_weight:
    normal: "400"
    medium: "500"
    semibold: "600"
    bold: "700"
```

**7. Spacing:**
```yaml
spacing:
  scale: [4, 8, 12, 16, 24, 32, 48, 64]
  grid_base: "8px"
```

**8. Psychology (from extraction):**
```yaml
psychology:
  style_classification: "{style}"
  emotions_evoked:
    - emotion: "{emotion}"
      reason: "{reason}"
  target_audience:
    primary:
      description: "{desc}"
      age_range: "{range}"
  why_it_works:
    - "{reason 1}"
    - "{reason 2}"
```

---

## STEP 5.6: Generate patterns/*.md

### buttons.md
- Primary, Secondary, Ghost, Outline, Icon variants
- Small, Medium, Large sizes
- Hover animations based on selection

### cards.md
- Default, Interactive, Feature, Pricing, Testimonial variants
- Hover effects based on selection

### forms.md
- Input, Error input, Select, Checkbox
- Form layout examples

### scroll-animations.md
- Fade In on Scroll
- Stacking Cards (GSAP)
- Parallax Section
- Slide In from Side

### decorations.md
- Gradient backgrounds
- Blob shapes
- Grid patterns
- Floating elements
- Dividers

Each file includes:
- Header with source, style, when to load
- TSX code examples
- Usage guidelines

---

## STEP 5.7: Generate README.md

Human-readable guide (~100 lines) with:

1. **Overview** - Style + theme description
2. **Color Palette** - All colors with usage
3. **Typography** - Font family, sizes, weights
4. **Spacing System** - Base unit, scale
5. **Shadows** - Elevation levels
6. **Border Radius** - Values and usage
7. **Theme** - Decorative direction (USE/AVOID)
8. **Animations** - Enabled patterns
9. **Component Library** - Recommended (shadcn/ui)
10. **Code Patterns** - Links to pattern files
11. **Critical Rules** - DO and DON'T

---

## STEP 6: Final Report

Display completion summary:
- Style selected
- Theme selected
- Files created (data.yaml, README.md, patterns/*.md)
- Next steps (/pageplan, /csetup, /cdev)
