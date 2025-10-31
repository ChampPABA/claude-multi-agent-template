# Claude Agent Kit

> 🤖 Universal multi-agent template for Claude Code - AI-assisted development with specialized agents

[![npm version](https://badge.fury.io/js/@champpaba%2Fclaude-agent-kit.svg)](https://www.npmjs.com/package/@champpaba/claude-agent-kit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/node/v/@champpaba/claude-agent-kit)](https://nodejs.org)

---

## 🎯 What is this?

A **production-ready CLI package** that sets up a multi-agent system for building software with AI:

- ✅ **6 Specialized Agents** - Integration, UX/UI Frontend, Test/Debug, Frontend, Backend, Database
- ✅ **Auto-Generated Best Practices** - Uses Context7 MCP to fetch latest framework docs
- ✅ **3-Level Project Indexing** - Agents auto-discover your project context
- ✅ **Universal Patterns** - Logging, testing, error handling, task classification
- ✅ **Design Foundation** - Color theory, spacing, typography, accessibility
- ✅ **Framework Agnostic** - Works with Next.js, React, Vue, FastAPI, Django, etc.

---

## 📦 Installation

### Using npm (recommended):
```bash
npm install -g @champpaba/claude-agent-kit
```

### Using pnpm:
```bash
pnpm add -g @champpaba/claude-agent-kit
```

### Using yarn:
```bash
yarn global add @champpaba/claude-agent-kit
```

---

## 🚀 Quick Start

### Step 1: Initialize in Your Project

```bash
# Go to your project directory
cd my-awesome-project

# Initialize Claude Agent Kit
cak init

# Or use the full command
claude-agent-kit init
```

**This will create a `.claude/` folder with:**
- 6 specialized agents
- Universal development patterns
- Design foundation
- Slash commands for workflows

---

### Step 2: Setup Context7 MCP (Optional but Recommended)

Context7 MCP provides up-to-date documentation for your framework/libraries.

1. Open Claude Code Settings → MCP Servers
2. Add this configuration:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp"]
    }
  }
}
```

3. Restart Claude Code
4. Verify: Type `/mcp` → should see `context7`

---

### Step 3: Setup Your Project

Run the project setup command in Claude Code:

```bash
/psetup
```

This will:
- Detect your tech stack (Next.js, Prisma, FastAPI, etc.)
- Create project-specific context files
- Fetch relevant documentation from Context7

---

### Step 4: Start Using Agents!

Invoke agents directly or use the orchestrator:

```bash
# Invoke specific agent
/agents uxui-frontend

# Or ask Claude to select the right agent
"Build a login form with Next.js and Prisma"
```

Claude will automatically:
1. Read task classification patterns
2. Select the appropriate agent(s)
3. Execute in the correct sequence
4. Update progress tracking

---

## 📚 CLI Commands

### `cak init`
Initialize Claude Agent Kit template in current project

**Options:**
- `--force` - Overwrite existing `.claude/` folder

**Example:**
```bash
cak init
cak init --force
```

---

### `cak update`
Update template files to the latest version

**Options:**
- `--backup` - Create backup before updating

**Example:**
```bash
cak update
cak update --backup
```

---

### `cak --version`
Show version number

```bash
cak --version
# → 1.0.0
```

---

### `cak --help`
Display help information

```bash
cak --help
```

---

## 🤖 Available Agents

| Agent | Color | When to Use | Phase |
|-------|-------|-------------|-------|
| **integration** | 🟠 Orange | Validate API contracts before connecting | 2.5 |
| **uxui-frontend** | 🔵 Blue | Design UI components with mock data | 1 |
| **test-debug** | 🔴 Red | Run tests and fix bugs (max 3-4 iterations) | 1,3,4 |
| **frontend** | 🟢 Green | Connect UI to backend APIs | 3 |
| **backend** | 🟣 Purple | Create API endpoints with validation | 2 |
| **database** | 🩷 Pink | Design schemas, migrations, complex queries | 2 |

---

## 📁 Project Structure After Init

```
your-project/
├── .claude/
│   ├── CLAUDE.md                    # Navigation guide
│   ├── agents/                      # 6 specialized agents
│   │   ├── 01-integration.md
│   │   ├── 02-uxui-frontend.md
│   │   ├── 03-test-debug.md
│   │   ├── 04-frontend.md
│   │   ├── 05-backend.md
│   │   └── 06-database.md
│   │
│   ├── commands/                    # Slash commands
│   │   ├── psetup.md               # Project setup
│   │   ├── agentsetup.md           # Auto-detect tech stack
│   │   ├── csetup.md               # Change setup (OpenSpec)
│   │   ├── cdev.md                 # Change development
│   │   ├── cview.md                # View change progress
│   │   └── cstatus.md              # Quick status
│   │
│   ├── contexts/
│   │   ├── design/                  # Design foundation
│   │   │   ├── index.md
│   │   │   ├── box-thinking.md
│   │   │   ├── color-theory.md
│   │   │   ├── spacing.md
│   │   │   ├── typography.md
│   │   │   ├── shadows.md
│   │   │   ├── accessibility.md
│   │   │   ├── layout.md
│   │   │   └── responsive.md
│   │   │
│   │   ├── patterns/                # Universal patterns
│   │   │   ├── task-classification.md
│   │   │   ├── agent-coordination.md
│   │   │   ├── error-recovery.md
│   │   │   ├── logging.md
│   │   │   ├── testing.md
│   │   │   ├── task-breakdown.md
│   │   │   ├── code-standards.md
│   │   │   └── ... (and more)
│   │   │
│   │   └── domain/                  # Your project context
│   │       └── README.md
│   │
│   ├── lib/                         # Implementation logic
│   │   ├── agent-executor.md        # Retry & escalation
│   │   ├── tdd-classifier.md        # TDD classification
│   │   ├── flags-updater.md         # Progress tracking
│   │   └── agent-router.md          # Agent routing rules
│   │
│   └── templates/                   # OpenSpec templates
│       └── ... (workflow templates)
```

---

## 🎨 Design System

The template includes **universal design foundation**:

- **Color Theory** - Harmony, WCAG AAA contrast, shade generation
- **Typography** - Font scales, hierarchy, readability
- **Spacing** - 8px grid system (8, 16, 24, 32, 40, 48px)
- **Shadows** - 4-level elevation system
- **Layout** - Grid, flexbox, responsive patterns
- **Box Thinking** - Systematic layout analysis framework
- **Accessibility** - ARIA, keyboard nav, WCAG 2.1 AA compliance

Agents follow these foundations automatically to ensure visual consistency.

---

## 🧪 Testing Philosophy

### TDD for Critical Paths (Required)
- Business logic calculations
- API endpoints with validation
- External service integrations
- Data transformations

### Test-Alongside for Simple Code
- CRUD operations
- UI components (presentational)
- Configuration files

**Test-Debug agent** runs tests automatically and fixes bugs (max 3-4 iterations, then escalates).

---

## 🔧 Supported Tech Stacks

Agents auto-detect your stack via Context7 MCP:

**Frontend:**
- Next.js, React, Vue, Svelte, Angular

**Backend:**
- FastAPI, Express, NestJS, Django, Flask, Next.js API Routes

**Database:**
- Prisma, SQLAlchemy, TypeORM, Drizzle

**Testing:**
- Vitest, Jest, Pytest, Playwright

---

## 📖 Usage Examples

### Example 1: Simple Task

```bash
# In Claude Code
"Build a user profile page with edit functionality"
```

Claude will:
1. Read `task-classification.md`
2. Select agents: `uxui-frontend` → `backend` → `frontend` → `test-debug`
3. Execute in sequence
4. Report completion

---

### Example 2: Complex Multi-Agent Workflow

Using OpenSpec workflow (`/csetup` command):

```bash
# Setup change context
/csetup login-system

