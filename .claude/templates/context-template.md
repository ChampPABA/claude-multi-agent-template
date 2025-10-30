# Agent Context: {CHANGE_ID} {CHANGE_TITLE}

## Change Info
- **ID:** {CHANGE_ID}
- **Type:** {CHANGE_TYPE}
- **Status:** Phase {CURRENT_PHASE_NUMBER}/{TOTAL_PHASES}
- **Created:** {CREATED_DATE}

## References
**IMPORTANT:** Agents MUST read these before starting work!

- **Proposal:** [../proposal.md](../proposal.md) - Business requirements and scope
- **Tasks:** [../tasks.md](../tasks.md) - Implementation checklist
- **Design:** [../design.md](../design.md) - Technical decisions (if exists)
- **Specs:** ../specs/ - Delta requirements

## Tech Stack

### Core (from project-level)
Reference: `@/.claude/contexts/domain/project/best-practices/`

{CORE_TECH_LIST}

### Additional (Change-specific)
**New tech for this Change only:**

{ADDITIONAL_TECH_LIST}

## Change-Specific Patterns

{CHANGE_SPECIFIC_PATTERNS}

## Agent Instructions per Phase

{AGENT_INSTRUCTIONS}

## Phase Tracking
**Current phase:** {CURRENT_PHASE}

See `flags.json` for detailed tracking.

---

**Last updated:** {UPDATED_DATE}
**Phase:** {CURRENT_PHASE} ({STATUS})
