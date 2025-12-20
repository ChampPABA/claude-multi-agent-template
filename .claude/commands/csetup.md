---
name: Change Setup
description: Setup change context by analyzing tasks and generating agent workflow
category: Multi-Agent
tags: [setup, change, multi-agent]
---

## Usage

```bash
/csetup {change-id}
```

## What It Does

Analyzes OpenSpec files (proposal, tasks, design) and:
1. **Parses ALL tasks** from tasks.md (single source of truth)
2. **AI-driven analysis** - complexity, risk, dependencies, agent assignment
3. **Auto-adds best practices** - checkpoints, error handling, verification
4. **Generates incremental milestones** for complex tasks
5. Generates `.claude/phases.md` (agent workflow)
6. Generates `.claude/flags.json` (progress tracking)
7. Generates `.claude/context.md` (change-specific tech)

**v2.0 Architecture:** Template-Free, AI-Driven

## Steps

### Step 1: Check Prerequisites

```bash
# Check if change exists
ls openspec/changes/{change-id}/
```

If not found:
```
❌ Error: Change {change-id} not found
Please create the change with OpenSpec first
```

### Step 1.5: Read PROJECT_STATUS.yml (v2.1.0)

**WHY:** Cross-session context helps understand blockers and infrastructure state before starting work.

1. Check if `PROJECT_STATUS.yml` exists in project root

**If file exists:**

2. Read the file `PROJECT_STATUS.yml`

3. Output header:
```
📊 Project Context (from PROJECT_STATUS.yml)
```

4. **If `current_focus.description` exists:**
   - Output: `   Focus: {description}`

5. **Check for blockers that might affect this change:**
   - Look at `blockers` array
   - For each blocker, check if `blocks` field contains:
     - The change-id (case-insensitive)
     - OR any keyword from change-id
     - OR vice versa

   **If relevant blockers found:**
   ```
   ⚠️ Potential blockers for this change:
      - {blocker.id}: {blocker.description}
      ... (for each relevant blocker)

   Consider resolving blockers before starting.
   ```

6. **Check infrastructure status:**
   - Look at `infrastructure` section
   - Find services where `status` is 'down' or 'degraded'

   **If degraded services found:**
   ```
   ⚠️ Infrastructure issues:
      - {service}: {status} ({notes if present})
      ... (for each down/degraded service)
   ```

7. **Check pending follow-ups (v2.1.6):**
   - Read `openspec/changes/{changeId}/proposal.md` (if exists)
   - Look at `pending_followups` array
   - For each pending item, check if `affects` field matches:
     - Change-id contains pattern
     - OR proposal contains pattern
     - OR special database patterns (db→table, schema→model, migration→database)

   **If related pending items found:**
   ```
   ⚠️ Found related pending follow-ups:
      - "{item}" (from {from_change})
        Reason: {reason}
        Affects: {affects list}
      ... (for each related pending)

   This change may be affected by unresolved follow-ups.
   Options:
      1. Continue anyway (risk: issues like schema sync)
      2. Address follow-up first (create separate proposal)
      3. Include follow-up in this change's scope

   How to proceed? (1/2/3)
   ```

   → Wait for user input

   **If user chose 2:**
   ```
   ❌ Setup paused. Create proposal for pending follow-up first.
   ```
   → STOP execution, exit command

   **If user chose 3:**
   ```
   ℹ️ Remember to include follow-up items in tasks.md
   ```
   → Continue

   **If user chose 1 or other:**
   ```
   ⚠️ Continuing with caution. Monitor for related issues.
   ```
   → Continue

8. **Check if status is stale:**
   - Calculate days since `last_updated`
   - Compare with `_config.stale_warning_days` (default: 7)

   **If days > threshold:**
   ```
   ℹ️ PROJECT_STATUS.yml last updated {days} days ago.
      Consider running /pstatus to refresh.
   ```

9. **Update active change if needed:**
   - Check if `current_focus.active_change` equals current changeId

   **If NOT equal:**
   - Ask user:
   ```
   📍 Update current_focus.active_change to "{changeId}"? (yes/no)
   ```

   **If user approves:**
   - Set `current_focus.active_change = changeId`
   - Set `last_updated = today's date (YYYY-MM-DD)`
   - Write updated YAML back to `PROJECT_STATUS.yml`
   - Output: `   ✅ Updated active_change to "{changeId}"`

10. Output blank line

**If file does not exist:**
- Skip to next step (no output needed)

### Step 1.6: Memory Context Query (v2.2.0 - claude-mem Integration)

**WHY:** Query past work to leverage decisions, avoid repeating mistakes, and maintain consistency.

1. Extract keywords from change-id:
   - Replace hyphens with spaces
   - Example: `add-auth-system` → `add auth system`

2. Read `openspec/changes/{changeId}/proposal.md` (if exists)
   - Extract first heading line (proposal title)
   - If no file or no heading, use changeId as title

3. Output:
```
🧠 Querying claude-mem for related past work...
```

4. Query claude-mem using natural language questions:
   - "decisions about {keywords}"
   - "bugs related to {keywords}"
   - "implementations of {keywords}"

   **Note:** The mem-search skill will auto-invoke when you ask these questions naturally.

5. Store results in memory for later use

6. Output:
```
   Searched for: {keywords}
   (Results will be included in pre-work-context.md if relevant)
```

7. Output blank line

---

**Integration with pre-work-context.md:**

When generating `pre-work-context.md` (Step 2.6.7), include a "Past Learnings" section:

**If relevant observations found:**
```markdown
## Past Learnings (from claude-mem)

> Related observations from previous sessions:

| ID | Type | Summary | Relevance |
|----|------|---------|-----------|
| #{id} | {type} | {summary} | {HIGH/MEDIUM/LOW} |
... (for each observation)

### Key Takeaways:
- {takeaway 1}
- {takeaway 2}
```

**If no relevant observations found:**
```markdown
## Past Learnings (from claude-mem)

No related past work found. Proceeding fresh.
```

