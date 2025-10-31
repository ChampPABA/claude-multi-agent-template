# Code Standards & Conventions

**Goal:** Consistent, readable, maintainable code across all projects.

---

## File Size Guidelines

| File Type | Max Lines | Reasoning |
|-----------|-----------|-----------|
| **Components** | 300 lines | Single responsibility, easier to test |
| **API Routes** | 200 lines | Delegate complex logic to services |
| **Services** | 400 lines | Single domain focus |
| **Utilities** | 150 lines | Pure functions, simple modules |
| **Tests** | 500 lines | Comprehensive coverage per module |

### When to Split Files

**❌ Too Large:**
```typescript
// user-management.ts (800 lines)
class UserManagement {
  createUser() { /* 100 lines */ }
  updateUser() { /* 100 lines */ }
  deleteUser() { /* 100 lines */ }
  sendWelcomeEmail() { /* 100 lines */ }
  generateReport() { /* 100 lines */ }
  exportToCSV() { /* 100 lines */ }
  // ... more methods
}
```

**✅ Properly Split:**
```typescript
// services/user-service.ts (150 lines)
class UserService {
  createUser() { /* ... */ }
  updateUser() { /* ... */ }
  deleteUser() { /* ... */ }
}

// services/email-service.ts (100 lines)
class EmailService {
  sendWelcomeEmail() { /* ... */ }
}

// services/report-service.ts (120 lines)
class ReportService {
  generateReport() { /* ... */ }
  exportToCSV() { /* ... */ }
}
```

---

## Function Complexity

| Function Type | Max Lines | Max Nesting |
|---------------|-----------|-------------|
| **React Components** | 100 lines | 3 levels |
| **Hooks** | 80 lines | 2 levels |
| **API Handlers** | 50 lines | 2 levels |
| **Service Methods** | 60 lines | 3 levels |
| **Utility Functions** | 40 lines | 2 levels |

### Reducing Complexity

**❌ Complex (6 levels deep):**
```typescript
function processOrder(order: Order) {
  if (order.items.length > 0) {
    if (order.user.isPremium) {
      if (order.total > 100) {
        if (order.shippingAddress) {
          if (order.paymentMethod === 'card') {
            if (order.user.hasValidCard) {
              // Deep nesting hell
              return processPayment(order)
            }
          }
        }
      }
    }
  }
}
```

**✅ Simple (Early Returns):**
```typescript
function processOrder(order: Order) {
  // Guard clauses
  if (order.items.length === 0) throw new Error('Empty order')
  if (!order.user.isPremium) throw new Error('Premium required')
  if (order.total <= 100) throw new Error('Minimum $100')
  if (!order.shippingAddress) throw new Error('Address required')
  if (order.paymentMethod !== 'card') throw new Error('Card payment only')
  if (!order.user.hasValidCard) throw new Error('Invalid card')

  // Happy path
  return processPayment(order)
}
```

---

## Naming Conventions

### TypeScript/JavaScript (Next.js, React, Node.js)

| Type | Convention | Example |
|------|-----------|---------|
| **Files/Folders** | kebab-case | `user-profile.tsx`, `api-routes/` |
| **Components** | PascalCase | `UserProfile`, `AssessmentCard` |
| **Functions/Variables** | camelCase | `calculateTotal`, `isAuthenticated` |
| **Constants** | UPPER_SNAKE_CASE | `MAX_FILE_SIZE`, `API_BASE_URL` |
| **Types/Interfaces** | PascalCase | `User`, `SessionData` |
| **Enums** | PascalCase | `UserRole`, `PaymentStatus` |
| **Private Fields** | _camelCase | `_internalState` |

**Examples:**

```typescript
// Files
user-profile.tsx
session-manager.ts
api-routes/users/route.ts

// Components
export default function UserProfile() { /* ... */ }
export function AssessmentCard({ data }: Props) { /* ... */ }

// Functions
function calculateBandScore(score: number) { /* ... */ }
const isAuthenticated = (user: User) => !!user.token

// Constants
const MAX_RECORDING_TIME = 120 // seconds
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL

// Types
interface User {
  id: string
  email: string
}

type SessionStatus = 'active' | 'expired' | 'invalid'

enum UserRole {
  Admin = 'ADMIN',
  User = 'USER',
  Guest = 'GUEST'
}

// Private
class SessionStore {
  private _sessions = new Map()
}
```

