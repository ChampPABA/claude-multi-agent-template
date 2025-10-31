# Error Handling & Resilience Patterns

**Core Principles:**
1. **Fail Fast** - Detect errors early and raise exceptions immediately
2. **Log Everything** - Every error must be logged with context
3. **User-Friendly Messages** - Never expose technical details to users
4. **Graceful Degradation** - System should degrade gracefully, not crash
5. **Retry with Backoff** - Transient errors should be retried intelligently

---

## API Error Boundaries

### Next.js API Route Pattern

```typescript
// app/api/items/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'
import { Prisma } from '@prisma/client'
import { logger } from '@/lib/logger'

export async function POST(request: NextRequest) {
  const requestId = crypto.randomUUID()

  try {
    // 1. Parse and validate input
    const body = await request.json()
    const validated = schema.parse(body)

    // 2. Business logic
    const result = await createItem(validated)

    // 3. Log success
    logger.info('api_success', { requestId, route: '/api/items' })

    return NextResponse.json(result)

  } catch (error) {
    logger.error('api_error', {
      requestId,
      route: '/api/items',
      error: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined
    })

    return handleError(error, requestId)
  }
}

function handleError(error: unknown, requestId: string): NextResponse {
  // 1. Zod validation errors
  if (error instanceof z.ZodError) {
    return NextResponse.json(
      {
        error: 'Validation failed',
        details: error.flatten().fieldErrors,
        requestId
      },
      { status: 400 }
    )
  }

  // 2. Prisma database errors
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    // P2002: Unique constraint violation
    if (error.code === 'P2002') {
      return NextResponse.json(
        {
          error: 'Resource already exists',
          field: error.meta?.target,
          requestId
        },
        { status: 409 }
      )
    }

    // P2025: Record not found
    if (error.code === 'P2025') {
      return NextResponse.json(
        { error: 'Resource not found', requestId },
        { status: 404 }
      )
    }

    return NextResponse.json(
      { error: 'Database error', requestId },
      { status: 500 }
    )
  }

  // 3. Custom application errors
  if (error instanceof AppError) {
    return NextResponse.json(
      { error: error.message, code: error.code, requestId },
      { status: error.statusCode }
    )
  }

  // 4. Unknown errors
  return NextResponse.json(
    {
      error: 'Internal server error',
      message: process.env.NODE_ENV === 'development'
        ? (error as Error).message
        : undefined,
      requestId
    },
    { status: 500 }
  )
}
```

---

### FastAPI Error Handler

```python
# app/api/items.py
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import IntegrityError
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class CreateItemRequest(BaseModel):
    name: str
    price: float

@router.post("/items")
async def create_item(request: CreateItemRequest):
    request_id = str(uuid.uuid4())

    try:
        # Business logic
        item = await db.create_item(request.name, request.price)

        logger.info({"event": "api_success", "request_id": request_id})

        return {"id": item.id, "name": item.name, "price": item.price}

    except ValidationError as e:
        logger.warning({"event": "validation_error", "request_id": request_id, "errors": e.errors()})
        raise HTTPException(status_code=400, detail={"error": "Validation failed", "details": e.errors()})

    except IntegrityError as e:
        logger.error({"event": "db_integrity_error", "request_id": request_id})
        raise HTTPException(status_code=409, detail={"error": "Resource already exists"})

    except Exception as e:
        logger.error({"event": "api_error", "request_id": request_id, "error": str(e)})
        raise HTTPException(status_code=500, detail={"error": "Internal server error", "request_id": request_id})
```

---

## Custom Error Classes

### TypeScript

```typescript
// lib/errors.ts

export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number,
    public code?: string
  ) {
    super(message)
    this.name = 'AppError'
  }
}

export class ValidationError extends AppError {
  constructor(message: string, public field?: string) {
    super(message, 400, 'VALIDATION_ERROR')
    this.name = 'ValidationError'
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 404, 'NOT_FOUND')
    this.name = 'NotFoundError'
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED')
    this.name = 'UnauthorizedError'
  }
}

export class ExternalServiceError extends AppError {
  constructor(
    service: string,
    public originalError?: Error
  ) {
    super(`${service} service error`, 503, 'EXTERNAL_SERVICE_ERROR')
    this.name = 'ExternalServiceError'
  }
}

// Usage
throw new NotFoundError('User')
throw new ValidationError('Invalid email format', 'email')
throw new ExternalServiceError('PaymentGateway', originalError)
```

### Python

```python
# lib/errors.py

class AppError(Exception):
    def __init__(self, message: str, status_code: int, code: str = None):
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(self.message)

class ValidationError(AppError):
    def __init__(self, message: str, field: str = None):
        super().__init__(message, 400, "VALIDATION_ERROR")
        self.field = field

class NotFoundError(AppError):
    def __init__(self, resource: str):
        super().__init__(f"{resource} not found", 404, "NOT_FOUND")

class UnauthorizedError(AppError):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401, "UNAUTHORIZED")

class ExternalServiceError(AppError):
    def __init__(self, service: str, original_error: Exception = None):
        super().__init__(f"{service} service error", 503, "EXTERNAL_SERVICE_ERROR")
        self.original_error = original_error

# Usage
raise NotFoundError("User")
raise ValidationError("Invalid email format", field="email")
raise ExternalServiceError("PaymentGateway", original_error)
```

