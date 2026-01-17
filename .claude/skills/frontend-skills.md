# Frontend Skills for Next.js App Router Applications

## Overview
This document defines frontend-specific technical skills for building modern, secure web applications using Next.js App Router, React, TypeScript, and Tailwind CSS. These skills ensure proper routing, authentication flows, secure API integration, robust state management, and responsive user interfaces.

---

## 1. App Router Design Patterns

### Purpose
Leverage Next.js App Router architecture to build performant, SEO-friendly applications with proper file-based routing, layouts, and data fetching patterns.

### Key Capabilities
- **File-Based Routing**: Organize routes using the app directory structure
- **Layout Composition**: Share UI elements across routes with nested layouts
- **Loading & Error States**: Handle async boundaries with loading.tsx and error.tsx
- **Server vs Client Components**: Choose appropriate rendering strategies
- **Route Groups**: Organize routes without affecting URL structure

### App Router File Structure

```text
app/
├── layout.tsx              # Root layout (wraps all pages)
├── page.tsx                # Home page (/)
├── loading.tsx             # Loading UI for home
├── error.tsx               # Error boundary for home
├── not-found.tsx           # 404 page
│
├── (auth)/                 # Route group (doesn't affect URL)
│   ├── layout.tsx          # Auth layout
│   ├── login/
│   │   └── page.tsx        # /login
│   └── signup/
│       └── page.tsx        # /signup
│
├── (dashboard)/            # Route group with shared layout
│   ├── layout.tsx          # Dashboard layout
│   ├── tasks/
│   │   ├── page.tsx        # /tasks (list)
│   │   ├── loading.tsx     # Loading state for tasks
│   │   ├── [id]/
│   │   │   ├── page.tsx    # /tasks/123 (detail)
│   │   │   └── edit/
│   │   │       └── page.tsx # /tasks/123/edit
│   │   └── new/
│   │       └── page.tsx    # /tasks/new
│   └── settings/
│       └── page.tsx        # /settings
│
└── api/                    # API routes (not covered here, use separate backend)
```

### Root Layout Pattern

```tsx
// app/layout.tsx
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { AuthProvider } from '@/providers/auth-provider'
import { Toaster } from '@/components/ui/toaster'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Task Manager',
  description: 'Manage your tasks efficiently',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          {children}
          <Toaster />
        </AuthProvider>
      </body>
    </html>
  )
}
```

### Nested Layout Pattern

```tsx
// app/(dashboard)/layout.tsx
import { redirect } from 'next/navigation'
import { getSession } from '@/lib/auth'
import { Sidebar } from '@/components/sidebar'
import { Header } from '@/components/header'

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  // Server-side auth check
  const session = await getSession()

  if (!session) {
    redirect('/login')
  }

  return (
    <div className="flex h-screen">
      <Sidebar user={session.user} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header user={session.user} />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
```

### Page Component Pattern

```tsx
// app/(dashboard)/tasks/page.tsx
import { Suspense } from 'react'
import { TaskList } from '@/components/task-list'
import { TaskListSkeleton } from '@/components/task-list-skeleton'
import { CreateTaskButton } from '@/components/create-task-button'

export const metadata = {
  title: 'Tasks | Task Manager',
}

export default function TasksPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Tasks</h1>
        <CreateTaskButton />
      </div>

      <Suspense fallback={<TaskListSkeleton />}>
        <TaskList />
      </Suspense>
    </div>
  )
}
```

### Loading State Pattern

```tsx
// app/(dashboard)/tasks/loading.tsx
import { Skeleton } from '@/components/ui/skeleton'

export default function TasksLoading() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Skeleton className="h-10 w-32" />
        <Skeleton className="h-10 w-32" />
      </div>

      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <Skeleton key={i} className="h-24 w-full" />
        ))}
      </div>
    </div>
  )
}
```

### Error Boundary Pattern

```tsx
// app/(dashboard)/tasks/error.tsx
'use client'

import { useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { AlertCircle } from 'lucide-react'

export default function TasksError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log error to monitoring service
    console.error('Tasks page error:', error)
  }, [error])

  return (
    <div className="flex flex-col items-center justify-center h-full space-y-4">
      <AlertCircle className="h-12 w-12 text-destructive" />
      <h2 className="text-2xl font-bold">Something went wrong</h2>
      <p className="text-muted-foreground">
        Failed to load tasks. Please try again.
      </p>
      <Button onClick={reset}>Try again</Button>
    </div>
  )
}
```

