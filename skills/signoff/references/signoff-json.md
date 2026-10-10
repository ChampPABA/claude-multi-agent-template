# signoff.json

Everything on the page that is not the flow. The flow (lanes, boxes, `system` / `outside`,
`page`, `changes`, `errors`, end text) stays in the drawio-swimlane spec; never copy it here.
Full worked file: `evals/files/team-recruitment/signoff.json`.

Step ids are the spec's permanent box ids, prefixed with the chapter: box `t3` on spec page
`"A3 - Partner ส่งข้อมูลและเซ็นสัญญา"` is `A3-t3`. A chapter is one non-overview spec page;
its id is the page name before ` - `.

| key | shape | shown in |
|-|-|-|
| `title`, `project`, `version`, `date`, `flow_source` | strings; `version` like `v5`, also the feedback-key prefix | header |
| `artifact` | published URL or `null`; set after the first publish | (republish target) |
| `story` | `{"overview": "...", "A1": "...", ...}`: every chapter + `overview` | ภาพรวม, chapter top |
| `questions` | `[{id, chapter, question, detail, default, pages: ["P8"]}]`; `chapter` = a chapter id or `"overview"` (no flow yet) | chapter / ภาพรวม, tab badge |
| `pages` | see below | Sitemap, หน้าจอ, ทำที่ไหน links |
| `sidebars` | `{"<role>": ["menu item", ...]}`; a page whose `role` matches gets this menu in its wireframe | หน้าจอ |
| `host` | domain shown in the wireframe URL bar | หน้าจอ |
| `emails` | `[{id, to, when, content, from_page, to_page, step}]`; `step` = the box that sends it | Sitemap (dashed edge + table) |
| `out_of_scope` | `["..."]` | Sitemap footer |
| `baseline` | `[{topic, status, now, needed, steps: ["A3-t2"]}]`; `status` ∈ `have extend add decided decide` | พื้นฐานระบบ |
| `baseline_date` | the day the code was read | พื้นฐานระบบ |
| `state_tables` | `[{title, rows: [[state, button, next_state, who, note]]}]`, one per entity (e.g. Partner, advisor account) | พื้นฐานระบบ |
| `changes`, `pending`, `removed` | `[[what, how/status/why]]` | เปลี่ยนอะไร |

## pages

```json
{"id": "P8", "url": "/team/partner", "status": "new", "status_note": "", "title": "ข้อมูล Partner",
 "role": "TL", "column": "Team Leader", "menu": "ทีมงาน",
 "purpose": "TL กรอกข้อมูลบริษัท upload เอกสาร อ่านสัญญา และเซ็นในหน้าเดียว",
 "fields": [["ข้อมูลบริษัท", "ชื่อ, เลขนิติบุคคล 13 หลัก, ที่อยู่"]],
 "actions": ["บันทึก", "เซ็นและส่งตรวจ"],
 "states": ["ไฟล์ไม่ครบหรือยังไม่เซ็น: ปุ่มส่งตรวจกดไม่ได้"],
 "wireframe": "<h4>ข้อมูล Partner</h4>...<div class=\"wrow\">[[บันทึกไว้ก่อน]][[เซ็นและส่งตรวจ->P7]]</div>"}
```

- `status`: `new | changed | old`. An `old` page (unchanged, e.g. `/set-password`) needs only
  `id url status title role column`: it appears in the sitemap, not in หน้าจอ.
- `column`: sitemap column (group by role and area); columns appear in first-use order.
- `wireframe`: low-fi HTML, black on white. `[[label->P7]]` is a button that opens P7's
  wireframe and draws the sitemap arrow; `[[label]]` is a dead button. The sitemap's arrows
  come only from these, so every real navigation needs one. Classes available: `wf-form`
  (label/value grid), `winput`, `wrow`, `wt` (table), `wtab` / `wtab on`, `wbanner`, `wpdf`,
  `wsig`, `wnote`. Use realistic Thai sample data, never lorem.
- Button labels use the same verbs as the flow boxes and the state tables (ส่งตรวจ / ผ่าน /
  ส่งกลับแก้ / เพิ่ม / ย้าย / ลบ ...): a stakeholder must recognise the same action everywhere.