# Start development
/cdev login-system

# View progress
/cview login-system
```

This follows a structured 4-phase approach:
1. **MVT** (Minimum Viable Test) - UI with mock data
2. **Complexity** - Real API + database
3. **Scale** - Full features + optimization
4. **Deploy** - Production-ready

---

## 🔄 Updating to Latest Version

### Method 1: Update the npm package
```bash
npm update -g @champpaba/claude-agent-kit
```

### Method 2: Update template in project
```bash
cd your-project
cak update --backup
```

This will:
- Create backup at `.claude.backup/`
- Update all template files
- Preserve your customizations in `domain/`

---

## 🎯 Customization

### Add Project-Specific Context

After running `cak init`, add your own context files:

```bash
mkdir -p .claude/contexts/domain/my-project
```

**Example:** E-commerce checkout flow
```markdown
<!-- .claude/contexts/domain/my-project/checkout-flow.md -->
# Checkout Flow

## Steps
1. Cart review
2. Shipping address
3. Payment method
4. Order confirmation

## Business Rules
- Free shipping over $50
- Tax calculation by state
- Inventory check before payment
```

Agents will auto-discover and use these patterns.

---

## 📊 What's Included?

### ✅ Universal Patterns
- Task classification (how to choose agents)
- Agent coordination (parallel/sequential execution)
- Error recovery (retry logic, escalation)
- Logging (structured JSON logging)
- Testing (TDD, Red-Green-Refactor)
- Code standards (naming, structure, comments)

### ✅ Design Foundation
- Color theory & harmony
- Typography scales
- Spacing system
- Shadow elevation
- Responsive layouts
- Accessibility (WCAG 2.1 AA)
- Box thinking framework

### ✅ Implementation Logic
- Agent retry & escalation
- TDD classification
- Progress tracking (flags.json)
- Agent routing rules

### ✅ Workflow Templates
- OpenSpec multi-agent workflow
- Phase templates (MVT → Complexity → Scale → Deploy)
- Validation gates

---

## 🤝 Contributing

This is an open-source project! Contributions welcome:

- Report bugs via [GitHub Issues](https://github.com/ChampPABA/claude-multi-agent-template/issues)
- Submit feature requests
- Send pull requests

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Credits

Built with:
- [Claude Code](https://claude.com/claude-code) - AI-powered coding assistant
- [Context7 MCP](https://context7.com) - Always up-to-date library documentation

---

## 🔗 Links

- **npm Package:** https://www.npmjs.com/package/@champpaba/claude-agent-kit
- **GitHub Repository:** https://github.com/ChampPABA/claude-multi-agent-template
- **Issues & Support:** https://github.com/ChampPABA/claude-multi-agent-template/issues

---

## 💡 Tips

1. **Always use `--backup` when updating:**
   ```bash
   cak update --backup
   ```

2. **Set up Context7 MCP for best results:**
   - Agents get latest framework docs
   - No manual docs updates needed

3. **Use `/psetup` after init:**
   - Auto-detects your tech stack
   - Creates project-specific context

4. **Read `.claude/CLAUDE.md` for navigation:**
   - Comprehensive guide to all features
   - Links to all contexts and patterns

---

**Ready to supercharge your development?** 🚀

```bash
npm install -g @champpaba/claude-agent-kit
cd your-project
cak init
/psetup
```

Let AI agents handle the implementation while you focus on the big picture!
