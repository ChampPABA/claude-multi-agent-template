# State Management Patterns

**Goal:** Predictable, scalable, and maintainable state across client and server.

---

## State Classification

| State Type | Location | Solution | When to Use |
|-------------|----------|----------|-------------|
| **Server State** | Backend DB | TanStack Query | API data, async operations |
| **Client State** | Browser | Zustand / Context | UI state, user preferences |
| **URL State** | URL params | useSearchParams | Filters, pagination, tabs |
| **Form State** | Form elements | React Hook Form | Form inputs, validation |
| **Session State** | Cookies / Storage | NextAuth / Custom | Authentication, tokens |

---

## Server State (TanStack Query)

**Use for:** API data, database records, external service responses

### Basic Query

```typescript
// hooks/use-items.ts
import { useQuery } from '@tanstack/react-query'
import { logger } from '@/lib/logger'

export function useItems(userId: string) {
  return useQuery({
    queryKey: ['items', userId],
    queryFn: async () => {
      logger.info('query_start', { queryKey: 'items', userId })

      const response = await fetch(`/api/items?userId=${userId}`)
      if (!response.ok) throw new Error('Failed to fetch items')

      const data = await response.json()

      logger.info('query_success', {
        queryKey: 'items',
        userId,
        count: data.length
      })

      return data
    },
    staleTime: 1000 * 60, // 1 minute
    gcTime: 1000 * 60 * 5 // 5 minutes (formerly cacheTime)
  })
}

// Usage in component
function ItemList({ userId }: { userId: string }) {
  const { data, isLoading, error } = useItems(userId)

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return <ul>{data.map(item => <li key={item.id}>{item.name}</li>)}</ul>
}
```

---

### Mutation

```typescript
// hooks/use-create-item.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { logger } from '@/lib/logger'

export function useCreateItem(userId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: { name: string; price: number }) => {
      logger.info('mutation_start', {
        mutation: 'createItem',
        userId
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
        itemId: result.id
      })

      // Invalidate and refetch items
      queryClient.invalidateQueries({ queryKey: ['items', userId] })
    },

    onError: (error) => {
      logger.error('mutation_error', {
        mutation: 'createItem',
        userId,
        error: error.message
      })
    }
  })
}

// Usage
function CreateItemForm({ userId }: { userId: string }) {
  const mutation = useCreateItem(userId)

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    mutation.mutate({
      name: formData.get('name') as string,
      price: parseFloat(formData.get('price') as string)
    })
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" required />
      <input name="price" type="number" required />
      <button disabled={mutation.isPending}>
        {mutation.isPending ? 'Creating...' : 'Create'}
      </button>
      {mutation.isError && <div>Error: {mutation.error.message}</div>}
    </form>
  )
}
```

---

### Optimistic Updates

```typescript
export function useUpdateItem(userId: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async ({ id, name }: { id: string; name: string }) => {
      const response = await fetch(`/api/items/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
      })
      if (!response.ok) throw new Error('Update failed')
      return response.json()
    },

    onMutate: async ({ id, name }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['items', userId] })

      // Snapshot previous value
      const previousItems = queryClient.getQueryData(['items', userId])

      // Optimistically update
      queryClient.setQueryData(['items', userId], (old: Item[]) =>
        old.map(item => item.id === id ? { ...item, name } : item)
      )

      logger.info('mutation_optimistic_update', { userId, itemId: id })

      return { previousItems }
    },

    onError: (error, variables, context) => {
      // Rollback on error
      if (context?.previousItems) {
        queryClient.setQueryData(['items', userId], context.previousItems)
      }
      logger.error('mutation_rollback', { userId, error: error.message })
    },

    onSettled: () => {
      // Refetch after mutation
      queryClient.invalidateQueries({ queryKey: ['items', userId] })
    }
  })
}
```

---

## Client State (Zustand)

**Use for:** UI state, user preferences, temporary data

### Basic Store

```typescript
// lib/stores/app-store.ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import { logger } from '@/lib/logger'

interface AppState {
  theme: 'light' | 'dark'
  sidebarOpen: boolean
  notifications: Notification[]
  setTheme: (theme: 'light' | 'dark') => void
  toggleSidebar: () => void
  addNotification: (notification: Notification) => void
  clearNotifications: () => void
}

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      (set, get) => ({
        theme: 'light',
        sidebarOpen: true,
        notifications: [],

        setTheme: (theme) => {
          logger.info('store_action', {
            store: 'app',
            action: 'setTheme',
            prevTheme: get().theme,
            newTheme: theme
          })
          set({ theme })
        },

        toggleSidebar: () => {
          const prevState = get().sidebarOpen
          logger.info('store_action', {
            store: 'app',
            action: 'toggleSidebar',
            prevState,
            newState: !prevState
          })
          set({ sidebarOpen: !prevState })
        },

        addNotification: (notification) => {
          logger.info('store_action', {
            store: 'app',
            action: 'addNotification',
            notificationId: notification.id
          })
          set((state) => ({
            notifications: [...state.notifications, notification]
          }))
        },

        clearNotifications: () => {
          logger.info('store_action', {
            store: 'app',
            action: 'clearNotifications',
            count: get().notifications.length
          })
          set({ notifications: [] })
        }
      }),
      {
        name: 'app-storage', // localStorage key
        partialize: (state) => ({
          theme: state.theme,
          sidebarOpen: state.sidebarOpen
          // Exclude notifications (don't persist)
        })
      }
    )
  )
)

