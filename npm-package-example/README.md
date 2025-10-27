# Create Claude Agent

> Universal multi-agent template for Claude Code with orchestrator and specialist agents

## 🚀 Quick Start

```bash
npx create-claude-agent
```

This will install the template into your current directory's `.claude/` folder.

## 📦 What's Included?

### Agents (6 specialized agents)
- **Orchestrator** (Sonnet 4.5) - Coordinates tasks and delegates to specialists
- **UX-UI Frontend** (Haiku 4.5) - Builds UI components with mock data
- **Test-Debug** (Haiku 4.5) - Automated testing with max 3-4 iteration loops
- **Frontend** (Haiku 4.5) - Connects components to APIs
- **Backend** (Haiku 4.5) - API endpoints with validation
- **Database** (Haiku 4.5) - Schema design and migrations

### Universal Patterns
- Logging, Testing, Error Handling
- Development Principles (SOLID, KISS, YAGNI)
- Code Standards
- Task Breakdown
- Frontend Component Strategy
- UI Component Consistency
- Git Workflow

### Design System Foundation
- Color Theory
- Spacing System
- Shadows & Elevation
- Typography Hierarchy
- Layout Patterns
- Responsive Behavior
- Box Thinking Framework
- Accessibility (WCAG)

## 🎯 Usage

### 1. Install Template
```bash
npx create-claude-agent
```

### 2. Create tasks.md
```markdown
# Feature: User Authentication

## Tech Stack
- Frontend: Next.js 15
- Backend: FastAPI
- Database: PostgreSQL + Prisma

## Tasks
### Phase 1: UX-UI (MVT)
- Task 1.1: Create login form
- Task 1.2: Test with Chrome DevTools
- Task 1.3: Human approval

### Phase 2: Frontend
- Task 2.1: Connect to API
...
```

### 3. Run Orchestrator
In Claude Code, type:
```
/agents orchestrator
```

The orchestrator will:
1. Read tasks.md
2. Detect tech stack
3. Delegate tasks to specialist agents
4. Wait for human approval at Task 1.3
5. Coordinate parallel execution for Phase 2+

## 🤖 Agent Workflow

```
Phase 1 (Sequential):
1.1 UX-UI Agent → Create component + mock data
1.2 Test Agent → Auto-test + fix (max 3-4 loops)
1.3 Human → MUST approve before proceeding

Phase 2+ (Parallel):
2.x Frontend Agent → Connect to APIs
3.x Backend Agent → Build endpoints
4.x Database Agent → Schema + migrations
```

## 📖 Documentation

After installation, read:
```bash
cat .claude/CLAUDE.md
```

## 🔧 Tech Stack Support

### Frontend
- Next.js (App Router, Server Components)
- React (Hooks, Context)
- Vue (Composition API)

### Backend
- FastAPI (Python)
- Express (Node.js)
- Next.js API Routes

### Database
- Prisma (PostgreSQL, MySQL, SQLite)
- SQLAlchemy (PostgreSQL, MySQL)
- TypeORM (PostgreSQL, MySQL)

### Testing
- Vitest, Jest, Playwright
- Pytest (Python)
- Chrome DevTools MCP Integration

## 🌟 Features

- ✅ Framework-agnostic (works with any stack)
- ✅ Context7 MCP integration (dynamic doc loading)
- ✅ Chrome DevTools MCP support
- ✅ Human approval workflow
- ✅ Parallel execution optimization
- ✅ Test loop with escalation
- ✅ Reusable across all projects

## 📝 License

MIT

## 🙏 Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md)

## 🔗 Links

- [GitHub Repository](https://github.com/yourusername/create-claude-agent)
- [Documentation](https://github.com/yourusername/create-claude-agent/wiki)
- [Issue Tracker](https://github.com/yourusername/create-claude-agent/issues)