---

### Step 2: Read OpenSpec Files

Read in order:
1. `openspec/changes/{change-id}/proposal.md`
2. `openspec/changes/{change-id}/tasks.md`
3. `openspec/changes/{change-id}/design.md` (if exists)

---

### Step 2.5: Validate Design System & Page Plan (v2.0.0)

> **Updated v2.0.0:** Validate design files + read page-plan.md if exists

1. Read `openspec/changes/{change-id}/tasks.md`

2. **Check if change involves UI/frontend work:**
   - Search tasks.md (case-insensitive) for keywords:
     - ui, component, page, frontend, design, responsive
   - Store result as `hasFrontend`

**If hasFrontend is TRUE:**

3. Output:
```
🎨 UI work detected - validating design system...
```

4. Check if these files exist:
   - `design-system/data.yaml`
   - `design-system/README.md`
   - `openspec/changes/{changeId}/page-plan.md`

5. **If `data.yaml` exists:**
   - Read and parse `design-system/data.yaml`
   - Output:
   ```
   ✅ data.yaml Loaded:
      - Style: {tokens.style.name}
      - Theme: {tokens.theme.name}
      - Animations: {Enabled/Disabled based on tokens.animations.enabled}
   ```
   - Store parsed tokens for later use

6. **If `page-plan.md` exists:**
   - Read `openspec/changes/{changeId}/page-plan.md`
   - Output:
   ```
   ✅ page-plan.md Found
   ```
   - Search for line matching pattern: `Page Type:**` or `**Page Type:**`
   - Extract page type value (trim whitespace, convert to lowercase)
   - Output: `   - Page Type: {pageType}`
   - Store page type for later use

   **If `page-plan.md` does NOT exist:**
   ```
   ℹ️ page-plan.md not found (optional)
      → Run /pageplan first for better component planning
   ```

7. **Check completeness:**

   **If `data.yaml` OR `README.md` is missing:**
   - Output warning:
   ```
   ⚠️ WARNING: UI work detected but design system incomplete!

   Found:
     {✅/❌} README.md (human-readable)
     {✅/❌} data.yaml
     {✅/❌} page-plan.md

   This may result in:
     - Inconsistent colors (random hex codes)
     - Arbitrary spacing (p-5, gap-7)
     - Duplicate components

   Recommendation:
     1. Run: /designsetup
     2. Run: /pageplan @prd.md (optional but recommended)
     3. Then: /csetup {changeId}

   Continue anyway? (yes/no)
   ```

   → Wait for user input

   **If user answered 'no':**
   - Output: `Setup cancelled. Run /designsetup first.`
   - STOP execution, exit command

   **If user answered 'yes' or other:**
   - Continue to next step

   **If both `data.yaml` AND `README.md` exist:**
   ```
   ✅ Design System Ready
      - README.md ✓ (human-readable)
      - data.yaml ✓
      - page-plan.md ✓   (only if exists)
   ```

**If hasFrontend is FALSE:**
- Skip all steps above, continue to Step 2.6

---

### Step 2.6: Generate Pre-Work Context (v3.2.0 - Consolidated)

> **EXECUTE THESE STEPS** - Not pseudocode, actual instructions for Main Claude
> **Output:** `openspec/changes/{changeId}/pre-work-context.md`
> **Purpose:** Single file containing ALL context agents need before implementation

**This step consolidates:**
- Adaptive Depth Research (domain knowledge)
- Library Best Practices (from Context7)
- Integration Warnings (cross-library concerns)
- Critical Checklists (security/compliance requirements)

---

#### Step 2.6.1: Analyze Change Characteristics

**Read and analyze these files:**
- `openspec/changes/{changeId}/proposal.md`
- `openspec/changes/{changeId}/tasks.md`
- `openspec/changes/{changeId}/design.md` (if exists)

**Determine:**
1. **Primary Type:** marketing | dashboard | api | auth | database | general
2. **Complexity (1-10):** Based on features, integrations, external APIs
3. **Risk Level:** LOW | MEDIUM | HIGH
4. **Domains:** healthcare, fintech, ecommerce, saas (if applicable)
5. **Features:** payment, auth, multi-tenancy, realtime (if detected)

**Output:**
```
📊 Change Analysis:
   Type: auth
   Complexity: 6/10
   Risk Level: HIGH
   Domains: fintech
   Features: payment, auth
```

---

#### Step 2.6.2: Detect Libraries

**Read these files and identify library/framework names:**
- `package.json` (dependencies, devDependencies)
- `requirements.txt` or `pyproject.toml` (Python)
- `openspec/changes/{changeId}/proposal.md`
- `openspec/changes/{changeId}/design.md`

**Look for:** React, Next.js, Vue, Angular, FastAPI, Express, Django, Prisma, Drizzle, SQLAlchemy, Vitest, Jest, Playwright, Stripe, better-auth, etc.

**Output:**
```
🔍 Libraries Detected:
   - Next.js (from package.json)
   - Prisma (from design.md)
   - better-auth (from tasks.md)
```

---

#### Step 2.6.3: Fetch Best Practices via Context7

**For EACH detected library, call these MCP tools:**

```
1. mcp__context7__resolve-library-id
   Input: { libraryName: "Next.js" }
   Output: Get the context7CompatibleLibraryID (e.g., "/vercel/next.js")

2. mcp__context7__get-library-docs
   Input: {
     context7CompatibleLibraryID: "/vercel/next.js",
     topic: "best practices, patterns, common mistakes, [other-lib-names]",
     mode: "code"
   }
   Output: Documentation with best practices
```

**Smart Topic Query:** Include OTHER detected library names in the topic for cross-library integration docs.
Example: When fetching Prisma docs, include "Next.js, React" in topic.

**Skip if:**
- Library not found in Context7 (note in warnings section instead)
- Library already has cached best practices from previous run

---

#### Step 2.6.4: Determine Research Layers

**Based on change analysis, select relevant research layers:**

