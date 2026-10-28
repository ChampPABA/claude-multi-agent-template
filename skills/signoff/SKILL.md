---
name: signoff
description: Build, publish, and revise the ONE stakeholder signoff page for a feature (a Claude artifact) from a confirmed drawio-swimlane spec plus a signoff.json - tabs ภาพรวม, one tab per chapter (story, flow, step table, pages used), Sitemap, พื้นฐานระบบ - and publish each revision Champ asks for as a new version at the same link. Use this whenever the flow is already agreed in draw.io and the next step is the page stakeholders read and approve, or when someone says "ทำ signoff", "signoff page", "หน้า signoff", "เอา flow ไปให้ stakeholder ดู", "publish signoff version ใหม่", "แก้ signoff", "/signoff", even without saying "skill". Not for drawing or fixing the flow itself (that is drawio-swimlane).
allowed-tools: Read, Write, Edit, Bash
---

# signoff

Stage 2 of 2. drawio-swimlane agrees the flow with Champ; this skill turns the agreed flow
plus everything around it into one signoff page that Champ shows to stakeholders. After
signoff, the page is the dev blueprint. Whether this skill also opens issues is not decided:
ask Champ, don't do it.

## Inputs

- **Spec**: the drawio-swimlane spec JSON, read back from Champ's `.drawio`. Each
  non-overview page is one chapter; its id is the page name before ` - ` (`A3`).
- **signoff.json**: everything that is not the flow, keyed by chapter id and step id
  (`A3-t3`). Lives next to the output, e.g. `docs/handbook/<feature>/signoff.json`.
  Schema: `references/signoff-json.md`.

## Steps

1. **Make sure the spec is the agreed flow.** If the `.drawio` is newer than the spec, run
   drawio-swimlane's `check_layout.py flow.drawio` then `gen_swimlane.py --read flow.drawio spec.json`.
   The flow is read-only here: never edit flow text, lanes or edges in the spec to make a
   build pass. Anything about the flow goes back to drawio-swimlane.
2. **Write or update signoff.json.** First time: read `references/signoff-json.md` and the
   worked file `evals/files/team-recruitment/signoff.json`. Baseline comes from reading the
   target repo's code (auth, roles and permissions, audit log, email, upload); stories,
   page details come from Champ. Anything Champ has not given is your proposal: say so in
   your reply. Open questions are discussed with Champ in chat, not put on the page.
3. **Build** (gate first; on any finding it writes nothing and exits 1):
   ```bash
   python3 <skill>/scripts/build_signoff.py spec.json signoff.json signoff.html
   ```
   Fix the input it names; never work around the gate. `[TBD]`, a `System` lane, an End with
   no outcome or an unlabelled decision branch are flow problems: back to drawio-swimlane.
   The gate also refuses a reference in text (`A2-d`, `A3.1`, `P8`, `E3`) to something
   that does not exist. It cannot check meaning, so then read each chapter's story, page
   states and emails against its flow and list every mismatch to Champ: a story promising a
   path the flow lacks, a field a step needs that its page lacks, an email landing on a page
   the recipient does not act on. Don't fix these silently; they are Champ's call.
   Flow box text explains the process and need not match on-screen labels word for word:
   a wording gap between a flow box and a button is not a mismatch, and never edit flow text
   to match a label.
4. **Look once, light and dark.** The artifact adds the doctype, so preview through a wrapper:
   ```bash
   P=$(mktemp --suffix=.html)
   (printf '<!doctype html><html><head><meta charset=utf8></head><body>'; cat signoff.html; printf '</body></html>') > $P
   agent-browser --session signoff-$$ open file://$P#A1 && agent-browser --session signoff-$$ screenshot light.png
   agent-browser --session signoff-$$ set media dark && agent-browser --session signoff-$$ screenshot dark.png
   ```
   Run it as one shell command: a fixed preview path or the shared browser session shows
   another run's page.
   Check a chapter, Sitemap and พื้นฐานระบบ. Nothing unreadable, nothing overflowing its box.
5. **Publish.** First time: Artifact publish of `signoff.html`, then write the returned URL
   into `signoff.json` `artifact`. Every later version: Artifact `read` that URL first (a
   publish to an unread URL is refused), bump `version`, rebuild, then publish with `url`.
   Same URL forever; versions, not new links. A revision that changes the flow goes to
   drawio-swimlane first.

## Content rules

- Content only. No how-to-answer text, platform or status hints ("บันทึกได้เมื่อเปิดผ่าน
  claude.ai", "ตกลงแล้วไม่ต้องตอบ", "ไม่มีความเห็น = ตกลง"), no explanatory ledes: Champ calls
  these AI smell. The gate refuses the phrases it knows; add a phrase to `BANNED` in
  `scripts/build_signoff.py` when Champ flags a new one.
- Page prose (stories, field descriptions, states, emails) is business Thai, English
  technical terms as-is. UI wording inside it (menu, page title, button, tab, status, empty
  state, toast) is quoted as the app shows it, not translated:
  - Screen already in code: quote the running code exactly, and check the app shell and
    sibling pages too, not only this feature's. Code Champ approved beats the signoff, so on
    a difference revise the signoff. A rename Champ wants is a change: list it in your
    reply, never slip it in.
  - No code yet: choose wording that fits the whole app's existing convention (language per
    zone, how menus and statuses are named), not wording invented per page.
- Two readers: stakeholders approve the page,
  front-end devs build from it. Screens are designed later in hi-fi and the back end later
  from the code, so no wireframes, data model or UML; ids, permissions and tables only where
  a stakeholder decides something (baseline, state tables).
- The palette is fixed in `assets/page.html`: neutrals for structure, one green accent for
  selected/clickable/highlight, amber only for items awaiting a decision, blue only for the
  system frame. Don't add colours, stat-tile colours, coloured left bars or tinted table heads.
