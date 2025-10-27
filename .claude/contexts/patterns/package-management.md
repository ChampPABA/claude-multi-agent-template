# Package Management

**Goal:** Consistent, reproducible, and fast dependency management across projects.

---

## Package Managers by Ecosystem

| Ecosystem | Manager | Config File | Lock File | Speed |
|-----------|---------|-------------|-----------|-------|
| **Node.js** | pnpm ✅ | `package.json` | `pnpm-lock.yaml` | Fastest |
| **Node.js** | npm | `package.json` | `package-lock.json` | Slow |
| **Node.js** | yarn | `package.json` | `yarn.lock` | Medium |
| **Python** | Poetry ✅ | `pyproject.toml` | `poetry.lock` | Fast |
| **Python** | pip | `requirements.txt` | N/A | Slow |

---

## pnpm (Node.js) ✅ RECOMMENDED

**Why pnpm?**
- ✅ 2-3x faster than npm
- ✅ Disk space efficient (symlinks, no duplication)
- ✅ Strict dependency resolution (no phantom dependencies)
- ✅ Built-in workspace support (monorepos)

### Installation

```bash
# Install pnpm globally
npm install -g pnpm

# Or use corepack (Node.js 16.13+)
corepack enable
corepack prepare pnpm@latest --activate
```

---

### Basic Commands

```bash
# Install all dependencies
pnpm install

# Add dependency
pnpm add <package>          # Production dependency
pnpm add -D <package>       # Dev dependency
pnpm add -g <package>       # Global install

# Remove dependency
pnpm remove <package>

# Update dependencies
pnpm update                 # Update all
pnpm update <package>       # Update specific package

# Run scripts
pnpm dev                    # Run dev script
pnpm build                  # Run build script
pnpm test                   # Run test script

# Execute binary
pnpm exec <binary>          # Execute local binary
pnpm dlx <package>          # Download and execute (like npx)
```

---

### Workspace (Monorepo)

```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

```json
// package.json (root)
{
  "name": "monorepo",
  "private": true,
  "scripts": {
    "dev": "pnpm --parallel -r dev",
    "build": "pnpm -r build",
    "test": "pnpm -r test"
  }
}

// apps/web/package.json
{
  "name": "@monorepo/web",
  "dependencies": {
    "@monorepo/shared": "workspace:*"  // Workspace dependency
  }
}
```

---

### Configuration

```ini
# .npmrc
# Use pnpm store instead of npm cache
store-dir=~/.pnpm-store

# Strict peer dependencies
auto-install-peers=false

# Lockfile settings
lockfile=true
prefer-frozen-lockfile=true

# Installation settings
shamefully-hoist=false
strict-peer-dependencies=true
```

---

## npm (Node.js)

**Use only if:** pnpm is not available

```bash
# Install all dependencies
npm install
npm ci                      # Clean install (CI/CD)

# Add dependency
npm install <package>
npm install -D <package>    # Dev dependency

# Remove dependency
npm uninstall <package>

# Update dependencies
npm update

# Run scripts
npm run dev
npm run build
npm test

# Execute binary
npx <binary>                # Execute local or remote binary
```

---

## Poetry (Python) ✅ RECOMMENDED

**Why Poetry?**
- ✅ Dependency resolution with lock file
- ✅ Virtual environment management
- ✅ Reproducible builds
- ✅ pyproject.toml (PEP 518 standard)

### Installation

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Or with pip
pip install poetry
```

---

### Basic Commands

```bash
# Create new project
poetry new myproject
poetry init                 # Initialize in existing project

# Install dependencies
poetry install              # Install from pyproject.toml
poetry install --no-dev     # Production only

# Add dependency
poetry add <package>
poetry add -D <package>     # Dev dependency
poetry add <package>@latest # Latest version

# Remove dependency
poetry remove <package>

# Update dependencies
poetry update               # Update all
poetry update <package>     # Update specific package

# Run scripts
poetry run python app.py
poetry run pytest

# Activate virtual environment
poetry shell
```

---

### Configuration

```toml
# pyproject.toml
[tool.poetry]
name = "myproject"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.0"
uvicorn = "^0.24.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.10.0"
ruff = "^0.1.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

---

### Virtual Environments

```bash
# Create virtual environment
poetry env use python3.11

# Show environment info
poetry env info

# List environments
poetry env list

# Remove environment
poetry env remove <env-name>
```

---

## pip (Python)

**Use only if:** Poetry is not available

```bash
# Install dependencies
pip install -r requirements.txt

# Install package
pip install <package>
pip install <package>==1.0.0   # Specific version

# Freeze dependencies
pip freeze > requirements.txt

# Uninstall package
pip uninstall <package>

# Upgrade package
pip install --upgrade <package>
```

### Requirements File

```txt
# requirements.txt
fastapi==0.104.0
uvicorn[standard]==0.24.0
python-dotenv==1.0.0