### Dynamic Route Pattern

```tsx
// app/(dashboard)/tasks/[id]/page.tsx
import { notFound } from 'next/navigation'
import { getTask } from '@/lib/api'
import { TaskDetail } from '@/components/task-detail'

interface TaskPageProps {
  params: { id: string }
  searchParams: { [key: string]: string | string[] | undefined }
}

export async function generateMetadata({ params }: TaskPageProps) {
  const task = await getTask(params.id)

  if (!task) {
    return { title: 'Task Not Found' }
  }

  return {
    title: `${task.title} | Task Manager`,
    description: task.description,
  }
}

export default async function TaskPage({ params }: TaskPageProps) {
  const task = await getTask(params.id)

  if (!task) {
    notFound()
  }

  return <TaskDetail task={task} />
}
```

### Server vs Client Components

```tsx
// Server Component (default) - Can access backend directly
// app/(dashboard)/tasks/page.tsx
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { db } from '@/lib/db'

export default async function TasksPage() {
  const session = await getServerSession(authOptions)

  // Direct database access (server-side only)
  const tasks = await db.task.findMany({
    where: { userId: session.user.id },
  })

  return <TaskList tasks={tasks} />
}

// Client Component - Requires 'use client' directive
// components/task-form.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export function TaskForm() {
  const [title, setTitle] = useState('')
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title }),
    })

    router.refresh() // Revalidate server components
    router.push('/tasks')
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Task title"
      />
      <button type="submit">Create Task</button>
    </form>
  )
}
```

### Route Groups

```text
app/
├── (marketing)/          # Route group for marketing pages
│   ├── layout.tsx        # Marketing layout (header, footer)
│   ├── page.tsx          # / (home/landing)
│   ├── about/
│   │   └── page.tsx      # /about
│   └── pricing/
│       └── page.tsx      # /pricing
│
└── (app)/                # Route group for application
    ├── layout.tsx        # App layout (sidebar, auth)
    └── dashboard/
        └── page.tsx      # /dashboard
```

### Success Criteria
- File structure matches URL structure
- Shared layouts reduce code duplication
- Loading states prevent layout shift
- Error boundaries gracefully handle failures
- Server components used for data fetching
- Client components only when interactivity needed

---

## 2. Auth-Aware UI Flows

### Purpose
Build authentication flows that provide seamless user experiences while maintaining security, with proper redirects, loading states, and error handling.

### Key Capabilities
- **Login/Signup Forms**: Secure credential collection with validation
- **Protected Routes**: Redirect unauthenticated users
- **Auth State Management**: Track authentication status globally
- **Token Refresh**: Handle expired tokens transparently
- **Logout Flow**: Clear session and redirect safely

### Auth Context Provider

```tsx
// providers/auth-provider.tsx
'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { useRouter } from 'next/navigation'
import { User } from '@/types/user'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  signup: (email: string, password: string, name: string) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    // Check for existing session on mount
    checkAuth()
  }, [])

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('access_token')

      if (!token) {
        setLoading(false)
        return
      }

      const response = await fetch('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })

      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
      } else {
        // Token invalid, clear it
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      }
    } catch (error) {
      console.error('Auth check failed:', error)
    } finally {
      setLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Login failed')
    }

    const { access_token, refresh_token, user: userData } = await response.json()

    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    setUser(userData)

    router.push('/dashboard')
  }

  const signup = async (email: string, password: string, name: string) => {
    const response = await fetch('/api/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, full_name: name }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Signup failed')
    }

    // Auto-login after signup
    await login(email, password)
  }

  const logout = async () => {
    const refreshToken = localStorage.getItem('refresh_token')

    try {
      await fetch('/api/auth/logout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken }),
      })
    } catch (error) {
      console.error('Logout API call failed:', error)
    }

    // Clear local state regardless of API success
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
    router.push('/login')
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, signup }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

### Login Page

```tsx
// app/(auth)/login/page.tsx
'use client'

