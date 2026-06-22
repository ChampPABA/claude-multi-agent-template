# Error Handling

---

## Critical Errors (Stop)

| Error | Message | Action |
|-------|---------|--------|
| Navigation fails | `❌ Failed to load URL: {url}` — check URL accessibility, site blocking | Stop |
| Browser unavailable | `❌ agent-browser not found` — run `npm install -g agent-browser && agent-browser install` | Stop |

---

## Non-Critical Errors (Continue with Fallbacks)

All failed extractions default to empty structures. Log `⚠️` warning and continue.

| Failure | Fallback |
|---------|----------|
| Individual extraction (colors, typography, etc.) | Empty arrays/objects for that section |
| Full-page screenshot | Try viewport-only |
| Component screenshot | Skip that component |
| All screenshots | Continue without, note in report |
| CORS blocks stylesheet | Use inline styles + accessible stylesheets |
| Element not found (no buttons, etc.) | Mark `detected: false` in YAML |

---

## Retry & Coverage

- On timeout: wait 2s, retry once. If still fails, use fallback. Never retry indefinitely.
- Track coverage: `detected_sections / 20 * 100` — list missing sections in `coverage.missing`

---

## Communication

Never silently fail. Always inform user:
- `❌` Critical → stop
- `⚠️` Warning → continue with fallback
- `ℹ️` Info → continue
