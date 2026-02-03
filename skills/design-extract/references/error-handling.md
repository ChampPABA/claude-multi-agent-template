# Error Handling

How to handle failures during design extraction.

---

## Critical Errors (Stop Execution)

### Navigation Failures

If browser navigation fails:

```
❌ Failed to load URL: {url}

Error: {error.message}

Check:
- Is the URL accessible?
- Is agent-browser installed? (npm install -g agent-browser && agent-browser install)
- Is the site blocking automated access?
```

**Action:** Stop execution. Cannot proceed without page loaded.

### Browser Not Available

If agent-browser is not available:

```
❌ Browser automation not available

Required: agent-browser CLI

Setup:
npm install -g agent-browser && agent-browser install
```

**Action:** Stop execution. Provide setup instructions.

---

## Non-Critical Errors (Continue with Fallbacks)

### Extraction Failures

If individual extraction steps fail:

| Extraction | Fallback |
|------------|----------|
| Colors | `{ backgrounds: [], texts: [], borders: [] }` |
| Typography | `{ h1: [], fonts: [], weights: [], sizes: [] }` |
| Shadows | `{ shadows: [], borderRadii: [] }` |
| Spacing | `{ grid_base: 8, common_values: [] }` |
| Components | `[]` (empty array) |
| Animations | `{ keyframes: [], transitions: [] }` |

Log warning and continue:
```
⚠️ Color extraction failed: {error.message}
   Using fallback empty data
```

### Screenshot Failures

| Scenario | Fallback |
|----------|----------|
| Full-page screenshot fails | Try viewport-only screenshot |
| Component screenshot fails | Skip component, continue with others |
| All screenshots fail | Continue without screenshots, note in report |

### CORS/Security Errors

Some sites block stylesheet access:

```
⚠️ Cannot access stylesheet: {url}
   Reason: CORS policy
   Skipping external stylesheet
```

**Action:** Continue with inline styles and accessible stylesheets.

### Element Not Found

If expected elements don't exist:

```
⚠️ No buttons found on page
   Skipping button extraction
```

**Action:** Mark section as `detected: false` in output YAML.

---

## Partial Success Handling

### Coverage Calculation

Track what was successfully extracted:

```yaml
coverage:
  total_sections: 17
  detected_sections: 12
  percentage: 71
  missing:
    - icons_imagery
    - navigation_patterns
    - loading_states
    - feedback_states
    - accessibility
```

### Final Report with Warnings

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ EXTRACTION COMPLETE (with warnings)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Coverage: 12/17 sections (71%)

⚠️ Warnings:
   - Color extraction partial: CORS blocked 2 stylesheets
   - Button hover states: 1 of 3 failed
   - Full-page screenshot failed, using viewport

📁 Output:
   ✓ design-system/extracted/example/data.yaml
   ⚠️ design-system/extracted/example/screenshots/ (partial)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Retry Strategy

For transient failures (network timeouts):

1. **First attempt:** Normal extraction
2. **If timeout:** Wait 2 seconds, retry once
3. **If still fails:** Use fallback data, continue

Do NOT retry indefinitely. Accept partial data over blocking on single failure.

---

## User Communication

Always inform user of issues:

| Severity | Format |
|----------|--------|
| Critical | ❌ Error message, stop |
| Warning | ⚠️ Warning, continue |
| Info | ℹ️ Note, continue |

Never silently fail. User should know what succeeded and what didn't.
