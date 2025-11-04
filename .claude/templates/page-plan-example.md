# Page Plan: Landing Page (EXAMPLE)
> This is an example template showing the structure of page-plan.md
> Generated from: proposal.md, prd.md, project_brief.md, STYLE_GUIDE.md
> Change ID: landing-page

---

## 1. Component Plan

### 🔄 Reuse Components (Found in codebase)

- **Navbar**
  - Path: `/components/layout/Navbar.tsx`
  - Usage: `<Navbar user={currentUser} showSearch={true} />`
  - Props: `user?: User, showSearch?: boolean, variant?: 'default' | 'transparent'`
  - Notes: Sticky navigation with logo, menu, and CTA button

- **Footer**
  - Path: `/components/layout/Footer.tsx`
  - Usage: `<Footer variant="default" />`
  - Props: `variant?: 'default' | 'minimal'`
  - Notes: Contains links, social media icons, copyright

---

### ✅ Create New Components

#### Shared Components (reusable across pages)

(None for this landing page - all new components are page-specific)

#### Page-Specific Components (used only here)

- **HeroSection**
  - Purpose: Landing page hero with headline, subheadline, CTA, and background image
  - Compose with: Button (shadcn/ui), background image
  - Store at: `/app/landing/HeroSection.tsx`
  - Responsive: Full height on desktop, auto height on mobile, stack content vertically

- **FeatureGrid**
  - Purpose: 3-column grid showcasing key features with icons and descriptions
  - Compose with: Card (shadcn/ui), icons from Material Symbols
  - Store at: `/app/landing/FeatureGrid.tsx`
  - Responsive: 3 columns desktop → 1 column mobile

- **HowItWorksSection**
  - Purpose: 3-step process timeline showing how the product works
  - Compose with: Custom step component with numbers
  - Store at: `/app/landing/HowItWorksSection.tsx`
  - Responsive: Horizontal timeline desktop → Vertical timeline mobile

- **TestimonialCarousel**
  - Purpose: Rotating testimonials with student photos, quotes, and ratings
  - Compose with: Card (shadcn/ui), Avatar component, Carousel logic
  - Store at: `/app/landing/TestimonialCarousel.tsx`
  - Responsive: 3 cards desktop → 1 card mobile with swipe

- **FAQAccordion**
  - Purpose: Collapsible FAQ section with common questions
  - Compose with: Accordion (shadcn/ui)
  - Store at: `/app/landing/FAQAccordion.tsx`
  - Responsive: Full width on all devices

- **CTASection**
  - Purpose: Final call-to-action with email signup form
  - Compose with: Input (shadcn/ui), Button (shadcn/ui)
  - Store at: `/app/landing/CTASection.tsx`
  - Responsive: Horizontal form desktop → Stacked form mobile

---

## 2. Page Structure

```tsx
<div className="landing-page">
  <Navbar user={null} showSearch={false} variant="transparent" />  {/* Reuse - transparent on hero */}

  <main>
    <HeroSection />                {/* New - full viewport height */}
    <FeatureGrid />                {/* New - 3 columns */}
    <HowItWorksSection />          {/* New - timeline */}
    <TestimonialCarousel />        {/* New - carousel */}
    <FAQAccordion />               {/* New - accordion */}
    <CTASection />                 {/* New - email form */}
  </main>

  <Footer variant="default" />     {/* Reuse */}
</div>
```

### Layout Flow:
- **Hero:** Full viewport height, centered content
- **Features:** Container max-width 1200px, padding 6rem vertical
- **How It Works:** Container max-width 1000px, padding 6rem vertical
- **Testimonials:** Full width background, container max-width 1200px
- **FAQ:** Container max-width 800px, padding 6rem vertical
- **CTA:** Full width colored background, container max-width 600px

---

## 3. 📦 Assets to Prepare (คุณต้องเตรียม)

### Images