// Usage
function ThemeToggle() {
  const theme = useAppStore(state => state.theme)
  const setTheme = useAppStore(state => state.setTheme)

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      {theme === 'light' ? '🌙' : '☀️'}
    </button>
  )
}
```

---

### Slices Pattern (Large Stores)

```typescript
// lib/stores/slices/user-slice.ts
import { StateCreator } from 'zustand'

export interface UserSlice {
  user: User | null
  setUser: (user: User) => void
  clearUser: () => void
}

export const createUserSlice: StateCreator<UserSlice> = (set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null })
})

// lib/stores/slices/cart-slice.ts
export interface CartSlice {
  items: CartItem[]
  addItem: (item: CartItem) => void
  removeItem: (id: string) => void
  clearCart: () => void
}

export const createCartSlice: StateCreator<CartSlice> = (set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) => set((state) => ({
    items: state.items.filter(item => item.id !== id)
  })),
  clearCart: () => set({ items: [] })
})

// lib/stores/app-store.ts
import { create } from 'zustand'
import { createUserSlice, UserSlice } from './slices/user-slice'
import { createCartSlice, CartSlice } from './slices/cart-slice'

type AppStore = UserSlice & CartSlice

export const useAppStore = create<AppStore>()((...a) => ({
  ...createUserSlice(...a),
  ...createCartSlice(...a)
}))
```

---

## URL State (useSearchParams)

**Use for:** Filters, pagination, tabs, search queries

```typescript
// app/products/page.tsx
'use client'
import { useSearchParams, useRouter } from 'next/navigation'

export default function ProductsPage() {
  const searchParams = useSearchParams()
  const router = useRouter()

  const category = searchParams.get('category') || 'all'
  const page = parseInt(searchParams.get('page') || '1')

  const setCategory = (category: string) => {
    const params = new URLSearchParams(searchParams)
    params.set('category', category)
    params.set('page', '1') // Reset to page 1
    router.push(`/products?${params.toString()}`)
  }

  const setPage = (page: number) => {
    const params = new URLSearchParams(searchParams)
    params.set('page', page.toString())
    router.push(`/products?${params.toString()}`)
  }

  return (
    <div>
      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        <option value="all">All</option>
        <option value="electronics">Electronics</option>
        <option value="clothing">Clothing</option>
      </select>

      <div>Page {page}</div>
      <button onClick={() => setPage(page - 1)}>Previous</button>
      <button onClick={() => setPage(page + 1)}>Next</button>
    </div>
  )
}
```

---

## Form State (React Hook Form)

**Use for:** Complex forms, validation, multi-step forms

```typescript
// components/signup-form.tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword']
})

type FormData = z.infer<typeof schema>

export function SignupForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema)
  })

  const onSubmit = (data: FormData) => {
    console.log(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input {...register('password')} type="password" />
      {errors.password && <span>{errors.password.message}</span>}

      <input {...register('confirmPassword')} type="password" />
      {errors.confirmPassword && <span>{errors.confirmPassword.message}</span>}

      <button type="submit">Sign Up</button>
    </form>
  )
}
```

---

## React Context (Small Apps Only)

**Use for:** Small apps, theme, i18n

**⚠️ Avoid for:** Large apps (use Zustand instead)

```typescript
// contexts/theme-context.tsx
import { createContext, useContext, useState, ReactNode } from 'react'

interface ThemeContextValue {
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined)

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light')

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) throw new Error('useTheme must be used within ThemeProvider')
  return context
}

// Usage
function App() {
  return (
    <ThemeProvider>
      <Header />
      <Main />
    </ThemeProvider>
  )
}

function Header() {
  const { theme, toggleTheme } = useTheme()
  return <button onClick={toggleTheme}>{theme}</button>
}
```

---

## Decision Tree

```
What type of state do I need?

├─ Data from API/Database?
│  └─ Use TanStack Query (Server State)
│
├─ UI state (theme, sidebar, modals)?
│  └─ Use Zustand (Client State)
│
├─ Filters, pagination, search?
│  └─ Use URL params (URL State)
│
├─ Form inputs with validation?
│  └─ Use React Hook Form (Form State)
│
├─ Authentication tokens?
│  └─ Use NextAuth or cookies (Session State)
│
└─ Small app with simple theme/i18n?
   └─ Use React Context (only if app is small)
```

---

## Best Practices

### DO:
- ✅ Use TanStack Query for server state
- ✅ Use Zustand for complex client state
- ✅ Use URL params for shareable state
- ✅ Use React Hook Form for forms
- ✅ Log all state changes
- ✅ Persist only necessary data

### DON'T:
- ❌ Use Context for everything (performance issues)
- ❌ Store API data in Zustand (use TanStack Query)
- ❌ Mix server and client state
- ❌ Forget to log state changes
- ❌ Persist sensitive data (tokens, passwords)

---

**💡 Remember:** The right state solution depends on your use case!
