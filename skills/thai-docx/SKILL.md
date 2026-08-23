---
name: thai-docx
description: >-
  Fix broken Thai rendering in Word (.docx) files generated with python-docx.
  Use this WHENEVER you create, edit, or generate a .docx that contains Thai text
  (สัญญา, คำให้การ, บันทึก, เอกสารราชการ, TH Sarabun New, ภาษาไทยใน Word), or when a
  Thai .docx looks wrong in Microsoft Word: Thai font shrinks while English stays
  big, bold/italic does not apply to Thai, tone marks/vowels (วรรณยุกต์/สระ) float
  off the consonant, or justified Thai stretches characters apart. Also use to
  QA-verify a generated Thai .docx before sending it.
  python-docx alone produces Thai that breaks in real Word even when it looks fine
  in the preview or LibreOffice, so reach for this skill any time Thai + Word + a
  generated document are involved, even if the user does not name the problem.
---

# thai-docx

Make python-docx output render Thai correctly in **Microsoft Word** (where the
reader actually opens it), not just in the preview.

## Why Thai breaks (read this once)

Word chooses a font **per character**, using several "font slots" inside a single
run. Latin text uses the **ascii/hAnsi** slot; Thai (a *complex script*) uses the
**Complex Script (cs)** slot. python-docx only ever fills the Latin slot — it sets
`w:ascii`/`w:hAnsi`/`w:sz` and leaves the cs side (`w:cs`, `w:szCs`, `w:bCs`,
`w:iCs`, `w:lang/@w:bidi`) empty. So the Thai half of every run falls back, which
is exactly the four symptoms:

| Symptom | Empty cs property | What Word does |
|---|---|---|
| Thai shrinks (~10pt) while English is 16pt | `w:szCs` | size applies to Latin only |
| Bold/italic doesn't stick to Thai | `w:bCs` / `w:iCs` | weight applies to Latin only |
| วรรณยุกต์/สระ float off the consonant | `w:rFonts/@w:cs` | falls back to a font with no Thai mark positioning |
| Lines break mid-word | `w:lang/@w:bidi` | no Thai dictionary for line breaking |

**The preview lies.** Word's own preview and LibreOffice silently guess a Thai
font when the cs slot is empty, so the document looks fine there and breaks on the
reader's real Microsoft Word. Never sign off from a screenshot. Verify the XML
with the scanner (below).

## The fix: one call before save

```python
from docx import Document
import sys; sys.path.insert(0, '<skill>/scripts')
from thai_docx import enforce_thai

doc = Document()
# ... build the document normally with python-docx ...
enforce_thai(doc)          # fills every Thai (cs) slot + Thai-Distributed body (default)
doc.save('out.docx')
```

**Default alignment = Thai Distributed (กระจายแบบไทย).** A bare `enforce_thai(doc)`
distributes body paragraphs (`w:jc='thaiDistribute'` + word-boundary breaks), which is
the ราชการ norm and renders beautifully in **real Microsoft Word**. For a plainly
left-aligned document pass `enforce_thai(doc, distribute=False)`. Headings, centred
titles and signatures keep their own alignment either way, and **table cells are never
distributed**: a narrow cell holds only a few words a line, so distribution would push
them far apart (the ห่าง look); cells stay ชิดซ้าย or whatever alignment you set on
them yourself.

> ⚠️ **thaiDistribute is a Word-only feature.** LibreOffice, Google Docs and previews
> render it as plain **left-aligned** (ชิดซ้าย) — that is the viewer's limitation, not
> a bug in the file. Judge alignment only in real Microsoft Word.

`enforce_thai(doc)` walks every run (body, tables, nested tables, text boxes,
headers, footers, footnotes), every style, the document defaults, `settings.xml`
and the theme, and sets the complex-script properties.

**Defaults = the ราชการ standard, so a bare `enforce_thai(doc)` is normally all you need:**

| | default | opt out with |
|---|---|---|
| Font | TH Sarabun New (Thai + Latin) | `thai_font=`, `latin_font=` |
| Size | **16pt on everything, headings included** (they differ by weight, not size) | `uniform=False` → each heading keeps its own size |
| Page | **A4, margins ซ้าย 3 / ขวา 2 / บน 2.5 / ล่าง 2 ซม.** (python-docx would emit US Letter) | `page=False` |
| Alignment | Thai Distributed on body paragraphs (table cells stay ชิดซ้าย) | `distribute=False` → ชิดซ้าย |
| Word breaks | ZWSP at every Thai word boundary + inside long URLs | — (see below; not optional) |

