# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2025-11-30

### 🎯 Claude 4.5 Optimization + Design System v2.0

**Two Major Improvements in One Release:**

1. **Claude 4.5 Optimization** - All files refactored using Claude 4 best practices for better AI comprehension
2. **Design System v2.0** - Interactive setup, theme selection, selective pattern loading, page type detection

**Based on:** [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)

### Added

#### Claude 4.5 Optimization

- **Shared Components** - New `.claude/agents/_shared/` folder
  - `pre-work-checklist.md` - Common validation steps
  - `package-manager.md` - Package manager protocol
  - `documentation-policy.md` - What files to create
  - `agent-boundaries.md` - When to use which agent
  - `README.md` - Overview

#### Design System v2.0

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

#### Claude 4.5 Optimization

- **All 6 Agent Files** - Professional tone, positive instructions (~65% smaller)
  - Replaced "MUST", "WILL BE REJECTED" with professional explanations
  - Changed "Don't do X" to "Use Y instead" with WHY
  - Added table formats with WHY explanations
  - Deduplicated content to shared files

- **6 Lib Files** - WHY explanations, table formats
  - `agent-router.md` - Routing table format, removed "CANNOT/forbidden"
  - `agent-executor.md` - Professional rejection messages
  - `context-loading-protocol.md` - WHY explanations
  - `flags-updater.md` - Best practices table
  - `document-loader.md` - Table format for guidelines
  - `detailed-guides/agent-system.md` - Compact references

- **4 Command Files** - Softer language, guidelines
  - `cdev.md` - WHY context for best practices
  - `csetup.md` - Best Practices / Anti-Patterns format
  - `pageplan.md` - "Guidelines" instead of "CRITICAL Rules"
  - `designsetup.md` - "Follow this format" instead of "EXACT format"

- **11 Pattern Files** - "⚠️ Common Mistakes" instead of "🚨 Critical"
  - `validation-framework.md` - WHY explanations
  - `error-recovery.md` - "⚠️" instead of "🚨"
  - `ui-component-consistency.md` - "Common Issues" format
  - `task-breakdown.md` - Positive framing
  - `agent-discovery.md` - Softer language
  - `code-standards.md` - "File Creation Policy" with WHY
  - `animation-patterns.md` - "⚠️ Common Mistakes"
  - `frontend-component-strategy.md` - "⚠️ Anti-Patterns"
  - `performance-optimization.md` - "⚠️ Common Mistakes"
  - `change-workflow.md` - Table format for read-only files
  - `task-classification.md` - "Agent Capabilities Reference"

- **3 Design Files** - "should check" instead of "MUST check"
  - `index.md` - Softer language
  - `box-thinking.md` - "⚠️ Common Mistakes"

- **3 Template Files** - Table with WHY
  - `phases-sections/frontend-mockup.md` - Design rules table
  - `design-context-template.md` - "⚠️ Design Rules"
  - `STYLE_GUIDE.template.md` - "🔧 Troubleshooting"

- **Other Lib Files**
  - `lib/README.md` - "📌 Important"
  - `detailed-guides/taskmaster-analysis.md` - "🔴 HIGH"

#### Design System v2.0

- **`STYLE_GUIDE.md`** - Now human-readable only (~150 lines, no code)
  - For humans to review design direction
  - Code patterns moved to `patterns/*.md`
  - References patterns files for code examples

- **Context Optimization** - 84% token reduction
  - Before: Full STYLE_GUIDE.md ~5000 tokens loaded everywhere
  - After: tokens.json ~800 tokens + selective patterns
  - Page type detection determines which patterns to load

- **CLAUDE.md** - Updated to v2.0.0
  - New Claude 4.5 Optimization section
  - New Design System v2.0.0 section with complete flow
  - Updated Context Optimization section
  - Updated Page Planning section with page type handling table

### Performance

#### Agent Token Savings (Claude 4.5)

