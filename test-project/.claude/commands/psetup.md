---
name: Project Setup
description: Setup project-level contexts (one-time)
category: Multi-Agent
tags: [setup, project, context7]
---

## Usage

```bash
/psetup
```

## What It Does

One-time project setup:
1. Detect tech stack from package files
2. Query Context7 for best practices
3. Create domain/ structure (3-level indexing)
4. Generate best practices files

## Steps

### 1. Check if Already Setup

```bash
ls .claude/contexts/domain/project/
```

If exists:
```
⚠️ Project already set up
Re-run will overwrite existing files
Continue? (yes/no)
```

### 2. Detect Package Manager

Check for lock files:
- `pnpm-lock.yaml` → pnpm
- `package-lock.json` → npm
- `yarn.lock` → yarn
- `uv.lock` → uv
- `poetry.lock` → poetry
- etc.

### 3. Detect Tech Stack

Parse `package.json` / `requirements.txt`:
- Extract framework names and versions
- Detect: Next.js, React, Prisma, FastAPI, etc.

### 4. Query Context7

For each framework:
```
mcp__context7__resolve-library-id({framework})
mcp__context7__get-library-docs({id}, {topic}, {tokens: 8000})
```

### 5. Generate Files

Create:
- `.claude/contexts/domain/index.md`
- `.claude/contexts/domain/project/README.md`
- `.claude/contexts/domain/project/tech-stack.md`
- `.claude/contexts/domain/project/best-practices/index.md`
- `.claude/contexts/domain/project/best-practices/{framework}.md` (each)

### 6. Output Summary

```
✅ Project setup complete!

📦 Package Manager: pnpm 9.x
🛠️ Tech Stack Detected:
- Frontend: Next.js 14.2.0
- Frontend: React 18.3.0
- Database: Prisma 6.5.0
- Testing: Vitest 2.0.0

📚 Best Practices Generated (from Context7):
✓ nextjs-14.md (8000 tokens)
✓ react-18.md (8000 tokens)
✓ prisma-6.md (8000 tokens)
✓ vitest-2.md (8000 tokens)

📁 Files Created:
✓ domain/index.md
✓ domain/project/README.md
✓ domain/project/tech-stack.md
✓ domain/project/best-practices/index.md
✓ domain/project/best-practices/ (4 files)

🚀 Ready for development!

Next steps:
1. Create change with OpenSpec
2. Setup change: /csetup {change-id}
3. Start development: /cdev {change-id}
```