| Trigger | Layer | Focus |
|---------|-------|-------|
| Always (complexity > 1) | Best Practices | How do others do this? |
| hasAuth OR hasPayment | Security | Authentication, data protection |
| healthcare OR fintech | Compliance | HIPAA, PCI-DSS, regulations |
| isExternalFacing + hasUI | UX Patterns | User journey, accessibility |
| marketing type | Conversion Psychology | Triggers, objections, social proof |
| hasDatabase | Data Architecture | Normalization, indexing, scaling |
| hasAPI | API Design | REST/GraphQL, versioning, errors |
| payment feature | Payment Flows | PCI compliance, webhooks, idempotency |

**For each selected layer, generate:**
- 3-5 key questions to consider
- 2-3 recommendations from domain knowledge
- Warnings if applicable

---

#### Step 2.6.5: Detect Integration Warnings

**Cross-reference library combinations for known issues:**

| Combination | Warning |
|-------------|---------|
| better-auth + custom JWT | better-auth handles JWT internally - don't duplicate |
| Prisma + serverless | Cold starts can timeout - use connection pooling |
| Next.js 14+ + pages router | App router is default - check which is intended |
| React 19 + old state libs | Check compatibility with new React features |

**Check Context7 docs for integration warnings:**
- Look for "migration", "breaking changes", "compatibility" in docs
- Note version-specific warnings

---

#### Step 2.6.6: Generate Critical Checklist Items

**Based on change characteristics, inject required items:**

**If hasAuth:**
```
☐ Password hashing with bcrypt/argon2 (cost ≥ 10)
☐ Rate limiting on login (max 5 per 15 min)
☐ Session timeout configured
☐ CSRF protection on state-changing endpoints
☐ Cookies: httpOnly, secure, sameSite=strict
```

**If hasPayment:**
```
☐ NO raw card storage (use Stripe tokens)
☐ HTTPS on all payment pages
☐ Webhook signature verification
☐ Idempotency keys for payments
☐ Server-side price verification
```

**If healthcare/fintech:**
```
☐ Encryption at rest for PII/PHI
☐ Audit logging for sensitive data access
☐ Data minimization applied
☐ Compliance documentation prepared
```

---

#### Step 2.6.7: Write pre-work-context.md

**Create `openspec/changes/{changeId}/pre-work-context.md`:**

```markdown
# Pre-Work Context: {changeId}

> **Generated:** {date}
> **Purpose:** All context agents need before implementation
> **Read by:** All agents in STEP 0

---

## 1. Change Analysis

| Aspect | Value |
|--------|-------|
| Type | {primaryType} |
| Complexity | {complexity}/10 |
| Risk Level | {riskLevel} |
| Domains | {domains or "General"} |
| Features | {features or "None detected"} |

---

## 2. Library Best Practices

### {Library 1}

**Source:** Context7 ({context7Id})

**DO:**
- {best practice 1}
- {best practice 2}

**DON'T:**
- {anti-pattern 1}
- {anti-pattern 2}

**Code Example:**
```{lang}
{example code from Context7}
```

### {Library 2}
{repeat structure}

---

## 3. Research Findings

### L1: {Layer Name}

**Key Questions:**
- {question 1}
- {question 2}

**Recommendations:**
- {recommendation based on domain knowledge}

**Warnings:**
- {warning if applicable}

{repeat for each layer}

---

## 4. Integration Warnings

⚠️ **{Library A} + {Library B}:**
{warning description}

⚠️ **{Another combination}:**
{warning description}

---

## 5. Critical Checklist

> **MUST complete before marking phase done**

### Security
{security items if applicable}

### Compliance
{compliance items if applicable}

### Data Protection
{data items if applicable}

---

## 6. Quick Reference

**Package Manager:** {from tech-stack.md or detected}
**Test Command:** {detected test script}
**Build Command:** {detected build script}

---

**Agents: Read this file in STEP 0 before implementation.**
```

---

#### Step 2.6.8: Output Summary

```
✅ Pre-Work Context Generated!

   📄 File: openspec/changes/{changeId}/pre-work-context.md

   Contents:
   - Change Analysis: {type}, {complexity}/10, {risk}
   - Libraries: {count} ({names})
   - Research Layers: {count}
   - Integration Warnings: {count}
   - Critical Checklist Items: {count}

   📌 Agents will read this in STEP 0
```

---

#### Step 2.6.9: Skip Conditions

**Skip this step entirely if:**
- Change is trivial (complexity = 1, risk = LOW, no special features)
- Output: `✅ Pre-Work Context: Skipped (trivial change)`

**Skip library lookup if:**
- No new libraries detected
- All libraries already have Context7 cache

---

**⚠️ IMPORTANT:** This step requires YOU (Main Claude) to:
1. Actually read the spec files
2. Actually call Context7 MCP tools
3. Actually write the pre-work-context.md file

Do NOT treat this as pseudocode. EXECUTE these instructions.

---

### Step 2.7: Library Capability Validation (v2.2.0)

> **NEW:** Verify chosen libraries support ALL spec requirements before proceeding
> **WHY:** Prevents spec drift - discovering during implementation that library doesn't support requirements

1. Output:
```
🔍 Validating Library Capabilities...
```

2. Check if `openspec/changes/{changeId}/design.md` exists

**If design.md does NOT exist:**
```
   ⚠️ No design.md found - skipping library validation
```
→ Skip to Step 3

**If design.md exists:**

3. Read `openspec/changes/{changeId}/design.md`

4. **Detect libraries mentioned in design.md:**

   Search for these library patterns (case-insensitive):

   | Library | Search Patterns | Context7 ID | Known Limitations |
   |---------|----------------|-------------|-------------------|
   | better-auth | better-auth, betterauth | (none) | ❌ refresh token rotation, ❌ redis session, ✅ jwt plugin, ✅ bearer plugin, ✅ session-based auth |
   | nextauth | next-auth, nextauth, authjs | /nextauthjs/next-auth | (none) |
   | lucia | lucia, lucia-auth | /lucia-auth/lucia | (none) |
   | prisma | prisma | /prisma/prisma | (none) |
   | drizzle | drizzle | /drizzle-team/drizzle-orm | (none) |

   **If libraries found:**
   ```
   📚 Libraries in Spec:
      - {library1}
      - {library2}
      ...
   ```