- [ ] **Hero Background Image**
  - Filename: `hero-background.jpg`
  - Size: 1920x1080 (16:9 ratio)
  - Format: WebP (preferred) or high-quality JPG
  - Location: `/public/images/hero-background.jpg`
  - Purpose: Hero section background
  - Style: Modern workspace, student studying, or abstract tech pattern
  - Note: Should support text overlay (darker or blurred area for text)

- [ ] **Logo**
  - Filename: `logo.svg`
  - Size: 200x60 (approx)
  - Format: SVG (transparent background)
  - Location: `/public/images/logo.svg`
  - Purpose: Navbar logo
  - Note: Should work on both light and dark backgrounds

### Icons

- [ ] **Feature Icons** (3 icons)
  - Filenames: `feature-ai.svg`, `feature-exam.svg`, `feature-analytics.svg`
  - Size: 24x24 pixels
  - Format: SVG, outline style (match Material Symbols)
  - Location: `/public/icons/features/`
  - Style: Consistent stroke width, simple line art
  - Suggested icons:
    - AI: Brain or robot symbol
    - Exam: Document or test paper
    - Analytics: Bar chart or growth graph

- [ ] **Step Icons** (3 icons - optional)
  - Filenames: `step-1.svg`, `step-2.svg`, `step-3.svg`
  - Size: 32x32 pixels
  - Format: SVG
  - Location: `/public/icons/steps/`
  - Alternative: Use CSS-styled numbers (no icons needed)

### Testimonial Photos

- [ ] **Student Photos** (3 photos)
  - Filenames: `testimonial-1.jpg`, `testimonial-2.jpg`, `testimonial-3.jpg`
  - Size: 100x100 pixels (will be displayed as circular)
  - Format: JPG or WebP
  - Location: `/public/images/testimonials/`
  - Note: Professional headshots or AI-generated avatars
  - Alternative: Use placeholder service (e.g., `https://i.pravatar.cc/100?img=X`)

### Other Assets

- [ ] **Social Media Icons** (if not using icon library)
  - Check if existing Footer component includes these
  - If needed: Facebook, Twitter, LinkedIn, Instagram
  - Size: 20x20 pixels, SVG format

---

**Asset Preparation Checklist:**
1. ✅ Review all assets above
2. ✅ Prepare images at specified sizes
3. ✅ Optimize images (compress without quality loss)
4. ✅ Place files in correct directories (`/public/images/`, `/public/icons/`)
5. ✅ Verify file naming matches exactly (case-sensitive!)
6. ✅ If assets not ready: Use placeholders temporarily
   - Images: `https://placehold.co/1920x1080/png`
   - Avatars: `https://i.pravatar.cc/100`
   - Icons: Material Symbols library (imported from @mui/icons-material)

---

## 4. 📝 Content Draft (AI-Generated - กรุณา Review & Edit)

> **Instructions:** This content is AI-generated based on PRD analysis.
> Please review, edit, and adjust tone/messaging as needed.

---

### Hero Section

**Headline:**
"Master TOEIC with AI-Powered Practice Tests"

_Rationale: Direct value proposition, mentions AI (key differentiator), targets TOEIC test-takers_
_Length: 44 characters (recommended: 40-60)_
_Source: Derived from PRD section 1 - Adaptive Learning System for TOEIC_

**Subheadline:**
"Experience exam-quality questions tailored to your skill level. Our AI generates tests validated against official TOEIC standards. Start your free diagnostic test today."

_Length: 180 characters (recommended: 120-180)_
_Rationale: Explains how it works, emphasizes quality/validation, includes CTA_

**CTA Button Text:**
"Start Free Test"

_Alternative options: "Try Now", "Get Started Free", "Begin Assessment"_

**CTA Button Action:**
Navigate to `/signup` or `/exam/diagnostic` (depending on flow)

---

### Features Section (3 Cards)

#### Feature 1: AI-Generated Questions

**Icon:** `feature-ai.svg` (brain/AI symbol)

**Title:** "AI-Generated Questions"

**Description:**
"Our advanced AI engine analyzes thousands of official TOEIC exams to generate practice questions with comparable difficulty and format. Each question is validated against real exam standards, ensuring you practice with the highest quality materials available."