| Agent | Before | After | Reduction |
|-------|--------|-------|-----------|
| uxui-frontend | ~1037 lines | ~375 lines | 64% |
| integration | ~600 lines | ~210 lines | 65% |
| backend | ~700 lines | ~244 lines | 65% |
| database | ~680 lines | ~273 lines | 60% |
| frontend | ~650 lines | ~296 lines | 54% |
| test-debug | ~580 lines | ~252 lines | 57% |
| **Total Agents** | **~4247** | **~1650** | **61%** |
| Shared files | 0 | ~500 lines | - |
| **Grand Total** | ~4247 | ~2150 | **49%** |

#### Design System Token Savings

| Approach | Tokens | Improvement |
|----------|--------|-------------|
| Old: Full STYLE_GUIDE.md | ~5000 | - |
| New: tokens.json + selective patterns | ~800-1200 | **84%** |

### Page Type Handling

| Page Type | Decorations | Scroll Anims | Buyer Avatar | Patterns Loaded |
|-----------|-------------|--------------|--------------|-----------------|
| Landing/Marketing | ✅ Full | ✅ Enabled | ✅ Enabled | buttons, cards, scroll-anims, decorations |
| Dashboard/Admin | ❌ Minimal | ❌ Disabled | ❌ Skipped | buttons, cards, forms |
| Auth (Login/Register) | ❌ None | ❌ Disabled | ❌ Skipped | buttons, forms |

### Benefits

- ✅ **Better AI comprehension** - Claude 4.5 works better with professional tone
- ✅ **Clearer instructions** - Positive "Use X" instead of negative "Don't Y"
- ✅ **Intelligent rule application** - WHY context helps Claude apply rules correctly
- ✅ **Smaller context** - 61% token reduction in agent files
- ✅ **No duplication** - Shared components prevent copy-paste
- ✅ **84% design token reduction** - tokens.json + selective patterns
- ✅ **Theme consistency** - USE/AVOID decorations enforced
- ✅ **Smart patterns** - Only load what's needed per page type

### Migration Guide

**For existing projects:**

1. Run `/extract` to extract design from reference sites (optional):
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

### Breaking Changes

- `STYLE_TOKENS.json` renamed to `tokens.json` with new structure
- `STYLE_GUIDE.md` no longer contains code (moved to patterns/*.md)
- Commands now read `tokens.json` instead of `STYLE_TOKENS.json`

All existing workflows continue to work - these are only breaking changes for the design system file names.

---

## [1.8.0] - 2025-11-26

### 🔄 Token Optimization - Streamlined Workflow

**Removed:**
- `/psetup` command - Merged into `/csetup`
- `/agentsetup` command - Merged into `/csetup`
- `documentation` phase from all templates
- `report` phase from all templates

**Changed:**
- `/csetup` now auto-detects tech stack and generates best practices

---

## [1.7.1] - 2025-11-25

### 📁 File Naming Conventions Clarification

**Added:**
- Documentation clarifying OpenSpec `design.md` vs Template `STYLE_GUIDE.md`

---

## [1.7.0] - 2025-11-25

### 🧠 Opus 4.5 Model Upgrade

**Changed:**
- All 6 agents now use Claude Opus 4.5 model instead of Haiku

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
- **Dependency Detection** - Automatic dependency graph
- **Risk Assessment** - Automatic risk scoring (LOW/MEDIUM/HIGH)
- **Research Requirements** - Auto-detects need for research phases
- **Subtask Breakdown** - Intelligent task expansion
- **Priority Ranking** - Scoring system (0-100)

---

## [1.2.0] - 2025-01-05

### ⚡ Context Optimization - 70% Token Reduction

**Added:**
- 3-tier loading strategy
- STYLE_TOKENS.json lightweight design tokens
- Document loader protocol

**Performance:**
- Token usage: ~20K → ~4.7K (70% reduction)
- Speed: 3-4x faster command execution

---

## [1.1.0] - 2024-12-XX

### Added
- TDD classification logic
- Agent retry & escalation
- Validation enforcement framework
- Progress tracking protocol
- Mandatory agent routing

---

## [1.0.0] - 2024-11-XX

### Initial Release
- 6 specialized agents
- `/designsetup` command
- `/pageplan` command
- OpenSpec integration
- 3-level indexing
- Context7 MCP integration

---

**Legend:**
- `Added` - New features
- `Changed` - Changes in existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security fixes