import { useState } from 'react'
import { useAuth } from '@/providers/auth-provider'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import Link from 'next/link'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await login(email, password)
      // Redirect handled by login function
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow">
        <div className="text-center">
          <h1 className="text-3xl font-bold">Welcome back</h1>
          <p className="text-muted-foreground">Sign in to your account</p>
        </div>

        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              disabled={loading}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              disabled={loading}
            />
          </div>

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign in'}
          </Button>
        </form>

        <p className="text-center text-sm text-muted-foreground">
          Don't have an account?{' '}
          <Link href="/signup" className="text-primary hover:underline">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  )
}
```

### Protected Route Component

```tsx
// components/protected-route.tsx
'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/providers/auth-provider'
import { Loader2 } from 'lucide-react'

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    )
  }

  if (!user) {
    return null // Will redirect
  }

  return <>{children}</>
}
```

### Auth-Aware Navigation

```tsx
// components/header.tsx
'use client'

import { useAuth } from '@/providers/auth-provider'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { LogOut, Settings, User } from 'lucide-react'
import Link from 'next/link'

export function Header() {
  const { user, logout } = useAuth()

  if (!user) {
    return (
      <header className="border-b">
        <div className="container flex items-center justify-between h-16">
          <Link href="/" className="text-xl font-bold">
            Task Manager
          </Link>
          <div className="flex gap-2">
            <Button variant="ghost" asChild>
              <Link href="/login">Sign in</Link>
            </Button>
            <Button asChild>
              <Link href="/signup">Sign up</Link>
            </Button>
          </div>
        </div>
      </header>
    )
  }

  const initials = user.full_name
    ?.split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase() || user.email[0].toUpperCase()

  return (
    <header className="border-b">
      <div className="container flex items-center justify-between h-16">
        <Link href="/dashboard" className="text-xl font-bold">
          Task Manager
        </Link>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="relative h-10 w-10 rounded-full">
              <Avatar>
                <AvatarFallback>{initials}</AvatarFallback>
              </Avatar>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>
              <div className="flex flex-col space-y-1">
                <p className="text-sm font-medium">{user.full_name}</p>
                <p className="text-xs text-muted-foreground">{user.email}</p>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem asChild>
              <Link href="/settings">
                <Settings className="mr-2 h-4 w-4" />
                Settings
              </Link>
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => logout()}>
              <LogOut className="mr-2 h-4 w-4" />
              Log out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  )
}
```

### Success Criteria
- Authentication state persisted across page refreshes
- Unauthenticated users redirected to login
- Login/signup forms have proper validation and error handling
- Tokens stored securely (not in cookies without httpOnly flag)
- Logout clears all auth state
- Loading states prevent UI flicker

---

## 3. Secure API Consumption

### Purpose
Safely interact with backend APIs using authenticated requests, proper error handling, automatic token refresh, and request/response validation.

### Key Capabilities
- **Authenticated Requests**: Attach JWT to all API calls
- **Automatic Token Refresh**: Handle expired tokens transparently
- **Error Handling**: Parse and display API errors appropriately
- **Request Validation**: Type-safe request payloads
- **Response Validation**: Validate API responses match expected types

### API Client Implementation

```typescript
// lib/api-client.ts
import { redirect } from 'next/navigation'

interface RequestOptions extends RequestInit {
  requiresAuth?: boolean
}

class ApiError extends Error {
  constructor(
    public status: number,
    public message: string,
    public details?: any
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = process.env.NEXT_PUBLIC_API_URL || '') {
    this.baseUrl = baseUrl
  }

  private async getAccessToken(): Promise<string | null> {
    // In client components
    if (typeof window !== 'undefined') {
      return localStorage.getItem('access_token')
    }
    // In server components
    return null
  }