_Length: 58 words (target: 50-60)_
_Source: PRD section 3 - Question Generation Engine_
_Tone: Professional, emphasizes technology + quality_

---

#### Feature 2: Real Exam Simulation

**Icon:** `feature-exam.svg` (document/test paper symbol)

**Title:** "Authentic Exam Experience"

**Description:**
"Practice with a testing interface identical to the official TOEIC format. Timed sections, question navigation, and scoring algorithms mirror the actual exam environment. Reduce test-day anxiety by familiarizing yourself with the real thing."

_Length: 50 words_
_Source: PRD section 4 - Quiz & Exam Interface_
_Tone: Reassuring, focuses on reducing anxiety_

---

#### Feature 3: Instant Performance Analytics

**Icon:** `feature-analytics.svg` (chart symbol)

**Title:** "Detailed Performance Insights"

**Description:**
"Receive immediate score breakdowns by skill category and difficulty level. Track your progress over time, identify knowledge gaps, and get personalized recommendations to improve your weakest areas. Data-driven learning for maximum efficiency."

_Length: 52 words_
_Source: PRD section 5 - Success Metrics_
_Tone: Data-focused, emphasizes personalization_

---

### How It Works Section (3 Steps)

**Section Headline:** "How It Works"

**Section Subheadline:** "Get started in three simple steps"

#### Step 1: Take Diagnostic Assessment

**Title:** "1. Take Diagnostic Test"

**Description:**
"Begin with a comprehensive diagnostic exam to establish your baseline TOEIC score and identify your current strengths and weaknesses across all skill categories."

_Length: 30 words_

---

#### Step 2: Receive Personalized Plan

**Title:** "2. Get Your Learning Path"

**Description:**
"Our AI analyzes your results and creates a customized study plan targeting your specific knowledge gaps, prioritizing areas where you can improve fastest."

_Length: 28 words_

---

#### Step 3: Practice & Improve

**Title:** "3. Practice & Track Progress"

**Description:**
"Work through tailored practice tests and exercises. Monitor your improvement with detailed analytics and adjust your study plan as you progress toward your target score."

_Length: 32 words_

---

### Testimonials Section (3 Reviews)

**Section Headline:** "What Our Students Say"

**Section Subheadline:** "Join thousands of successful test-takers"

---

#### Testimonial 1

**Name:** "Somchai Pattanapong"
**Role:** "University Student, Chulalongkorn University"
**Photo:** `testimonial-1.jpg`

**Quote:**
"I improved my TOEIC score by 150 points in just one month using this platform. The AI-generated questions felt exactly like the real exam, and the instant feedback helped me focus on my weak areas. Highly recommended for serious test-takers!"

_Length: 95 words_
_Tone: Enthusiastic, focuses on results (150-point improvement)_

---

#### Testimonial 2

**Name:** "Natthida Kaewkham"
**Role:** "Marketing Professional"
**Photo:** `testimonial-2.jpg`

**Quote:**
"As a working professional, I needed flexible practice that fit my busy schedule. The platform's adaptive tests and detailed analytics made my study time efficient and effective. I passed my target score on the first attempt!"

_Length: 72 words - **EXPAND TO ~100 words**_
_Tone: Professional, emphasizes flexibility + efficiency_

**Suggested expansion:**
"As a working professional preparing for job applications, I needed flexible TOEIC practice that fit my busy schedule. The platform's adaptive tests and detailed analytics made my limited study time incredibly efficient and effective. The real-time progress tracking kept me motivated. I reached my target score of 850 on my first official attempt and secured my dream job at a multinational company!"

---

#### Testimonial 3

**Name:** "Wanchai Thongchai"
**Role:** "Graduate Student"
**Photo:** `testimonial-3.jpg`

**Quote:**
"The quality of practice questions is outstanding. I've tried many TOEIC prep services, but this AI-generated content is the closest to official exams I've experienced. The explanations for each answer helped me understand my mistakes and avoid repeating them."

_Length: 85 words - **EXPAND TO ~100 words**_
_Tone: Quality-focused, comparison with competitors_