---

### Python (FastAPI, Django, Flask)

| Type | Convention | Example |
|------|-----------|---------|
| **Files/Modules** | snake_case | `user_service.py`, `api_routes.py` |
| **Classes** | PascalCase | `UserService`, `DatabaseClient` |
| **Functions/Variables** | snake_case | `calculate_total`, `is_authenticated` |
| **Constants** | UPPER_SNAKE_CASE | `MAX_FILE_SIZE`, `API_BASE_URL` |
| **Private** | _snake_case | `_internal_method` |

**Examples:**

```python
# Files
user_service.py
session_manager.py

# Classes
class UserService:
    pass

class DatabaseClient:
    pass

# Functions
def calculate_band_score(score: float) -> float:
    pass

def is_authenticated(user: User) -> bool:
    return user.token is not None

# Constants
MAX_RECORDING_TIME = 120  # seconds
API_BASE_URL = os.getenv("API_BASE_URL")

# Private
class SessionStore:
    def __init__(self):
        self._sessions = {}
```

---

## Database Naming

### Prisma (TypeScript)

| Type | Convention | Example |
|------|-----------|---------|
| **Models** | PascalCase singular | `User`, `Session`, `Order` |
| **Fields** | camelCase | `userId`, `createdAt`, `firstName` |
| **Relations** | camelCase | `user`, `orders`, `sessions` |
| **Enums** | PascalCase | `UserRole`, `OrderStatus` |

```prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  firstName String
  lastName  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  // Relations
  sessions  Session[]
  orders    Order[]

  @@map("users")
}

enum UserRole {
  ADMIN
  USER
  GUEST

  @@map("user_roles")
}
```

---

### SQLAlchemy (Python)

| Type | Convention | Example |
|------|-----------|---------|
| **Models** | PascalCase | `User`, `Session`, `Order` |
| **Tables** | snake_case | `users`, `sessions`, `orders` |
| **Columns** | snake_case | `user_id`, `created_at`, `first_name` |

```python
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relations
    sessions = relationship("Session", back_populates="user")
    orders = relationship("Order", back_populates="user")
```

---

## Code Organization

### Next.js App Router

```
project/
├── app/
│   ├── api/
│   │   ├── users/
│   │   │   ├── route.ts          # API endpoint
│   │   │   └── [id]/route.ts     # Dynamic route
│   │   └── auth/
│   │       └── route.ts
│   ├── (dashboard)/              # Route group
│   │   ├── layout.tsx
│   │   └── page.tsx
│   └── page.tsx                  # Home page
├── components/
│   ├── ui/                       # Reusable UI components
│   │   ├── button.tsx
│   │   └── card.tsx
│   └── features/                 # Feature-specific components
│       ├── user-profile.tsx
│       └── assessment-card.tsx
├── lib/
│   ├── db.ts                     # Database client
│   ├── logger.ts                 # Logging utility
│   ├── validators/               # Zod schemas
│   │   ├── user.ts
│   │   └── session.ts
│   ├── services/                 # Business logic
│   │   ├── user-service.ts
│   │   └── email-service.ts
│   ├── types/                    # TypeScript types
│   │   ├── user.ts
│   │   └── session.ts
│   └── utils/                    # Utility functions
│       ├── formatters.ts
│       └── validators.ts
├── prisma/
│   ├── schema.prisma
│   └── migrations/
├── tests/
│   ├── unit/
│   │   └── lib/
│   ├── integration/
│   │   └── api/
│   └── e2e/
└── public/
```

---

### FastAPI

