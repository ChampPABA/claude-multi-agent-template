# Extract → Output Mapping

Source: `design-system/extracted/*/data.yaml` (17 sections + psychology + animations)

## Multi-Site Merge

User selects **primary site** in Round 1. Data comes from:

| Data | Source |
|------|--------|
| Colors, typography, spacing, borders, shadows, components, icons, psychology | Primary site |
| Animations | Union ALL sites → user picks in Round 2 |
| Accessibility | Best values across all sites |
| Feedback/loading | Primary, supplement from others if missing |
| CSS custom properties | Primary only |

---

## Field Mapping

### Colors

| Extract → Output | Logic |
|-----------------|-------|
| `color_palette.primary[0].hex` → `colors.primary.DEFAULT` | Highest usage count |
| darken DEFAULT 10% → `colors.primary.hover` | Computed |
| contrast color → `colors.primary.foreground` | Based on luminance |
| `color_palette.primary[1].hex` → `colors.secondary.DEFAULT` | 2nd highest |
| `color_palette.background_colors[0-2]` → `colors.background.{DEFAULT,muted,subtle}` | By count |
| `color_palette.text_colors[0-2]` → `colors.foreground.{DEFAULT,muted,subtle}` | By count |
| `color_palette.accent[0]` → `colors.accent.DEFAULT` | First accent |
| `color_palette.transparency_layers` → `colors.transparency` | Pass through |
| `feedback_states.{error,success,warning}.color` → `colors.semantic.*` | Fallback: #ef4444/#22c55e/#f59e0b |

### Typography

| Extract → Output | Logic |
|-----------------|-------|
| `typography.fonts[0]` → `font_family.{sans,heading}` | First = primary |
| font matching "mono"/"code" → `font_family.mono` | Fallback: Fira Code |
| `typography.sizes[]` → `font_size.{xs..5xl}` | Sort ascending, map xs=smallest, base≈16px |
| `typography.weights[]` → `font_weight` | 400=normal, 500=medium, 600=semibold, 700=bold |

### Spacing, Layout, Shadows, Borders

| Extract → Output |
|-----------------|
| `spacing_system.grid_base` → `spacing.base` |
| `spacing_system.common_values` → `spacing.scale` |
| `layout_patterns.{container_width,grid_columns,breakpoints}` → `layout.*` |
| `shadows_elevation.values[]` → `shadows.{sm,md,lg}` (sort by spread) |
| `border_radius.primary_radius` → `border_radius.DEFAULT` |
| `border_radius.values[]` → `border_radius.{sm,md,lg,full}` (9999px→full) |

### Animations

| Extract → Output |
|-----------------|
| shortest/median/longest transition duration → `durations.{fast,normal,slow}` |
| `easing_signature` → `easing.default` |
| `libraries[]` (detected=true) → `animations.libraries` |
| `animations.{component}.description` → `component_animations` |
| User-selected (Round 2) → `scroll_animations` + `keyframes` |

### Other Sections

| Extract → Output |
|-----------------|
| `psychology.*` → pass through entire section |
| `icons_imagery.{system,common_sizes,style}` → `icons.*` |
| `accessibility.{contrast_ratios,focus_styles}` → `accessibility.*` |
| `feedback_states.toast_pattern.library` → `feedback.toast_library` |
| `css_custom_properties` → `css_variables` (if present) |
| `theme` from Round 3 → `theme.{name,decorative_elements,icons_suggestion}` |