5. **Extract requirements from design.md:**

   Search for these requirement patterns:

   | Requirement | Search Pattern |
   |-------------|----------------|
   | JWT access token | jwt + (access OR token) + (number + min) |
   | Refresh token | refresh token |
   | Token rotation | rotation OR rotate |
   | Redis session | redis + session (any order) |
   | Bearer token | bearer + (token OR auth) |
   | OAuth providers | oauth OR google OR github OR social login |
   | Rate limiting | rate limit |
   | Account lockout | lockout OR lock account |

   **If requirements found:**
   ```
   📋 Spec Requirements Found:
      - {requirement1}
      - {requirement2}
      ...
   ```

6. **Check each library's capabilities:**

   For each detected library:
   ```
   🔍 Checking {library} capabilities...
   ```

   For each requirement:
   - Check known limitations database
   - Match requirement with limitation feature (partial match OK)

   **If known limitation says NOT supported:**
   ```
      ❌ {requirement} - NOT SUPPORTED
   ```
   → Add to capability gaps list

   **If known limitation says supported:**
   ```
      ✅ {requirement} - Supported
   ```

   **If unknown (not in limitations database):**
   - **If library has Context7 ID:**
     ```
        🔍 {requirement} - Checking Context7...
        ⚠️ {requirement} - Verify manually
     ```
   - **If NO Context7 ID:**
     ```
        ⚠️ {requirement} - Verify manually (no Context7 mapping)
     ```

7. **Report capability gaps (if any):**

   **If gaps found:**
   ```
   ⚠️ Library Capability Gaps Detected!

   The following spec requirements are NOT supported by chosen libraries:

      {library1}:
        - {requirement1}
        - {requirement2}
      {library2}:
        - {requirement3}

   This will cause spec drift during implementation!

   Options:
      A) Change library - Use a library that supports these features
      B) Downgrade spec - Remove unsupported requirements (must document trade-off)
      C) Custom implementation - Build missing features on top of library
      D) Continue anyway - Proceed and let agent handle at implementation time
   ```

   → Ask user: "How would you like to handle the capability gaps?"

   **If user chose A (Change library):**
   ```
   📝 Suggested alternative libraries:
   ```
   - If better-auth has gaps:
     ```
        Instead of better-auth, consider:
        - lucia-auth (supports custom session storage)
        - NextAuth.js (supports refresh token rotation with JWT strategy)
        - Custom implementation with jose + Redis

     Please update design.md with new library choice and re-run /csetup.
     ```
   → STOP execution, exit command

   **If user chose B (Downgrade spec):**
   ```
   📝 Update design.md to remove unsupported requirements:

   ```markdown
   ### D{n}: Library Capability Alignment

   **Changed requirements to match {library} capabilities:**

   - ~~{requirement1}~~ → Use {library}'s default approach instead
   - ~~{requirement2}~~ → Use {library}'s default approach instead

   **Reason:** Library limitation
   **Trade-off:** {requirement1}, {requirement2} not available
   **Date:** {today's date YYYY-MM-DD}
   ```

   Please update design.md and re-run /csetup.
   ```
   → STOP execution, exit command

   **If user chose C (Custom implementation):**
   ```
   📝 Custom implementation notes for agents:

   Add to context.md:
   ```markdown
   ## Custom Implementation Required

   The following features need custom implementation:
   - {requirement1} (not supported by {library1})
   - {requirement2} (not supported by {library2})

   Agents should implement these on top of the base library.
   ```
   ```
   → Store gaps for context.md generation (Step 7)
   → Continue to Step 3

   **If user chose D (Continue anyway):**
   → Store gaps for agent awareness
   → Continue to Step 3

   **If NO gaps found:**
   ```
   ✅ All spec requirements supported by chosen libraries
   ```

**If no libraries detected:**
```
   ℹ️ No specific libraries detected in spec
```

8. Store capability analysis for later use:
   - Detected libraries
   - Spec requirements
   - Capability gaps
   - Custom implementation needs

---


---

### Step 3: Task Analyzer v2.0 (Template-Free, AI-Driven)

> **NEW in v2.0:** No templates, no keyword matching. AI analyzes tasks and makes decisions.
> **See:** `.claude/lib/task-analyzer.md` for complete analysis logic

1. Read `openspec/changes/${changeId}/tasks.md`

2. Output:
```
📊 Task Analyzer v2.0 (Template-Free)...
```

3. **Parse ALL tasks from tasks.md:**
   - Extract EVERY checkbox item
   - Pattern: `- [ ] {id} {description}`
   - Nothing is filtered out
   - Output: `   Found: {count} tasks from tasks.md`

4. Output:
```
🔍 Analyzing each task...
```

5. **AI-Driven Analysis - For EACH task, determine:**

   **a) Complexity (1-10):**
   - Consider: number of operations, systems involved, business logic
   - 1-3: Simple CRUD
   - 4-6: Multiple operations, some logic
   - 7-8: Complex logic, multiple systems
   - 9-10: High complexity, many dependencies

   **b) Risk (LOW/MEDIUM/HIGH):**
   - Consider: What happens if this fails?
   - HIGH: Security, money, data loss
   - MEDIUM: User experience, performance
   - LOW: UI tweaks, minor features

   **c) Agent Assignment:**
   - **DO NOT use keyword matching**
   - Read full task description and context
   - Decide which agent: uxui-frontend, backend, database, frontend, test-debug, integration
   - Write brief reason why this agent

   **d) Dependencies:**
   - Identify which tasks must complete first (blockedBy)
   - Identify which tasks depend on this (blocks)
   - Identify tasks that can run in parallel (no shared dependencies)

   **e) Incremental Testing Needed:**
   - YES if ANY of these:
     - Batch processing
     - External API integration
     - Data transformation
     - Multiple methods to implement
     - Complex form
     - Risk = HIGH
     - Complexity >= 7

   Store all analysis results with each task.

