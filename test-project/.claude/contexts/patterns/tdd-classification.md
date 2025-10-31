# Universal Task Classification

## Purpose

Classify tasks to determine if Test-Driven Development (TDD) is required, regardless of task source (file, command, spec framework, etc.).

---

## Classification Output

**Input:** Task description (string)
**Output:** Classification object

```typescript
{
  type: 'critical' | 'standard' | 'ui' | 'ui-complex' | 'config',
  tdd_required: boolean,
  workflow: 'red-green-refactor' | 'test-alongside',
  reason: string
}
```

---

## Critical Code Patterns (TDD Required ✅)

### 1. API Mutations
- POST, PUT, PATCH, DELETE methods
- Any `/api/` endpoint that modifies data
- GraphQL mutations
- Webhook handlers, callbacks

**Examples:**
```
✅ "Implement POST /api/auth/login"
✅ "Add PUT /api/users/:id/profile"
✅ "Create webhook handler for Stripe payments"
✅ "Delete endpoint for products"
```

### 2. Business Logic
- Calculations, computations, algorithms
- Validation rules, verification logic
- Transformations, conversions, parsing
- Domain-specific logic

**Keywords:** calculate, compute, algorithm, validate, verify, check, transform, convert, parse

**Business domains:** discount, pricing, payment, commission, fee, tax, shipping, score, rate, evaluate

**Examples:**
```
✅ "Calculate shipping cost based on weight and distance"
✅ "Add discount calculation for VIP users"
✅ "Implement tax calculation logic"
✅ "Validate credit card numbers using Luhn algorithm"
✅ "Transform user data for export"
```

### 3. External Integrations
- Third-party APIs, webhooks, callbacks
- Payment gateways
- Email/SMS services
- Cloud storage providers
- Analytics platforms
- Authentication providers

**Payment providers:** Stripe, PayPal, Square, Braintree, Adyen, Razorpay
**Email services:** SendGrid, Mailgun, Postmark, AWS SES, Mailchimp
**SMS providers:** Twilio, Vonage, MessageBird, AWS SNS
**Storage:** S3, GCS, Azure Storage, Cloudinary, DigitalOcean Spaces
**Analytics:** Google Analytics, Mixpanel, Amplitude, Segment
**Auth:** Auth0, Firebase Auth, Cognito, Okta

**Examples:**
```
✅ "Integrate Stripe payment processing"
✅ "Add SendGrid email notifications"
✅ "Implement Twilio SMS verification"
✅ "Connect to Google Analytics API"
✅ "Upload images to S3"
```

### 4. Data Transformations
- Serialization, deserialization
- ETL operations, data pipelines
- Complex mapping, aggregations
- Data normalization/denormalization

**Keywords:** serialize, deserialize, transform, convert, parse, ETL, pipeline, aggregate, map, reduce, filter (complex), normalize, denormalize

**Examples:**
```
✅ "Parse CSV and transform to JSON"
✅ "Aggregate user analytics data"
✅ "Serialize user data for API response"
✅ "ETL pipeline for data migration"
```

### 5. Security & Critical Operations
- Authentication, authorization
- Encryption, decryption, hashing, signing
- Permissions, access control
- Transactions, financial operations
- Audit logging

**Keywords:** auth, authenticate, authorize, JWT, OAuth, encrypt, decrypt, hash, sign, permission, access control, transaction, rollback, commit, audit

**Examples:**
```
✅ "Implement JWT authentication"
✅ "Add password hashing with bcrypt"
✅ "Create payment transaction handler"
✅ "Implement role-based access control"
✅ "Add audit log for sensitive operations"
```

---

## Standard Code Patterns (Test-Alongside OK ⚠️)

- Simple GET endpoints (read-only)
- Basic list/show/display operations
- Simple data fetching (no transformations)
- Configuration, setup, initialization

**Examples:**
```
⚠️ "Add GET /api/users endpoint"
⚠️ "Fetch user profile data"
⚠️ "Display product list"
⚠️ "Setup environment configuration"
```

---

## UI Code Patterns (Usually No TDD ❌)

- Presentational components (Button, Card, Modal, etc.)
- Styling, themes, CSS
- Simple renders, displays
- Layout components

**Keywords:** component, button, card, modal, navbar, footer, style, CSS, theme, render, display, layout

**Examples:**
```
❌ "Create Button component"
❌ "Add Card component with shadow"
❌ "Style navigation bar"
❌ "Update footer layout"
```

### Exception: Complex UI Logic (TDD Required ✅)

**UI tasks that DO require TDD:**
- Multi-step forms with validation
- State machines (wizards, checkout flows)
- Complex form validation logic
- Accessibility features (keyboard navigation, screen reader support)
- Dynamic form generation

