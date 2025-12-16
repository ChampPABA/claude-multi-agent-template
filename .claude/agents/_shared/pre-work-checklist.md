# Pre-Work Checklist (Shared by All Agents)

> **Version:** 2.2.0 (Library Feasibility Validation)
> **Purpose:** Single source of truth for pre-work validation

---

## Pre-Work Steps

Complete these steps before implementation to ensure alignment with project standards:

### Step 0: Library Requirements Check

**Scan for required libraries before writing code:**

1. **Read `tasks.md`** - Look for these patterns:
   - `Install X and dependencies` → Use library X
   - `Configure X with Y adapter` → Use X with adapter Y
   - Backtick packages like `better-auth` → Required dependency

2. **Read `design.md`** - Look for these patterns:
   - `### D1: Use X Library` → Decision to use X
   - `**Decision:** Use X` → Chosen library
   - Alternatives table → Shows why X was chosen over others

3. **List required libraries** in your validation report

4. **Use the libraries specified in tasks.md/design.md**
   - WHY: The team chose these libraries for specific reasons (compatibility, features, constraints)
   - Custom implementations waste effort and may miss edge cases the library handles

5. **Implement according to Design Spec (not library defaults)**
   - If design.md specifies configurations → Use those values (not library defaults)
   - If design.md specifies custom endpoints → Implement those endpoints
   - WHY: Design decisions were made for specific project requirements

**Example:**
```
tasks.md says: "Install better-auth and dependencies"
design.md says: "JWT 15min + Redis refresh token 30d"

→ Use better-auth library (from tasks.md)
→ Configure JWT with 15min expiry (from design.md)
→ Configure Redis refresh with 30d (from design.md)
→ Implement /api/auth/refresh endpoint (from design.md)

WHY not defaults? Design spec has project-specific security requirements.
```

---

### Step 0.5: Library Feasibility Validation (v2.2.0)

**Before implementing, verify the chosen library supports ALL spec requirements:**

WHY: Implementing without verifying library capabilities leads to spec drift. Better to discover gaps early than during implementation.

1. **List spec requirements from design.md:**

   Extract specific technical requirements, for example:
   - "JWT access token 15min expiry"
   - "Redis refresh token 30d"
   - "Refresh token rotation on each use"
   - "Token revocation capability"

2. **For each requirement, verify library support:**

   - Check library documentation
   - Query Context7 if available: "How to implement {requirement} with {library}?"
   - Search for feature in library's plugin/extension list
   - Check if feature is: built-in, plugin-available, or unsupported

3. **Report feasibility in your validation:**

   ```markdown
   Library Feasibility Check:
   - [ ] {requirement 1} → {library} supports: YES/PARTIAL/NO
   - [ ] {requirement 2} → {library} supports: YES/PARTIAL/NO
   - [ ] {requirement 3} → {library} supports: YES/PARTIAL/NO
   ```

4. **If ANY requirement is NOT FULLY supported:**

   **STOP - Do not proceed with implementation**

   Report to Main Claude using the Spec Deviation Protocol:

   ```markdown
   ⚠️ Library Capability Gap Detected

   **Library:** {name}
   **Requirement (from design.md):** {exact requirement text}
   **Support Status:** NO / PARTIAL

   **What library supports:** {alternative approach library offers}
   **What spec requires:** {original requirement}

   **Gap Analysis:**
   {explain what cannot be implemented as specified}

   **Options:**
   A) Change library → {suggest alternative library that supports this}
   B) Change spec → Update design.md to use what library supports
   C) Custom implementation → Build missing feature on top of library

   **My Recommendation:** {A/B/C} because {reasoning}

   Awaiting decision before proceeding.
   ```

5. **Wait for explicit decision before implementing**

   - Do NOT implement alternative approach silently
   - Do NOT assume user would prefer simpler option
   - Do NOT continue with "close enough" solution

   WHY: Silent spec drift creates technical debt and user confusion. Explicit decisions create documented trade-offs.

