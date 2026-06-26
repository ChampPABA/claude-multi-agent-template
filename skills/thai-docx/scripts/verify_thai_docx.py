#!/usr/bin/env python3
"""verify_thai_docx.py — QA scanner: does a .docx actually carry the complex-script
properties Thai needs to render correctly in Microsoft Word?

WHY this exists: Word's print/preview AND LibreOffice silently auto-pick a Thai
font when the cs slot is empty, so the defects are INVISIBLE there. They only
appear in real Microsoft Word — which is exactly where your reader opens the file.
Never trust the preview. Trust this scanner: it reads the raw OOXML and flags
every run whose Thai slot is unset.

Usage:  python verify_thai_docx.py path/to/file.docx [--quiet]
Exit code 0 = clean (safe to send). Exit code 1 = defects found.
"""

import sys
import re
import zipfile
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
def w(tag): return '{%s}%s' % (W, tag)

THAI = re.compile('[฀-๿]')


def _run_text(r):
    return ''.join(t.text or '' for t in r.iter(w('t')))


def scan_runs(root, part):
    defects = []
    for r in root.iter(w('r')):
        text = _run_text(r)
        if not THAI.search(text):
            continue
        snippet = (text[:24] + '…') if len(text) > 24 else text
        rPr = r.find(w('rPr'))
        rFonts = rPr.find(w('rFonts')) if rPr is not None else None

        cs = rFonts.get(w('cs')) if rFonts is not None else None
        if not cs:
            defects.append((part, snippet, 'rFonts missing @w:cs',
                            'Thai falls back to a default font: shrinks, tone marks float'))
        if rPr is not None:
            if rPr.find(w('sz')) is not None and rPr.find(w('szCs')) is None:
                defects.append((part, snippet, 'has w:sz but no w:szCs',
                                'Thai size ignores w:sz and shrinks vs the Latin text'))
            if rPr.find(w('b')) is not None and rPr.find(w('bCs')) is None:
                defects.append((part, snippet, 'has w:b but no w:bCs',
                                'bold applies to Latin only; Thai stays regular weight'))
            if rPr.find(w('i')) is not None and rPr.find(w('iCs')) is None:
                defects.append((part, snippet, 'has w:i but no w:iCs',
                                'italic applies to Latin only; Thai stays upright'))
    return defects


def scan(path):
    defects = []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        run_parts = [n for n in names if re.match(
            r'word/(document|header\d*|footer\d*|footnotes|endnotes|comments)\.xml$', n)]
        for n in run_parts:
            root = etree.fromstring(z.read(n))
            defects += scan_runs(root, n.split('/')[-1])

        # settings.xml must tag the complex-script language so Word uses the Thai
        # dictionary for line breaking instead of cutting mid-word.
        if 'word/settings.xml' in names:
            st = etree.fromstring(z.read('word/settings.xml'))
            tfl = st.find(w('themeFontLang'))
            if tfl is None or not tfl.get(w('bidi')):
                defects.append(('settings.xml', '(document)',
                                'themeFontLang missing @w:bidi',
                                'Word may break lines in the middle of Thai words'))
    return defects


def main(argv):
    args = [a for a in argv[1:] if not a.startswith('-')]
    quiet = '--quiet' in argv
    if not args:
        print(__doc__.strip().splitlines()[-2])
        return 2
    path = args[0]
    defects = scan(path)
    if not defects:
        print(f"PASS  {path}  — Thai complex-script properties present on every Thai run.")
        return 0
    print(f"FAIL  {path}  — {len(defects)} defect(s):")
    if not quiet:
        for part, snippet, defect, symptom in defects:
            print(f"  [{part}] \"{snippet}\"")
            print(f"        ✗ {defect}")
            print(f"          → {symptom}")
    print(f"\n{len(defects)} defect(s). Do NOT judge from the Word preview — it hides these.")
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