# Dev dependencies (separate file)
# requirements-dev.txt
pytest==7.4.0
black==23.10.0
```

---

## Version Pinning

### Node.js (package.json)

```json
{
  "dependencies": {
    "next": "^15.0.0",        // ✅ Caret: Allow minor updates
    "react": "~19.0.0",       // ⚠️ Tilde: Allow patch updates only
    "lodash": "4.17.21"       // ❌ Exact: No updates (not recommended)
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "vitest": "^1.0.0"
  }
}
```

**Version Ranges:**
- `^1.2.3` - Compatible with 1.2.3 (allow 1.x.x updates) ✅ Recommended
- `~1.2.3` - Approximately 1.2.3 (allow 1.2.x updates)
- `1.2.3` - Exact version (no updates) ❌ Avoid

---

### Python (Poetry)

```toml
[tool.poetry.dependencies]
python = "^3.11"          # ✅ 3.11.0 - 3.x.x (exclude 4.0.0)
fastapi = "^0.104.0"      # ✅ 0.104.0 - 0.x.x (exclude 1.0.0)
uvicorn = "~0.24.0"       # ⚠️ 0.24.0 - 0.24.x
pydantic = "2.5.0"        # ❌ Exact version (not recommended)
```

---

### Python (pip)

```txt
# requirements.txt
fastapi>=0.104.0,<1.0.0   # ✅ Compatible range
uvicorn==0.24.0           # ❌ Exact version
pydantic~=2.5.0           # ⚠️ Compatible with 2.5.x
```

---

## Lock Files

### Why Lock Files?

- ✅ **Reproducible builds** - Same versions on dev, CI, production
- ✅ **Security** - Prevent unexpected updates
- ✅ **Debugging** - Know exactly which version caused issues

### pnpm-lock.yaml

```yaml
# pnpm-lock.yaml (auto-generated)
lockfileVersion: '6.0'
dependencies:
  next:
    specifier: ^15.0.0
    version: 15.0.2
  react:
    specifier: ^19.0.0
    version: 19.0.0
```

**Important:**
- ✅ Commit lock file to Git
- ✅ Use `pnpm install --frozen-lockfile` in CI/CD
- ❌ Never manually edit lock file

---

### poetry.lock

```toml
# poetry.lock (auto-generated)
[[package]]
name = "fastapi"
version = "0.104.1"
description = "FastAPI framework"
category = "main"
```

**Important:**
- ✅ Commit lock file to Git
- ✅ Use `poetry install --no-update` in CI/CD
- ❌ Never manually edit lock file

---

## CI/CD Best Practices

### pnpm (Node.js)

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: pnpm/action-setup@v2
        with:
          version: 8

      - uses: actions/setup-node@v3
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile
      - run: pnpm test
      - run: pnpm build
```

---

### Poetry (Python)

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Poetry
        run: pip install poetry

      - name: Install dependencies
        run: poetry install --no-root

      - name: Run tests
        run: poetry run pytest

      - name: Lint
        run: poetry run ruff check .
```

---

## Troubleshooting

### pnpm Issues

**Problem:** "ERR_PNPM_PEER_DEP_ISSUES"
```bash
# Solution 1: Auto-install peer dependencies
pnpm install --shamefully-hoist

# Solution 2: Disable strict peers
echo "auto-install-peers=true" >> .npmrc
```

**Problem:** "Lockfile is up to date"
```bash
# Force update
pnpm install --force
```

---

### Poetry Issues

**Problem:** "Lock file is not compatible"
```bash
# Update lock file
poetry lock --no-update
```

**Problem:** "Virtual environment not found"
```bash
# Recreate environment
poetry env use python3.11
poetry install
```

---

## Migration Guides

### npm → pnpm

```bash
# 1. Remove npm artifacts
rm -rf node_modules package-lock.json

# 2. Install pnpm
npm install -g pnpm

# 3. Install with pnpm
pnpm install

# 4. Update scripts (optional)
# package.json
{
  "scripts": {
    "dev": "next dev",      # Works with both npm and pnpm
    "build": "next build"
  }
}
```

---

### pip → Poetry

```bash
# 1. Install Poetry
pip install poetry

# 2. Initialize project
poetry init

# 3. Import from requirements.txt
poetry add $(cat requirements.txt)

# 4. Verify
poetry install
poetry run pytest
```

---

## Quick Reference

### pnpm

| Command | npm equivalent |
|---------|----------------|
| `pnpm install` | `npm install` |
| `pnpm add <pkg>` | `npm install <pkg>` |
| `pnpm remove <pkg>` | `npm uninstall <pkg>` |
| `pnpm update` | `npm update` |
| `pnpm dlx <pkg>` | `npx <pkg>` |

### Poetry

| Command | pip equivalent |
|---------|----------------|
| `poetry install` | `pip install -r requirements.txt` |
| `poetry add <pkg>` | `pip install <pkg>` |
| `poetry remove <pkg>` | `pip uninstall <pkg>` |
| `poetry update` | `pip install --upgrade <pkg>` |
| `poetry run <cmd>` | `python <cmd>` |

---

**💡 Remember:** Always commit lock files to Git for reproducible builds!
