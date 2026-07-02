---
name: fable-advisor
description: >-
  Cost-aware router for tackling a task with the cheapest tool AND model that's
  actually good enough — deciding between just doing it, a quick `advisor`
  second-opinion, spawning Fable 5 for clean-room planning, or offloading research
  to NotebookLM, and which tier (haiku/sonnet/opus/fable) should run the work you
  keep. Use whenever the user says "/fable-advisor", "ถาม fable", "ใช้ fable วางแผน",
  "ให้ fable ช่วยคิด", "should this go to fable", "plan this efficiently", "แจก model",
  or wants a hard/ambiguous task handled without burning Fable quota. ALSO use before
  starting any genuinely hard, multi-approach, or high-stakes task where
  planning-before-coding would pay off, when a cheaper model has stalled and you're
  weighing escalation, or when a task is really "go read/synthesize a pile of
  sources" (that goes to NotebookLM, not burned tokens here). The router runs FIRST
  and is cheap even when the answer is "just do it" — under-routing (flailing without
  help, leaking easy work to Fable, or researching by hand) is the real cost.
---

# Fable Advisor

A router for spending the expensive resources — Fable 5 quota and your own tokens —
only where they buy something. It decides on **two axes**:

- **Axis 1 — where does this task go?** just do it / `advisor` / NotebookLM / Fable.
- **Axis 2 — which model runs the work you keep?** haiku → sonnet → opus → fable.

