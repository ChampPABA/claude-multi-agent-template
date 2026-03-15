# Style Detection

Guide for classifying design styles during extraction.

---

## Design Styles

| Style | Key Characteristics |
|-------|--------------------|
| **Neo-Brutalism** | Bold 2-4px borders, high contrast, offset shadows (no blur), thick black outlines |
| **Minimalist** | Maximum whitespace, 2-3 colors, thin/no borders, no shadows, typography-focused |
| **Glassmorphism** | `backdrop-filter: blur`, semi-transparent bg, 1px white borders, gradient backgrounds |
| **Modern SaaS** | Subtle gradients, soft shadows, rounded corners (8-16px), clean hierarchy |
| **Corporate** | Conservative colors, traditional typography, structured grids, formal tone |
| **Playful** | Bright saturated colors, illustrations, curved shapes, animation-heavy |
| **Dark Mode Native** | Dark bg (#0a0a0a–#1a1a1a), high contrast text, glowing accents, subtle borders |

---

## Detection Criteria

### By Border

| Pattern | Indicates |
|---------|-----------|
| 2-4px solid black | Neo-Brutalism |
| 1px subtle | Minimalist / Modern SaaS |
| 1px white/translucent | Glassmorphism |
| No borders | Minimalist |

### By Shadow

| Pattern | Indicates |
|---------|-----------|
| Offset (4px 4px, no blur) | Neo-Brutalism |
| Soft blur (0 4px 16px) | Modern SaaS |
| None | Minimalist |
| Inner glow | Glassmorphism |

### By Color

| Pattern | Indicates |
|---------|-----------|
| High contrast, saturated | Neo-Brutalism / Playful |
| Muted, desaturated | Minimalist / Corporate |
| Gradients + transparency | Glassmorphism |
| Dark backgrounds | Dark Mode Native |

### By Typography

| Pattern | Indicates |
|---------|-----------|
| Extra bold (800-900) | Neo-Brutalism |
| Variable weights, modern sans | Modern SaaS |
| Serif fonts | Corporate / Editorial |
| Rounded, friendly | Playful |

---

## Psychology Mapping

| Style | Emotions | Best For |
|-------|----------|----------|
| Neo-Brutalism | Bold, Rebellious | Creative tools, indie brands |
| Minimalist | Calm, Premium | Luxury, productivity |
| Glassmorphism | Modern, Futuristic | Tech products, dashboards |
| Modern SaaS | Professional, Trustworthy | B2B, enterprise |
| Playful | Fun, Approachable | Consumer apps, social |
| Dark Mode | Sophisticated, Technical | Developer tools, gaming |
