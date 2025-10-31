# Logging & Observability Patterns

**Critical Rule:** Every API call, database operation, external service interaction, user action, and error MUST be logged with proper context.

---

## When to Log

| Event Type | Log Level | Required Fields |
|------------|-----------|-----------------|
| **API Route Entry/Exit** | INFO | `route`, `method`, `requestId`, `duration` |
| **Database Operations** | INFO | `operation`, `table`, `duration`, `rowCount` |
| **External API Calls** | INFO | `service`, `endpoint`, `duration`, `statusCode` |
| **User Actions** | INFO | `action`, `userId/sessionId`, `timestamp` |
| **Errors & Exceptions** | ERROR | `error`, `stack`, `context`, `userId` |
| **Performance Metrics** | INFO | `operation`, `duration`, `memoryUsage` |
| **State Changes** | DEBUG | `store`, `action`, `prevState`, `nextState` |

---

## Implementation Patterns

### API Route Pattern (Next.js)

```typescript
// app/api/items/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { logger } from '@/lib/logger'

export async function POST(request: NextRequest) {
  const startTime = Date.now()
  const requestId = crypto.randomUUID()

  logger.info('api_route_entry', {
    requestId,
    route: '/api/items',
    method: 'POST',
    timestamp: new Date().toISOString()
  })

  try {
    const body = await request.json()
    const result = await createItem(body)

    logger.info('api_route_success', {
      requestId,
      route: '/api/items',
      duration: Date.now() - startTime,
      resultSize: JSON.stringify(result).length
    })

    return NextResponse.json(result)
  } catch (error) {
    logger.error('api_route_error', {
      requestId,
      route: '/api/items',
      error: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined,
      duration: Date.now() - startTime
    })
    throw error
  }
}
```

---

### Database Operation Pattern (Prisma)

```typescript
// lib/db-operations.ts
import { prisma } from '@/lib/db'
import { logger } from '@/lib/logger'

export async function createUser(data: UserData) {
  const startTime = Date.now()

  logger.info('db_operation_start', {
    operation: 'createUser',
    table: 'User'
  })

  try {
    const user = await prisma.user.create({ data })

    logger.info('db_operation_success', {
      operation: 'createUser',
      table: 'User',
      userId: user.id,
      duration: Date.now() - startTime
    })

    return user
  } catch (error) {
    logger.error('db_operation_error', {
      operation: 'createUser',
      table: 'User',
      error: error instanceof Error ? error.message : 'Unknown error',
      duration: Date.now() - startTime
    })
    throw error
  }
}
```

---

### Database Pattern (SQLAlchemy - Python)

```python
# app/db/user.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
import logging
import time

logger = logging.getLogger(__name__)

async def create_user(db: AsyncSession, email: str, name: str) -> User:
    start_time = time.time()

    logger.info({"event": "db_operation_start", "operation": "create_user", "table": "users"})

    try:
        user = User(email=email, name=name)
        db.add(user)
        await db.commit()
        await db.refresh(user)

        logger.info({
            "event": "db_operation_success",
            "operation": "create_user",
            "table": "users",
            "user_id": user.id,
            "duration": time.time() - start_time
        })

        return user
    except Exception as e:
        logger.error({
            "event": "db_operation_error",
            "operation": "create_user",
            "table": "users",
            "error": str(e),
            "duration": time.time() - start_time
        })
        raise
```

---

### External API Pattern

```typescript
// lib/external-api.ts
import { logger } from '@/lib/logger'

export async function fetchExternalData(userId: string) {
  const startTime = Date.now()

  logger.info('external_api_start', {
    service: 'external-api',
    userId,
    endpoint: '/api/data'
  })

  try {
    const response = await fetch('https://api.example.com/data', {
      headers: { Authorization: `Bearer ${process.env.API_KEY}` }
    })

    const result = await response.json()

    logger.info('external_api_success', {
      service: 'external-api',
      userId,
      statusCode: response.status,
      duration: Date.now() - startTime
    })

    return result
  } catch (error) {
    logger.error('external_api_error', {
      service: 'external-api',
      userId,
      error: error instanceof Error ? error.message : 'Unknown error',
      duration: Date.now() - startTime
    })
    throw error
  }
}
```

---

### State Management Logging (Zustand)