6. **Calculate and output analysis summary:**
   - Calculate average complexity
   - Count tasks by risk level
   - Count tasks by agent

   Output:
   ```
   📊 Analysis Results:
      Complexity: avg {average}/10
      Risk: {HIGH count} HIGH, {MEDIUM count} MEDIUM, {LOW count} LOW
      Agents: {agent1} ({count1}), {agent2} ({count2}), ...
   ```

7. **Auto-Add Best Practice Tasks:**

   For each analyzed task, apply these rules:

   **Rule 1: HIGH Risk → Add checkpoint**
   - If risk = HIGH
   - Add new task: `{task.id}.verify - Checkpoint: Verify {description} before proceeding`
   - Mark as autoAdded, type: verification

   **Rule 2: External API → Add error handling**
   - If task involves external API
   - Check if error handling task already exists
   - If not, add: `{task.id}.errors - Add error handling for external API`
   - Mark as autoAdded, type: implementation

   **Rule 3: Security-Critical → Add security review**
   - If task is security-critical (auth, payment, data access)
   - Add: `{task.id}.security - Security review: {description}`
   - Mark as autoAdded, type: verification

   **Rule 4: Database Changes → Add migration safety**
   - If task involves database schema changes
   - Add: `{task.id}.backup - Backup affected tables before {description}`
   - Mark as autoAdded, type: safety

   Output: `   Auto-added: {count} best practice tasks`

8. **Generate Incremental Milestones:**

   For each task where needsIncremental = true:
   - Determine task type (Repository/API/Batch/Form)
   - Generate appropriate milestones:
     - **Repository/Service:** method-by-method implementation
     - **External API:** mock → single → errors → scale
     - **Batch Processing:** 1 record → 5 → 20 → 100
     - **Complex Form:** architecture → e2e → all fields

   Count totals and output:
   ```
      Incremental: {count} tasks with {total milestones} milestones
   ```

9. **Sort Tasks by Priority:**

   Combine analyzed tasks + auto-added tasks

   Sort using these rules:
   1. Preserve original phase order from tasks.md
   2. Within each phase:
      - Dependencies first (tasks with no blockers)
      - HIGH risk early (fail fast principle)
      - Foundation before features
      - Lower complexity first (quick wins)

10. Output:
```
✅ Task Analysis Complete
   Total: {original count} original + {auto-added count} auto-added = {total count} tasks
```

---

**Expected Output Example:**
```
📊 Task Analyzer v2.0 (Template-Free)...
   Found: 47 tasks from tasks.md

🔍 Analyzing each task...

📊 Analysis Results:
   Complexity: avg 5.8/10
   Risk: 8 HIGH, 15 MEDIUM, 24 LOW
   Agents: backend (35), test-debug (8), uxui-frontend (4)

   Auto-added: 12 best practice tasks
   Incremental: 6 tasks with 18 milestones

✅ Task Analysis Complete
   Total: 47 original + 12 auto-added = 59 tasks
```

---

### Step 4: Create .claude Directory

**WHY:** `/cdev` expects files at `openspec/changes/{id}/.claude/` - creating the directory first ensures consistent file paths.

1. Check if directory exists: `openspec/changes/{changeId}/.claude`

**If directory does NOT exist:**
- Create the directory
- Output: `📁 Created: openspec/changes/{changeId}/.claude`

**If directory exists:**
- Skip (no output needed)

---

### Step 4.5: Inject UX Testing Phases (v2.7.0)

> **CRITICAL:** Auto-inject Phase X.5 (ux-tester) after EVERY uxui-frontend phase
> **Purpose:** User approval gate before proceeding to backend development

1. **Group tasks by phase:**
   - Use sorted tasks from Step 3
   - Group by phase number
   - Create phase objects with number, name, tasks list

2. **Check if ANY phase has uxui-frontend work:**
   - For each phase, count tasks by agent
   - Find most common agent for that phase
   - Check if most common agent = 'uxui-frontend'
   - Store result as `hasUIWork`

**If hasUIWork is TRUE:**

3. Output:
```
🧪 UX Testing Injection...
```

4. **Find all uxui-frontend phases:**
   - Filter phases where dominant agent = 'uxui-frontend'
   - Store as `uiFrontendPhases`

5. **For EACH uxui-frontend phase:**

   a) Create new UX Testing phase object:
   - Phase number: `{uiPhase.number}.5` (e.g., if UI phase is 1, UX phase is 1.5)
   - Phase name: `UX Testing (Approval Gate)`
   - Agent: `ux-tester`
   - Mark as approval gate: `isApprovalGate: true`
   - Strategy: `approval-required`

   b) Add these tasks to UX Testing phase:
   - `{phaseNum}.5.1 - Generate personas from product context` (autoAdded)
   - `{phaseNum}.5.2 - Test UI from each persona perspective` (autoAdded)
   - `{phaseNum}.5.3 - Generate UX test report with conversion prediction` (autoAdded)
   - `{phaseNum}.5.4 - ⏸️ PAUSE: Wait for user approval` (autoAdded)

   c) Insert UX Testing phase into phases array:
   - Find position of UI phase
   - Insert UX Testing phase RIGHT AFTER (position + 1)

   d) Output: `   Injected Phase {uiPhase.number}.5 (ux-tester) after Phase {uiPhase.number}`

6. Output:
```
   ✅ {count} UX approval gate(s) added
```

**If hasUIWork is FALSE:**
- Skip all steps above

---

**Workflow with UX Testing:**
```
Phase 1: uxui-frontend (build UI)
    ↓
Phase 1.5: ux-tester (APPROVAL GATE)
    → Generate personas
    → Test from each persona
    → Calculate conversion prediction
    → ⏸️ PAUSE for user approval
    ↓
[User APPROVE] → Continue to Phase 2
[User REJECT]  → Return to Phase 1 with feedback
```