  private async refreshToken(): Promise<boolean> {
    const refreshToken = localStorage.getItem('refresh_token')

    if (!refreshToken) {
      return false
    }

    try {
      const response = await fetch(`${this.baseUrl}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken }),
      })

      if (!response.ok) {
        return false
      }

      const { access_token, refresh_token: newRefreshToken } = await response.json()

      localStorage.setItem('access_token', access_token)
      if (newRefreshToken) {
        localStorage.setItem('refresh_token', newRefreshToken)
      }

      return true
    } catch (error) {
      console.error('Token refresh failed:', error)
      return false
    }
  }

  private async request<T>(
    endpoint: string,
    options: RequestOptions = {}
  ): Promise<T> {
    const { requiresAuth = true, ...fetchOptions } = options

    const url = `${this.baseUrl}${endpoint}`
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...fetchOptions.headers,
    }

    // Add auth token if required
    if (requiresAuth) {
      const token = await this.getAccessToken()
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }
    }

    let response = await fetch(url, {
      ...fetchOptions,
      headers,
    })

    // Handle token expiration and retry
    if (response.status === 401 && requiresAuth) {
      const refreshed = await this.refreshToken()

      if (refreshed) {
        // Retry request with new token
        const newToken = await this.getAccessToken()
        if (newToken) {
          headers['Authorization'] = `Bearer ${newToken}`
        }

        response = await fetch(url, {
          ...fetchOptions,
          headers,
        })
      } else {
        // Refresh failed, redirect to login
        if (typeof window !== 'undefined') {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
        throw new ApiError(401, 'Authentication required')
      }
    }

    // Handle non-2xx responses
    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}`
      let errorDetails

      try {
        const errorData = await response.json()
        errorMessage = errorData.detail || errorData.message || errorMessage
        errorDetails = errorData
      } catch {
        // Response not JSON
      }

      throw new ApiError(response.status, errorMessage, errorDetails)
    }

    // Handle empty responses (204 No Content)
    if (response.status === 204) {
      return undefined as T
    }

    // Parse JSON response
    try {
      return await response.json()
    } catch (error) {
      throw new ApiError(500, 'Invalid JSON response from server')
    }
  }

  async get<T>(endpoint: string, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' })
  }

  async post<T>(
    endpoint: string,
    data?: any,
    options?: RequestOptions
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async put<T>(
    endpoint: string,
    data?: any,
    options?: RequestOptions
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async patch<T>(
    endpoint: string,
    data?: any,
    options?: RequestOptions
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PATCH',
      body: JSON.stringify(data),
    })
  }

  async delete<T>(endpoint: string, options?: RequestOptions): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' })
  }
}

export const apiClient = new ApiClient()
export { ApiError }
```

### Type-Safe API Service

```typescript
// lib/api/tasks.ts
import { apiClient, ApiError } from '@/lib/api-client'
import { z } from 'zod'

// Validation schemas
export const TaskSchema = z.object({
  id: z.number(),
  title: z.string(),
  description: z.string().nullable(),
  status: z.enum(['pending', 'in_progress', 'completed', 'cancelled']),
  priority: z.enum(['low', 'medium', 'high', 'urgent']),
  due_date: z.string().nullable(),
  created_at: z.string(),
  updated_at: z.string(),
})

export const TaskCreateSchema = z.object({
  title: z.string().min(1, 'Title is required').max(255),
  description: z.string().optional(),
  priority: z.enum(['low', 'medium', 'high', 'urgent']).default('medium'),
  due_date: z.string().optional(),
})

export const TaskUpdateSchema = TaskCreateSchema.partial()

// Types
export type Task = z.infer<typeof TaskSchema>
export type TaskCreate = z.infer<typeof TaskCreateSchema>
export type TaskUpdate = z.infer<typeof TaskUpdateSchema>

// API functions
export async function getTasks(): Promise<Task[]> {
  const response = await apiClient.get<{ items: Task[] }>('/api/tasks')

  // Validate response
  const tasks = response.items.map((task) => TaskSchema.parse(task))
  return tasks
}

export async function getTask(id: number): Promise<Task> {
  const task = await apiClient.get<Task>(`/api/tasks/${id}`)
  return TaskSchema.parse(task)
}

export async function createTask(data: TaskCreate): Promise<Task> {
  // Validate input
  const validData = TaskCreateSchema.parse(data)

  const task = await apiClient.post<Task>('/api/tasks', validData)
  return TaskSchema.parse(task)
}

export async function updateTask(id: number, data: TaskUpdate): Promise<Task> {
  // Validate input
  const validData = TaskUpdateSchema.parse(data)

  const task = await apiClient.patch<Task>(`/api/tasks/${id}`, validData)
  return TaskSchema.parse(task)
}

export async function deleteTask(id: number): Promise<void> {
  await apiClient.delete(`/api/tasks/${id}`)
}
```

### Usage in Components

```tsx
// components/task-list.tsx
'use client'

