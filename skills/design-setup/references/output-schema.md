# Output Schema: data.yaml

**Location:** `design-system/data.yaml`
**Populate via:** [extract-mapping.md](extract-mapping.md)

## Root-Level Sections (all required)

```yaml
meta:
  generated_at: "{ISO}"
  source_sites: ["{site1}", "{site2}"]     # all extracted sites
  primary_site: "{site}"                    # user's Round 1 selection
  style: "{style_classification}"
  theme: "{theme_name}"

psychology:        # Pass through entire section from primary site's extract

style:
  name: "{style_classification}"
  characteristics: ["{from extract overview}"]
  feel: "{from design_philosophy.core_belief}"

colors:
  primary:    { DEFAULT, foreground, hover }
  secondary:  { DEFAULT, foreground, hover }
  background: { DEFAULT, muted, subtle }
  foreground: { DEFAULT, muted, subtle }
  accent:     { DEFAULT, foreground }
  semantic:   { success, warning, error, info }
  transparency: [{value, usage}]            # dark themes only

typography:
  font_family: { sans, heading, mono }
  font_size:   { xs, sm, base, lg, xl, 2xl, 3xl, 4xl, 5xl }
  font_weight: { normal, medium, semibold, bold }

spacing:
  base: "{grid_base}px"
  scale: [values]

layout:
  container_width: "{px}"
  grid_columns: 12
  breakpoints: { mobile, tablet, desktop }

border_radius: { DEFAULT, sm, md, lg, full }
shadows:       { sm, md, lg }

animations:
  durations: { fast, normal, slow }
  easing:    { default, bounce }
  libraries: [{name, usage}]
  component_animations: { button_hover, card_hover, input_focus }
  scroll_animations:    { enabled, patterns }
  keyframes: [{name, css}]

theme:
  name: "{from Round 3}"
  decorative_elements: { use: [], avoid: [] }
  icons_suggestion: ["{Lucide names}"]

icons:         { system, sizes, style }
accessibility: { contrast_ratios, focus_approach }
feedback:      { error_color, success_color, warning_color, toast_library }
css_variables: {}    # pass through from extract if present
```

Values in `{}` are mapped from extract data — see extract-mapping.md for exact field paths.

---

## README.md (~100 lines)

Sections: Overview, Color Palette, Typography, Spacing, Shadows & Borders, Theme Direction, Animations, Accessibility, Critical Rules (DO: use data.yaml tokens / DON'T: hardcode hex), Next Steps.

---

## patterns/*.md (80-120 lines each)

Each file: variants with TSX, sizes (sm/md/lg), states (default→hover→focus). Use extract's computed styles and transition values directly — don't improvise.

Only create a pattern file if the extract has data for it. Skip scroll-animations.md if no scroll animations were detected.

| File | Variants | States |
|------|----------|--------|
| `buttons.md` | 3-4 variants, 3 sizes | Hover + focus with transition from extract |
| `cards.md` | 3 variants | Hover effect with shadow transition |
| `forms.md` | 3 input types | Focus ring + validation (error/success from feedback) |
| `scroll-animations.md` | Only if selected in Round 2 | Implementation with Intersection Observer or library |
| `decorations.md` | 3 theme USE elements | TSX with data.yaml token references |
