# Claude Agent Kit

> 🤖 **Multi-Agent Implementation Engine** - The perfect companion for [OpenSpec](https://github.com/Fission-AI/OpenSpec) spec-driven development

[![npm version](https://badge.fury.io/js/@champpaba%2Fclaude-agent-kit.svg)](https://www.npmjs.com/package/@champpaba/claude-agent-kit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## What is this?

**Claude Agent Kit** turns OpenSpec plans into working code using 6 specialized AI agents.

```
OpenSpec Planning → proposal.md + tasks.md
                          ↓
Claude Agent Kit → 6 agents execute in phases → Working code + tests
```

---

## Quick Start

```bash
# Install
npm install -g @champpaba/claude-agent-kit

# Initialize in your project
cd your-project
cak init

# Use in Claude Code
/csetup my-feature    # Setup change context
/cdev my-feature      # Execute with agents
/cstatus my-feature   # Check progress
```

---

## The 6 Agents

| Agent | Phase | Responsibility |
|-------|-------|----------------|
| **uxui-frontend** | 1 | UI components with mock data |
| **backend** | 2 | API endpoints |
| **database** | 2 | Schemas, migrations |
| **integration** | 2.5 | Validate API contracts |
| **frontend** | 3 | Connect UI to APIs |
| **test-debug** | 4 | Tests and bug fixes |

---

## Commands

### CLI Commands

```bash
cak init              # Initialize template
cak update --backup   # Update to latest version
```

### Slash Commands (in Claude Code)

| Command | Description |
|---------|-------------|
| `/designsetup` | Generate style guide (one-time) |
| `/pageplan @prd.md` | Generate UI page plan |
| `/csetup {id}` | Setup change context |
| `/cdev {id}` | Execute with agents |
| `/cview {id}` | Detailed progress |
| `/cstatus {id}` | Quick status |
| `/pstatus` | Update project status |

---

## Cross-Session Context (v2.1.0)

`PROJECT_STATUS.yml` helps Claude remember project state between sessions:

```yaml
# PROJECT_STATUS.yml
current_focus:
  description: "Building auth system"
  active_change: auth-system

infrastructure:
  database: { status: healthy }
  api: { status: healthy }

blockers:
  - id: domain-config
    description: "Need domain for Cloudflare"
    blocks: [production-launch]

next_priorities:
  - id: payment-integration
    reason: "Revenue blocker"
```

Created by `cak init` (optional). Update with `/pstatus`.

---

## Project Structure

```
your-project/
├── PROJECT_STATUS.yml          # Cross-session context (optional)
├── openspec/
│   └── changes/{id}/
│       ├── proposal.md         # From OpenSpec
│       ├── tasks.md            # From OpenSpec
│       └── page-plan.md        # From /pageplan
├── design-system/
│   └── STYLE_GUIDE.md          # From /designsetup
└── .claude/
    ├── agents/                 # 6 specialized agents
    ├── commands/               # Slash commands
    └── contexts/               # Patterns & domain context
```

---

## Key Features

- ✅ **6 Specialized Agents** - Each focused on its domain
- ✅ **Auto Best Practices** - Context7 MCP integration
- ✅ **Design System** - Consistent UI via tokens.json
- ✅ **Page Planning** - Component reuse, real content
- ✅ **Progress Tracking** - flags.json, /cstatus, /cview
- ✅ **Cross-Session Context** - PROJECT_STATUS.yml

---

## Workflow Example

```bash
# 1. OpenSpec creates: proposal.md + tasks.md

# 2. Setup (optional design + page plan)
/designsetup
/pageplan @prd.md

# 3. Execute
/csetup my-feature
/cdev my-feature

# 4. Monitor
/cstatus my-feature
```

---

## Changelog

### v2.1.0 (2025-12-01)
- Added `PROJECT_STATUS.yml` for cross-session context
- Added `/pstatus` command
- `/csetup` reads blockers from PROJECT_STATUS.yml
- `/cstatus` shows project + change status

### v2.0.0 (2025-11-30)
- Claude 4.5 optimization (61% token reduction)
- Design System v2.0 (tokens.json, selective patterns)
- All agents use Opus 4.5 model

### v1.8.0 (2025-11-26)
- Merged `/psetup` into `/csetup`
- Auto tech stack detection
- Auto best-practices from Context7

[Full changelog in releases](https://github.com/ChampPABA/claude-multi-agent-template/releases)

---

## Links

- [npm Package](https://www.npmjs.com/package/@champpaba/claude-agent-kit)
- [GitHub](https://github.com/ChampPABA/claude-multi-agent-template)
- [OpenSpec](https://github.com/Fission-AI/OpenSpec)
- [Issues](https://github.com/ChampPABA/claude-multi-agent-template/issues)

---

## License

MIT License - see [LICENSE](LICENSE)

---

**Ready to start?**

```bash
npm install -g @champpaba/claude-agent-kit
cd your-project
cak init
```