import { useEffect, useState } from 'react'
import { getTasks, Task, ApiError } from '@/lib/api/tasks'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { TaskCard } from './task-card'

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadTasks()
  }, [])

  const loadTasks = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getTasks()
      setTasks(data)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('Failed to load tasks')
      }
      console.error('Load tasks error:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div>Loading tasks...</div>
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    )
  }

  if (tasks.length === 0) {
    return <div>No tasks found. Create your first task!</div>
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} onUpdate={loadTasks} />
      ))}
    </div>
  )
}
```

### Environment Configuration

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Success Criteria
- All API calls go through centralized client
- JWT automatically attached to authenticated requests
- Expired tokens refreshed transparently
- API responses validated with Zod schemas
- Type safety enforced throughout
- Proper error handling and user feedback

---

## 4. State & Error Handling

### Purpose
Manage application state effectively with proper loading, error, and success states, providing clear feedback to users for all operations.

### Key Capabilities
- **Loading States**: Show progress during async operations
- **Error Boundaries**: Catch and display errors gracefully
- **Optimistic Updates**: Update UI before server confirmation
- **Form State**: Manage form inputs and validation
- **Toast Notifications**: Provide feedback for user actions

### React Query Integration

```typescript
// lib/query-client.ts
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      retry: 1,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 0,
    },
  },
})

// providers/query-provider.tsx
'use client'

import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from '@/lib/query-client'
import { ReactNode } from 'react'

export function QueryProvider({ children }: { children: ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}
```

### Query Hook Pattern

```typescript
// hooks/use-tasks.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getTasks, createTask, updateTask, deleteTask, Task, TaskCreate, TaskUpdate } from '@/lib/api/tasks'
import { useToast } from '@/hooks/use-toast'

export function useTasks() {
  return useQuery({
    queryKey: ['tasks'],
    queryFn: getTasks,
  })
}

export function useTask(id: number) {
  return useQuery({
    queryKey: ['tasks', id],
    queryFn: () => getTask(id),
    enabled: !!id,
  })
}

export function useCreateTask() {
  const queryClient = useQueryClient()
  const { toast } = useToast()

  return useMutation({
    mutationFn: createTask,
    onSuccess: (newTask) => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: ['tasks'] })

      toast({
        title: 'Task created',
        description: `"${newTask.title}" has been created successfully.`,
      })
    },
    onError: (error) => {
      toast({
        title: 'Failed to create task',
        description: error instanceof Error ? error.message : 'Unknown error',
        variant: 'destructive',
      })
    },
  })
}

export function useUpdateTask() {
  const queryClient = useQueryClient()
  const { toast } = useToast()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: TaskUpdate }) =>
      updateTask(id, data),
    onMutate: async ({ id, data }) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['tasks', id] })

      // Snapshot previous value
      const previousTask = queryClient.getQueryData<Task>(['tasks', id])

      // Optimistically update
      if (previousTask) {
        queryClient.setQueryData<Task>(['tasks', id], {
          ...previousTask,
          ...data,
        })
      }

      return { previousTask }
    },
    onError: (error, variables, context) => {
      // Rollback on error
      if (context?.previousTask) {
        queryClient.setQueryData(['tasks', variables.id], context.previousTask)
      }

      toast({
        title: 'Failed to update task',
        description: error instanceof Error ? error.message : 'Unknown error',
        variant: 'destructive',
      })
    },
    onSuccess: (updatedTask) => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })

      toast({
        title: 'Task updated',
        description: 'Your changes have been saved.',
      })
    },
  })
}

export function useDeleteTask() {
  const queryClient = useQueryClient()
  const { toast } = useToast()

  return useMutation({
    mutationFn: deleteTask,
    onSuccess: (_, deletedId) => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      queryClient.removeQueries({ queryKey: ['tasks', deletedId] })

      toast({
        title: 'Task deleted',
        description: 'Task has been permanently deleted.',
      })
    },
    onError: (error) => {
      toast({
        title: 'Failed to delete task',
        description: error instanceof Error ? error.message : 'Unknown error',
        variant: 'destructive',
      })
    },
  })
}
```

### Component with Query

```tsx
// components/task-list.tsx
'use client'

import { useTasks } from '@/hooks/use-tasks'
import { TaskCard } from './task-card'
import { Skeleton } from '@/components/ui/skeleton'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { AlertCircle } from 'lucide-react'

export function TaskList() {
  const { data: tasks, isLoading, error } = useTasks()

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <Skeleton key={i} className="h-24 w-full" />
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>
          {error instanceof Error ? error.message : 'Failed to load tasks'}
        </AlertDescription>
      </Alert>
    )
  }

  if (!tasks || tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">No tasks yet. Create your first one!</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  )
}
```

### Form State Management

```tsx
// components/task-form.tsx
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { TaskCreateSchema, TaskCreate } from '@/lib/api/tasks'
import { useCreateTask } from '@/hooks/use-tasks'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

