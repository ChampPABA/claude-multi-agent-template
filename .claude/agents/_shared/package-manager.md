# Package Manager Protocol (Shared by All Agents)

> **Version:** 2.0.0 (Claude 4.5 Optimized)
> **Purpose:** Single source of truth for package manager usage

---

## Quick Rule

Read `tech-stack.md` before ALL install/run commands.

```bash
# Location:
.claude/contexts/domain/{project}/tech-stack.md
```

---

## Why This Matters

Using wrong package manager causes:
- Duplicate lock files (package-lock.json + pnpm-lock.yaml)
- CI/CD pipeline failures
- Version conflicts
- Incorrect dependency locations

---

## Protocol

**Step 1:** Read tech-stack.md

**Step 2:** Extract and use detected tool

| If Detected | Install Command | Run Command |
|-------------|-----------------|-------------|
| pnpm | `pnpm install {pkg}` | `pnpm run {script}` |
| npm | `npm install {pkg}` | `npm run {script}` |
| bun | `bun add {pkg}` | `bun run {script}` |
| uv | `uv pip install {pkg}` | `uv run {script}` |
| poetry | `poetry add {pkg}` | `poetry run {cmd}` |

**Step 3:** Report in validation

```
Package Manager: pnpm (from tech-stack.md)
```

---

## If tech-stack.md Missing

```
Warning: tech-stack.md not found
Suggestion: Run /csetup to generate tech-stack.md
Fallback: Detect from package.json or pyproject.toml
```

→ Full details: `.claude/lib/context-loading-protocol.md#level-0`
