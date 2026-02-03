# Development Principles

**Core Philosophy:** Build software that is simple, maintainable, observable, and resilient.

---

## KISS (Keep It Simple, Stupid)

Simplicity should be a key goal in design. Choose straightforward solutions over complex ones.

### Examples

**❌ Complex:**
```typescript
// Over-engineered abstraction
class UserRepositoryFactory {
  createRepository(type: 'sql' | 'nosql') {
    return type === 'sql'
      ? new SQLUserRepository(new DatabaseConnection())
      : new NoSQLUserRepository(new MongoConnection())
  }
}
```

**✅ Simple:**
```typescript
// Direct, readable
import { prisma } from '@/lib/db'

export async function getUser(id: string) {
  return prisma.user.findUnique({ where: { id } })
}
```

---

## YAGNI (You Aren't Gonna Need It)

Avoid building functionality on speculation. Implement features only when needed.

### When to Apply

**❌ Don't Build:**
- "We might need this someday"
- Premature optimization
- Unused abstractions
- Speculative features

**✅ Build Only:**
- Features with clear requirements
- Immediate user needs
- Proven performance bottlenecks

### Example

```typescript
// ❌ YAGNI Violation - Building for future maybe-needs
interface User {
  id: string
  email: string
  name: string
  preferences?: UserPreferences // Not needed yet
  settings?: UserSettings       // Not needed yet
  metadata?: Record<string, unknown> // "Just in case"
}

// ✅ YAGNI Compliant - Build what you need now
interface User {
  id: string
  email: string
  name: string
}
// Add fields when requirements are clear
```

---

## SOLID Principles

### 1. Single Responsibility Principle (SRP)

Each module/class/function should have ONE reason to change.

**❌ Violates SRP:**
```typescript
class UserService {
  createUser(data: UserData) { /* ... */ }
  sendWelcomeEmail(user: User) { /* ... */ }
  logActivity(action: string) { /* ... */ }
  validateEmail(email: string) { /* ... */ }
}
```

**✅ Follows SRP:**
```typescript
// lib/services/user-service.ts
class UserService {
  createUser(data: UserData) { /* ... */ }
}

// lib/services/email-service.ts
class EmailService {
  sendWelcomeEmail(user: User) { /* ... */ }
}

// lib/logger.ts
export const logger = { /* ... */ }

// lib/validators.ts
export function validateEmail(email: string) { /* ... */ }
```

---

### 2. Open/Closed Principle (OCP)

Software entities should be **open for extension** but **closed for modification**.

**❌ Violates OCP:**
```typescript
function calculateDiscount(user: User, order: Order) {
  if (user.type === 'regular') {
    return order.total * 0.05
  } else if (user.type === 'premium') {
    return order.total * 0.10
  } else if (user.type === 'vip') {
    return order.total * 0.20
  }
  // Adding new user types requires modifying this function
}
```

**✅ Follows OCP:**
```typescript
interface DiscountStrategy {
  calculate(order: Order): number
}

class RegularDiscount implements DiscountStrategy {
  calculate(order: Order) { return order.total * 0.05 }
}

class PremiumDiscount implements DiscountStrategy {
  calculate(order: Order) { return order.total * 0.10 }
}

class VIPDiscount implements DiscountStrategy {
  calculate(order: Order) { return order.total * 0.20 }
}

// Adding new discount types = create new class (no modification needed)
function calculateDiscount(strategy: DiscountStrategy, order: Order) {
  return strategy.calculate(order)
}
```

---

### 3. Liskov Substitution Principle (LSP)

Subtypes must be substitutable for their base types without altering correctness.

**❌ Violates LSP:**
```typescript
class Bird {
  fly() { console.log('Flying') }
}

class Penguin extends Bird {
  fly() { throw new Error('Penguins cannot fly') } // Breaks substitution
}
```

**✅ Follows LSP:**
```typescript
interface Bird {
  move(): void
}

class FlyingBird implements Bird {
  move() { console.log('Flying') }
}

class Penguin implements Bird {
  move() { console.log('Swimming') }
}
```

---

### 4. Interface Segregation Principle (ISP)

Clients should not depend on interfaces they don't use.

**❌ Violates ISP:**
```typescript
interface Worker {
  work(): void
  eat(): void
  sleep(): void
}

class Robot implements Worker {
  work() { /* ... */ }
  eat() { throw new Error('Robots do not eat') } // Forced to implement
  sleep() { throw new Error('Robots do not sleep') } // Forced to implement
}
```

**✅ Follows ISP:**
```typescript
interface Workable {
  work(): void
}

interface Eatable {
  eat(): void
}

interface Sleepable {
  sleep(): void
}

class Human implements Workable, Eatable, Sleepable {
  work() { /* ... */ }
  eat() { /* ... */ }
  sleep() { /* ... */ }
}

class Robot implements Workable {
  work() { /* ... */ }
}
```

---

### 5. Dependency Inversion Principle (DIP)

High-level modules should not depend on low-level modules. Both should depend on abstractions.

**❌ Violates DIP:**
```typescript
class MySQLDatabase {
  query(sql: string) { /* ... */ }
}

class UserService {
  private db = new MySQLDatabase() // Direct dependency on low-level module

  getUser(id: string) {
    return this.db.query(`SELECT * FROM users WHERE id = ${id}`)
  }
}
```

