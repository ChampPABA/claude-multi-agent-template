# Claude Agent Kit

> Multi-Agent Implementation Engine for [OpenSpec](https://github.com/Fission-AI/OpenSpec)

[![npm version](https://badge.fury.io/js/@champpaba%2Fclaude-agent-kit.svg)](https://www.npmjs.com/package/@champpaba/claude-agent-kit)

## Quick Start

```bash
npm install -g @champpaba/claude-agent-kit
cd your-project
cak init

# In Claude Code
/csetup my-feature
/cdev my-feature
```

## Agents

| Agent | Phase | Role |
|-------|-------|------|
| uxui-frontend | 1 | UI with mock data |
| backend | 2 | API endpoints |
| database | 2 | Schemas |
| integration | 2.5 | Contract validation |
| frontend | 3 | Connect UI to API |
| test-debug | 4 | Tests & fixes |

## Features

- **4-Layer Validation (v2.2.0)** - Feature BP → Spec Alignment → Library Capability → Stack BP
- **Spec Drift Prevention** - Validates library supports spec before implementation
- **Instruction-based Library Detection** - Agents scan `tasks.md`/`design.md` for required libraries
- **Cross-session Context** - `PROJECT_STATUS.yml` maintains state across sessions
- **Design System v2.0** - Interactive setup with theme selection

## Validation Flow (v2.2.0)

```
/csetup
  ├── Step 2.6: Feature Best Practice (Auth, Payment, etc. vs industry standard)
  ├── Step 2.7: Stack Best Practice (React, Next.js, etc.)
  └── Step 2.8: Library Capability (verify library supports spec)

/cdev
  └── Agent Step 0.5: Double-check feasibility before implement
```

## Commands

**CLI:** `cak init` | `cak update`

**Slash:** `/designsetup` `/pageplan` `/csetup {id}` `/cdev {id}` `/cstatus {id}` `/pstatus`

## Links

[npm](https://www.npmjs.com/package/@champpaba/claude-agent-kit) | [GitHub](https://github.com/ChampPABA/claude-multi-agent-template) | [OpenSpec](https://github.com/Fission-AI/OpenSpec)

MIT License