```
project/
├── app/
│   ├── main.py                   # FastAPI app
│   ├── api/
│   │   ├── __init__.py
│   │   ├── users.py              # User routes
│   │   └── auth.py               # Auth routes
│   ├── models/                   # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── session.py
│   ├── schemas/                  # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── session.py
│   ├── services/                 # Business logic
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── email_service.py
│   └── utils/                    # Utilities
│       ├── __init__.py
│       ├── logger.py
│       └── validators.py
├── tests/
│   ├── unit/
│   └── integration/
└── alembic/                      # Database migrations
```

---

## Import Order

### TypeScript/JavaScript

```typescript
// 1. External libraries
import { useState, useEffect } from 'react'
import { z } from 'zod'

// 2. Internal absolute imports (@/)
import { Button } from '@/components/ui/button'
import { logger } from '@/lib/logger'
import { userService } from '@/lib/services/user-service'

// 3. Types
import type { User, SessionData } from '@/lib/types'

// 4. Relative imports
import { calculateScore } from './utils'
import type { LocalProps } from './types'
```

---

### Python

```python
# 1. Standard library
import os
import sys
from datetime import datetime

# 2. Third-party libraries
from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, String

# 3. Local application imports
from app.models.user import User
from app.services.user_service import UserService
from app.utils.logger import logger
```

---

## Comments & Documentation

### When to Comment

**✅ Good Comments:**
- Explain **why** (not what)
- Document non-obvious business logic
- Warn about edge cases
- Explain workarounds

**❌ Bad Comments:**
```typescript
// Increment counter by 1
counter++

// Check if user is admin
if (user.role === 'ADMIN') { /* ... */ }
```

**✅ Good Comments:**
```typescript
// Use exponential backoff to avoid overwhelming the API during rate limiting
// Speechace API allows max 16 TPS, so we use delay = 2^attempt * 100ms
await retryWithBackoff(() => callSpeechaceAPI(), { maxRetries: 3 })

// WORKAROUND: Next.js 15 requires 'use client' for localStorage access
// See: https://github.com/vercel/next.js/issues/12345
'use client'
export function useLocalStorage() { /* ... */ }
```

---

### JSDoc / Docstrings

**TypeScript:**
```typescript
/**
 * Calculates IELTS band score from Speechace percentage score.
 *
 * Speechace scores range from 0-100, IELTS ranges from 0-9.
 * Conversion uses linear mapping with rounding to nearest 0.5.
 *
 * @param speechaceScore - Score from Speechace API (0-100)
 * @returns IELTS band score (0-9, rounded to nearest 0.5)
 * @throws {ValidationError} If speechaceScore is outside 0-100 range
 *
 * @example
 * calculateBandScore(85) // Returns 7.5
 * calculateBandScore(60) // Returns 5.5
 */
export function calculateBandScore(speechaceScore: number): number {
  // Implementation
}
```

**Python:**
```python
def calculate_band_score(speechace_score: float) -> float:
    """
    Calculates IELTS band score from Speechace percentage score.

    Speechace scores range from 0-100, IELTS ranges from 0-9.
    Conversion uses linear mapping with rounding to nearest 0.5.

    Args:
        speechace_score: Score from Speechace API (0-100)

    Returns:
        IELTS band score (0-9, rounded to nearest 0.5)

    Raises:
        ValidationError: If speechace_score is outside 0-100 range

    Examples:
        >>> calculate_band_score(85)
        7.5
        >>> calculate_band_score(60)
        5.5
    """
    # Implementation
```

---

## Quick Reference

### TypeScript

| Element | Convention |
|---------|-----------|
| Files | `kebab-case.tsx` |
| Components | `PascalCase` |
| Functions | `camelCase` |
| Constants | `UPPER_SNAKE_CASE` |
| Types | `PascalCase` |

### Python

| Element | Convention |
|---------|-----------|
| Files | `snake_case.py` |
| Classes | `PascalCase` |
| Functions | `snake_case` |
| Constants | `UPPER_SNAKE_CASE` |

### Database

| ORM | Model | Table | Column |
|-----|-------|-------|--------|
| Prisma | `PascalCase` | `snake_case` | `camelCase` |
| SQLAlchemy | `PascalCase` | `snake_case` | `snake_case` |

---

**💡 Remember:** Consistency is more important than perfection!
