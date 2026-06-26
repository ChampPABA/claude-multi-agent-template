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
enforce_thai(doc)          # fills every Thai (cs) slot across the whole document
doc.save('out.docx')
```

`enforce_thai(doc)` walks every run (body, tables, nested tables, text boxes,
headers, footers, footnotes), every style, the document defaults, `settings.xml`
and the theme, and sets the complex-script properties. Defaults give the user's
standard: **TH Sarabun New, 16pt**.

### The one invariant that keeps headings intact

`enforce_thai` follows a deliberate rule so it never damages a document it is
trying to fix:

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
# Thai government-document norm — EVERYTHING one font, one size, headings included
# (headings differ only by weight, not size). This is the common case for ราชการ docs:
enforce_thai(doc, uniform_size_pt=16)             # all TH Sarabun New 16pt, headings too

# Thai Distributed (กระจายแบบไทย) on body content — the standard for เนื้อความ.
# Distributes only plain body paragraphs (headings, centred titles and signatures
# keep their alignment), auto-inserts word-boundary breaks so lines don't stretch,
# and sets w:doNotExpandShiftReturn. Typical ราชการ call:
enforce_thai(doc, uniform_size_pt=16, distribute=True)

# Split Latin vs Thai font inside the same run (no need to split text into runs):
enforce_thai(doc, latin_font="Times New Roman")   # English Times, Thai TH Sarabun
enforce_thai(doc, thai_font="TH SarabunPSK", size_pt=14)
# Thai often looks smaller than a Latin face at the same point size — size each:
enforce_thai(doc, latin_font="Angsana New", thai_size_pt=16, latin_size_pt=14)

# Fix justified / Thai-Distributed paragraphs that stretch glyphs apart:
enforce_thai(doc, add_zwsp=True)   # inserts U+200B at word boundaries (pythainlp)
```

`add_zwsp` gives Word legal break points at word boundaries (Thai has no spaces),
so it breaks *between* words instead of stretching the glyphs of one word across
the line. It needs `pythainlp`; without it the step is skipped with a warning and
nothing else breaks. Because it edits run text, it runs last.

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
- `pythainlp` — optional; only needed for `add_zwsp`. Everything else works without it.

## Scope

This skill's job is to convert **already-written** Thai text into a .docx that
renders faithfully in Microsoft Word. It touches **font and rendering properties
only** — `enforce_thai` does not alter a single character of the text (the one
exception is the opt-in `add_zwsp`, which inserts invisible word-break hints). It
does not clean, rewrite, or check the source text, and it does not write or review
legal content. Every generated document is a **draft** — the wording of a
contract, คำให้การ, or บันทึกความเห็น is drafted and reviewed by a person.
