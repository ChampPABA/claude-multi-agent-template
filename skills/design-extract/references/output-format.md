# Output Format: data.yaml

Complete schema for the extracted design data file.

---

## File Location

```
design-system/extracted/{site-name}/data.yaml
```

---

## Complete Schema

```yaml
# Design Extraction: {siteName}
# Extracted: {ISO timestamp}
# URL: {url}

meta:
  site_name: "airbnb"
  url: "https://airbnb.com"
  extracted_at: "2026-02-03T15:30:00Z"
  extractor_version: "2.1.0"
  coverage:
    total_sections: 17
    detected_sections: 15
    percentage: 88

psychology:
  style_classification: "Modern SaaS"

  brand_personality: ["professional", "minimal"]
  # Tags for design-setup match scoring. Pick from:
  # bold, professional, playful, minimal, technical, elegant, creative, warm

  emotions_evoked:
    - emotion: "Trust"
      reason: "Clean typography and ample whitespace"
    - emotion: "Excitement"
      reason: "Vibrant accent colors on CTAs"

  target_audience:
    primary:
      description: "Young professionals"
      age_range: "25-40"
      tech_savvy: "high"
    secondary:
      description: "Families"
      age_range: "30-50"

  visual_principles:
    - name: "Hierarchy"
      description: "Clear visual hierarchy through size and weight"
    - name: "Whitespace"
      description: "Generous padding creates breathing room"

  why_it_works:
    - "Large hero images create emotional connection"
    - "Simple navigation reduces cognitive load"

  design_philosophy:
    core_belief: "Design should feel human and approachable"
    key_principles:
      - "Simplicity over complexity"
      - "Content-first approach"

sections:
  overview:
    detected: true
    style: "Modern SaaS"
    tech_stack: "Framework-agnostic"

  color_palette:
    detected: true
    primary:
      - hex: "#FF5A5F"
        rgb: "rgb(255, 90, 95)"
        usage: "brand-primary"
        count: 23
      - hex: "#00A699"
        rgb: "rgb(0, 166, 153)"
        usage: "brand-secondary"
        count: 12
    text_colors:
      - hex: "#484848"
        usage: "body-text"
        count: 156
      - hex: "#767676"
        usage: "muted-text"
        count: 89
    border_colors:
      - hex: "#EBEBEB"
        usage: "divider"
        count: 45

  typography:
    detected: true
    fonts:
      - "Circular"
      - "Cereal"
      - "-apple-system"
    weights: ["400", "500", "600", "700", "800"]
    sizes: ["12px", "14px", "16px", "18px", "22px", "26px", "32px"]
    h1:
      - text: "Find places to stay"
        fontSize: "32px"
        fontWeight: "800"
        fontFamily: "Circular, sans-serif"
    h2:
      - fontSize: "22px"
        fontWeight: "600"
    body:
      - fontSize: "16px"
        fontWeight: "400"
        lineHeight: "1.5"

  spacing_system:
    detected: true
    grid_base: 8
    common_values: [8, 16, 24, 32, 48, 64]
    paddings: ["8px", "16px", "24px", "32px", "48px"]
    margins: ["8px", "16px", "24px", "32px"]
    gaps: ["8px", "16px", "24px"]

  component_styles:
    detected: true
    buttons:
      - id: "button-0"
        text: "Search"
        backgroundColor: "rgb(255, 90, 95)"
        color: "rgb(255, 255, 255)"
        padding: "14px 24px"
        borderRadius: "8px"
        fontSize: "16px"
        fontWeight: "600"
        transition: "all 0.2s ease"
        hover_animation: "Background darkens + Shadow appears"
    cards:
      - id: "card-0"
        backgroundColor: "rgb(255, 255, 255)"
        padding: "16px"
        borderRadius: "12px"
        boxShadow: "0 2px 8px rgba(0, 0, 0, 0.1)"
        transition: "all 0.3s ease"
        hover_animation: "Shadow increases + Slight lift"
    inputs:
      - id: "input-0"
        type: "text"
        height: "48px"
        padding: "0 16px"
        borderRadius: "8px"
        border: "1px solid #EBEBEB"
        fontSize: "16px"
        transition: "border-color 0.2s ease"
        focus_animation: "Border color changes to primary"

  shadows_elevation:
    detected: true
    values:
      - "0 1px 2px rgba(0, 0, 0, 0.08)"
      - "0 2px 8px rgba(0, 0, 0, 0.1)"
      - "0 4px 16px rgba(0, 0, 0, 0.12)"
      - "0 8px 28px rgba(0, 0, 0, 0.15)"

  animations_transitions:
    detected: true
    keyframes:
      - name: "fadeIn"
        css: "@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }"
    transitions:
      - duration: "0.2s"
        timing: "ease"
        property: "all"
      - duration: "0.3s"
        timing: "ease-out"
        property: "transform"

  border_radius:
    detected: true
    values: ["4px", "8px", "12px", "16px", "24px", "50%"]

  border_styles:
    detected: true
    widths: ["1px", "2px"]
    colors: ["#EBEBEB", "#DDDDDD"]

  layout_patterns:
    detected: true
    container_width: "1280px"
    grid_columns: 12
    breakpoints:
      - name: "mobile"
        max_width: "744px"
      - name: "tablet"
        max_width: "1128px"
      - name: "desktop"
        min_width: "1128px"

# Detailed animation states
animations:
  button-0:
    type: "button"
    description: "Background darkens + Shadow appears"
    transition: "all 0.2s ease"
    states:
      default:
        background: "rgb(255, 90, 95)"
        boxShadow: "none"
        transform: "none"
      hover:
        background: "rgb(230, 80, 85)"
        boxShadow: "0 2px 8px rgba(255, 90, 95, 0.3)"
        transform: "none"
  card-0:
    type: "card"
    description: "Shadow increases + Slight lift"
    transition: "all 0.3s ease"
    states:
      default:
        boxShadow: "0 2px 8px rgba(0, 0, 0, 0.1)"
        transform: "translateY(0)"
      hover:
        boxShadow: "0 4px 16px rgba(0, 0, 0, 0.15)"
        transform: "translateY(-2px)"
```

