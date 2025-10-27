# Claude Multi-Agent Template

> Reusable multi-agent system for spec-driven development with automatic Context7 integration.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 What is this?

A **production-ready template** for building software with AI agents that:

- ✅ **Coordinate complex tasks** - Orchestrator delegates to specialists
- ✅ **Always up-to-date** - Uses Context7 MCP for latest framework docs
- ✅ **Zero maintenance** - No tech stack docs to update (Context7 handles it)
- ✅ **Reusable** - Works for Next.js, FastAPI, Vue, Django, or any stack
- ✅ **Incremental** - 4-phase methodology (MVT → Complexity → Scale → Deploy)

---

## 🚀 Quick Start

### มาถึงปุ๊บ ต้องทำอะไร? (Step-by-Step)

#### 📥 Step 1: Clone Template (1 นาที)

```bash
# Clone template มา
git clone https://github.com/anongecko/claude-multi-agent-template.git my-project
cd my-project

# ลบ .git เดิม แล้วสร้างใหม่
rm -rf .git
git init
git add .
git commit -m "Initial commit from template"
```

---

#### 🔌 Step 2: Setup Context7 MCP (2 นาที)

**ทำไมต้องมี?** ให้ AI หา docs ล่าสุดของ framework ให้เอง (Next.js, FastAPI, Vue, etc.)

**วิธีติดตั้ง:**

1. เปิด Claude Code Settings → MCP Servers
2. เพิ่ม config นี้:

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
4. เช็คว่าใช้งานได้: พิมพ์ `/mcp` ดู list → ต้องมี `context7`

---

#### 🎨 Step 3: (Optional) กำหนดสี Design Tokens (5 นาที)

ถ้าโปรเจคมีสีเฉพาะ เช่น brand colors:

```bash
mkdir -p .claude/contexts/domain/myproject
```

สร้างไฟล์ `.claude/contexts/domain/myproject/design-tokens.md`:

```markdown
# MyProject Design Tokens

## Brand Colors
- Primary: `rgb(255, 87, 34)` (Orange - Energy, Innovation)
- Secondary: `rgb(33, 150, 243)` (Blue - Trust, Stability)
- Accent: `rgb(76, 175, 80)` (Green - Success)

## Usage
- Primary: CTA buttons, links, brand elements
- Secondary: Headers, navigation
- Accent: Success messages, completed states
```

**หมายเหตุ:** ถ้าไม่กำหนดเอง AI จะใช้ design foundation จาก `.claude/contexts/design/` (สีทั่วไป)

---

#### 🏗️ Step 4: เริ่มทำงาน - เลือก 1 ใน 2 วิธี

### **วิธีที่ 1: สั่งตรงๆ (Simple, Ad-hoc)**

```bash
# เปิด Orchestrator
/agents orchestrator

# สั่งงาน
"สร้าง login form ใช้ Next.js + Prisma"
```

**Orchestrator จะ:**
1. ตรวจสอบ tech stack ในโปรเจค (อ่าน `package.json` หรือ `requirements.txt`)
2. ค้น Context7 หา docs (Next.js 15, Prisma 6)
3. มอบหมายงานให้ agents:
   - **UX-UI Frontend**: สร้าง form + mock data
   - **Test-Debug**: เขียน tests
   - **Frontend**: ต่อ API
   - **Backend**: สร้าง POST /api/auth/login
   - **Database**: สร้าง User model

---

### **วิธีที่ 2: ใช้ tasks.md (Structured, Complex Projects)**

สร้างไฟล์ `tasks.md`:

