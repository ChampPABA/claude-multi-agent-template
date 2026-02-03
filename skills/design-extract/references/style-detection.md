# Style Detection

Guide for classifying design styles during extraction.

---

## Common Design Styles

### Neo-Brutalism

**Characteristics:**
- Bold, chunky borders (2-4px)
- High contrast colors
- Offset shadows (no blur)
- Raw, intentionally "unpolished" look
- Thick black outlines

**Example sites:** Gumroad, Figma marketing pages

### Minimalist

**Characteristics:**
- Maximum whitespace
- Limited color palette (2-3 colors)
- Thin or no borders
- Subtle shadows or none
- Typography-focused

**Example sites:** Apple, Notion

### Glassmorphism

**Characteristics:**
- Frosted glass effect (backdrop-filter: blur)
- Semi-transparent backgrounds
- Subtle borders (1px white/light)
- Layered depth
- Gradient backgrounds

**Example sites:** macOS Big Sur UI, many fintech apps

### Modern SaaS

**Characteristics:**
- Clean, professional aesthetic
- Subtle gradients
- Soft shadows
- Rounded corners (8-16px)
- Clear visual hierarchy

**Example sites:** Linear, Stripe, Vercel

### Corporate/Enterprise

**Characteristics:**
- Conservative color choices
- Traditional typography
- Structured grid layouts
- Formal tone
- Accessibility-focused

**Example sites:** IBM, Microsoft, Salesforce

### Playful/Creative

**Characteristics:**
- Bright, saturated colors
- Illustrated elements
- Curved shapes
- Animation-heavy
- Informal typography

**Example sites:** Slack, Mailchimp, Dropbox

### Dark Mode Native

**Characteristics:**
- Dark backgrounds (#0a0a0a to #1a1a1a)
- High contrast text
- Glowing accents
- Subtle borders for separation
- Reduced eye strain focus

**Example sites:** Discord, GitHub (dark), VS Code

---

## Detection Criteria

### Border Analysis

| Pattern | Style Indicator |
|---------|-----------------|
| 2-4px solid black borders | Neo-Brutalism |
| 1px subtle borders | Minimalist/Modern SaaS |
| 1px white/translucent borders | Glassmorphism |
| No borders | Minimalist |

### Shadow Analysis

| Pattern | Style Indicator |
|---------|-----------------|
| Offset shadows (4px 4px, no blur) | Neo-Brutalism |
| Soft blur shadows (0 4px 16px) | Modern SaaS |
| No shadows | Minimalist |
| Inner glow effects | Glassmorphism |

### Color Analysis

| Pattern | Style Indicator |
|---------|-----------------|
| High contrast, saturated | Neo-Brutalism / Playful |
| Muted, desaturated | Minimalist / Corporate |
| Gradients with transparency | Glassmorphism |
| Dark backgrounds | Dark Mode Native |

### Typography Analysis

| Pattern | Style Indicator |
|---------|-----------------|
| Extra bold weights (800-900) | Neo-Brutalism |
| Variable weights, modern sans | Modern SaaS |
| Serif fonts | Corporate / Editorial |
| Rounded, friendly fonts | Playful |

---

## Psychology Mapping

| Style | Primary Emotions | Best For |
|-------|------------------|----------|
| Neo-Brutalism | Bold, Rebellious, Confident | Creative tools, indie brands |
| Minimalist | Calm, Focused, Premium | Luxury, productivity |
| Glassmorphism | Modern, Futuristic, Sleek | Tech products, dashboards |
| Modern SaaS | Professional, Trustworthy | B2B, enterprise |
| Playful | Fun, Approachable, Friendly | Consumer apps, social |
| Dark Mode | Sophisticated, Technical | Developer tools, gaming |