```typescript
// lib/stores/app-store.ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import { logger } from '@/lib/logger'

interface AppState {
  userId: string | null
  currentView: string
  setUserId: (id: string) => void
  setCurrentView: (view: string) => void
}

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      (set, get) => ({
        userId: null,
        currentView: 'home',

        setUserId: (id) => {
          logger.info('store_action', {
            store: 'app',
            action: 'setUserId',
            userId: id,
            prevState: get().userId
          })
          set({ userId: id })
        },

        setCurrentView: (view) => {
          logger.info('store_action', {
            store: 'app',
            action: 'setCurrentView',
            userId: get().userId,
            prevView: get().currentView,
            nextView: view
          })
          set({ currentView: view })
        }
      }),
      { name: 'app-storage' }
    )
  )
)
```

---

### TanStack Query Logging Pattern

```typescript
// hooks/use-create-item.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { logger } from '@/lib/logger'

export function useCreateItem(userId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: ItemData) => {
      logger.info('mutation_start', {
        mutation: 'createItem',
        userId,
        dataSize: JSON.stringify(data).length
      })

      const response = await fetch('/api/items', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })

      if (!response.ok) throw new Error('Creation failed')
      return response.json()
    },

    onSuccess: (result) => {
      logger.info('mutation_success', {
        mutation: 'createItem',
        userId,
        resultId: result.id
      })
      queryClient.invalidateQueries({ queryKey: ['items', userId] })
    },

    onError: (error) => {
      logger.error('mutation_error', {
        mutation: 'createItem',
        userId,
        error: error instanceof Error ? error.message : 'Unknown error'
      })
    }
  })
}
```

---

## Logger Implementation

### TypeScript/JavaScript

```typescript
// lib/logger.ts
type LogLevel = 'DEBUG' | 'INFO' | 'WARN' | 'ERROR'

interface LogContext {
  [key: string]: unknown
}

class Logger {
  private log(level: LogLevel, event: string, context?: LogContext) {
    const timestamp = new Date().toISOString()
    const logEntry = {
      timestamp,
      level,
      event,
      ...context
    }

    // Development: Pretty console output
    if (process.env.NODE_ENV === 'development') {
      console[level.toLowerCase() as 'log'](`[${level}] ${event}`, context)
    }

    // Production: Structured JSON logs
    if (process.env.NODE_ENV === 'production') {
      console[level.toLowerCase() as 'log'](JSON.stringify(logEntry))
      // Optional: Send to monitoring service (Sentry, LogRocket, etc.)
    }
  }

  debug(event: string, context?: LogContext) {
    this.log('DEBUG', event, context)
  }

  info(event: string, context?: LogContext) {
    this.log('INFO', event, context)
  }

  warn(event: string, context?: LogContext) {
    this.log('WARN', event, context)
  }

  error(event: string, context?: LogContext) {
    this.log('ERROR', event, context)
  }
}

export const logger = new Logger()
```

### Python

```python
# lib/logger.py
import logging
import json
from datetime import datetime
from typing import Any, Dict

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

    def _log(self, level: str, event: str, context: Dict[str, Any] = None):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "event": event,
            **(context or {})
        }

        # Development: Human-readable
        if os.getenv("ENV") == "development":
            self.logger.log(getattr(logging, level), f"{event}: {context}")
        # Production: JSON
        else:
            self.logger.log(getattr(logging, level), json.dumps(log_entry))

    def debug(self, event: str, context: Dict[str, Any] = None):
        self._log("DEBUG", event, context)

    def info(self, event: str, context: Dict[str, Any] = None):
        self._log("INFO", event, context)

    def warning(self, event: str, context: Dict[str, Any] = None):
        self._log("WARNING", event, context)

    def error(self, event: str, context: Dict[str, Any] = None):
        self._log("ERROR", event, context)

logger = StructuredLogger(__name__)
```

---

## Quick Reference

```typescript
// API Route
logger.info('api_route_entry', { route, method, requestId })
logger.info('api_route_success', { route, duration, requestId })
logger.error('api_route_error', { route, error, stack, requestId })

// Database
logger.info('db_operation_start', { operation, table })
logger.info('db_operation_success', { operation, table, duration })
logger.error('db_operation_error', { operation, table, error, duration })

// External API
logger.info('external_api_start', { service, endpoint })
logger.info('external_api_success', { service, statusCode, duration })
logger.error('external_api_error', { service, error, duration })

// State Management
logger.info('store_action', { store, action, context })

// Performance
logger.info('performance_metric', { operation, duration, memoryUsage })
```

---

**💡 Remember:** If an action happens without logs, it's invisible in production!