**Suggested expansion:**
"The quality of practice questions is truly outstanding. I've tried many TOEIC preparation services over the years, but this AI-generated content is the closest to official exams I've experienced. The detailed explanations for each answer helped me understand not just what I got wrong, but why I made those mistakes and how to avoid repeating them. After three weeks of practice, my reading comprehension score improved by 80 points!"

---

### FAQ Section (5 Questions)

**Section Headline:** "Frequently Asked Questions"

---

#### FAQ 1
**Question:** "How accurate are the AI-generated questions compared to real TOEIC exams?"

**Answer:**
"Our AI model is trained on thousands of official TOEIC questions and validated against real exam standards. Statistical analysis shows a strong correlation (r > 0.85) between scores on our practice tests and official TOEIC scores. While no practice material can perfectly replicate the official exam, our questions are designed to match the format, difficulty, and content distribution of real TOEIC tests."

_Length: 110 words_

---

#### FAQ 2
**Question:** "What's included in the free diagnostic test?"

**Answer:**
"The free diagnostic test includes 100 questions covering TOEIC Reading sections (Parts 5, 6, and 7). You'll receive a detailed score report showing your performance by skill category, estimated TOEIC score range, and personalized recommendations for improvement. No credit card required."

_Length: 60 words - **EXPAND with what happens after free test**_

**Suggested expansion:**
"The free diagnostic test includes 100 questions covering TOEIC Reading sections (Parts 5, 6, and 7). You'll receive a detailed score report showing your performance by skill category, estimated TOEIC score range, and personalized study recommendations. After completing the free test, you can access additional practice tests, listening sections, and advanced analytics through our subscription plans. No credit card required for the diagnostic test."

---

#### FAQ 3
**Question:** "How does the scoring system work?"

**Answer:**
"Our scoring algorithm is calibrated against official TOEIC scoring standards. Each practice test is scored on a scale matching the real exam (10-990 points). You'll see your total score, section-by-section breakdown, and performance trends over time. The system also provides difficulty ratings for individual questions to help you understand your progress."

_Length: 85 words_

---

#### FAQ 4
**Question:** "Can I retake practice tests?"

**Answer:**
"Yes, you can retake any practice test. However, for the most accurate assessment, we recommend taking each test only once and then moving to new practice sets. Our AI generates unlimited unique practice tests, so you'll never run out of fresh material to practice with."

_Length: 65 words_

---

#### FAQ 5
**Question:** "Is the platform mobile-friendly?"

**Answer:**
"Yes, the platform is fully responsive and works on desktop, tablet, and mobile devices. However, we recommend using a desktop or laptop for full-length practice tests to simulate the actual TOEIC exam environment. You can use mobile devices for reviewing explanations, checking your progress, or practicing individual question sets."

_Length: 75 words_

---

### Final CTA Section

**Headline:** "Ready to Ace Your TOEIC Exam?"

**Subheadline:** "Join thousands of students improving their scores with AI-powered practice."

**CTA Button Text:** "Start Free Diagnostic Test"

**CTA Button Action:** Navigate to `/signup` or `/exam/diagnostic`

**Alternative CTA:** "Create Free Account"

---

**Content Review Checklist:**
1. ✅ Read all content above
2. ✅ Adjust tone to match brand voice
3. ✅ Edit headlines for clarity/impact
4. ✅ Expand testimonials to ~100 words each (if needed)
5. ✅ Verify claims are accurate (150-point improvement, r > 0.85 correlation)
6. ✅ Replace placeholder names with real testimonials (if available)
7. ✅ Finalize CTA actions (confirm routes: `/signup` vs `/exam/diagnostic`)

---

## 5. Design Notes

**Follow STYLE_GUIDE.md for all design decisions:**

