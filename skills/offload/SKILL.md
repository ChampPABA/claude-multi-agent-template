---
name: offload
description: >-
  Routes work that needs outside information to the right place instead of pulling
  it all into the main conversation. Use this BEFORE gathering anything, whenever a
  task means reading or synthesizing external sources — "research X", "what's the
  current best practice for Y", "read these papers / RFCs / talks and tell me",
  "compare the approaches out there", "ค้นเรื่อง ... ให้หน่อย", "หาข้อมูลเรื่อง ...",
  "สรุป best practice เรื่อง ...", "ไปอ่าน ... มา" — whenever files are handed over to be
  understood rather than edited, and ALSO mid-task, the moment you notice you don't
  actually have enough information to decide and are about to answer from memory
  anyway. Picks between reading a slice locally, NotebookLM deep or fast research, a
  WebSearch subagent, or just answering, and sizes any attached files in tokens
  first. Cheap to over-trigger, because one branch is "just answer" — the expensive
  mistakes are answering from stale memory and filling the context window with
  twenty sources.
---

# Offload

Decide where information-gathering happens, then hand off. This skill does not do
the research and does not teach the NotebookLM CLI — the `notebooklm` skill owns
every command. Invoke it once the route is chosen.

Two things justify the detour, and neither is money:

- **Context hygiene.** Twenty sources read inline sit in the window for the rest of
  the session and degrade every later turn.
- **Answer quality.** Content buried in the middle of a huge context loses accuracy
  (context rot / lost-in-the-middle). Fitting is not the same as working.

If the request is "check my thinking" rather than "find something out", that is the
built-in `advisor` tool's job, not this one.

## When to run

Two entry points. The second matters more.

1. **Someone asks for research, or hands over files to be understood.**
2. **You realize mid-task that you don't know.** You are weighing options, or about
   to state a version number, a current best practice, a benchmark result — and the
   honest answer is that your training data may be stale. Stop and route instead of
   answering confidently. This produces a wrong answer that looks right, which is
   why it costs more than the obvious case.

## Step 1 — look before you route

Never decide from a file's size on disk or its page count. Spend a few seconds
finding out what is actually in it, because that usually collapses the decision:

```bash
pdfinfo file.pdf | grep Pages
pdftotext -layout file.pdf - | wc -c        # extracted characters
pdftotext -layout file.pdf - | grep -n "<the section you need>"
```

`-layout` matters for Thai: default mode silently drops vowels and tone marks
(`จาหน่าย` for `จำหน่าย`) and breaks space-insensitive greps. If Thai looks corrupted,
that is usually an extraction-mode artifact, not a property of the document — retry
with `-layout` and check per-page text density before concluding a file is unreadable.

A nastier variant has no visible symptom: some exporters (InDesign especially) emit
**doubled combining marks** — `โครงสร้้าง` with two ไม้โท — so an exact grep returns
nothing at all and looks like "the section isn't there." When a grep for a heading you
can see in the document comes back empty, search a shorter fragment or a distinctive
substring before believing it.

**Cite something the reader can find again.** Line numbers in your scratch extraction
are not stable references — `-layout` pads whitespace and shifts every line, so the
number you saw is not the number they will see. Cite the document's own page number,
or quote a distinctive string they can search for. A confident line number that leads
nowhere is worse than no citation, because it looks checkable and isn't.

**Prove the slice was complete.** The real risk of reading part of a document is
silently cutting a row. Cross-foot whatever you extracted: percentages should sum to
100, components should reconcile to the stated total. One extraction truncated a
revenue table mid-row and its column summed to 96.18% — back-solving the gap surfaced
a missing line worth 111 million. That check costs one line of arithmetic and is the
only cheap evidence you read the whole thing.

**Extracted text costs no image tokens at all.** A PDF sent as a document block pays
roughly 1,500 tokens per page just to rasterize the page, on top of its text. Pulling
the text out locally skips that entirely, which is why a 375-page report can often be
answered for ~10k tokens. Reserve sending the actual PDF for when the visual layout,
figures, or scanned pages are the point.

Very often the answer lives in a small, findable slice — a table of contents, one
table, one section. Reading 4 pages out of 375 beats every other route on cost,
latency, and precision simultaneously. Look for that first.

