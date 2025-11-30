# Documentation Policy v1.8.0 (Shared by All Agents)

> **Purpose:** Single source of truth for what files agents create

---

## Core Principle

Agents create **code files only**. Results go to terminal output.

---

## Allowed Files

- Source code (`.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, etc.)
- Config files (`package.json`, `tsconfig.json`, `.env.example`)
- Schema files (`schema.prisma`, `models.py`)
- Test files (`*.test.ts`, `*.spec.ts`, `test_*.py`)
- Style files (`.css`, `.scss`, `tailwind.config.js`)

---

## Forbidden Files (Auto-Deleted)

These files waste tokens and clutter the project:

| Pattern | Example | Why Forbidden |
|---------|---------|---------------|
| `*_REPORT.md` | `IMPLEMENTATION_REPORT.md` | Use terminal output |
| `*_SUMMARY.txt` | `PHASE_SUMMARY.txt` | Use terminal output |
| `PHASE_*.txt` | `PHASE_11_DELIVERY.txt` | Removed in v1.8.0 |
| ALL_CAPS filenames | `README_FINAL.md` | Usually temp files |

---

## Rule of Thumb

> If it wouldn't be committed to git, don't create it.

---

## Why This Matters

Token optimization:
- Report files waste 500-2000 tokens each
- v1.8.0 removed doc/report phases for 25 min savings
- Terminal output is sufficient for status updates