**✅ Follows DIP:**
```typescript
interface Database {
  query(sql: string): Promise<unknown>
}

class MySQLDatabase implements Database {
  query(sql: string) { /* ... */ }
}

class PostgreSQLDatabase implements Database {
  query(sql: string) { /* ... */ }
}

class UserService {
  constructor(private db: Database) {} // Depends on abstraction

  getUser(id: string) {
    return this.db.query(`SELECT * FROM users WHERE id = ${id}`)
  }
}

// Usage
const userService = new UserService(new MySQLDatabase())
// Easy to swap: new UserService(new PostgreSQLDatabase())
```

---

## Fail Fast

Detect errors early and raise exceptions immediately when issues occur.

### When to Fail Fast

**✅ Fail immediately on:**
- Invalid input
- Missing required configuration
- Broken dependencies
- Database connection failures
- Authentication failures

**❌ Don't fail fast on:**
- Transient network errors (retry instead)
- User input errors (validate gracefully)
- Optional features

### Examples

**❌ Silent Failure:**
```typescript
function divide(a: number, b: number) {
  if (b === 0) {
    return 0 // Silent failure - wrong!
  }
  return a / b
}
```

**✅ Fail Fast:**
```typescript
function divide(a: number, b: number) {
  if (b === 0) {
    throw new Error('Division by zero') // Immediate failure
  }
  return a / b
}
```

**✅ Fail Fast with Validation:**
```typescript
import { z } from 'zod'

const userSchema = z.object({
  email: z.string().email(),
  age: z.number().min(18)
})

export async function createUser(data: unknown) {
  // Fail fast if data is invalid
  const validated = userSchema.parse(data) // Throws on invalid input

  // Continue with valid data
  return prisma.user.create({ data: validated })
}
```

---

## Observability First

Every significant action must be observable through logging.

**Critical Rule:** If an action happens without logs, it's invisible in production.

### What to Log

| Event Type | Log Level |
|------------|-----------|
| API Route Entry/Exit | INFO |
| Database Operations | INFO |
| External API Calls | INFO |
| User Actions | INFO |
| Errors & Exceptions | ERROR |
| State Changes | DEBUG |

**See `patterns/logging.md` for complete patterns.**

---

## DRY (Don't Repeat Yourself)

Every piece of knowledge should have a single, authoritative representation.

**❌ Violates DRY:**
```typescript
// File 1
const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB

// File 2
const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB (duplicate!)

// File 3
if (file.size > 5 * 1024 * 1024) { /* ... */ } // Hardcoded (duplicate!)
```

**✅ Follows DRY:**
```typescript
// lib/constants.ts
export const MAX_FILE_SIZE = 5 * 1024 * 1024 // Single source of truth

// File 1
import { MAX_FILE_SIZE } from '@/lib/constants'

// File 2
import { MAX_FILE_SIZE } from '@/lib/constants'

// File 3
import { MAX_FILE_SIZE } from '@/lib/constants'
if (file.size > MAX_FILE_SIZE) { /* ... */ }
```

---

## Separation of Concerns

Different concerns should be handled by different modules.

**Example: Next.js API Route**

**❌ Mixed Concerns:**
```typescript
export async function POST(request: NextRequest) {
  const body = await request.json()

  // Validation mixed with business logic
  if (!body.email || !body.email.includes('@')) {
    return NextResponse.json({ error: 'Invalid email' }, { status: 400 })
  }

  // Database logic mixed with API logic
  const user = await prisma.user.create({
    data: { email: body.email, name: body.name }
  })

  // Email sending mixed with everything else
  await fetch('https://api.sendgrid.com/send', {
    method: 'POST',
    body: JSON.stringify({ to: user.email, subject: 'Welcome' })
  })

  return NextResponse.json(user)
}
```

**✅ Separated Concerns:**
```typescript
// app/api/users/route.ts (API Layer)
export async function POST(request: NextRequest) {
  const body = await request.json()
  const validated = validateUserInput(body) // Validation layer
  const user = await userService.createUser(validated) // Business layer
  await emailService.sendWelcome(user) // Email layer
  return NextResponse.json(user)
}

// lib/validators/user.ts (Validation Layer)
export function validateUserInput(data: unknown) {
  return userSchema.parse(data)
}

// lib/services/user-service.ts (Business Layer)
export const userService = {
  async createUser(data: ValidatedUserData) {
    return prisma.user.create({ data })
  }
}

// lib/services/email-service.ts (Email Layer)
export const emailService = {
  async sendWelcome(user: User) {
    await sendEmail({ to: user.email, subject: 'Welcome' })
  }
}
```

---

## Principle of Least Surprise

Code should behave in a way that minimizes surprise for other developers.

**❌ Surprising:**
```typescript
// Function name suggests it only reads, but it also writes
function getUser(id: string) {
  const user = db.findUser(id)
  db.updateLastAccessed(id) // Surprise! Side effect!
  return user
}
```

**✅ Expected:**
```typescript
// Clear function names, no surprises
function getUser(id: string) {
  return db.findUser(id)
}

function getUserAndUpdateAccess(id: string) {
  const user = db.findUser(id)
  db.updateLastAccessed(id) // Expected from function name
  return user
}
```

---

## Quick Reference

| Principle | Summary |
|-----------|---------|
| **KISS** | Choose simple solutions over complex ones |
| **YAGNI** | Build only what you need now |
| **SRP** | One responsibility per module |
| **OCP** | Open for extension, closed for modification |
| **LSP** | Subtypes must be substitutable |
| **ISP** | Don't force clients to depend on unused methods |
| **DIP** | Depend on abstractions, not concretions |
| **Fail Fast** | Detect and raise errors immediately |
| **Observability** | Log everything that matters |
| **DRY** | Single source of truth for all knowledge |
| **Separation** | Different concerns in different modules |
| **Least Surprise** | Code should behave as expected |

---

**💡 Remember:** Good principles lead to maintainable code!