export function TaskForm({ onSuccess }: { onSuccess?: () => void }) {
  const createTask = useCreateTask()

  const form = useForm<TaskCreate>({
    resolver: zodResolver(TaskCreateSchema),
    defaultValues: {
      title: '',
      description: '',
      priority: 'medium',
    },
  })

  const onSubmit = async (data: TaskCreate) => {
    await createTask.mutateAsync(data)
    form.reset()
    onSuccess?.()
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="title">Title *</Label>
        <Input
          id="title"
          {...form.register('title')}
          placeholder="Task title"
          disabled={createTask.isPending}
        />
        {form.formState.errors.title && (
          <p className="text-sm text-destructive">
            {form.formState.errors.title.message}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">Description</Label>
        <Textarea
          id="description"
          {...form.register('description')}
          placeholder="Optional description"
          disabled={createTask.isPending}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="priority">Priority</Label>
        <Select
          value={form.watch('priority')}
          onValueChange={(value) => form.setValue('priority', value as any)}
          disabled={createTask.isPending}
        >
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="low">Low</SelectItem>
            <SelectItem value="medium">Medium</SelectItem>
            <SelectItem value="high">High</SelectItem>
            <SelectItem value="urgent">Urgent</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <Button type="submit" disabled={createTask.isPending}>
        {createTask.isPending ? 'Creating...' : 'Create Task'}
      </Button>
    </form>
  )
}
```

### Toast Notifications

```tsx
// components/ui/toaster.tsx
'use client'

import { useToast } from '@/hooks/use-toast'
import {
  Toast,
  ToastClose,
  ToastDescription,
  ToastProvider,
  ToastTitle,
  ToastViewport,
} from '@/components/ui/toast'

export function Toaster() {
  const { toasts } = useToast()

  return (
    <ToastProvider>
      {toasts.map(({ id, title, description, action, ...props }) => (
        <Toast key={id} {...props}>
          <div className="grid gap-1">
            {title && <ToastTitle>{title}</ToastTitle>}
            {description && <ToastDescription>{description}</ToastDescription>}
          </div>
          {action}
          <ToastClose />
        </Toast>
      ))}
      <ToastViewport />
    </ToastProvider>
  )
}
```

### Success Criteria
- Loading states shown for all async operations
- Errors displayed with helpful messages
- Optimistic updates for instant UI feedback
- Form validation with clear error messages
- Toast notifications for user actions
- Global error boundary catches unexpected errors

---

## 5. Responsive Design Principles

### Purpose
Build user interfaces that adapt seamlessly across all device sizes using mobile-first design, flexible layouts, and Tailwind CSS utilities.

### Key Capabilities
- **Mobile-First Approach**: Design for small screens first, enhance for larger
- **Breakpoint Management**: Use consistent breakpoints across the app
- **Flexible Layouts**: Leverage CSS Grid and Flexbox for adaptive layouts
- **Responsive Typography**: Scale text appropriately for screen size
- **Touch Targets**: Ensure interactive elements are appropriately sized

### Tailwind Breakpoints

```text
Breakpoint prefix | Minimum width | CSS
------------------|---------------|-----
sm                | 640px         | @media (min-width: 640px) { ... }
md                | 768px         | @media (min-width: 768px) { ... }
lg                | 1024px        | @media (min-width: 1024px) { ... }
xl                | 1280px        | @media (min-width: 1280px) { ... }
2xl               | 1536px        | @media (min-width: 1536px) { ... }
```

### Responsive Layout Pattern

```tsx
// app/(dashboard)/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-background">
      {/* Mobile: Stacked | Desktop: Sidebar */}
      <div className="flex flex-col md:flex-row">
        {/* Sidebar - hidden on mobile, shown on md+ */}
        <aside className="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0">
          <Sidebar />
        </aside>

        {/* Main content */}
        <main className="flex-1 md:pl-64">
          {/* Mobile header with menu */}
          <MobileHeader className="md:hidden" />

          {/* Desktop header */}
          <Header className="hidden md:block" />

          {/* Content area with responsive padding */}
          <div className="p-4 sm:p-6 lg:p-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
```

### Responsive Grid Pattern

```tsx
// components/task-grid.tsx
export function TaskGrid({ tasks }: { tasks: Task[] }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 lg:gap-6">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  )
}
```

### Responsive Typography

```tsx
// components/page-header.tsx
export function PageHeader({
  title,
  description,
}: {
  title: string
  description?: string
}) {
  return (
    <div className="space-y-2">
      {/* Mobile: text-2xl, Desktop: text-4xl */}
      <h1 className="text-2xl font-bold tracking-tight sm:text-3xl lg:text-4xl">
        {title}
      </h1>

      {description && (
        <p className="text-sm sm:text-base text-muted-foreground max-w-3xl">
          {description}
        </p>
      )}
    </div>
  )
}
```

### Responsive Navigation

```tsx
// components/mobile-header.tsx
'use client'

import { useState } from 'react'
import { Menu, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { Sidebar } from './sidebar'

export function MobileHeader({ className }: { className?: string }) {
  const [open, setOpen] = useState(false)

  return (
    <header className={className}>
      <div className="flex items-center justify-between h-16 px-4 border-b">
        <h1 className="text-xl font-bold">Task Manager</h1>

        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon">
              <Menu className="h-6 w-6" />
              <span className="sr-only">Open menu</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-64 p-0">
            <Sidebar onNavigate={() => setOpen(false)} />
          </SheetContent>
        </Sheet>
      </div>
    </header>
  )
}
```

### Responsive Card Pattern

```tsx
// components/task-card.tsx
export function TaskCard({ task }: { task: Task }) {
  return (
    <div className="
      flex flex-col
      p-4 sm:p-6
      space-y-3 sm:space-y-4
      border rounded-lg
      hover:shadow-md
      transition-shadow
    ">
      {/* Header: Stack on mobile, row on desktop */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <h3 className="text-lg sm:text-xl font-semibold line-clamp-2">
          {task.title}
        </h3>
        <TaskStatusBadge status={task.status} />
      </div>

      {/* Description: Truncate on mobile */}
      {task.description && (
        <p className="text-sm text-muted-foreground line-clamp-2 sm:line-clamp-3">
          {task.description}
        </p>
      )}

      {/* Footer: Stack on mobile, row on desktop */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 sm:gap-4 pt-2">
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <Calendar className="h-4 w-4" />
          <span>{formatDate(task.due_date)}</span>
        </div>

        {/* Actions: Full width on mobile, auto on desktop */}
        <div className="flex gap-2 sm:w-auto">
          <Button variant="outline" size="sm" className="flex-1 sm:flex-none">
            Edit
          </Button>
          <Button variant="destructive" size="sm" className="flex-1 sm:flex-none">
            Delete
          </Button>
        </div>
      </div>
    </div>
  )
}
```

### Container Pattern

```tsx
// components/container.tsx
import { cn } from '@/lib/utils'

export function Container({
  children,
  className,
}: {
  children: React.ReactNode
  className?: string
}) {
  return (
    <div className={cn(
      'mx-auto',
      'w-full',
      'px-4 sm:px-6 lg:px-8',
      'max-w-7xl',
      className
    )}>
      {children}
    </div>
  )
}
```

### Responsive Table Pattern

```tsx
// components/task-table.tsx
export function TaskTable({ tasks }: { tasks: Task[] }) {
  return (
    <>
      {/* Desktop: Table view */}
      <div className="hidden md:block">
        <table className="w-full">
          <thead>
            <tr className="border-b">
              <th className="text-left py-3 px-4">Title</th>
              <th className="text-left py-3 px-4">Status</th>
              <th className="text-left py-3 px-4">Priority</th>
              <th className="text-left py-3 px-4">Due Date</th>
              <th className="text-right py-3 px-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map((task) => (
              <tr key={task.id} className="border-b">
                <td className="py-3 px-4">{task.title}</td>
                <td className="py-3 px-4">
                  <TaskStatusBadge status={task.status} />
                </td>
                <td className="py-3 px-4">
                  <TaskPriorityBadge priority={task.priority} />
                </td>
                <td className="py-3 px-4">{formatDate(task.due_date)}</td>
                <td className="py-3 px-4 text-right">
                  <TaskActions task={task} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile: Card view */}
      <div className="md:hidden space-y-4">
        {tasks.map((task) => (
          <TaskCard key={task.id} task={task} />
        ))}
      </div>
    </>
  )
}
```

### Touch Target Guidelines

```tsx
// Minimum touch target: 44x44px (following WCAG guidelines)

// ❌ Too small for mobile
<button className="p-1">
  <Icon className="h-4 w-4" />
</button>

// ✅ Proper touch target
<button className="p-3 min-h-[44px] min-w-[44px] flex items-center justify-center">
  <Icon className="h-5 w-5" />
</button>

// ✅ Using Tailwind utilities
<Button size="icon" className="h-11 w-11">
  <Icon className="h-5 w-5" />
</Button>
```

### Responsive Utilities

```tsx
// Hide on mobile, show on desktop
<div className="hidden md:block">Desktop only</div>

// Show on mobile, hide on desktop
<div className="md:hidden">Mobile only</div>

// Different layouts per breakpoint
<div className="
  flex
  flex-col        /* Mobile: vertical stack */
  sm:flex-row     /* Tablet+: horizontal row */
  lg:grid         /* Desktop: grid layout */
  lg:grid-cols-3
">
  {/* Content */}
</div>

// Responsive spacing
<div className="
  p-4           /* Mobile: 16px padding */
  sm:p-6        /* Tablet: 24px padding */
  lg:p-8        /* Desktop: 32px padding */
">
  {/* Content */}
</div>

// Responsive text sizes
<h1 className="
  text-2xl      /* Mobile: 1.5rem */
  sm:text-3xl   /* Tablet: 1.875rem */
  lg:text-4xl   /* Desktop: 2.25rem */
  font-bold
">
  Heading
</h1>
```

### Success Criteria
- Mobile-first approach in all components
- Consistent breakpoint usage (sm, md, lg, xl)
- Touch targets minimum 44x44px
- No horizontal scrolling on any screen size
- Readable text sizes across all devices
- Interactive elements properly sized for touch
- Tables switch to cards on mobile

---

## Integration Example: Complete Feature with All Skills

```tsx
// app/(dashboard)/tasks/page.tsx
import { Suspense } from 'react'
import { PageHeader } from '@/components/page-header'
import { TaskList } from '@/components/task-list'
import { TaskListSkeleton } from '@/components/task-list-skeleton'
import { CreateTaskDialog } from '@/components/create-task-dialog'
import { Container } from '@/components/container'

export const metadata = {
  title: 'Tasks | Task Manager',
  description: 'Manage your tasks efficiently',
}

export default function TasksPage() {
  return (
    <Container>
      {/* Responsive page header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <PageHeader
          title="Tasks"
          description="Organize and track your work"
        />
        <CreateTaskDialog />
      </div>

      {/* Suspense boundary with loading state */}
      <Suspense fallback={<TaskListSkeleton />}>
        <TaskList />
      </Suspense>
    </Container>
  )
}

// components/task-list.tsx
'use client'

import { useTasks } from '@/hooks/use-tasks'
import { TaskCard } from './task-card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { AlertCircle } from 'lucide-react'

export function TaskList() {
  const { data: tasks, isLoading, error } = useTasks()

  if (isLoading) {
    return <TaskListSkeleton />
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>
          {error instanceof Error ? error.message : 'Failed to load tasks'}
        </AlertDescription>
      </Alert>
    )
  }

  if (!tasks || tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">
          No tasks yet. Create your first one!
        </p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  )
}

// components/create-task-dialog.tsx
'use client'

import { useState } from 'react'
import { useCreateTask } from '@/hooks/use-tasks'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Plus } from 'lucide-react'
import { TaskForm } from './task-form'

export function CreateTaskDialog() {
  const [open, setOpen] = useState(false)

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="w-full sm:w-auto">
          <Plus className="h-4 w-4 mr-2" />
          New Task
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Create New Task</DialogTitle>
        </DialogHeader>
        <TaskForm onSuccess={() => setOpen(false)} />
      </DialogContent>
    </Dialog>
  )
}
```

---

## References

- Next.js App Router: https://nextjs.org/docs/app
- React Documentation: https://react.dev/
- TanStack Query: https://tanstack.com/query/latest
- React Hook Form: https://react-hook-form.com/
- Zod Validation: https://zod.dev/
- Tailwind CSS: https://tailwindcss.com/
- shadcn/ui Components: https://ui.shadcn.com/
- WCAG Touch Target Guidelines: https://www.w3.org/WAI/WCAG21/Understanding/target-size.html
- `.specify/memory/constitution.md` - Project-specific frontend standards