### icons_imagery (Section 11 — actively detect)

```yaml
  icons_imagery:
    detected: true
    system: "inline-svg"  # inline-svg | icon-font | img-based | sprite
    count: 24
    common_sizes: ["16px", "20px", "24px"]
    style: "outline"  # outline | filled | duotone | mixed
```

### loading_states (Section 15 — detect from stylesheets)

```yaml
  loading_states:
    detected: true
    patterns:
      - type: "spinner"
        keyframe: "spin"
        css: "@keyframes spin { to { transform: rotate(360deg) } }"
      - type: "skeleton"
        class_pattern: ".skeleton"
        properties: "background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%)"
      - type: "pulse"
        keyframe: "pulse"
```

### accessibility (Section 17 — actively detect)

```yaml
  accessibility:
    detected: true
    focus_styles:
      - element: "button"
        style: "outline: 2px solid #0070F3; outline-offset: 2px"
      - element: "a"
        style: "box-shadow: 0 0 0 2px #0070F3"
    aria_usage:
      aria_label: 12
      aria_hidden: 8
      role: 15
    semantic_html: ["nav", "main", "footer", "header", "section"]
    contrast_ratios:
      - pair: "primary-text on background"
        ratio: 15.3
        wcag_aa: true
```

### form_patterns (Section 13 — actively detect from DOM)

```yaml
  form_patterns:
    detected: true
    forms:
      - type: "newsletter"  # newsletter | login | signup | contact | search
        fields: ["email"]
        layout: "inline"  # inline | stacked | grid
        submit_text: "Subscribe"
        validation: ["required", "type=email"]
      - type: "search"
        fields: ["query"]
        layout: "inline"
```

### feedback_states (Section 14 — detect from stylesheets + DOM)

```yaml
  feedback_states:
    detected: true
    error:
      color: "#ef4444"
      classes: [".error", ".is-invalid", "[aria-invalid='true']"]
      border_style: "1px solid #ef4444"
    success:
      color: "#22c55e"
      classes: [".success", ".is-valid"]
    warning:
      color: "#f59e0b"
      classes: [".warning", ".alert-warning"]
    toast_pattern:
      detected: true
      classes: [".toast", ".notification"]
      position: "top-right"
    alert_elements:
      - role: "alert"
        aria_live: "polite"
```

### animation_libraries (bonus section — include in animations_transitions)

```yaml
  animations_transitions:
    detected: true
    keyframes: [...]
    transitions: [...]
    libraries:
      - name: "gsap"
        detected: true
        modules: ["ScrollTrigger"]
      - name: "framer-motion"
        detected: false
      - name: "lottie"
        detected: true
        players: 2
      - name: "anime"
        detected: false
      - name: "three"
        detected: false
    scroll_animations:
      system: "data-aos"  # data-aos | data-scroll | custom | none
      patterns: ["fade-up", "slide-in"]
      count: 12
    background_media:
      videos: 1
      animated_gifs: 0
      lottie_players: 2
```

### css_custom_properties (from Call 2 #15 — include when detected)

```yaml
css_custom_properties:
  colors:
    --color-primary: "#FF5A5F"
    --color-background: "#ffffff"
  spacing:
    --space-1: "4px"
    --space-2: "8px"
  fonts:
    --font-sans: "'Inter', sans-serif"
  other:
    --radius-md: "8px"
    --shadow-sm: "0 1px 2px rgba(0,0,0,0.05)"
```

Group by category prefix. Include all `--*` properties found on `:root`, `html`, `body`, `[data-theme]`. If none found, omit this section entirely (don't write `detected: false`).

---

All 17 sections should be actively detected. Mark `detected: false` only when genuinely not found after searching DOM + stylesheets.

**Required field:** `coverage.missing` must always list undetected section names.

Coverage = detected_sections / 17 * 100
