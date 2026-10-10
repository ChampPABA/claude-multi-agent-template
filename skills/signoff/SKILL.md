---
name: signoff
description: Build, publish, and revise the ONE stakeholder signoff page for a feature (a Claude artifact) from a confirmed drawio-swimlane spec plus a signoff.json - tabs ภาพรวม, one tab per chapter (story, flow, step table, screens, questions), Sitemap, หน้าจอ (low-fi wireframes), พื้นฐานระบบ, เปลี่ยนอะไร - and fold the comments typed into it back into the next version. Use this whenever the flow is already agreed in draw.io and the next step is the page stakeholders read and approve, or when someone says "ทำ signoff", "signoff page", "หน้า signoff", "เอา flow ไปให้ stakeholder ดู", "publish signoff version ใหม่", "อ่าน comment ใน signoff", "แก้ตาม feedback ใน signoff", "/signoff", even without saying "skill". Not for drawing or fixing the flow itself (that is drawio-swimlane).
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
   questions and their defaults come from Champ. A default Champ has not given is your
   proposal: say so in your reply.
3. **Build** (gate first; on any finding it writes nothing and exits 1):
   ```bash
   python3 <skill>/scripts/build_signoff.py spec.json signoff.json signoff.html
   ```
   Fix the input it names; never work around the gate. `[TBD]`, a `System` lane, an End with
   no outcome or an unlabelled decision branch are flow problems: back to drawio-swimlane.
4. **Look once, light and dark.** The artifact adds the doctype, so preview through a wrapper:
   ```bash
   (printf '<!doctype html><html><head><meta charset=utf8></head><body>'; cat signoff.html; printf '</body></html>') > /tmp/preview.html
   agent-browser open file:///tmp/preview.html#A1 && agent-browser screenshot light.png
   agent-browser set media dark && agent-browser screenshot dark.png
   ```
   Check a chapter, หน้าจอ and พื้นฐานระบบ. Nothing unreadable, nothing overflowing its box.
5. **Publish.** First time: Artifact publish of `signoff.html` with
   `capabilities: {db: {}, user: {scopes: ["profile"]}}` (the comment boxes need both), then
   write the returned URL into `signoff.json` `artifact`. Every later version: Artifact `read`
   that URL first (a publish to an unread URL is refused), then publish with `url` and no
   `capabilities` (omitting keeps them). Same URL forever; versions, not new links.
6. **Fold comments into the next version.** Champ types each stakeholder comment into the box
   under the question, screen, sitemap or baseline. Read them with `ArtifactData` `list` on
   collection `feedback`; doc ids are `<version>-Q3`, `<version>-page-P8`, `<version>-sitemap`,
   `<version>-baseline`; empty `text` = no comment. Read every comment of the current version
   before bumping it. For each: change signoff.json (or hand the flow change to
   drawio-swimlane), add a row to `changes`, bump `version`, rebuild, republish. Tell Champ
   per comment what you changed, or why you didn't.

## Content rules

- Content only. No how-to-answer text, platform or status hints ("บันทึกได้เมื่อเปิดผ่าน
  claude.ai", "ตกลงแล้วไม่ต้องตอบ", "ไม่มีความเห็น = ตกลง"), no explanatory ledes: Champ calls
  these AI smell. The gate refuses the phrases it knows; add a phrase to `BANNED` in
  `scripts/build_signoff.py` when Champ flags a new one.
- Business Thai, English technical terms as-is. Ids, permissions and tables are dev detail:
  only where a stakeholder decides something (baseline, state tables).
- The palette is fixed in `assets/page.html`: neutrals for structure, one green accent for
  selected/clickable/highlight, amber only for items awaiting a decision, blue only for the
  system frame. Don't add colours, stat-tile colours, coloured left bars or tinted table heads.