```markdown
# Feature: User Authentication

## Tech Stack
- Frontend: Next.js 15 App Router
- Backend: Next.js API Routes
- Database: Prisma + PostgreSQL
- Testing: Vitest

---

## Phase 1: MVT (Minimum Viable Test)
**Goal:** 1 user สามารถ login ได้

### Task 1.1: Create Login Form (UX-UI Frontend Agent)
- Email input (required, type=email)
- Password input (required, minLength=8)
- Submit button
- Mock data: `{ email: 'test@example.com', password: 'password123' }`

### Task 1.2: Write Unit Tests (Test-Debug Agent)
- Test form validation (empty fields, invalid email)
- Test mock login flow

### Task 1.3: Human Approval ✋
**STOP** - User tests manually, approves before Phase 2

---

## Phase 2: Complexity (Add Real API)
**Goal:** Connect form to real backend

### Task 2.1: Create Login API (Backend Agent)
- POST /api/auth/login
- Validate email + password with Zod
- Return 200 + JWT token OR 401 error

### Task 2.2: Connect Form to API (Frontend Agent)
- Replace mock data with fetch('/api/auth/login')
- Handle loading state
- Handle error messages

### Task 2.3: Add State Management (Frontend Agent)
- Zustand store for auth state
- Store JWT token in localStorage
- Add logout action

---

## Phase 3: Scale (Full Auth Flow)

### Task 3.1: Database Schema (Database Agent)
```prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  password  String   // bcrypt hash
  name      String?
  createdAt DateTime @default(now())
}
```

### Task 3.2: Password Hashing (Backend Agent)
- Install bcrypt
- Hash password before saving
- Compare hash during login

### Task 3.3: JWT Generation (Backend Agent)
- Install jsonwebtoken
- Generate token with user.id payload
- Set expiry (7 days)

### Task 3.4: Protected Routes (Frontend Agent)
- Create middleware to check JWT
- Redirect to /login if not authenticated

---

## Phase 4: Deploy (Production Ready)

### Task 4.1: Error Handling (Backend Agent)
- Add try-catch to all API routes
- Return proper HTTP status codes
- Log all errors with logger.error()

### Task 4.2: Integration Tests (Test-Debug Agent)
- Test complete login flow (form → API → database)
- Test error cases (wrong password, user not found)

### Task 4.3: Security Review (Backend Agent)
- Add rate limiting (max 5 login attempts/minute)
- Add CORS configuration
- Add input sanitization

### Task 4.4: Documentation (Orchestrator)
- API documentation (endpoints, request/response)
- Setup instructions (environment variables)
```

**วิธีใช้:**

```bash
/agents orchestrator
"Execute tasks.md"
```

**Orchestrator จะ:**
1. อ่าน tasks.md ทั้งหมด
2. ตรวจสอบ tech stack (Next.js 15, Prisma)
3. ดึง docs จาก Context7
4. ทำงาน Phase 1 → รอ approval → Phase 2 → Phase 3 → Phase 4
5. หยุดรอที่ "Human Approval ✋" (Task 1.3, 2.3, etc.)

---

#### 🔄 Step 5: ใช้งานต่อเนื่อง

**เพิ่ม Feature ใหม่:**
```bash
/agents orchestrator
"สร้าง user profile page - ให้แก้ไขชื่อ/อีเมลได้"
```

**แก้ Bug:**
```bash
/agents test-debug
"Login form ไม่แสดง error message เมื่อ password ผิด"
```

**Refactor Code:**
```bash
/agents backend
"Refactor /api/auth/login - แยก validation logic ออกมา"
```

---

#### 📚 Step 6: เรียนรู้เพิ่มเติม

**อ่าน navigation guide:**
```bash
cat .claude/CLAUDE.md
```

**ดู agent ทั้งหมด:**
```bash
ls .claude/agents/
```

**ดู universal patterns:**
```bash
ls .claude/contexts/patterns/
# - logging.md (structured JSON logging)
# - testing.md (TDD, Red-Green-Refactor)
# - error-handling.md (try-catch, retry, circuit breaker)
# - task-breakdown.md (4-phase methodology)
```

**ดู design foundation:**
```bash
ls .claude/contexts/design/
# - box-thinking.md (layout analysis framework)
# - accessibility.md (WCAG 2.1 AA compliance)
# - color-theory.md, typography.md, spacing.md, etc.
```

---

## 🤖 Agents

### **Orchestrator** (Sonnet 4.5)
Coordinates multi-step tasks, detects tech stack, delegates to specialists.

### **UX-UI Frontend** (Haiku 4.5)
Creates components with mock data, follows design foundation.

### **Test-Debug** (Haiku 4.5)
Runs tests, fixes bugs automatically (max 3-4 iterations, then escalates).

### **Frontend** (Haiku 4.5)
Connects components to real APIs, implements state management.

### **Backend** (Haiku 4.5)
Builds API endpoints with validation (FastAPI, Express, Next.js API Routes).

### **Database** (Haiku 4.5)
Designs schemas, writes migrations (Prisma, SQLAlchemy, TypeORM).

---

## 📁 Structure