---

### Step 5: Generate phases.md (Template-Free)

> **v2.0:** No templates loaded. Phases generated directly from analyzed tasks.
> **v2.7.0:** UX Testing phases already injected in Step 4.5

**Prepare data:**

1. Extract proposal title from `openspec/changes/{changeId}/proposal.md`
   - Get first heading line
   - If not found, use changeId

2. Get current timestamp (ISO format)

3. Calculate totals from sorted tasks:
   - Original tasks count (where autoAdded is false)
   - Auto-added tasks count (where autoAdded is true)
   - Incremental tasks count (where milestones exist)
   - Total milestones (sum of all milestone arrays)

**Generate overview table:**

4. For each phase:
   - Get tasks for this phase
   - Find dominant agent (most common agent in phase tasks)
   - Check if phase has incremental tasks
   - Get max risk level in phase
   - Create table row: `| {number} | {name} | {task count} | {agent} | {strategy} | {risk} |`

**Generate phase sections:**

5. For each phase, generate phase section:

   a) Header:
   ```markdown
   ## Phase {number}: {name}

   **Agent:** {dominantAgent}
   **Strategy:** {🔄 INCREMENTAL or Standard}
   **Risk:** {maxRisk}
   ```

   b) **If phase has TDD tasks (v3.1.0):**
   - Filter tasks where tdd.tdd_required = true
   - Collect unique TDD reasons
   - Add:
   ```markdown
   **TDD Required:** ✅ YES
   **TDD Reason:** {reasons, max 2}
   **TDD Workflow:** red-green-refactor

   ⚠️ **TDD WORKFLOW REQUIRED:**
   1. 🔴 RED: Write tests FIRST (they should fail)
   2. ✅ GREEN: Write minimal implementation to pass tests
   3. 🔧 REFACTOR: Improve code quality while keeping tests green
   ```

   c) **Standard tasks list:**
   - Filter tasks without milestones
   - For each task:
     ```markdown
     - [ ] {✨ if autoAdded}{task.id} {task.description}
     ```

   d) **Incremental tasks with milestones:**
   - Filter tasks with milestones
   - For each incremental task:
     ```markdown
     ### Task {id}: {description}
     **Complexity:** {complexity}/10 | **Why Agent:** {agentReason}
     ```

     For each milestone:
     ```markdown
     #### Milestone {milestone.id}/{total milestones}: {milestone.name}
     **Goal:** {milestone.goal}

     {milestone tasks as checkboxes}

     **Exit Criteria:**
     {exit criteria as checkboxes}

     **CHECKPOINT:** Report results before {next milestone or next phase}

     ---
     ```

   e) **Phase exit criteria:**
   ```markdown
   ### Phase {number} Exit Criteria
   - [ ] All tasks completed
   - [ ] All tests pass
   - [ ] No regression in existing functionality
   ```

**Generate auto-added summary:**

6. **If auto-added tasks exist:**
   ```markdown
   ## Auto-Added Tasks (Best Practices)

   | Task | Reason | Phase |
   |------|--------|-------|
   | {description} | {reason} | {phase number} |
   ... (for each auto-added task)
   ```

**Assemble final content:**

7. Combine all sections:
   ```markdown
   # Phases: {title}

   > **Generated by:** Task Analyzer v2.0 (Template-Free)
   > **Source:** tasks.md (Single Source of Truth)
   > **Strategy:** Incremental development (small → large)
   > **Generated:** {timestamp}

   ---

   ## Overview

   | Phase | Name | Tasks | Agent | Strategy | Risk |
   |-------|------|-------|-------|----------|------|
   {overview rows}

   **Total Tasks:** {original} original + {auto-added} auto-added = {total}
   **Incremental Tasks:** {incremental count} tasks with {total milestones} milestones

   ---

   {all phase sections separated by ---}

   {auto-added summary if exists}

   ---

   **End of phases.md**
   ```

8. Write to: `openspec/changes/{changeId}/.claude/phases.md`

---

### Step 6: Generate flags.json (Template-Free)

> **v2.0:** Flags generated from analyzed tasks, not templates.

1. **Group tasks by phase** (use phases from Step 4.5 which includes UX Testing phases)

2. **Detect change type from tasks:**
   - Check agents assigned to tasks
   - Rules:
     - If has uxui-frontend + backend + database → `full-stack`
     - If has uxui-frontend but NO backend → `frontend-only`
     - If has backend but NO uxui-frontend → `backend-only`
     - If has test-debug and total tasks <= 5 → `bug-fix`
     - Otherwise → `feature`

3. **Create flags.json structure:**

```json
{
  "version": "2.0.0",
  "change_id": "{changeId}",
  "change_type": "{detected type}",
  "created_at": "{current timestamp ISO}",
  "updated_at": "{current timestamp ISO}",
  "current_phase": "{first phase number or 1}",
  "meta": {
    "total_phases": {total phase count},
    "pending_phases": {total phase count},
    "completed_phases": 0,
    "total_tasks": {total sorted tasks count},
    "original_tasks": {count where autoAdded = false},
    "auto_added_tasks": {count where autoAdded = true},
    "incremental_tasks": {count where milestones exist},
    "total_milestones": {sum of all milestone counts}
  },
  "phases": {
    "{phase.number}": {
      "phase_number": {sequential index starting from 1},
      "name": "{phase.name}",
      "status": "pending",
      "agent": "{dominant agent in phase}",
      "task_count": {tasks in this phase},
      "strategy": "{incremental or standard}",
      "milestones": {milestone count or 0}
    }
    ... (for each phase)
  }
}
```

4. **For each phase, add to phases object:**
   - Get tasks for this phase
   - Find dominant agent (most common agent)
   - Check if any task has milestones
   - Count total milestones in phase
   - Create phase entry with structure above

5. Write JSON to: `openspec/changes/{changeId}/.claude/flags.json`
   - Format with proper indentation (2 spaces)

