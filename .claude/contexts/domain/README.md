# Domain-Specific Contexts

This folder contains **project-specific** business logic, design tokens, and domain patterns.

---

## 📁 Structure

```
domain/
├── README.md (this file)
└── {project-name}/          # Your project domain
    ├── overview.md          # Domain overview
    ├── design-tokens.md     # Project-specific colors, fonts
    ├── business-rules.md    # Domain logic, validations
    ├── api-contracts.md     # API specifications
    └── workflows.md         # User flows, process diagrams
```

---

## 🎯 Examples

### E-commerce Project
```
domain/ecommerce/
├── overview.md           # E-commerce platform overview
├── design-tokens.md      # Brand colors (primary, secondary, accent)
├── checkout-flow.md      # 4-step checkout process
├── inventory-rules.md    # Stock management, backorder logic
└── payment-gateway.md    # Stripe integration patterns
```

### IELTS Speaking Test
```
domain/ielts/
├── overview.md           # IELTS platform overview
├── design-tokens.md      # Primary: rgb(15, 42, 74), Secondary: rgb(212, 185, 120)
├── test-structure.md     # Part 1, 2, 3 specifications
├── scoring.md            # Speechace (0-100) → IELTS (0-9) conversion
├── speechace-api.md      # API integration, rate limits
└── audio-validation.md   # Part-specific audio limits (45s, 110s, 60s)
```

### CRM System
```
domain/crm/
├── overview.md           # CRM system overview
├── design-tokens.md      # Enterprise brand colors
├── sales-pipeline.md     # Lead → Opportunity → Customer
├── contact-management.md # Contact lifecycle, data model
└── reporting.md          # Dashboard metrics, KPIs
```

---

## 🔧 How to Create Your Domain

### Step 1: Create Directory
```bash
mkdir -p .claude/contexts/domain/myproject
```

### Step 2: Add Overview
```markdown
<!-- domain/myproject/overview.md -->
# MyProject Overview

## What is this?
Brief description of your project domain.

## Core Concepts
- Concept 1: Description
- Concept 2: Description

## Key Features
- Feature 1
- Feature 2
```

### Step 3: Add Design Tokens (Optional)
```markdown
<!-- domain/myproject/design-tokens.md -->
# MyProject Design Tokens

## Colors
```css
--color-primary: #007bff    /* Brand Blue */
--color-secondary: #6c757d  /* Gray */
--color-accent: #28a745     /* Green */
--color-error: #dc3545      /* Red */
```

## Typography
- Font Family: 'Inter', sans-serif
- Headings: 700 (bold)
- Body: 400 (regular)
```

### Step 4: Add Business Rules (Optional)
```markdown
<!-- domain/myproject/business-rules.md -->
# Business Rules

## Validation Rules
- Email must be unique
- Password min 8 characters
- Phone number format: +XX-XXX-XXX-XXXX

## Business Logic
- Free shipping: Orders > $50
- Discount: 10% for members
- Refund: Within 30 days
```

---

## 🤖 How Agents Use Domain Contexts

### Automatic Loading
```
Orchestrator:
1. Detects tech stack (Next.js, Prisma)
2. Checks domain/ folder
3. IF exists → Loads domain/{project}/*.md
4. Passes to specialist agents

Example:
Task: "Create login form"
→ uxui-frontend agent loads:
  ✅ patterns/testing.md (universal)
  ✅ design/color-theory.md (universal)
  ✅ domain/myproject/design-tokens.md (project-specific)
  ✅ Context7: Next.js docs (dynamic)
```

---

## ✅ Best Practices

### DO:
- ✅ Create domain folder for each project
- ✅ Document business rules clearly
- ✅ Include examples and edge cases
- ✅ Keep design tokens separate from universal design foundation
- ✅ Update when requirements change

### DON'T:
- ❌ Mix domain logic with universal patterns
- ❌ Hardcode values (use env variables)
- ❌ Leave outdated documentation
- ❌ Skip domain context for complex projects

---

## 📖 References

- **Universal Patterns:** `.claude/contexts/patterns/`
- **Design Foundation:** `.claude/contexts/design/`
- **Agents:** `.claude/agents/`

---

**Start by creating `domain/{your-project}/overview.md`!**