On both axes the rule is the same: pick the **cheapest option that's actually good
enough, and stop there.** Fable is superb but expensive (on a Max plan the Fable
pool is ~half, and it's 10× Haiku / 2× Opus per token), and it can't be wired up as
the built-in `advisor` — so it's the last resort on both axes, gated hard.

## Triggers

- Explicit: "/fable-advisor", "ถาม fable", "ใช้ fable วางแผน", "ให้ fable ช่วยคิด",
  "should this go to fable", "แจก model / which model for this".
- Implicit: about to start a genuinely hard, multi-approach, or high-stakes task;
  a cheaper model has stalled and you're weighing escalation; the task is really
  broad research over many sources.
- Cheap to over-trigger (the router short-circuits to "just do it"); costly to
  under-trigger. When unsure, run it.

---

## Axis 1 — Route the task (do this first, every time)

| Need | Route to | Cost | Prep |
|------|----------|------|------|
| Path is clear / mechanical | **Just do it** | lowest | none |
| "Am I on the right track? poke holes in this" | **`advisor` tool** | low, **no Fable quota** | none |
| Read / synthesize external sources | **NotebookLM** | offloaded to Google | light |
| Design a hard thing / genuinely stuck | **Spawn Fable** `Agent(Plan, model: fable)` | highest (Fable quota) | curated brief |

Walk the ladder top-down, stop at the first rung that holds:

**1. Just do it** — path is clear, scope small and reversible, mechanical (rename,
format, obvious bug, boilerplate, wiring), or you're applying a pattern the codebase
already has. No judgment is missing, so no tool adds value. (Run it on the right
Axis-2 model.)

**2. `advisor` tool** — you have work *in your current context* and the need is
"check my thinking": review my approach, catch a mistake, sanity-check a decision
I've already framed. `advisor` sees your full conversation automatically, is backed
by a strong reviewer, needs **zero brief**, and does **not** touch Fable quota.
Reach for it liberally — the cheap second opinion. (Built-in tool, no arguments.)
If this environment has no `advisor` tool (it's harness-specific, not stock Claude
Code), get the same value by spawning a fresh review subagent on Opus/Sonnet,
primed to poke holes, handed the diff and the decision you're unsure about.

**3. NotebookLM** — the task is really *research*: read/synthesize a body of
external material. Reading it all into context burns tokens for grunt work; offload
it to Google instead. See the NotebookLM path below.

**4. Spawn Fable** — genuine architectural ambiguity (several viable approaches,
high cost of wrong), a hard design/algorithm problem with no obvious pattern, a
cross-cutting decision shaping many files, a high-stakes irreversible choice, or a
blocker that has honestly resisted ≥2 real attempts. The only rung that spends Fable
quota — clear the bar below.

**advisor vs Fable — the distinction the router turns on:**
- `advisor` answers *"is what I'm doing right?"* — reviews **your** in-flight
  context: fast, free of Fable cost, but shares your framing and can inherit your
  blind spots.
- Fable answers *"design/plan this from scratch"* / *"unblock this"* — works
  **clean-room** from a brief you curate, re-deriving without your baggage. Reserve
  it for generative planning and hard unblocks, ideally *after* cheaper rungs failed.

**The Fable bar (the "กันหลุด" gate):** a Fable call is worth it only when the value
of a better decision exceeds its cost. Thrashing ten turns to "save" one call is
false economy; one call to rubber-stamp what you already know is pure waste. Fable
also carries real friction that justifies gating — ~10× Haiku pricing, a 30-day
data-retention requirement, it can return `stop_reason: refusal`, and its turns run
for minutes. State the verdict in one line before acting (e.g. "Route: Fable — two
viable state models, wrong pick means a painful migration").

---

## Axis 2 — Which model runs the work you keep

For anything you *don't* offload (rungs 1 and the implementation of a Fable plan),
pick the cheapest tier that clears the task. Prices are $ per Mtok (input/output):

| Model | id | $ in/out | vs Haiku | Use for |
|-------|-----|----------|----------|---------|
| **Haiku 4.5** | `claude-haiku-4-5` | 1 / 5 | 1× | mechanical, high-volume, low-judgment: bulk edits, running/scanning, and **wait/poll subagents** (e.g. the NotebookLM research-wait below) |
| **Sonnet 5** | `claude-sonnet-5` | 3 / 15 | 3× | default implementer: routine coding, tests, standard subagent work |
| **Opus 4.8** | `claude-opus-4-8` | 5 / 25 | 5× | orchestrator (the main loop) + hard/ambiguous work, careful multi-file changes |
| **Fable 5** | `claude-fable-5` | 10 / 50 | 10× (2× Opus) | apex planning / hardest unblock only — via Axis 1, gated |

**Why spawn cheaper subagents instead of switching the main loop's model:** prompt
caching is **model-scoped** — changing the model mid-conversation invalidates the
entire cache (and any byte change to the prefix does too). So the cost-correct
pattern is to keep the orchestrator on one model and hand sub-tasks to
cheaper-model **subagents**, not to flip the main loop down and back. Cache reads
are ~0.1× input, so a stable orchestrator prefix is a big saving on its own.

Default reflex: **Sonnet** for kept implementation, **Haiku** for pure mechanical /
waiting work, **Opus** for the orchestrator and the genuinely tricky steps. Don't
reach past the tier a step needs.

---

## Fable path

### 1. Prepare a clean brief

Fable spawns with **no memory of this conversation** — the brief is its entire
world. That's deliberate: instead of `advisor` auto-forwarding the whole transcript
(input tokens balloon), you hand-curate a lean, self-contained brief. That curation
is most of the saving, so invest in it. Front-load context so Fable spends its
tokens *thinking*, not exploring; paste real snippets rather than "see file X".

```
## Objective
<1–2 sentences: what "done" looks like.>

## Context (curated — should be enough; read files only if it isn't)
<Minimal facts, real code snippets, paths, stack, conventions that matter.>

## Constraints & non-goals
<Stack, versions, patterns to follow, what NOT to do, hard boundaries.>

## Already tried  (only if escalating from a stuck state)
<What was attempted, what happened, exact error/behavior.>

## The decision I need from you
<The specific question — what you're choosing between or stuck on.>

## Return format
Give me a plan, not code:
- Chosen approach + one-line why; rejected alternatives + why (brief)
- Ordered steps — each with: what to do, which files, how to verify it
- Risks / gotchas
- Per-step difficulty tag: [routine] or [tricky]
```

Batch related questions into one brief — one dense call beats several thin ones,
each paying fixed spawn overhead.

### 2. Spawn Fable clean

`Agent` tool, **fresh and read-only**:
- `subagent_type: "Plan"` — read-only (Read/Grep/Bash, no Edit/Write, can't spawn
  agents). This enforces "architect, not bricklayer" mechanically, not by hope:
  Fable physically can't start typing code. It can still read a file to verify a
  thin brief.
- `model: "fable"`
- `prompt`: the brief.

Do **not** use `subagent_type: "fork"` — a fork ignores the model override and
inherits your whole context, defeating both the clean-context and cost goals.

Read the plan critically — you own the outcome. A quick `SendMessage` follow-up to
the same agent is cheaper than discovering a gap mid-implementation.

### 3. Implement the plan (cheap models — Axis 2)

Work the steps by their difficulty tags:
- `[routine]` → Sonnet subagent (`model: "sonnet"`), or do it yourself. Pure
  mechanical sub-steps can drop to Haiku.
- `[tricky]` → Opus (you, or `model: "opus"`) — careful, still not Fable.

Verify each step with the real check Fable specified (test/build/typecheck, not a
proxy). Independent steps can run as parallel subagents. Fable does not implement —
spending Fable tokens to type code Sonnet could produce is the exact leak this
skill prevents.

### 4. Escalate narrowly when stuck

"Stuck" = a step honestly failed ≥2 real attempts, or you're guessing. First
re-run Axis 1 at this smaller scope — a typo or wrong import doesn't need Fable. If
it's a genuine blocker, don't re-plan the whole task; package just the blocker into
a fresh, tight brief to a new `Agent(Plan, model: fable)` spawn:

```
## Objective          <the one blocked step>
## Already tried      <attempts + exact error/behavior/state>
## The decision I need <the narrow question>
## Return format      <targeted fix + why; not a full re-plan>
```

Apply the fix, resume step 3. Keep the original plan; only the blocked step changed.

---

## advisor path

Just call the `advisor` tool (no arguments — it forwards your full context). No
brief, no spawn, no Fable quota. Use it freely to check an approach before
committing, after a substantial change, or when you're unsure and it's your own
in-context work being judged.

**Portable fallback:** the `advisor` tool is harness-specific and may be absent on
another machine. When it is, spawn a fresh review subagent (`model: "opus"` or
`"sonnet"`) with a short "poke holes in this approach; what breaks?" prompt plus the
diff / the decision in question. Same job (a second opinion, no Fable quota); it
just costs a brief instead of being free, so still prefer the real tool when present.

## NotebookLM path

Route here when the job is *research* — reading/synthesizing a body of sources —
because doing it by hand pulls every source into your context (expensive), and if
you then hand it to Fable, into the expensive pool too. NotebookLM offloads the
find-and-read to Google; you pay only for the distilled answer you pull back.

Drive it through the `notebooklm` skill (it owns the full CLI). The cost-saving
pattern:

1. `notebooklm status` — confirm authenticated (else `notebooklm login`).
2. `notebooklm create "Research: <topic>" --json` → capture the notebook id and
   pass it explicitly as `-n <id>` on later calls (don't rely on shared context).
3. Get sources in — match the mode to the time budget:
   - Quick/targeted → `--mode fast` (5-10 sources, ~30s-2min), or just use a cheap
     Claude research subagent (Haiku/Sonnet + WebSearch) if you need it *now*.
   - Broad/can-wait → `notebooklm source add-research "<query>" --mode deep
     --no-wait` (deep ≈ 20+ sources, ~15-30 min). **The big win** — Google reads
     the web so you and Fable don't.
   - Specific URLs / YouTube / PDFs you already have → `notebooklm source add "<url>"`.
4. Deep research is long, so **don't block or poll in your main context** — spawn a
   **Haiku** background subagent to wait: `notebooklm research wait -n <id>
   --import-all --timeout 1800` (or `source wait`). Your main loop keeps going.
5. Pull back only the synthesis, never raw text:
   - `notebooklm ask "<specific question>" -n <id> --json` → cited answer, or
   - `notebooklm generate report --format briefing-doc -n <id>` → structured doc.

Bring back the answer/report, not the sources. Chat, research, and report are the
reliable operations; audio/video/quiz can hit Google rate limits, so avoid them
when the goal is a research offload.

---

## Quick reference

```
Task arrives
  └─ Axis 1: ROUTE (stop at first that fits)
       1. clear / mechanical ........ just do it. Done.
       2. "check my thinking" ....... advisor tool (no Fable quota). Done.
       3. read/synthesize sources ... NotebookLM (deep=background via Haiku). Done.
       4. hard design / stuck ....... Fable path ▼
             brief → Agent(Plan, model: fable) → plan
                   → implement per tags (Axis 2: Haiku/Sonnet/Opus)
                   → stuck ≥2 tries? re-route → narrow Fable fix → resume
  └─ Axis 2: run kept work on the cheapest tier that clears it
       Haiku (mechanical/wait) · Sonnet (implement) · Opus (orchestrate/hard) · Fable (gated)
```

Failure modes this guards against, all equally wasteful:
- **Leaking** easy work, or research, to Fable.
- **Flailing** on hard work without it.
- Using **Fable for review** when `advisor` (free of Fable quota) was the fit.
- Running kept work on a **richer model than the step needs** (Axis 2).
