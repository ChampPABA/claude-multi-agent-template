# signoff.json

Everything on the page that is not the flow. The flow (lanes, boxes, `system` / `outside`,
`page`, `changes`, `errors`, end text) stays in the drawio-swimlane spec; never copy it here.
Full worked file: `evals/files/team-recruitment/signoff.json`.

Step ids are the spec's permanent box ids, prefixed with the chapter: box `t3` on spec page
`"A3 - Partner ส่งข้อมูลและเซ็นสัญญา"` is `A3-t3`. A chapter is one non-overview spec page;
its id is the page name before ` - `.

| key | shape | shown in |
|-|-|-|
| `title`, `project`, `version`, `date`, `flow_source` | strings; `version` like `v5` | header |
| `artifact` | published URL or `null`; set after the first publish | (republish target) |
| `story` | `{"overview": "...", "A1": "...", ...}`: every chapter + `overview` | ภาพรวม, chapter top |
| `pages` | see below | Sitemap, chapter ทำที่ไหน |
| `emails` | `[{id, to, when, content, from_page, to_page, step}]`; `step` = the box that sends it; a page may name its tab after the id (`"P3 (แท็บ Company)"`) | Sitemap (dashed edge + table) |
| `out_of_scope` | `["..."]` | Sitemap footer |
| `baseline` | `[{topic, status, now, needed, steps: ["A3-t2"]}]`; `status` ∈ `have extend add decided decide` | พื้นฐานระบบ |
| `baseline_date` | the day the code was read | พื้นฐานระบบ |
| `state_tables` | `[{title, rows: [[state, button, next_state, who, note]]}]`, one per entity (e.g. Partner, advisor account) | พื้นฐานระบบ |

## pages

```json
{"id": "P8", "url": "/team/partner", "status": "new", "status_note": "", "title": "ข้อมูล Partner",
 "role": "TL", "column": "Team Leader",
 "purpose": "TL กรอกข้อมูลบริษัท upload เอกสาร อ่านสัญญา และเซ็นในหน้าเดียว",
 "fields": [["ข้อมูลบริษัท", "ชื่อ, เลขนิติบุคคล 13 หลัก, ที่อยู่"]],
 "actions": ["บันทึก", "เซ็นและส่งตรวจ"],
 "states": ["ไฟล์ไม่ครบหรือยังไม่เซ็น: ปุ่มส่งตรวจกดไม่ได้"],
 "next": ["P7"]}
```

- `status`: `new | changed | old`. An `old` page (unchanged, e.g. `/set-password`) needs only
  `id url status title role column`: it appears in the sitemap, not in the page table.
- `column`: sitemap column (group by role and area); columns appear in first-use order.
- `next`: the pages a user can go to from this one. The sitemap's solid arrows come only
  from here, so every real navigation needs an entry; email hops go in `emails`, not here.
- `fields`: `[[field or group, description]]`. The description holds what a dev cannot guess
  from the label: format, must be unique, when the field appears, what the user sees when it
  is wrong. Don't restate the label.
- `states`: only what a front-end dev would build wrong without being told: business rules,
  who sees what, when a button is disabled, how the page differs per status, empty-state
  wording and its action. Generic loading, error toasts and offline handling are designed in
  the hi-fi build, not here.
- Action and status labels come from the UI wording rule in SKILL.md (code first, else the
  app's convention), and one action reads the same in pages, state tables and emails: a
  stakeholder must recognise the same action everywhere.