---

### Step 7: Generate context.md

**Load template and populate:**

1. **Read the context template:**
   - Load: `.claude/templates/context-template.md`

2. **Load project tech stack:**
   - Read: `.claude/contexts/domain/project/tech-stack.md`
   - This contains the core technologies used in the project

3. **Detect additional technologies:**
   - Use Step 2.7's library detection results from pre-work-context.md
   - Extract libraries mentioned in proposal.md and tasks.md

4. **Load design information (if UI work detected):**
   - Check if any task has `agent: uxui-frontend`
   - If yes and `design-system/data.yaml` exists:
     - Read design tokens from `design-system/data.yaml`
     - Check for page-plan.md at `openspec/changes/{changeId}/page-plan.md`
     - Determine page type from tasks (landing/marketing/auth/dashboard)
     - Build design system section with:
       - Design file paths (data.yaml, patterns/, README.md, page-plan.md)
       - Style direction (style name, theme name, feel)
       - Design tokens (primary color, component library, spacing scale, animations status)
       - Theme & decorations (enabled for landing/marketing, disabled for others)
       - Pattern files to load (selective based on page type)
       - Agent loading instructions (STEP 0.5 checklist)
       - Style guidelines table

5. **Group tasks by phase:**
   - Use the groupTasksByPhase helper (see Helper Functions section below)
   - Count total phases

6. **Replace template placeholders:**
   - `{CHANGE_ID}` → changeId parameter
   - `{CHANGE_TITLE}` → Extract title from proposal.md (first heading)
   - `{CHANGE_TYPE}` → Use detectChangeType helper (full-stack/frontend-only/backend-only/bug-fix/feature)
   - `{CURRENT_PHASE_NUMBER}` → "1"
   - `{TOTAL_PHASES}` → Total phase count
   - `{CREATED_DATE}` → Current timestamp in ISO format
   - `{CORE_TECH_LIST}` → Markdown list from tech-stack.md
   - `{ADDITIONAL_TECH_LIST}` → Markdown list from detected libraries
   - `{CURRENT_PHASE}` → First phase name or "Phase 1"
   - `{STATUS}` → "pending"
   - `{DESIGN_SYSTEM}` → Design info section (from step 4)

7. **Write to file:**
   - Write final content to: `openspec/changes/{changeId}/.claude/context.md`

### Step 8: Output Summary (v2.0.0 - Template-Free)

**Calculate statistics from analyzed tasks:**

1. **Group tasks and count:**
   - Use groupTasksByPhase helper to organize tasks
   - Count total phases
   - Count tasks with incremental milestones
   - Sum all milestones across tasks
   - Count auto-added tasks

2. **Check for UI work:**
   - Check if any task has `agent: uxui-frontend`
   - If yes, check if `openspec/changes/{changeId}/page-plan.md` exists

3. **Calculate agent breakdown:**
   - Count tasks per agent
   - Format as: "agent1 (count1), agent2 (count2), ..."

4. **Build output message with these sections:**

   **Header:**
   ```
   ✅ Change setup complete!

   📦 Change: {changeId}
   📊 Architecture: Task Analyzer v2.0 (Template-Free)
   🛠️ Agents: {agent summary}
   ```

   **Files created:**
   ```
   📁 Files created:
   ✓ openspec/changes/{changeId}/.claude/phases.md
   ✓ openspec/changes/{changeId}/.claude/flags.json
   ✓ openspec/changes/{changeId}/.claude/context.md
   ```

   **Task analysis:**
   ```
   📊 Task Analysis:
      Total: X tasks (Y original + Z auto-added)
      Incremental: X tasks with Y milestones
      Phases: X
      UX Approval Gates: X
   ```

   **Phase overview:**
   ```
   📋 Phase Overview:
      Phase 1: {name} ({agent}, {count} tasks)
      Phase 2: {name} ({agent}, {count} tasks)
      ...
   ```

5. **Add UI work recommendation (if applicable):**
   - If UI work detected AND page-plan.md exists:
     - Show: "✅ page-plan.md found: {path}"
     - Note: "uxui-frontend will use this for component planning"

   - If UI work detected AND page-plan.md missing:
     - Show banner: "🎨 UI Work Detected!"
     - List phases with UI work
     - Explain benefits: Content variants, component index, asset checklist, approval process
     - Show recommended steps (4 steps with /pageplan workflow)

6. **Add next steps:**
   - If UI work without page-plan:
     ```
     🚀 Ready to start development!

     Next steps:
     1. (Recommended) Run: /pageplan @prd.md
     2. Edit page-plan.md (content, assets, approval)
     3. Review workflow: openspec/changes/{changeId}/.claude/phases.md
     4. Start development: /cdev {changeId}
     5. View progress: /cview {changeId}
     ```

   - Otherwise:
     ```
     🚀 Ready to start development!

     Next steps:
     1. Review workflow: openspec/changes/{changeId}/.claude/phases.md
     2. Start development: /cdev {changeId}
     3. View progress: /cview {changeId}
     ```

7. **Display the complete output message**

---

## Helper Functions

### extractTaskIds()

To extract task IDs from tasks.md content:

1. Search for patterns matching: `- [ ] X.X` (checkbox followed by number.number)
   - Pattern: `-\s*\[\s*\]\s*(\d+\.\d+)`
   - Matches: `- [ ] 1.1`, `- [ ] 2.3`, etc.

2. Extract the number portion (e.g., "1.1", "1.2", "2.1")

3. Return all found task IDs as a list

**Example:**
- Input: `- [ ] 1.1 Setup database\n- [ ] 1.2 Create schema`
- Output: `["1.1", "1.2"]`

---

### getMostCommonAgent() (v2.0 - Template-Free)

> **v2.0:** Agent determined by AI analysis of tasks, not phase templates

To find the most common agent in a list of tasks:

1. **Handle empty list:**
   - If tasks list is empty, return `'integration'` as default

2. **Count agents:**
   - Create a count map for each agent
   - Loop through tasks and increment count for each task's agent

