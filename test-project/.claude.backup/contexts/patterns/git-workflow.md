# Git Workflow

## Commit Message Guidelines

### Format

```
<type>: <subject>

<body (optional)>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Rules

**DO:**
- ✅ Write clear, concise commit messages
- ✅ Use imperative mood ("add feature" not "added feature")
- ✅ Keep subject line under 72 characters
- ✅ Explain WHY in the body, not WHAT (code shows what)

**DON'T:**
- ❌ **Do NOT add Claude Code footer** (`🤖 Generated with [Claude Code]...`)
- ❌ **Do NOT add Co-Authored-By: Claude** attribution
- ❌ Don't use vague messages ("fix bug", "update code")
- ❌ Don't commit commented-out code
- ❌ Don't commit secrets or credentials

### Examples

**✅ GOOD:**
```
feat: add user authentication with JWT

Implemented JWT-based authentication to replace session-based auth.
This improves security and enables stateless API design.
```

**❌ BAD:**
```
feat: add user authentication

Added authentication stuff.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Branching Strategy

### Main Branch
- Always production-ready
- Never commit directly (use PRs)
- Protected branch with reviews

### Feature Branches
- Format: `feature/description` or `feat/description`
- Short-lived (merge within days)
- Delete after merge

### Bug Fix Branches
- Format: `fix/description` or `bugfix/description`
- Create from main
- Merge back to main

---

## Pull Request Workflow

### Before Creating PR

1. **Update from main:**
   ```bash
   git checkout main
   git pull
   git checkout feature/your-feature
   git rebase main
   ```

2. **Run tests:**
   ```bash
   npm test
   # or
   pytest
   ```

3. **Review your changes:**
   ```bash
   git diff main...HEAD
   ```

### PR Description Template

```markdown
## Summary
Brief description of changes

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] No breaking changes

## Screenshots (if UI changes)
[Add screenshots]
```

**DO NOT include:**
- ❌ Claude Code attribution footer
- ❌ AI-generated disclaimers

---

## Best Practices

### Commits

1. **Atomic commits** - One logical change per commit
2. **Frequent commits** - Commit working code often
3. **Meaningful messages** - Future you will thank you

### Files to .gitignore

```gitignore
# Environment
.env
.env.local
*.local

# Dependencies
node_modules/
__pycache__/
*.pyc

# Build outputs
dist/
build/
.next/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

---

## Recovery Commands

### Undo last commit (keep changes)
```bash
git reset --soft HEAD~1
```

### Undo last commit (discard changes)
```bash
git reset --hard HEAD~1
```

### Undo changes to file
```bash
git checkout -- file.txt
```

### Unstage file
```bash
git restore --staged file.txt
```

---

## IMPORTANT: No AI Attribution

**When committing code:**

- ❌ **Do NOT add:** `🤖 Generated with [Claude Code]`
- ❌ **Do NOT add:** `Co-Authored-By: Claude <noreply@anthropic.com>`
- ❌ **Do NOT add:** Any AI-related footers or attributions

**Reason:**
- Git history should reflect actual code changes, not tooling
- Attribution clutters git log
- Code ownership is clear from git author
- Professional projects don't need AI disclaimers

**Keep commits clean and professional.**