- **Primary Color:** `#0d7276` (from STYLE_GUIDE.md Section 3)
- **Font Family:** `Prompt` (from STYLE_GUIDE.md Section 4)
- **Spacing Scale:** 8px grid system - use `p-4`, `p-6`, `p-8`, `gap-4`, `gap-6` (from STYLE_GUIDE.md Section 5)
- **Component Library:** shadcn/ui (from STYLE_GUIDE.md Section 6)
- **Icons:** Material Symbols (Outline style) (from STYLE_GUIDE.md Section 17)
- **Shadows:**
  - Cards: `shadow-sm` on default, `shadow-md` on hover
  - Elevated elements: `shadow-lg`
- **Border Radius:** `rounded-lg` for cards, `rounded-md` for buttons/inputs
- **Responsive Breakpoints:** (from STYLE_GUIDE.md Section 13)
  - Mobile: < 640px
  - Tablet: 640px - 1024px
  - Desktop: > 1024px

**Accessibility Requirements:**
- WCAG 2.1 Level AA compliance
- Color contrast ratio: minimum 4.5:1 (text), 3:1 (large text)
- Keyboard navigation: All interactive elements focusable
- ARIA labels: All icons, buttons, form inputs
- Alt text: All images

---

## 6. Implementation Notes

### Component Imports (Reference for Developer)

```tsx
// ===== REUSE (Existing Components) =====
import { Navbar } from '@/components/layout/Navbar'
import { Footer } from '@/components/layout/Footer'

// ===== SHADCN/UI (Component Library) =====
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components/ui/accordion'

// ===== NEW (To Be Created) =====
// Page-specific components
import { HeroSection } from './HeroSection'
import { FeatureGrid } from './FeatureGrid'
import { HowItWorksSection } from './HowItWorksSection'
import { TestimonialCarousel } from './TestimonialCarousel'
import { FAQAccordion } from './FAQAccordion'
import { CTASection } from './CTASection'
```

### File Structure

```
app/
├── landing/
│   ├── page.tsx              # Main landing page (composes all sections)
│   ├── HeroSection.tsx       # New
│   ├── FeatureGrid.tsx       # New
│   ├── HowItWorksSection.tsx # New
│   ├── TestimonialCarousel.tsx # New
│   ├── FAQAccordion.tsx      # New
│   └── CTASection.tsx        # New
components/
├── layout/
│   ├── Navbar.tsx            # Reuse (existing)
│   └── Footer.tsx            # Reuse (existing)
└── ui/
    ├── button.tsx            # shadcn/ui (existing)
    ├── card.tsx              # shadcn/ui (existing)
    ├── input.tsx             # shadcn/ui (existing)
    └── accordion.tsx         # shadcn/ui (existing)
public/
├── images/
│   ├── hero-background.jpg   # Prepare
│   ├── logo.svg              # Prepare
│   └── testimonials/
│       ├── testimonial-1.jpg # Prepare
│       ├── testimonial-2.jpg # Prepare
│       └── testimonial-3.jpg # Prepare
└── icons/
    └── features/
        ├── feature-ai.svg     # Prepare
        ├── feature-exam.svg   # Prepare
        └── feature-analytics.svg # Prepare
```

---

## 7. Next Steps

1. ✅ **Review this page plan**
   - Verify component structure makes sense
   - Check content tone and messaging
   - Confirm asset requirements are clear

2. ✅ **Edit content draft**
   - Adjust headlines, descriptions as needed
   - Replace placeholder names with real testimonials (if available)
   - Finalize CTA button text and actions

3. ✅ **Prepare assets**
   - Gather or create all images, icons per checklist (Section 3)
   - Optimize images for web (compress without quality loss)
   - Place files in correct directories with exact filenames

4. ✅ **Run setup command**
   ```bash
   /csetup landing-page
   ```
   - This will analyze the plan and create development phases

5. ✅ **Start development**
   ```bash
   /cdev landing-page
   ```
   - uxui-frontend agent will read this page-plan.md
   - Agent will skip component search (already done here)
   - Agent will implement with real content (not lorem ipsum)

---

**Generated by:** /pageplan command
**Date:** 2025-01-15
**For:** Change ID `landing-page`
**Context files used:** proposal.md, prd.md, project_brief.md, STYLE_GUIDE.md

---

**END OF PAGE PLAN**
