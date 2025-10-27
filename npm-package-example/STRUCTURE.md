# Package Structure

```
create-claude-agent/
├── package.json                 # npm package config
├── README.md                    # Documentation
├── bin/
│   └── cli.js                   # CLI installer script
└── template/                    # Template files to be copied
    ├── CLAUDE.md
    ├── agents/
    │   ├── 01-orchestrator.md
    │   ├── 02-uxui-frontend.md
    │   ├── 03-test-debug.md
    │   ├── 04-frontend.md
    │   ├── 05-backend.md
    │   └── 06-database.md
    ├── contexts/
    │   ├── patterns/
    │   │   ├── logging.md
    │   │   ├── testing.md
    │   │   ├── error-handling.md
    │   │   ├── development-principles.md
    │   │   ├── code-standards.md
    │   │   ├── task-breakdown.md
    │   │   ├── frontend-component-strategy.md
    │   │   ├── ui-component-consistency.md
    │   │   └── git-workflow.md
    │   └── design/
    │       ├── index.md
    │       ├── color-theory.md
    │       ├── spacing.md
    │       ├── shadows.md
    │       ├── typography.md
    │       ├── layout.md
    │       ├── responsive.md
    │       ├── box-thinking.md
    │       └── accessibility.md
    └── settings.local.json
```

## How to Build

1. Copy your `.claude/` directory to `template/`:
   ```bash
   cp -r ../.claude/* template/
   ```

2. Test locally:
   ```bash
   npm link
   npx create-claude-agent
   ```

3. Publish:
   ```bash
   npm publish
   ```