```
.claude/
├── CLAUDE.md                    # Navigation guide
├── agents/                      # 6 agents (Orchestrator + 5 specialists)
│   ├── 01-orchestrator.md
│   ├── 02-uxui-frontend.md
│   ├── 03-test-debug.md
│   ├── 04-frontend.md
│   ├── 05-backend.md
│   └── 06-database.md
│
└── contexts/
    ├── patterns/                # Universal patterns (static)
    │   ├── logging.md
    │   ├── testing.md
    │   ├── error-handling.md
    │   ├── task-breakdown.md
    │   ├── development-principles.md
    │   ├── code-standards.md
    │   # REMOVED - Use Context7 MCP instead
    │   # REMOVED - Use Context7 MCP instead
    │   # REMOVED - Optional (OpenSpec, BMAD, SpecKit)
    │
    ├── design/                  # Design foundation (static)
    │   ├── index.md
    │   ├── color-theory.md
    │   ├── typography.md
    │   ├── spacing.md
    │   ├── shadows.md
    │   ├── layout.md
    │   ├── responsive.md
    │   ├── box-thinking.md
    │   └── accessibility.md
    │
    └── domain/                  # Project-specific (you create)
        └── README.md
```

---

## 🎨 Design System

Template includes **universal design foundation**:

- **Color Theory** - Harmony, WCAG AAA contrast, shade generation
- **Typography** - Font scales, hierarchy, readability
- **Spacing** - 8px grid system
- **Shadows** - 4-level elevation system
- **Layout** - Grid, flexbox, responsive patterns
- **Accessibility** - ARIA, keyboard nav, screen readers

**Project-specific colors:** Define in `.claude/contexts/domain/{project}/design-tokens.md`

---

## 🧪 Testing Philosophy

### TDD for Critical Paths (Required)
- Business logic (calculations, transformations)
- API endpoints (validation, error handling)
- External service integrations
- Data transformations

### Test-Alongside for Simple Code
- CRUD operations
- UI components (presentational)
- Configuration files

**Test-Debug agent** runs tests automatically, fixes bugs (max 3-4 iterations).

---

## 📊 Logging & Observability

**Every significant action must be logged** (structured JSON):

```typescript
logger.info('api_route_entry', { route, method, requestId })
logger.info('db_operation_success', { operation, table, duration })
logger.error('api_route_error', { route, error, stack, requestId })
```

See: `.claude/contexts/patterns/logging.md`

---

## 🔧 Tech Stack Support

### Automatically Detected via Context7

**Frontend:**
- Next.js, React, Vue, Svelte, Angular

**Backend:**
- FastAPI, Express, NestJS, Django, Flask

**Database:**
- Prisma, SQLAlchemy, TypeORM, Drizzle

**Testing:**
- Vitest, Jest, Pytest, Playwright

Agents search Context7 MCP for latest docs automatically.

---

## 📖 Examples

### Example 1: Next.js + Prisma

```bash
# Your project
package.json: { "dependencies": { "next": "15.5.0", "@prisma/client": "6.5.0" } }

# Orchestrator detects:
Frontend = Next.js 15
Database = Prisma
→ Agents use Context7: Next.js App Router docs + Prisma docs
```

### Example 2: FastAPI + SQLAlchemy

```bash
# Your project
requirements.txt: fastapi, sqlalchemy

# Orchestrator detects:
Backend = FastAPI
Database = SQLAlchemy
→ Agents use Context7: FastAPI docs + SQLAlchemy docs
```

---

## 🎯 Customization

### Add Domain-Specific Context

```bash
mkdir -p .claude/contexts/domain/myproject
```

Example (E-commerce):
```markdown
<!-- .claude/contexts/domain/ecommerce/checkout-flow.md -->
# Checkout Flow

## Steps
1. Cart review
2. Shipping address
3. Payment method
4. Order confirmation

## Business Rules
- Free shipping > $50
- Tax calculation by state
- Inventory check before payment
```

Agents will load these patterns automatically.

---

## 🤝 Contributing

This is a template repo. Fork and customize for your needs!

**Improvements welcome:**
- Additional patterns (caching, rate limiting, etc.)
- More design foundation content
- Example projects
- Documentation improvements

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Credits

Built with:
- [Claude Code](https://claude.com/claude-code) - AI-powered coding assistant
- [Context7 MCP](https://context7.com) - Always up-to-date library documentation
- [OpenSpec](https://openspec.dev) - Spec-driven development framework (optional)

---

**Ready to build?** Clone this template and start creating! 🚀
