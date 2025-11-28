# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2025-01-28

### 🎨 Design System v2.0.0 - Interactive Setup & Smart Page Planning

**Major Release:** Complete overhaul of design system with interactive setup, theme selection, selective pattern loading, and auto page type detection.

### Added

- **`/extract` command** - Multi-URL design extraction
  - Extract from multiple reference sites (merged-insights.json)
  - Style detection (Neo-Brutalism, Minimalist, Glassmorphism, Modern SaaS, Playful)
  - Animation library detection (GSAP, ScrollTrigger, Framer Motion, Lottie, AOS)
  - Scroll pattern detection (stacking-cards, parallax, fade-in, slide-in, sticky-section)
  - Decorative element detection (blobs, gradients, 3D elements, SVG decorations)
  - Output: `.claude/extractions/*.json` + `merged-insights.json`

- **Interactive Design Setup** - `/designsetup` v2.0.0
  - 3-round interactive loop (Present → Feedback → Adjust)
  - Verbose style options with match scores
  - Theme + decorative direction recommendation (AI recommends based on project context)
  - USE/AVOID elements for theme consistency
  - Max 3 rounds until user accepts 100%

- **`tokens.json` v2.0.0** - Enhanced design tokens (~800 tokens)
  - New `style` section (name, confidence, characteristics, feel, source_site)
  - New `theme` section (name, description, feeling, decorative_elements.use/avoid, icons_suggestion)
  - New `animations` section (enabled, libraries, selected_patterns, scroll_animations, component_animations)
  - New `patterns_index` section (references to patterns/*.md files)
  - Colors, typography, spacing, shadows, borders from extracted data

- **`patterns/*.md` files** - Selective code patterns for agents
  - `buttons.md` - Button patterns (primary, secondary, ghost, outline, icon, sizes, states)
  - `cards.md` - Card patterns (default, interactive, feature, pricing, testimonial)
  - `forms.md` - Form patterns (input, error state, select, checkbox, layout)
  - `scroll-animations.md` - Scroll animation patterns (fade-in, stacking-cards, parallax, slide-in)
  - `decorations.md` - Decorative elements (gradients, blobs, grids, floating elements, dividers)

- **Auto Page Type Detection** - `/pageplan` v2.0.0
  - Auto-detects page type from `proposal.md`/`tasks.md` (landing/dashboard/auth)
  - Reads `tokens.json` for style/theme/animations
  - Loads patterns selectively based on page type
  - Landing/Marketing: Full decorations, scroll animations, buyer avatar analysis
  - Dashboard/Admin: Minimal decorations, data-focused, no buyer avatar
  - Auth (Login/Register): Clean, form-focused, no decorations

- **`/csetup` v2.0.0 enhancements**
  - Reads `tokens.json` instead of `STYLE_TOKENS.json`
  - Reads `page-plan.md` if exists
  - Extracts page type from page-plan.md
  - Includes page type info in context.md with pattern loading instructions

### Changed

- **`STYLE_GUIDE.md`** - Now human-readable only (~150 lines, no code)
  - For humans to review design direction
  - Code patterns moved to `patterns/*.md`
  - References patterns files for code examples

- **Context Optimization** - 84% token reduction
  - Before: Full STYLE_GUIDE.md ~5000 tokens loaded everywhere
  - After: tokens.json ~800 tokens + selective patterns
  - Page type detection determines which patterns to load

- **CLAUDE.md** - Updated to v2.0.0
  - New Design System v2.0.0 section with complete flow
  - New Context Optimization v2.0.0 section
  - Updated Page Planning section with page type handling table
  - New flow diagram: extract → designsetup → pageplan → csetup → cdev

### Page Type Handling

| Page Type | Decorations | Scroll Anims | Buyer Avatar | Patterns Loaded |
|-----------|-------------|--------------|--------------|-----------------|
| Landing/Marketing | ✅ Full | ✅ Enabled | ✅ Enabled | buttons, cards, scroll-anims, decorations |
| Dashboard/Admin | ❌ Minimal | ❌ Disabled | ❌ Skipped | buttons, cards, forms |
| Auth (Login/Register) | ❌ None | ❌ Disabled | ❌ Skipped | buttons, forms |

### Migration Guide

**For existing projects:**

1. Run `/extract` to extract design from reference sites:
   ```bash
   /extract https://your-reference.com
   ```

2. Run `/designsetup` to generate new design system:
   ```bash
   /designsetup @prd.md
   ```

3. Verify new files exist:
   ```bash
   ls design-system/tokens.json
   ls design-system/patterns/
   ls design-system/STYLE_GUIDE.md
   ```

4. Continue normal workflow:
   ```bash
   /pageplan @prd.md
   /csetup feature-name
   /cdev feature-name
   ```

**Breaking Changes:**
- `STYLE_TOKENS.json` renamed to `tokens.json` with new structure
- `STYLE_GUIDE.md` no longer contains code (moved to patterns/*.md)
- Commands now read `tokens.json` instead of `STYLE_TOKENS.json`

---

## [1.6.0] - 2025-01-27

### 📋 Page Plan Enhancement - Buyer Avatar & Conversion Copy

**Added:**
- Buyer avatar analysis (Eugene Schwartz framework) for marketing pages
- Conversion-optimized content generation (pain → promise → CTA)
- Auto-detection of marketing vs dashboard pages

---

## [1.5.1] - 2025-01-26

### 🔧 Git Compatibility Fix

**Fixed:**
- Normalized line endings to LF for Windows compatibility

---

## [1.5.0] - 2025-01-25

### ✨ Minor Improvements

**Added:**
- Various stability improvements
- Documentation updates

---

## [1.3.0] - 2025-01-05

### 🧠 TaskMaster Integration - Intelligent Task Analysis

**Major Intelligence Upgrade:** Enhanced /csetup with 6-dimensional task analysis (complexity, dependencies, risk, research, subtasks, priority).

**Inspired by:** [claude-task-master](https://github.com/eyaltoledano/claude-task-master)

### Added

- **task-analyzer.md** - Complete task analysis framework
  - Location: `.claude/lib/task-analyzer.md`
  - 6 analysis dimensions
  - ~500 lines of analysis logic

- **Complexity Scoring** - Automatic task complexity assessment (1-10)
  - Factors: Time, keywords, multi-step, dependencies
  - Levels: Simple (1-3), Moderate (4-6), Complex (7-8), Critical (9-10)
  - Auto-adjusts time estimates with buffers

- **Dependency Detection** - Automatic dependency graph
  - Detects: UI → Backend, Backend → Database, Tests → Implementation
  - Outputs: Blocks, Blocked by, Parallelizable tasks
  - Ensures correct execution order

- **Risk Assessment** - Automatic risk scoring
  - Levels: LOW, MEDIUM, HIGH
  - Factors: Complexity, security, external deps, migrations
  - Mitigation strategies: TDD, security checklist, time buffer, pair programming

- **Research Requirements** - Auto-detects need for research phases
  - Categories: New tech, best practices, integration, performance, migration
  - Generates research queries automatically
  - Adds Phase 0.x (before implementation)

- **Subtask Breakdown** - Intelligent task expansion
  - When: Complexity >= 7, multiple verbs, time > 90 min
  - Patterns: UI + Backend, CRUD operations, multi-entity
  - Example: Login system → 5 subtasks

- **Priority Ranking** - Scoring system (0-100)
  - Labels: CRITICAL (80+), HIGH (60-79), MEDIUM (40-59), LOW (0-39)
  - Factors: Business value, blockers, risk, complexity
  - Tasks sorted by priority in phases.md

### Changed

- **`/csetup` command** - STEP 3.5: Task Analysis added
  - Analyzes all tasks from tasks.md
  - Generates task metadata (complexity, deps, risk, etc.)
  - Sorts tasks by priority
  - Reports analysis summary to user

- **phases.md template** - Enhanced with task metadata
  - Task Analysis Summary section
  - Research phases (Phase 0.x) added automatically
  - Each phase includes:
    - Complexity score & level
    - Priority label & score
    - Risk level & mitigation
    - Dependencies graph
    - Subtasks (if applicable)
    - Adjusted time estimates

- **CLAUDE.md** - v1.3.0 with TaskMaster section
  - New section: "TaskMaster-style Analysis"
  - 6 analysis dimensions explained
  - Before/after comparison
  - Generated output examples
  - Workflow guide

### Examples

**Task Analysis Output:**
```
✅ Task Analysis Complete

📊 Summary:
   Total tasks: 8 → 15 (subtask expansion)
   Average complexity: 5.8/10

📈 Priority Distribution:
   🔴 CRITICAL: 2 (Login, Payment)
   🟠 HIGH: 3 (User Profile, API endpoints)
   🟡 MEDIUM: 2 (Email notifications)
   🟢 LOW: 1 (Documentation)

⚠️ Risk Assessment:
   🚨 HIGH: 2 tasks → TDD required, security checklist
   ⚠️ MEDIUM: 3 tasks
   ✅ LOW: 3 tasks

🔬 Research Required: 2 tasks
   - React Query v5 migration (15 min)
   - Stripe payment best practices (15 min)

⏱️ Time Estimates:
   Original: 6.5 hours
   Adjusted: 9.2 hours (+41% buffer)
```

### Benefits

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Task Analysis** | Basic | Intelligent | 6 dimensions |
| **Complexity** | Ignored | Scored 1-10 | Risk-aware |
| **Dependencies** | Manual | Auto-detected | Faster planning |
| **Time Estimates** | Optimistic | With buffer | +30-50% accuracy |
| **Research Phases** | Missing | Auto-added | Informed decisions |
| **Subtasks** | None | Auto-expanded | Clearer workflow |
| **Priority** | Random | Scored 0-100 | Right execution order |

---

## [1.2.0] - 2025-01-05

### ⚡ Context Optimization - 70% Token Reduction

**Major Performance Improvement:** Optimized design context loading to reduce token usage from ~20K to ~4.7K tokens while maintaining quality.

### Added

- **STYLE_TOKENS.json** - Lightweight design tokens file (~500 tokens)
  - Auto-generated by `/designsetup` command
  - Contains: colors, spacing, typography, shadows, borders, animations
  - Replaces full STYLE_GUIDE.md for most commands

- **design-context-template.md** - Project design summary template
  - Location: `.claude/templates/design-context-template.md`
  - Generated per project with design system overview
  - ~1K tokens vs ~5K for full style guide

- **document-loader.md** - Unified document loading pattern
  - Location: `.claude/lib/document-loader.md`
  - 3-tier loading strategy (tokens → context → full guide)
  - Pattern A (Planning), Pattern B (Execution), Pattern C (Agents)

### Changed

- **`/designsetup` command** - Now generates both STYLE_GUIDE.md and STYLE_TOKENS.json
  - STEP 5.5: Extract design tokens to JSON
  - Validates JSON before writing
  - Reports both files in final output

- **`/pageplan` command** - Uses STYLE_TOKENS.json instead of full STYLE_GUIDE.md
  - Token usage: ~1.5K (was ~5K)
  - Loads: STYLE_TOKENS.json + validates STYLE_GUIDE.md exists
  - 70% reduction in loading time

- **`/csetup` command** - Validates design system for UI work
  - STEP 2.5: Design System Validation (new)
  - Warns if STYLE_GUIDE.md or STYLE_TOKENS.json missing
  - Adds design info to context.md

- **`/cdev` command** - Sends design reference instead of full content
  - buildAgentPrompt() function added
  - Sends file paths (~200 tokens) instead of content (~5K tokens)
  - Enforces STEP 0.5 design loading for uxui-frontend agent

- **CLAUDE.md** - Updated to v1.2.0 with Context Optimization documentation
  - New section: "Context Optimization (v1.2.0)"
  - Updated Quick Navigation with STYLE_TOKENS.json
  - Token comparison table (before/after)

### Performance

| Metric | Before (v1.1.0) | After (v1.2.0) | Improvement |
|--------|----------------|---------------|-------------|
| **Total tokens** | ~20,000 | ~4,700 | **70% reduction** |
| **Loading speed** | Slow | Fast | **3-4x faster** |
| **/pageplan** | ~5,000 tokens | ~1,500 tokens | **70% faster** |
| **/csetup** | ~5,000 tokens | ~500 tokens | **90% faster** |
| **/cdev** | ~5,000 tokens | ~200 tokens | **96% faster** |
| **uxui-frontend agent** | ~5,000 tokens | ~3,500 tokens | **30% faster** |

### Migration Guide

**For existing projects:**

1. Run `/designsetup` again to generate STYLE_TOKENS.json:
   ```bash
   /designsetup
   ```

2. Verify both files exist:
   ```bash
   ls design-system/STYLE_GUIDE.md
   ls design-system/STYLE_TOKENS.json
   ```

3. Continue normal workflow:
   ```bash
   /psetup
   /csetup feature-name
   /cdev feature-name
   ```

**No breaking changes** - All commands backward compatible!

---

## [1.1.0] - 2024-12-XX

### Added
- TDD classification logic (`.claude/lib/tdd-classifier.md`)
- Agent retry & escalation (`/agent-executor.md`)
- Validation enforcement framework
- Progress tracking protocol (`flags-updater.md`)
- Mandatory agent routing (`agent-router.md`)

### Changed
- `/csetup` now classifies TDD requirements per phase
- `/cdev` implements retry logic (max 2 retries)
- Validation gates enforce pre-work checklists

---

## [1.0.0] - 2024-11-XX

### Initial Release
- 6 specialized agents (integration, uxui-frontend, backend, database, frontend, test-debug)
- `/designsetup` command (auto-generate style guide)
- `/pageplan` command (page planning with component reuse)
- OpenSpec integration (`/csetup`, `/cdev`, `/cview`, `/cstatus`)
- 3-level indexing (project discovery)
- Context7 MCP integration (dynamic best practices)

---

## [Unreleased]

### Planned for 1.3.0
- TaskMaster-style task analysis (subtask breakdown, risk scoring)
- `cak init` smart merge (overwrite templates, keep user files)
- Enhanced `/csetup` with dependency graph and research phases

---

**Legend:**
- `Added` - New features
- `Changed` - Changes in existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security fixes