**Example Gap Detection:**
```markdown
Library Feasibility Check:
- [x] JWT access token 15min → better-auth jwt plugin: YES ✅
- [x] Refresh token → better-auth: PARTIAL ⚠️ (session-based, not separate token)
- [ ] Refresh token rotation → better-auth: NO ❌
- [ ] Redis session storage → better-auth: NO ❌

⚠️ STOP - Gaps found in requirements 3 and 4

Reporting to Main Claude...
```

---

### Step 0.6: Memory Context Query (v2.2.0 - claude-mem Integration)

**Before implementation, query claude-mem for related past work:**

WHY: Avoid repeating mistakes, leverage past decisions, maintain consistency.

1. **Identify current task keywords:**
   - Component name (e.g., "authentication", "payment")
   - Technology (e.g., "JWT", "Stripe")
   - Pattern type (e.g., "form validation", "API endpoint")

2. **Query past observations:**
   Ask naturally - mem-search skill auto-invokes:
   ```
   "What decisions were made about {component}?"
   "Did we solve similar problems with {technology}?"
   "Any past bugs related to {pattern}?"
   ```

3. **Apply relevant learnings:**
   - If past decision exists → Follow established pattern
   - If past bug was fixed → Apply the fix
   - If conflict with current spec → Note and report to Main Claude

4. **Report in validation:**
   ```markdown
   Memory Context: (Step 0.6)
   - [ ] Queried claude-mem for related past work
   - Relevant observations found:
     - [#ID] {summary} → Will apply: {how}
   - No relevant observations: Proceeding fresh
   ```

**Example:**
```
Task: Implement refresh token endpoint

Query: "decisions about refresh tokens"
Result: #12345 - "Chose rotating refresh tokens with Redis storage"

→ Apply: Use rotating tokens + Redis (not in-memory)
→ Report: "Following decision #12345 - rotating tokens"
```

---

### Step 1-4: Standard Checks

1. **Context Discovery** - Load project context via agent-discovery.md
2. **Pattern Loading** - Load relevant patterns for your agent type
3. **Validation Report** - Provide pre-implementation validation report
4. **Wait for Approval** - Proceed only after orchestrator validation

→ Details: `.claude/contexts/patterns/validation-framework.md` (agent-specific sections)

---

## Validation Report Template

```markdown
Pre-Implementation Validation

Library Requirements: (Step 0)
- [ ] Scanned tasks.md for "Install X" patterns
- [ ] Scanned design.md for design decisions
- Required libraries: {list from tasks.md/design.md}

Design Spec Implementation: (Step 5)
- [ ] Read design.md specifications
- [ ] Identified custom configurations (not library defaults)
- Design requirements:
  - {requirement 1 from design.md}
  - {requirement 2 from design.md}

Memory Context: (Step 0.6 - claude-mem)
- [ ] Queried claude-mem for related past work
- Relevant observations:
  - {#ID: summary → will apply how}
  - OR: No relevant observations found

Project Context:
- Project: {name}
- Stack: {tech-stack}
- Package Manager: {pm} (from tech-stack.md)

Patterns Loaded:
- [ ] error-handling.md
- [ ] logging.md
- [ ] testing.md
- [ ] code-standards.md
- [ ] {agent-specific patterns}

Best Practices:
- [ ] {framework} best practices loaded (from Context7)

Ready to Implement:
- [ ] Task understood
- [ ] Dependencies identified
- [ ] Required libraries identified
- [ ] Memory context applied (if available)
- [ ] Approach planned (using specified libraries)
```

---

## Why This Matters

Pre-work validation prevents:
- **Wrong library choices** - Using custom code when a library was already chosen by the team
- **Library defaults instead of spec** - Using default configs when design.md specifies custom values
- Misaligned implementations (wrong patterns, wrong style)
- Duplicate components (not searching existing code first)
- Wrong package manager usage (CI/CD breaks)
- Missing best practices (outdated patterns)

→ 80% of implementation issues are caught at validation stage
