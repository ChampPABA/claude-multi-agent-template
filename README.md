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

## Commands

**CLI:** `cak init` | `cak update`

**Slash:** `/designsetup` `/pageplan` `/csetup {id}` `/cdev {id}` `/cstatus {id}` `/pstatus`

## Links

[npm](https://www.npmjs.com/package/@champpaba/claude-agent-kit) | [GitHub](https://github.com/ChampPABA/claude-multi-agent-template) | [OpenSpec](https://github.com/Fission-AI/OpenSpec)

MIT License
