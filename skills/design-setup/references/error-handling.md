# Error Handling

How to handle failures during design setup.

---

## Error 1: No Extracted Data

**When:** No `design-system/extracted/*/data.yaml` files found

**Message:**
```
❌ No extracted data found

Please extract at least 1 site:
  /extract https://airbnb.com

Then run: /designsetup @prd.md
```

**Action:** Stop execution.

---

## Error 2: AI Analysis Fails

**When:** LLM call fails during context analysis or theme generation

**Message:**
```
❌ AI analysis failed: {error.message}

This may be due to:
- Extracted data too large (try fewer sites)
- API rate limit (wait and retry)
- Invalid context files

Retry or use --debug for details
```

**Action:** Allow retry or proceed with fallback (interactive questions).

---

## Error 3: User Cancels

**When:** User selects "Cancel" at any point

**Message:**
```
⚠️ Design setup cancelled

Your data is preserved:
- Extracted: design-system/extracted/
- Options: design-system/synthesis/options/ (if any)

Run /designsetup again when ready.
```

**Action:** Stop execution, preserve existing data.

---

## Error 4: Max Rounds Reached

**When:** User has adjusted 3 times without accepting

**Message:**
```
⚠️ ครบ 3 รอบแล้ว

แนะนำ:
1. รัน /extract กับ reference ใหม่
2. หรือ accept แล้วค่อย manual edit ไฟล์ที่สร้าง
```

**Action:** Force decision (Yes to generate / Cancel to exit).

---

## Error 5: Write Fails

**When:** Cannot write to design-system/ directory

**Actions:**
1. Try to save backup to `/tmp/design-system-backup/`
2. Display error with backup location:

```
❌ Failed to write files

Check permissions: design-system/

Backup saved: /tmp/design-system-backup/
```

---

## Error 6: Context File Not Found

**When:** User-provided context file doesn't exist

**Message:**
```
⚠️ Context file not found: {filename}
   Skipping this file...
```

**Action:** Continue with other files, warn user.

---

## Error 7: Invalid Extracted Data

**When:** Extracted YAML is malformed or missing required fields

**Message:**
```
⚠️ Invalid data in {site}/data.yaml
   Missing: {missing fields}
   Skipping this site...
```

**Action:** Continue with other sites if available.

---

## Graceful Degradation

| Scenario | Fallback |
|----------|----------|
| No context files | Use interactive questions |
| AI analysis fails | Use interactive questions |
| Some extractions invalid | Use valid ones only |
| Theme generation fails | Use "Abstract" theme |
| Pattern generation fails | Skip patterns, generate data.yaml only |

---

## Recovery Suggestions

For persistent errors:

1. **Clear and re-extract:**
   ```bash
   rm -rf design-system/extracted/
   /extract https://site.com
   ```

2. **Use fewer sites:**
   Large extractions may exceed context limits

3. **Simplify context:**
   Use shorter, focused context files

4. **Manual generation:**
   If all else fails, manually create `data.yaml` based on extraction data