---

## Retry Logic with Exponential Backoff

```typescript
// lib/retry.ts
import { logger } from '@/lib/logger'

interface RetryOptions {
  maxRetries?: number
  initialDelayMs?: number
  maxDelayMs?: number
  exponentialBase?: number
  shouldRetry?: (error: Error) => boolean
}

export async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const {
    maxRetries = 3,
    initialDelayMs = 1000,
    maxDelayMs = 10000,
    exponentialBase = 2,
    shouldRetry = () => true
  } = options

  let lastError: Error

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      logger.info('retry_attempt', { attempt, maxRetries })
      return await fn()

    } catch (error) {
      lastError = error as Error

      if (!shouldRetry(lastError)) {
        logger.error('retry_non_retryable', { attempt, error: lastError.message })
        throw lastError
      }

      if (attempt === maxRetries) {
        logger.error('retry_exhausted', { attempt, maxRetries, error: lastError.message })
        throw lastError
      }

      const delay = Math.min(
        initialDelayMs * Math.pow(exponentialBase, attempt - 1),
        maxDelayMs
      )

      logger.warn('retry_waiting', {
        attempt,
        nextAttempt: attempt + 1,
        delayMs: delay,
        error: lastError.message
      })

      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }

  throw lastError!
}

// Usage - External API with retry
export async function fetchExternalDataWithRetry(userId: string) {
  return withRetry(
    () => fetchExternalData(userId),
    {
      maxRetries: 3,
      initialDelayMs: 1000,
      shouldRetry: (error) => {
        // Retry on network errors or 5xx status codes
        return (
          error.message.includes('network') ||
          error.message.includes('timeout') ||
          error.message.includes('503')
        )
      }
    }
  )
}
```

---

## Circuit Breaker Pattern

For external services that may go down.

```typescript
// lib/circuit-breaker.ts
import { logger } from '@/lib/logger'

export class CircuitBreaker {
  private failures = 0
  private lastFailureTime: number | null = null
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED'

  constructor(
    private threshold: number = 5,           // Open after 5 failures
    private timeout: number = 60000,         // Reset after 1 minute
    private halfOpenRequests: number = 1     // Test with 1 request
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      // Check if we should try again (timeout elapsed)
      if (Date.now() - this.lastFailureTime! >= this.timeout) {
        logger.info('circuit_breaker_half_open')
        this.state = 'HALF_OPEN'
      } else {
        logger.warn('circuit_breaker_rejected')
        throw new Error('Circuit breaker is OPEN')
      }
    }

    try {
      const result = await fn()

      // Success - reset failures
      if (this.state === 'HALF_OPEN') {
        logger.info('circuit_breaker_closed')
        this.state = 'CLOSED'
        this.failures = 0
        this.lastFailureTime = null
      }

      return result

    } catch (error) {
      this.failures++
      this.lastFailureTime = Date.now()

      if (this.failures >= this.threshold) {
        logger.error('circuit_breaker_opened', {
          failures: this.failures,
          threshold: this.threshold
        })
        this.state = 'OPEN'
      }

      throw error
    }
  }

  getState() {
    return this.state
  }
}

// Usage
const externalApiCircuit = new CircuitBreaker(5, 60000)

export async function fetchDataSafe(userId: string) {
  return externalApiCircuit.execute(() =>
    fetchExternalData(userId)
  )
}
```

---

## Input Validation (Zod)

```typescript
// Always validate with Zod
import { z } from 'zod'

const userSchema = z.object({
  email: z.string().email(),
  age: z.number().min(18).max(120),
  country: z.string().length(2), // ISO country code
  newsletter: z.boolean().optional()
})

export async function POST(request: NextRequest) {
  const body = await request.json()

  // Safe parse (returns result object)
  const result = userSchema.safeParse(body)

  if (!result.success) {
    logger.warn('validation_error', {
      errors: result.error.flatten()
    })

    return NextResponse.json(
      {
        error: 'Invalid input',
        details: result.error.flatten().fieldErrors
      },
      { status: 400 }
    )
  }

  // Use validated data
  const data = result.data // Type-safe!
  // ...
}
```

---

## Best Practices

### DO:
- ✅ Validate all inputs (never trust user data)
- ✅ Log every error with context (requestId, userId, etc.)
- ✅ Return user-friendly error messages
- ✅ Use custom error classes for domain errors
- ✅ Implement retry logic for transient failures
- ✅ Use circuit breakers for external services
- ✅ Fail fast (don't continue with invalid data)

### DON'T:
- ❌ Expose stack traces to users
- ❌ Return raw database errors
- ❌ Catch errors and do nothing
- ❌ Use generic error messages ("Something went wrong")
- ❌ Retry non-retryable errors (validation, 404, etc.)
- ❌ Hardcode API keys in error logs

---

**💡 Remember:** Good error handling makes debugging 10x easier!