**Keywords:** multi-step, wizard, state machine, validation (complex), keyboard navigation, accessibility, ARIA, dynamic form

**Examples:**
```
✅ "Implement multi-step checkout wizard with validation"
✅ "Add keyboard navigation for dropdown menu"
✅ "Create dynamic form with conditional fields"
✅ "Build wizard with state management"
```

---

## Pattern Matching Algorithm

```typescript
const CRITICAL_PATTERNS = [
  // HTTP mutations
  /\b(post|put|patch|delete)\b.*\/api\//i,

  // Business logic
  /\b(calculate|compute|algorithm|validate|verify|check)\b/i,
  /\b(discount|pricing|payment|commission|fee|tax|shipping)\b/i,
  /\b(score|rate|evaluate|transform|convert|parse)\b/i,

  // External services (extensible)
  /\b(integrate|webhook|callback|third-party|external)\b/i,

  // Payment providers
  /\b(stripe|paypal|square|braintree|adyen|razorpay)\b/i,

  // Communication services
  /\b(sendgrid|mailgun|postmark|ses|mailchimp)\b/i,
  /\b(twilio|vonage|messagebird|sns)\b/i,

  // Storage providers
  /\b(s3|gcs|azure.*storage|cloudinary|digitalocean.*spaces)\b/i,

  // Analytics
  /\b(analytics|mixpanel|amplitude|segment)\b/i,

  // Auth providers
  /\b(auth0|firebase.*auth|cognito|okta)\b/i,

  // Data operations
  /\b(serialize|deserialize|etl|pipeline|aggregate)\b/i,

  // Security
  /\b(auth|jwt|oauth|encrypt|decrypt|hash|sign)\b/i,
  /\b(permission|access.*control|authorize)\b/i,

  // Transactions
  /\b(transaction|rollback|commit|audit)\b/i,
]

function classifyTask(description: string): Classification {
  const text = description.toLowerCase()

  // Check critical patterns
  for (const pattern of CRITICAL_PATTERNS) {
    if (pattern.test(text)) {
      return {
        type: 'critical',
        tdd_required: true,
        workflow: 'red-green-refactor',
        reason: `Matched critical pattern: ${pattern.source}`
      }
    }
  }

  // Check simple GET (read-only)
  if (/^get\s+\/api\//i.test(text) && !/\b(complex|join|aggregate|transform)\b/i.test(text)) {
    return {
      type: 'standard',
      tdd_required: false,
      workflow: 'test-alongside',
      reason: 'Simple read-only operation'
    }
  }

  // Check UI
  if (/\b(component|button|card|modal|navbar|footer|style|theme|css|layout)\b/i.test(text)) {
    // Check for complex UI logic
    if (/\b(multi-step|wizard|state.*machine|keyboard.*navigation|accessibility|aria|dynamic.*form)\b/i.test(text)) {
      return {
        type: 'ui-complex',
        tdd_required: true,
        workflow: 'red-green-refactor',
        reason: 'Complex UI logic detected'
      }
    }

    return {
      type: 'ui',
      tdd_required: false,
      workflow: 'test-alongside',
      reason: 'Presentational UI component'
    }
  }

  // Check config/setup
  if (/\b(config|setup|init|install|env)\b/i.test(text)) {
    return {
      type: 'config',
      tdd_required: false,
      workflow: 'test-alongside',
      reason: 'Configuration task'
    }
  }

  // Default: standard
  return {
    type: 'standard',
    tdd_required: false,
    workflow: 'test-alongside',
    reason: 'Default classification (no critical patterns matched)'
  }
}
```

---

## Classification Examples

| Task Description | Type | TDD? | Reason |
|-----------------|------|------|--------|
| "Implement POST /api/auth/login" | critical | ✅ YES | API mutation + authentication |
| "Add discount calculation for VIP users" | critical | ✅ YES | Business logic |
| "Integrate Stripe webhook handler" | critical | ✅ YES | External integration + webhook |
| "Parse CSV and transform to JSON" | critical | ✅ YES | Data transformation |
| "Add JWT authentication middleware" | critical | ✅ YES | Security operation |
| "Create multi-step checkout wizard" | ui-complex | ✅ YES | Complex UI state machine |
| "Implement keyboard navigation" | ui-complex | ✅ YES | Accessibility feature |
| "Create GET /api/users list" | standard | ⚠️ Optional | Simple read-only |
| "Fetch user profile data" | standard | ⚠️ Optional | Simple fetch |
| "Create Button component" | ui | ❌ No | Presentational UI |
| "Style navigation bar" | ui | ❌ No | CSS/styling |
| "Setup environment variables" | config | ❌ No | Configuration |

---

## Usage by Orchestrator