## The routes

Once you know what is in the material, choose by **where the answer lives** and
**how long it can wait**.

| Situation | Route |
|---|---|
| Answer is inside files you already have | **Read a slice** — grep to it, read those pages only |
| Answer needs many outside sources synthesized, 15–30 min is fine | NotebookLM **deep** research, non-blocking, with a waiter subagent |
| Answer needs a few outside sources, 2–3 min is fine | NotebookLM **fast** research |
| Needed right now, a handful of sources is enough | **WebSearch** subagent (`haiku` or `sonnet`) |
| Whole corpus must be digested, or files are too big to slice | NotebookLM with the files as sources |
| Already known, or one lookup | **Just answer.** Offloading here is pure overhead |

These combine. "Read the local slice, and also search the web" is a normal answer.

Two rules the `notebooklm` skill does not state, so they belong here:

- **The waiter subagent runs on `haiku`.** It does nothing but poll for completion.
- **Bring back the synthesis, never the sources.** Use `notebooklm ask` or
  `generate report`. Importing raw sources into the main context recreates exactly
  the problem this skill exists to prevent.

## Sizing files

The deciding number is tokens, not pages — a graphics-heavy page and a text-only
page differ by more than 2× in the same document.

**Estimate with two terms**, because page-image cost is roughly fixed per page while
text cost varies with actual density:

```
tokens ≈ (extracted characters × 0.8)  +  (pages × 1,500)      # Thai
       ≈ (extracted characters × 0.4)  +  (pages × 1,500)      # English
```

Thai costs about 2.1× English per character — measured on identical character counts,
because Claude's tokenizer carries almost no Thai vocabulary and falls back to bytes.
Drop the second term entirely when you are reading extracted text rather than sending
the PDF; that term is the rasterization you just avoided.

A flat per-page rate is not good enough: on a text-dominant document it overestimated
by 1.57×, enough to push a file into the wrong band.

| Estimate | Do this |
|---|---|
| **< 50k tokens** | Just read it. Measuring and asking both cost more than they save |
| **50k – 300k** | Measure exactly (below), then decide. This is the only band where precision changes the answer |
| **> 300k** | Slice it or offload it. Measuring changes nothing |

Sending a PDF as a document block caps at **32 MB** and **600 pages** (100 when the
context window is under 1M). Local text extraction has no such cap — a document past
those limits is not unreadable, it just cannot be sent whole.

**Measuring exactly** is free (`count_tokens` is not billed and is rate-limited
separately), so do it without hesitation inside the middle band:

```bash
ant messages count-tokens --transform input_tokens -r <<'YAML'
model: claude-opus-5
messages:
  - role: user
    content:
      - type: document
        source:
          type: base64
          media_type: application/pdf
          data: "@/absolute/path/file.pdf"
YAML
```

For text files, swap the document block for `content: "@/absolute/path/file.md"`.

If `ant` fails — its OAuth token expires every 8 hours, so this is a normal Tuesday —
use the estimate, label the number approximate, and move on. Never block on it.

## Asking the user

Ask when **two or more routes are genuinely live** and differ in depth, latency, or
precision in a way only the user can adjudicate — deep versus fast versus search-now
is exactly that choice, files or no files.

Do not ask when the evidence has already collapsed the decision: a 3-page PDF, a
question you can answer outright, or a probe that just showed the answer sits in one
findable table. A chooser offered after the choice is gone is theater, and it trains
the user to click through without reading.

When you do ask, use **one** `AskUserQuestion` — measure and probe silently first
rather than asking permission to look. Put the recommended option first, and show the
**token total**, that total as a **percentage of the context window**, and **whether it
was measured or estimated**, because people weigh a number differently once they know
where it came from.

```
AT206_Project_Example.pdf, 93 pages = 171,996 tokens  ✓ measured  (17% of context window)

▸ Read the relevant slice (recommended)   สารบัญ + บทที่ 3 · ~12k of context · exact quotes
  NotebookLM fast + this file             also search 5–10 web sources · ~3 min
  NotebookLM deep + this file             also search 20+ web sources · ~20 min, background
  Read the whole file directly            full fidelity · costs 172k of context
```

Keep a read-directly option on the list whenever editing or exact quoting might be
needed — it is the only route that supports them.
