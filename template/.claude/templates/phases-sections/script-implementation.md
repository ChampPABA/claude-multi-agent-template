# Phase: Script Implementation

**Agent:** `backend` (reused for scripts)
**Metadata:** `| TDD | script | cli |`
**Estimated time:** 60 minutes

## 🎯 Purpose

Implement CLI tool or background script with proper error handling, logging, and user-friendly output.

## 📚 Context Loading

- ✅ `tech-stack.md` → Python/Node.js version, package manager
- ✅ `testing.md` (TDD: RED-GREEN-REFACTOR)
- ✅ `error-handling.md` → Network/file errors
- ✅ `logging.md` → CLI logging patterns
- ❌ Skip: API-specific contexts

## 📝 Follow TDD

This is a **CLI script**, not an API.

Focus on:
- CLI argument parsing (Click/argparse/yargs)
- Progress indicators (tqdm/ora)
- Exit codes (0 = success, 1 = error)
- User-friendly error messages
- File I/O operations
- Network requests (if applicable)

## ✅ Success Criteria

- [ ] Script functionality implemented
- [ ] CLI arguments working
- [ ] Progress indicators shown
- [ ] Error handling implemented
- [ ] Tests pass (≥80% coverage)

## 📤 Output

- Script files
- Test files
- Update flags.json
