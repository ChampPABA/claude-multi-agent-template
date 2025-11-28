# Claude Agent Kit

> 🤖 **Multi-Agent Implementation Engine** - The perfect companion for [OpenSpec](https://github.com/Fission-AI/OpenSpec) spec-driven development

[![npm version](https://badge.fury.io/js/@champpaba%2Fclaude-agent-kit.svg)](https://www.npmjs.com/package/@champpaba/claude-agent-kit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/node/v/@champpaba/claude-agent-kit)](https://nodejs.org)

---

## 🎯 What is this?

**Claude Agent Kit picks up where OpenSpec planning ends.**

While OpenSpec handles **alignment** (Draft Proposal → Review & Align), Claude Agent Kit handles **implementation** (Implement Tasks → Archive & Update) with specialized AI agents.

### The Complete Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenSpec Planning                        │
│  (Spec-Driven Development for AI Coding Assistants)        │
└─────────────────────────────────────────────────────────────┘
                            ↓
              Generates: proposal.md + tasks.md
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Claude Agent Kit Implementation                │
│         (Multi-Agent Execution with 6 Specialists)          │
└─────────────────────────────────────────────────────────────┘
                            ↓
              Completes: All tasks with quality gates
```

---

## 🔄 How They Work Together

| Stage | Tool | What Happens | Output |
|-------|------|--------------|--------|
| **1. Draft Proposal** | OpenSpec | Human requests change, AI scaffolds structure | `proposal.md` + `tasks.md` |
| **2. Review & Align** | OpenSpec | Team iterates until consensus | Approved specs |
| **2.5. Page Planning** | **Claude Agent Kit** | *(UI tasks only)* Generate content & component plan | `page-plan.md` |
| **3. Setup Context** | **Claude Agent Kit** | Classify tasks, generate workflow | `workflow.md` |
| **4. Implement Tasks** | **Claude Agent Kit** | 6 specialized agents execute work | Working code + tests |
| **5. Archive & Update** | OpenSpec | Merge changes back to specs | Updated `specs/` |

### What OpenSpec Generates

**proposal.md** - Business case and scope
```markdown
# Change Proposal: User Authentication System

## Motivation
Users need secure login functionality...

## Scope
- Email/password authentication
- JWT token generation
- Protected routes middleware
```

**tasks.md** - Implementation checklist
```markdown
## Database Setup
- [ ] Create User model with email, password fields
- [ ] Add unique constraint on email

## Backend Implementation
- [ ] POST /api/auth/login endpoint
- [ ] Password hashing with bcrypt
- [ ] JWT token generation

## Frontend Implementation
- [ ] Login form component
- [ ] Form validation
- [ ] Token storage
```

### What Claude Agent Kit Does

**Input:** Reads `proposal.md` + `tasks.md` from OpenSpec

**Process:**
1. `/pageplan` *(UI tasks only)* - Generate content & component reuse plan
2. `/csetup {change-id}` - Analyze tasks, classify by agent, generate workflow
3. `/cdev {change-id}` - Execute with 6 specialized agents in phases:
   - **Phase 1:** UI with mock data (uxui-frontend)
   - **Phase 2:** Real API + database (backend + database, parallel)
   - **Phase 2.5:** Validate contracts (integration)
   - **Phase 3:** Connect UI to API (frontend)
   - **Phase 4:** Tests + bug fixes (test-debug)

**Output:** Working implementation ready for review

---

## 🎨 NEW: Page Planning for UI Tasks

**Problem:** Before `/pageplan`, agents would:
- ❌ Create duplicate components (3 different Navbar components!)
- ❌ Use inconsistent colors (`#0d7276` on landing, `#4f46e5` on dashboard)
- ❌ Generate lorem ipsum instead of real content
- ❌ Waste time searching for components during implementation

**Solution:** `/pageplan` command analyzes BEFORE implementing

### How It Works

```bash
# Step 1: OpenSpec generates tasks
User: "Build landing page for TOEIC app"
→ Creates: openspec/changes/landing-page/proposal.md + tasks.md

# Step 2: Generate page plan (NEW!)
User: /pageplan @prd.md @project_brief.md

# What it does:
# 1. Reads user-specified files (PRD, brief)
# 2. Reads proposal.md (technical architecture)
# 3. Reads STYLE_GUIDE.md (visual design)
# 4. Searches existing components (Navbar, Footer, etc.)
# 5. AI drafts real content from PRD
# 6. Generates: openspec/changes/landing-page/page-plan.md
```

### page-plan.md Output

```markdown
# Page Plan: Landing Page

## 1. Component Plan
🔄 Reuse: Navbar, Footer (found in codebase)
✅ New Shared: (none)
✅ New Specific: HeroSection, FeatureGrid, TestimonialCarousel

## 2. Page Structure
<Layout>
  <Navbar /> {/* Reuse */}
  <HeroSection /> {/* New - see content below */}
  <FeatureGrid />
  <TestimonialCarousel />
  <Footer /> {/* Reuse */}
</Layout>

## 3. Assets to Prepare
- [ ] hero-image.jpg (1920x1080)
- [ ] logo.svg (200x60)
- [ ] feature-icons (3x 24x24 SVG)

## 4. Content Draft (AI-Generated - Please Review & Edit)
**Headline:** "Master TOEIC with AI-Powered Tests"
**Subheadline:** "Experience exam-quality questions with instant AI scoring"
**CTA:** "Start Free Test"

**Features:**
- Real TOEIC-style questions
- Instant AI scoring
- Progress tracking dashboard
```

### Step 3: User Prepares

- ✅ Review content draft (edit as needed)
- ✅ Prepare assets (images, icons)
- ✅ Approve `page-plan.md`

### Step 4: Implementation

```bash
/csetup landing-page
/cdev landing-page

# uxui-frontend agent automatically:
# - STEP 0.5: Reads page-plan.md ✅
# - STEP 3: SKIP component search (already done!) ⚡ 25% faster
# - Uses: Real content from page-plan
# - Reuses: Navbar, Footer (no duplicates)
# - Creates: HeroSection, FeatureGrid, TestimonialCarousel
# - Applies: Colors/spacing from STYLE_GUIDE.md
```

### Benefits

| Before (No page-plan) | After (With page-plan) |
|----------------------|------------------------|
| ❌ Agent searches during implementation | ✅ Search done once upfront (25% faster) |
| ❌ Duplicate components created | ✅ Clear reuse plan |
| ❌ Lorem ipsum content | ✅ Real content from PRD |
| ❌ Missing assets mid-work | ✅ Asset checklist prepared |
| ❌ Inconsistent design | ✅ Synced with STYLE_GUIDE |
| ❌ Agent guesses structure | ✅ Clear component hierarchy |

### When to Use /pageplan

```
✅ Use for:
- Landing pages
- Dashboards
- Multi-section UI pages
- Any task with multiple components

❌ Skip for:
- Backend API endpoints
- Database schemas
- Single-component tasks
- Non-UI work
```

---

## 🤖 The 6 Specialized Agents

| Agent | Color | Responsibility | Phase |
|-------|-------|---------------|-------|
| **uxui-frontend** | 🔵 Blue | Design UI components with mock data | 1 |
| **backend** | 🟣 Purple | Create API endpoints with validation | 2 |
| **database** | 🩷 Pink | Design schemas, migrations, queries | 2 |
| **integration** | 🟠 Orange | Validate API contracts before connecting | 2.5 |
| **frontend** | 🟢 Green | Connect UI to backend APIs | 3 |
| **test-debug** | 🔴 Red | Run tests and fix bugs (max 3-4 iterations) | 1,3,4 |

Each agent:
- ✅ Auto-discovers your project context (tech stack, best practices)
- ✅ Follows framework-specific patterns from Context7 MCP
- ✅ Maintains design consistency across the codebase
- ✅ Reports progress with detailed logging
- ✅ **Smart auto-proceed:** Eliminates double confirmations when user approves workflow

---

## 📦 Installation

```bash
npm install -g @champpaba/claude-agent-kit
```

### Alternative Package Managers

```bash
# Using pnpm
pnpm add -g @champpaba/claude-agent-kit

# Using yarn
yarn global add @champpaba/claude-agent-kit
```

---

## 🚀 Quick Start (with OpenSpec)

### Step 1: OpenSpec Planning

```bash
# In your OpenSpec-enabled project
cd my-app

# Draft a change proposal (OpenSpec handles this)
"I want to build a landing page for my TOEIC app"
# → Generates: openspec/changes/landing-page/proposal.md + tasks.md
```

### Step 2: Initialize Claude Agent Kit

```bash
# Initialize the agent system
cak init

# Setup project context (detects tech stack)
# In Claude Code:
/psetup
```

### Step 3: Generate Page Plan (UI tasks only)

```bash
# In Claude Code:
/pageplan @prd.md @project_brief.md

# → Generates: openspec/changes/landing-page/page-plan.md
# → Review content, prepare assets
```

### Step 4: Setup Change Context

```bash
/csetup landing-page
```

**What happens:**
- Reads `openspec/changes/landing-page/proposal.md` (business context)
- Reads `openspec/changes/landing-page/tasks.md` (implementation checklist)
- Reads `openspec/changes/landing-page/page-plan.md` (if exists - content plan)
- Classifies tasks by agent (database, backend, frontend, etc.)
- Generates `workflow.md` (execution plan)

### Step 5: Execute Implementation

```bash
/cdev landing-page
```

**What happens:**
1. **Phase 1:** uxui-frontend reads `page-plan.md` → creates UI with real content
2. **Phase 2:** backend + database create APIs + models (parallel, if needed)
3. **Phase 2.5:** integration validates API contracts
4. **Phase 3:** frontend connects UI to APIs (if needed)
5. **Phase 4:** test-debug runs tests, fixes bugs

### Step 6: Monitor Progress

```bash
# View detailed progress
/cview landing-page

# Quick status check
/cstatus landing-page
# → Phase 1/4 - UI Implementation (100%)
```

---

## 🎯 Complete Workflow Examples

### Workflow A: UI Feature (with /pageplan)

```bash
# 1. OpenSpec Planning
User: "Build landing page for TOEIC app"
→ Creates: proposal.md + tasks.md

# 2. Page Planning (NEW!)
/pageplan @prd.md @project_brief.md
→ Creates: page-plan.md
→ User reviews content & prepares assets

# 3. Setup Context
/csetup landing-page
→ Reads: proposal.md, tasks.md, page-plan.md
→ Generates: workflow.md

# 4. Implementation
/cdev landing-page
→ uxui-frontend reads page-plan.md (STEP 0.5)
→ Skips redundant component search
→ Uses real content + reuse plan
→ 25% faster implementation

# 5. Monitor
/cview landing-page
```

### Workflow B: Backend Feature (skip /pageplan)

```bash
# 1. OpenSpec Planning
User: "Add payment processing API"
→ Creates: proposal.md + tasks.md

# 2. Setup Context (skip /pageplan - not UI work)
/csetup payment-api

# 3. Implementation
/cdev payment-api
→ Phase 2: backend + database agents (parallel)
→ Phase 2.5: integration validates contracts
→ Phase 3: frontend connects (if UI exists)
→ Phase 4: test-debug validates

# 4. Monitor
/cview payment-api
```

### Workflow C: Full-Stack Feature (with /pageplan)

```bash
# 1. OpenSpec Planning
User: "Build user authentication system"
→ Creates: proposal.md + tasks.md

# 2. Page Planning (for login UI only)
/pageplan @prd.md
→ Creates: page-plan.md (login form content + components)

# 3. Setup Context
/csetup auth-system

# 4. Implementation
/cdev auth-system
→ Phase 1: uxui-frontend (login form, reads page-plan.md)
→ Phase 2: backend (POST /api/auth/login) + database (User model)
→ Phase 2.5: integration (validate contract)
→ Phase 3: frontend (connect form to API)
→ Phase 4: test-debug (E2E tests)

# 5. Monitor
/cview auth-system
```

---

## 📁 Project Structure After Init

```
your-project/
├── openspec/
│   ├── specs/                       # Source of truth (OpenSpec)
│   └── changes/
│       └── landing-page/
│           ├── proposal.md          ← OpenSpec generates
│           ├── tasks.md             ← OpenSpec generates
│           ├── page-plan.md         ← /pageplan generates (UI tasks)
│           ├── workflow.md          ← /csetup generates
│           └── flags.json           ← /cdev tracks progress
│
├── design-system/
│   └── STYLE_GUIDE.md               ← /designsetup generates
│
└── .claude/
    ├── CLAUDE.md                    # Navigation guide
    │
    ├── agents/                      # 6 specialized agents
    │   ├── 01-integration.md
    │   ├── 02-uxui-frontend.md
    │   ├── 03-test-debug.md
    │   ├── 04-frontend.md
    │   ├── 05-backend.md
    │   └── 06-database.md
    │
    ├── commands/                    # Slash commands
    │   ├── designsetup.md           # Generate style guide
    │   ├── pageplan.md              # Generate page plan (NEW!)
    │   ├── psetup.md                # Project setup
    │   ├── csetup.md                # Change setup
    │   ├── cdev.md                  # Change development
    │   ├── cview.md                 # View progress
    │   └── cstatus.md               # Quick status
    │
    ├── contexts/
    │   ├── design/                  # Design foundation
    │   ├── patterns/                # Universal patterns
    │   └── domain/                  # Project context
    │
    └── lib/                         # Implementation logic
        ├── agent-executor.md
        ├── tdd-classifier.md
        ├── flags-updater.md
        └── agent-router.md
```

---

## 🎯 Why Use Claude Agent Kit?

### Without Claude Agent Kit (Manual Implementation)

```
❌ You manually interpret tasks.md
❌ You context-switch between frontend/backend/database
❌ You might forget edge cases or tests
❌ Inconsistent code patterns across features
❌ No systematic error handling
❌ Duplicate components everywhere
❌ Lorem ipsum content in UI
```

### With Claude Agent Kit

```
✅ Agents auto-classify and execute tasks
✅ Each agent focuses on its specialty
✅ Built-in validation gates (integration agent)
✅ Consistent patterns via auto-discovery
✅ Automatic retry with escalation
✅ Component reuse plan (/pageplan)
✅ Real content from PRD
✅ 25% faster UI implementation
```

---

## 📚 Key Features

### ✅ Seamless OpenSpec Integration

- Reads `proposal.md` for business context
- Parses `tasks.md` for implementation checklist
- Generates `page-plan.md` for UI tasks (NEW!)
- Tracks progress in `flags.json`
- Updates completion status back to OpenSpec

### ✅ Auto-Generated Best Practices

Uses Context7 MCP to fetch latest framework docs:

```bash
/psetup
# → Detects: Next.js 15, React 18, Prisma 6
# → Generates: .claude/contexts/domain/{project}/best-practices/
#    - nextjs-15.md
#    - react-18.md
#    - prisma-6.md
```

### ✅ 3-Level Project Indexing

Agents auto-discover context:

```
1. Read: domain/index.md → Get current project
2. Read: domain/{project}/README.md → Get tech stack
3. Read: domain/{project}/best-practices/index.md → Load patterns
```

### ✅ Design Foundation

Universal design principles:
- Color theory (WCAG AAA contrast)
- Typography scales
- 8px spacing grid (8, 16, 24, 32, 40, 48px)
- 4-level shadow system
- Box thinking framework
- Accessibility (WCAG 2.1 AA)

### ✅ Quality Gates

- **TDD for critical paths** (auth, payments, data transforms)
- **Test-alongside for simple code** (CRUD, UI components)
- **Max 3-4 retry iterations** before escalation
- **Integration validation** before connecting UI to API
- **Smart auto-proceed** (eliminate redundant confirmations, 25% faster)

---

## 🔧 CLI Commands

### `cak init`
Initialize agent system in current project

```bash
cak init
cak init --force  # Overwrite existing .claude/
```

**Creates:**
- `.claude/` folder with 6 agents
- Slash commands (`/psetup`, `/csetup`, `/cdev`, etc.)
- Universal patterns & design foundation

---

### `cak update`
Update to latest agent templates

```bash
cak update
cak update --backup  # Create .claude.backup/ first
```

**What it does:**
- Updates all template files to latest version
- Preserves your customizations in `domain/`
- Creates backup before updating (with `--backup` flag)

---

### `cak --version`
Show version number

```bash
cak --version
# → 1.0.0
```

---

### `cak --help`
Display help information

```bash
cak --help
```

---

## 🔄 Workflow Commands (in Claude Code)

### `/designsetup` - Generate style guide (one-time)

```bash
/designsetup
```

**Auto-detects from:**
1. `reference/` folder → Extract design from HTML/screenshots
2. Existing codebase → Reverse engineer patterns
3. AI generation → Modern best practices

**Creates:** `design-system/STYLE_GUIDE.md`

---

### `/pageplan` - Generate page plan (UI tasks only) 🆕

```bash
/pageplan @prd.md @project_brief.md
```

**What it does:**
- Reads user-specified files (PRD, brief)
- Reads `proposal.md` + `STYLE_GUIDE.md`
- Searches existing components
- AI drafts real content from PRD
- Generates asset checklist

**Creates:** `page-plan.md`
- Component reuse plan (🔄 Reuse vs ✅ New)
- Page structure (component hierarchy)
- Assets to prepare (images, icons)
- Content draft (headlines, descriptions)

---

### `/psetup` - Setup project (one-time)

```bash
/psetup
```

**What it does:**
- Detects tech stack (Next.js, React, Prisma, etc.)
- Creates `domain/{project}/README.md`
- Generates best practices via Context7 MCP

---

### `/csetup {change-id}` - Setup change context

```bash
/csetup landing-page
```

**What it does:**
- Reads `proposal.md` (business context)
- Reads `tasks.md` (implementation checklist)
- Reads `page-plan.md` (if exists - UI content plan)
- Classifies tasks by agent
- Generates `workflow.md` (execution plan)

---

### `/cdev {change-id}` - Execute implementation

```bash
/cdev landing-page

# Or with explicit approval
"ลุยเลย"  # Continue without confirmation prompts
```

**What it does:**
- Runs agents in phases (1 → 2 → 2.5 → 3 → 4)
- uxui-frontend auto-reads `page-plan.md` (STEP 0.5)
- **Auto-proceed:** Detects user approval ("continue", "ลุยเลย") and eliminates redundant confirmation prompts
- Updates `flags.json` (progress tracking)
- Reports completion status

**Auto-Proceed Feature:**
- When you say "continue", "proceed", "yes", or "ลุยเลย", Main Claude auto-responds to agent questions
- **50-90% fewer confirmations** (1x per workflow instead of 2x per phase)
- **25% faster execution** (no waiting for redundant approvals)

---

### `/cview {change-id}` - View detailed progress

```bash
/cview landing-page
```

**Shows:**
- Completed/pending tasks
- Agent activity log
- Current phase
- Error messages (if any)

---

### `/cstatus {change-id}` - Quick status

```bash
/cstatus landing-page
# → Phase 2/4 - Backend Implementation (75%)
```

---

## 🎨 Design System Integration

### Auto-Generate Style Guide

```bash
/designsetup
```

**Detection priority:**
1. **reference/ folder** (HTML/screenshots) → Extract design style
2. **Existing codebase** (>10 components) → Reverse engineer patterns
3. **AI generation** → Modern best practices

**Output:** `design-system/STYLE_GUIDE.md`

**17 Comprehensive Sections:**
1. Overview
2. Design Philosophy
3. Color Palette (HEX codes, usage, Tailwind classes)
4. Typography (headings, body, weights)
5. Spacing System (4px/8px grid)
6. Component Styles (Button, Card, Input, Badge, etc.)
7. Shadows & Elevation
8. Animations & Transitions
9. Border Styles
10. Border Radius
11. Opacity & Transparency
12. Z-Index Layers
13. Responsive Breakpoints
14. CSS Variables / Tailwind Theme (Design Tokens)
15. Layout Patterns
16. Example Component Reference (React + Tailwind code)
17. Additional Sections (Best Practices, Accessibility, Icon System)

**Agents automatically use `STYLE_GUIDE.md` for:**
- Color palette (no hardcoded colors)
- Spacing scale (consistent gaps/padding)
- Typography (font hierarchy)
- Component patterns (reuse before create)

---

## 🧪 Testing Philosophy

**Agents follow TDD classification:**

| Code Type | Approach | Example |
|-----------|----------|---------|
| **Critical paths** | TDD (Red-Green-Refactor) | Auth logic, payments, calculations |
| **Simple code** | Test-alongside | CRUD, UI components, config |

**Test-debug agent:**
- Runs tests automatically after implementation
- Fixes bugs (max 3-4 iterations)
- Escalates if stuck (reports to user)

---

## 🔧 Supported Tech Stacks

Agents auto-detect your stack via Context7 MCP:

**Frontend:**
- Next.js, React, Vue, Svelte, Angular

**Backend:**
- FastAPI, Express, NestJS, Django, Flask, Next.js API Routes

**Database:**
- Prisma, SQLAlchemy, TypeORM, Drizzle

**Testing:**
- Vitest, Jest, Pytest, Playwright

---

## 📖 Usage Examples

### Example 1: Simple UI Task (with /pageplan)

```bash
# In Claude Code
"Build a user profile page with edit functionality"

# If it's a UI task, optionally run:
/pageplan @prd.md

# Then execute:
/csetup profile-page
/cdev profile-page
```

Claude will:
1. Read `task-classification.md`
2. Select agents: `uxui-frontend` → `backend` → `frontend` → `test-debug`
3. uxui-frontend reads `page-plan.md` (if exists)
4. Execute in sequence
5. Report completion

---

### Example 2: Complex Multi-Agent Workflow (OpenSpec)

Using OpenSpec workflow:

```bash
# 1. OpenSpec generates proposal + tasks
"I want to add a dashboard with analytics"
# → proposal.md + tasks.md created

# 2. Generate page plan
/pageplan @prd.md @analytics_spec.md

# 3. Setup change context
/csetup analytics-dashboard

# 4. Start development
/cdev analytics-dashboard

# 5. View progress
/cview analytics-dashboard
```

This follows a structured 4-phase approach:
1. **Phase 1:** UI with mock data (uxui-frontend reads page-plan.md)
2. **Phase 2:** Real API + database (backend + database)
3. **Phase 2.5:** Validate contracts (integration)
4. **Phase 3:** Connect UI to API (frontend)
5. **Phase 4:** Tests + bug fixes (test-debug)

---

## 🔄 Updating to Latest Version

### Method 1: Update the npm package

```bash
npm update -g @champpaba/claude-agent-kit
```

### Method 2: Update template in project

```bash
cd your-project
cak update --backup
```

This will:
- Create backup at `.claude.backup/`
- Update all template files
- Preserve your customizations in `domain/`

---

## 🎯 Customization

### Add Project-Specific Context

After running `cak init`, add your own context files:

```bash
mkdir -p .claude/contexts/domain/my-project
```

**Example:** E-commerce checkout flow
```markdown
<!-- .claude/contexts/domain/my-project/checkout-flow.md -->
# Checkout Flow

## Steps
1. Cart review
2. Shipping address
3. Payment method
4. Order confirmation

## Business Rules
- Free shipping over $50
- Tax calculation by state
- Inventory check before payment
```

Agents will auto-discover and use these patterns.

---

## 🔗 Ecosystem

**Claude Agent Kit works with:**

| Tool | Purpose | Integration |
|------|---------|-------------|
| **OpenSpec** | Spec-driven planning | Reads `proposal.md` + `tasks.md` |
| **Context7 MCP** | Always-updated docs | Auto-generates best practices |
| **Claude Code** | AI coding assistant | Execution environment |

---

## 🤝 Contributing

We welcome contributions!

- Report bugs: [GitHub Issues](https://github.com/ChampPABA/claude-multi-agent-template/issues)
- Feature requests: [Discussions](https://github.com/ChampPABA/claude-multi-agent-template/discussions)
- Pull requests: Follow [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Credits

Built with:
- [OpenSpec](https://github.com/Fission-AI/OpenSpec) - Spec-driven development framework
- [Claude Code](https://claude.com/claude-code) - AI coding assistant
- [Context7 MCP](https://context7.com) - Always up-to-date library docs

---

## 🆕 What's New in v2.0.0

**Major Release: Design System v2.0.0 - Interactive Setup & Smart Page Planning** 🎨

### Complete Design System Overhaul

**Problem Solved:**
- Before: One massive STYLE_GUIDE.md loaded everywhere (~5000 tokens)
- Before: No theme direction, random decorations
- Before: Same patterns loaded for landing pages AND dashboards
- Before: Manual style selection with no recommendations

**Solution Implemented:**
- ✅ `/extract` - Extract design from multiple reference sites
- ✅ `/designsetup` - Interactive 3-round loop with theme recommendations
- ✅ `tokens.json` - Smart design tokens with style/theme/animations (~800 tokens)
- ✅ `patterns/*.md` - Selective code patterns based on page type
- ✅ Auto page type detection (landing/dashboard/auth)

**Results:**
- **84% token reduction** (~800 vs ~5000 tokens)
- **Theme consistency** (USE/AVOID decorations enforced)
- **Smart patterns** (only load what's needed per page type)
- **Interactive setup** (AI recommends, user confirms)

### New Flow

```
/extract https://site.com → .claude/extractions/*.json
                    ↓
/designsetup @prd.md → tokens.json + patterns/*.md + STYLE_GUIDE.md
                    ↓
/pageplan @prd.md → page-plan.md (auto-detects page type)
                    ↓
/csetup → phases.md (reads page-plan.md)
                    ↓
/cdev → uxui-frontend (loads patterns selectively)
```

### Page Type Auto-Detection

| Page Type | Decorations | Scroll Anims | Buyer Avatar | Patterns Loaded |
|-----------|-------------|--------------|--------------|-----------------|
| Landing/Marketing | ✅ Full | ✅ Enabled | ✅ Enabled | buttons, cards, scroll-anims, decorations |
| Dashboard/Admin | ❌ Minimal | ❌ Disabled | ❌ Skipped | buttons, cards, forms |
| Auth (Login/Register) | ❌ None | ❌ Disabled | ❌ Skipped | buttons, forms |

### New Features

**`/extract` command:**
- Multi-URL support (extract from multiple sites)
- Style detection (Neo-Brutalism, Minimalist, Glassmorphism, Modern SaaS)
- Animation library detection (GSAP, ScrollTrigger, Framer Motion)
- Scroll pattern detection (stacking-cards, parallax, fade-in)
- Decorative element detection (blobs, gradients, 3D elements)

**`/designsetup` v2.0.0:**
- Interactive 3-round loop (Present → Feedback → Adjust)
- Verbose style options with match scores
- AI recommends themes based on project context
- USE/AVOID decorative direction

**`tokens.json` v2.0.0:**
- `style` - Detected design style with confidence
- `theme` - Theme name, feeling, decorative direction
- `animations` - Libraries, patterns, component animations
- `patterns_index` - References to pattern files

**`patterns/*.md` files:**
- `buttons.md` - Button patterns (primary, secondary, ghost, sizes, states)
- `cards.md` - Card patterns (default, interactive, feature, pricing)
- `forms.md` - Form patterns (input, error state, select, checkbox)
- `scroll-animations.md` - Scroll animation patterns
- `decorations.md` - Decorative elements (gradients, blobs, grids)

### Upgrading to v2.0.0

```bash
# Update npm package
npm update -g @champpaba/claude-agent-kit

# Update template in your project
cd your-project
cak update --backup

# Generate new design system
/extract https://your-reference.com  # Optional
/designsetup @prd.md
```

**Breaking Changes:**
- `STYLE_TOKENS.json` → `tokens.json` (new structure)
- `STYLE_GUIDE.md` no longer contains code (moved to `patterns/*.md`)
- Commands read `tokens.json` instead of `STYLE_TOKENS.json`

All your customizations in `.claude/contexts/domain/` are preserved!

---

## 📜 Changelog

### v2.0.0 (2025-01-28)
**Major: Design System v2.0.0 - Interactive Setup & Smart Page Planning**

**Added:**
- `/extract` command - Multi-URL design extraction with style/animation detection
- Interactive `/designsetup` - 3-round loop with theme recommendations
- `tokens.json` v2.0.0 - Enhanced design tokens with style/theme/animations (~800 tokens)
- `patterns/*.md` files - Selective code patterns (buttons, cards, forms, scroll-animations, decorations)
- Auto page type detection in `/pageplan` (landing/dashboard/auth)

**Changed:**
- `STYLE_TOKENS.json` → `tokens.json` (new structure)
- `STYLE_GUIDE.md` - Human-readable only, code moved to patterns/*.md
- `/csetup` - Reads tokens.json + page-plan.md

**Performance:**
- 84% token reduction (~800 vs ~5000 tokens)
- Selective pattern loading based on page type
- Theme consistency with USE/AVOID decorations

**Breaking Changes:**
- `STYLE_TOKENS.json` renamed to `tokens.json`
- `STYLE_GUIDE.md` no longer contains code
- Commands read `tokens.json` instead of `STYLE_TOKENS.json`

### v1.6.0 (2025-01-27)
**Feature: Page Plan Enhancement - Buyer Avatar & Conversion Copy**

### v1.5.1 (2025-01-26)
**Patch: Git Compatibility Fix**

### v1.5.0 (2025-01-25)
**Feature: Minor Improvements**

### v1.4.1 (2025-11-06)
**Feature: Intelligent Auto-Proceed**

### v1.4.0 (2025-11-05)
**Major: Context Optimization & DRY Consolidation**

### v1.3.0 (2025-10-30)
**Feature: TaskMaster-style Intelligent Task Analysis**

**Added:**
- 6-dimension task analysis in `/csetup`:
  - Complexity scoring (1-10)
  - Dependency detection (auto-detects blocks/blocked-by)
  - Risk assessment (LOW/MEDIUM/HIGH with mitigation)
  - Research requirements (auto-generates queries)
  - Subtask breakdown (complex tasks → smaller steps)
  - Priority ranking (CRITICAL → LOW, scored 0-100)
- Task analyzer implementation: `.claude/lib/task-analyzer.md`
- Enhanced phases.md with metadata, time buffers, research phases

**Improved:**
- Time estimates with automatic buffers (+41% average)
- Research phases auto-added for new tech/libraries
- Dependency order in workflow execution
- Risk mitigation strategies per task

**Inspired by:** [claude-task-master](https://github.com/eyaltoledano/claude-task-master)

### v1.2.0 (2025-10-27)
**Feature: Context Optimization - 70% Token Reduction**

**Added:**
- 3-tier loading strategy: STYLE_TOKENS.json (500) → design-context.md (1K) → STYLE_GUIDE.md (5K)
- Document loader protocol: `.claude/lib/document-loader.md`
- Lightweight design tokens: `design-system/STYLE_TOKENS.json`

**Improved:**
- Token usage: ~20K → ~4.7K (70% reduction for design system)
- Speed: 3-4x faster command execution
- Consistency: Enforced design tokens, no random colors

### v1.1.1 (2025-10-25)
**Patch: Minor Fixes**

**Fixed:**
- Template path correction: `template/.claude` → `.claude`
- Documentation typos and formatting

### v1.1.0 (2025-10-24)
**Feature: Enhanced Implementation Logic**

**Added:**
- Implementation logic overview: `lib/README.md`
- Agent executor with retry & escalation: `lib/agent-executor.md`
- TDD classifier logic: `lib/tdd-classifier.md`
- Progress tracking protocol: `lib/flags-updater.md`
- Mandatory agent routing: `lib/agent-router.md`
- Shared agent discovery flow: `contexts/patterns/agent-discovery.md`

### v1.0.0 (2025-10-20)
**Initial Release: Multi-Agent Template**

**Core Features:**
- 6 specialized agents (integration, uxui-frontend, test-debug, frontend, backend, database)
- OpenSpec integration (`/csetup`, `/cdev`, `/cview`, `/cstatus`)
- Auto-generated best practices via Context7 MCP
- 3-level project indexing (domain → project → best-practices)
- Design foundation (color theory, spacing, typography)
- `/designsetup` command (auto-generate style guide)
- `/pageplan` command (UI content & component planning)
- Universal patterns (logging, testing, error-handling, TDD)
- CLI: `cak init`, `cak update`

---

## 🔗 Links

- **npm Package:** https://www.npmjs.com/package/@champpaba/claude-agent-kit
- **GitHub:** https://github.com/ChampPABA/claude-multi-agent-template
- **OpenSpec:** https://github.com/Fission-AI/OpenSpec
- **Issues:** https://github.com/ChampPABA/claude-multi-agent-template/issues

---

## 💡 Quick Tips

1. **Run `/designsetup` FIRST** - Ensures visual consistency from day 1
2. **Use `/pageplan` for UI tasks** - 25% faster implementation, better content
3. **Review `page-plan.md` before `/cdev`** - Edit content, prepare assets
4. **Setup Context7 MCP** - Agents get latest framework docs automatically
5. **Use OpenSpec for complex features** - Better alignment before implementation
6. **Monitor with `/cview`** - See exactly what agents are doing
7. **Always use `--backup` when updating** - Protects your customizations

---

## 📋 Complete Flow Summary

```
1️⃣ OpenSpec Planning
   → proposal.md + tasks.md

2️⃣ Generate Style Guide (one-time)
   /designsetup
   → STYLE_GUIDE.md

3️⃣ Setup Project (one-time)
   /psetup
   → domain/{project}/best-practices/

4️⃣ Generate Page Plan (UI tasks only)
   /pageplan @prd.md
   → page-plan.md (content + component plan)

5️⃣ Setup Change Context
   /csetup {change-id}
   → workflow.md

6️⃣ Execute Implementation
   /cdev {change-id}
   → Working code + tests

7️⃣ Monitor Progress
   /cview {change-id}
   → Detailed progress report

8️⃣ OpenSpec Archive & Update
   → Merge to specs/
```

---

**Ready to implement with confidence?** 🚀

```bash
# Install globally
npm install -g @champpaba/claude-agent-kit

# Initialize in your project
cd your-project
cak init

# Setup project context
/psetup

# Generate style guide (optional but recommended)
/designsetup

# Start building (after OpenSpec planning)
/pageplan @prd.md           # UI tasks only
/csetup your-feature
/cdev your-feature
```

Let specialized agents handle implementation while you focus on specs and architecture!