3. **Find the most common:**
   - Sort agents by count (descending)
   - Return the agent with highest count

**Example:**
- Input: `[{agent: 'backend'}, {agent: 'backend'}, {agent: 'test-debug'}]`
- Output: `'backend'` (appears 2 times)

---

### groupTasksByPhase()

To group tasks into phases:

1. **Create a phase map** (keyed by phase number)

2. **For each task:**
   - Get phase number from `task.phase.number` (default to 1 if not set)
   - Get phase name from `task.phase.name` (default to `"Phase {number}"` if not set)

3. **Add to map:**
   - If phase number not in map yet:
     - Create new phase entry with: number, name, empty tasks array
   - Add task to that phase's tasks array

4. **Convert map to sorted array:**
   - Convert map values to array
   - Sort by phase number (ascending)
   - Return sorted phases

**Example:**
- Input: `[{phase: {number: 2, name: "Backend"}}, {phase: {number: 1, name: "UI"}}]`
- Output: `[{number: 1, name: "UI", tasks: [...]}, {number: 2, name: "Backend", tasks: [...]}]`

---

### getMaxRisk()

To find the highest risk level across tasks:

1. Check if any task has `risk: 'HIGH'` → return `'HIGH'`
2. Otherwise, check if any task has `risk: 'MEDIUM'` → return `'MEDIUM'`
3. Otherwise, return `'LOW'`

**Example:**
- Input: `[{risk: 'LOW'}, {risk: 'MEDIUM'}, {risk: 'LOW'}]`
- Output: `'MEDIUM'`

---

### detectChangeType() (v2.0 - AI-Driven)

> **v2.0:** Detect from analyzed tasks, not keywords

To detect change type from task agents:

1. **Check which agents are present:**
   - `hasUI`: Any task with `agent: 'uxui-frontend'`
   - `hasBackend`: Any task with `agent: 'backend'`
   - `hasDatabase`: Any task with `agent: 'database'`
   - `hasTests`: Any task with `agent: 'test-debug'`

2. **Determine type based on combination:**
   - If `hasUI` AND `hasBackend` AND `hasDatabase` → `'full-stack'`
   - If `hasUI` AND NOT `hasBackend` → `'frontend-only'`
   - If `hasBackend` AND NOT `hasUI` → `'backend-only'`
   - If `hasTests` AND total tasks <= 5 → `'bug-fix'`
   - Otherwise → `'feature'`

**Example:**
- Input: `[{agent: 'uxui-frontend'}, {agent: 'backend'}, {agent: 'database'}]`
- Output: `'full-stack'`

### detectAdditionalTech() - REMOVED (v3.1.0)

> **Note:** This function was removed in v3.1.0. Use Step 2.7's direct Context7 instructions instead.
> Main Claude now directly calls Context7 MCP tools to detect and resolve libraries.

---

## Error Handling

**If tasks.md is missing or empty:**
```
❌ Error: tasks.md not found or empty
Please ensure the change has been properly initialized with OpenSpec
```

**If no tasks detected:**
```
⚠️ Warning: No checkboxes found in tasks.md
Please ensure tasks.md contains checkbox items:
  - [ ] 1.1 Task description
  - [ ] 1.2 Another task
```

---

## Example Session (v2.0 - Template-Free)

```bash
$ /csetup refactor-backend-architecture

🔍 Reading OpenSpec files...
✓ Read: proposal.md (3.1 KB)
✓ Read: tasks.md (4.2 KB)
✓ Read: design.md (1.8 KB)

📊 Task Analyzer v2.0 (Template-Free)...
   Found: 47 tasks from tasks.md

🔍 Analyzing each task...

📊 Analysis Results:
   Complexity: avg 5.8/10
   Risk: 8 HIGH, 15 MEDIUM, 24 LOW
   Agents: backend (35), test-debug (8), uxui-frontend (4)

   Auto-added: 12 best practice tasks
   Incremental: 6 tasks with 18 milestones

✅ Task Analysis Complete
   Total: 47 original + 12 auto-added = 59 tasks

📁 Created: openspec/changes/refactor-backend-architecture/.claude

Generating workflow...
✓ Generated phases.md (250 lines, 5 phases)
✓ Generated flags.json (with task analysis metadata)
✓ Generated context.md (change context with tech references)

✅ Change setup complete!

📦 Change: refactor-backend-architecture
📊 Architecture: Task Analyzer v2.0 (Template-Free)
🛠️ Agents: backend (35), test-debug (8), uxui-frontend (4)

📁 Files created:
✓ openspec/changes/refactor-backend-architecture/.claude/phases.md
✓ openspec/changes/refactor-backend-architecture/.claude/flags.json
✓ openspec/changes/refactor-backend-architecture/.claude/context.md

📊 Task Analysis:
   Total: 59 tasks (47 original + 12 auto-added)
   Incremental: 6 tasks with 18 milestones
   Phases: 5

📋 Phase Overview:
   Phase 1: Foundation (backend, 17 tasks)
   Phase 2: Repository Layer (backend, 15 tasks)
   Phase 3: Service Layer (backend, 12 tasks)
   Phase 4: Migration (backend, 8 tasks)
   Phase 5: Verification (test-debug, 7 tasks)

🚀 Ready to start development!

Next steps:
1. Review workflow: openspec/changes/refactor-backend-architecture/.claude/phases.md
2. Start development: /cdev refactor-backend-architecture
3. View progress: /cview refactor-backend-architecture
```

---

## Important Notes

1. **Re-run safe:** Running `/csetup` again will **overwrite** existing files. Use with caution.
2. **Manual adjustments:** You can manually edit phases.md after generation if needed
3. **AI-driven analysis:** Agent assignment and complexity are determined by AI context understanding, not keyword matching
4. **Incremental milestones:** Complex tasks automatically get milestone-based execution for progressive validation
5. **Auto-added best practices:** Checkpoints, error handling, and verification tasks are added automatically (no warnings)