```markdown
1. Receive task (from any source: file, command, framework)
2. Extract task description
3. Run classification algorithm
4. Add classification metadata to task
5. Delegate to specialist agent with metadata
```

**Example Orchestrator Code:**
```typescript
// 1. Receive tasks
const tasks = parseTasks(input)

// 2. Classify each task
for (const task of tasks) {
  const classification = classifyTask(task.description)

  task.type = classification.type
  task.tdd_required = classification.tdd_required
  task.workflow = classification.workflow
  task.reason = classification.reason
}

// 3. Delegate with metadata
for (const task of tasks) {
  delegateToAgent(task.agent, {
    description: task.description,
    type: task.type,
    tdd_required: task.tdd_required,
    workflow: task.workflow,
    reason: task.reason
  })
}
```

---

## Usage by Specialist Agents

```markdown
1. Receive task with classification metadata
2. Check `tdd_required` flag
3. If true → Red-Green-Refactor workflow
4. If false → Test-Alongside workflow
```

**Example Agent Code:**
```typescript
// Receive task from Orchestrator
const task = receiveTask()

if (task.tdd_required === true) {
  // TDD Workflow
  console.log(`⚠️ TDD Required: ${task.reason}`)

  // RED: Write test first
  writeTests()
  runTests() // Must FAIL

  // GREEN: Implement
  writeImplementation()
  runTests() // Must PASS

  // REFACTOR: Improve
  refactorCode()
  runTests() // Must STILL PASS

} else {
  // Standard Workflow
  console.log(`ℹ️ Test-Alongside OK: ${task.reason}`)

  writeImplementation()
  writeTests()
  runTests()
}
```

---

## Extending the Classification

### Adding New Service Providers

**To support new payment provider (e.g., Payoneer):**
```typescript
// Before
/\b(stripe|paypal|square|braintree|adyen|razorpay)\b/i

// After
/\b(stripe|paypal|square|braintree|adyen|razorpay|payoneer)\b/i
```

### Adding New Critical Keywords

**To add new business domain (e.g., inventory):**
```typescript
// Add to business logic patterns
/\b(discount|pricing|payment|commission|fee|tax|shipping|inventory|stock)\b/i
```

### Adding New Pattern Categories

```typescript
// Example: Add AI/ML operations as critical
const AI_ML_PATTERNS = [
  /\b(train.*model|inference|prediction|openai|anthropic)\b/i,
]

CRITICAL_PATTERNS.push(...AI_ML_PATTERNS)
```

---

## Testing Classification

```typescript
const testCases = [
  // Critical - API
  {
    input: "Implement POST /api/auth/login",
    expected: { type: 'critical', tdd_required: true }
  },

  // Critical - Business logic
  {
    input: "Add discount calculation for VIP members",
    expected: { type: 'critical', tdd_required: true }
  },

  // Critical - External integration
  {
    input: "Integrate Stripe payment processing",
    expected: { type: 'critical', tdd_required: true }
  },

  // Critical - Data transformation
  {
    input: "Parse XML and convert to JSON",
    expected: { type: 'critical', tdd_required: true }
  },

  // Standard
  {
    input: "Create GET /api/users endpoint",
    expected: { type: 'standard', tdd_required: false }
  },

  // UI - Presentational
  {
    input: "Add Button component",
    expected: { type: 'ui', tdd_required: false }
  },

  // UI - Complex
  {
    input: "Build multi-step checkout wizard",
    expected: { type: 'ui-complex', tdd_required: true }
  },
]

// Run tests
for (const test of testCases) {
  const result = classifyTask(test.input)

  console.assert(
    result.type === test.expected.type &&
    result.tdd_required === test.expected.tdd_required,
    `Failed: ${test.input}`
  )
}
```

---

## Troubleshooting

### Task Classified Incorrectly

**Problem:** Simple task marked as critical
**Solution:** Check if task description contains critical keywords unintentionally

**Example:**
```
Task: "Display payment history"
→ Wrongly classified as critical (contains "payment")
→ Fix: Add context check "display" + "payment" → standard
```

### Missing Pattern

**Problem:** Critical task not detected
**Solution:** Add new pattern to CRITICAL_PATTERNS

**Example:**
```
Task: "Implement Razorpay integration"
→ Not detected (Razorpay not in list)
→ Fix: Add "razorpay" to payment providers pattern
```

---

## Summary

**Key Principles:**
1. ✅ **Content-based:** Classification based on task description only
2. ✅ **Source-agnostic:** Works with any task source
3. ✅ **Extensible:** Easy to add new patterns
4. ✅ **Explicit:** Clear reason for each classification
5. ✅ **Conservative:** Default to standard if unclear

**Remember:** When in doubt about classification, prefer `tdd_required: false` and let the specialist agent decide if TDD is needed.