### The invariant behind `uniform=False`

With `uniform=False`, `enforce_thai` never resizes text it did not size itself:

- **Font (`w:cs`) and language (`w:lang/@w:bidi`): set everywhere.** Always safe.
- **Size (`w:szCs`): only mirror where an explicit `w:sz` already exists.** A run
  or style with no size of its own *inherits* from its paragraph style (e.g. a
  Heading). Forcing a body-size `szCs` onto it would shrink the heading. So:
  no `w:sz` → no `w:szCs`, and the heading scales from its style. The 16pt base is
  set once at the document defaults, where unspecified text picks it up.
- **Bold/italic (`w:bCs`/`w:iCs`): only mirror where `w:b`/`w:i` exists**, copying
  the on/off value so Thai weight matches Latin exactly.

### Common options

```python
# Plain left-aligned (ชิดซ้าย) instead of Thai Distributed:
enforce_thai(doc, distribute=False)

# Keep each heading's own size instead of flattening everything to 16pt:
enforce_thai(doc, uniform=False)

# Leave the document's existing page size/margins alone:
enforce_thai(doc, page=False)

# Split Latin vs Thai font inside the same run (no need to split text into runs):
enforce_thai(doc, latin_font="Times New Roman")   # English Times, Thai TH Sarabun
enforce_thai(doc, thai_font="TH SarabunPSK", size_pt=14)
# Thai often looks smaller than a Latin face at the same point size — size each:
enforce_thai(doc, latin_font="Angsana New", thai_size_pt=16, latin_size_pt=14)

# Fix justified / Thai-Distributed paragraphs that stretch glyphs apart:
enforce_thai(doc, add_zwsp=True)   # inserts U+200B at word boundaries (pythainlp)
```

### Word breaks (ZWSP) — why they are mandatory, not optional

Word only applies its Thai word-breaking dictionary if the *reader* has Thai
enabled as an editing/proofing language. On a machine where it is not, Word breaks
a Thai line **only at a real space (U+0020)** — and Thai barely has any. Lines then
end at ~60% of the column, and Thai Distributed stretches those few characters
across the full width: the "some lines are spread far too wide" symptom.

So `enforce_thai` inserts U+200B at every Thai word boundary (pythainlp), which is
a legal break opportunity in Word and is *not* expanded as whitespace during
justification. It also adds break points inside long non-Thai tokens (URLs, paths,
e-mails > 15 chars) — a 43-char URL is one unbreakable token to Word, so the line
before it would otherwise end at ~60%.

Measured line fill (TH Sarabun New 16pt, 6.5" column, before Word stretches):

| break points available | long Thai paragraph | paragraph with a URL |
|---|---|---|
| real spaces only (no pythainlp) | **63%** | **58%** |
| + Thai word boundaries | 91% | 63% |
| + long-URL/Latin breaks (current) | 91% | **99%** |

Because it edits run text, this step runs last. With `distribute=True` (the
default) a missing `pythainlp` **raises** — silently emitting a document Word
cannot break is the exact defect above. Install it, or pass `distribute=False`.
Do *not* break Thai at syllable level to pack lines tighter: it splits หน้า into
ห / น้า across two lines, which is wrong Thai typography.

## QA scanner: trust this, not the preview

After saving, always run the scanner. It reads the raw OOXML and flags any Thai
run whose cs slot is unset, plus a missing `themeFontLang`.

```bash
python <skill>/scripts/verify_thai_docx.py out.docx
```

Exit code **0 = clean, safe to send**; **1 = defects found** (prints each run, the
missing property, and the symptom it will cause). Wire it into CI or run it by
hand — it is the source of truth, because the preview hides these defects.

## Dependencies

- `python-docx` — required.
- `pythainlp` — required whenever `distribute=True` (the default) or `add_zwsp=True`;
  `enforce_thai` raises without it. `pip install pythainlp`. Only a
  `distribute=False` document works without it.

## Scope

This skill's job is to convert **already-written** Thai text into a .docx that
renders faithfully in Microsoft Word. It touches **font and rendering properties
only** — `enforce_thai` does not alter a single character of the text (the one
exception is the opt-in `add_zwsp`, which inserts invisible word-break hints). It
does not clean, rewrite, or check the source text, and it does not write or review
legal content. Every generated document is a **draft** — the wording of a
contract, คำให้การ, or บันทึกความเห็น is drafted and reviewed by a person.
