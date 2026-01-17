# Quickstart Guide - Todo Full-Stack Web Application

**Feature**: Phase II - Todo Full-Stack Web Application
**Date**: 2026-01-17
**Status**: COMPLETE

## Overview

This guide provides step-by-step instructions for setting up the development environment, running the application locally, and testing all features. Follow these instructions to get the Todo application running on your machine.

---

## Prerequisites

### Required Software

| Software | Minimum Version | Purpose | Installation Link |
|----------|----------------|---------|-------------------|
| **Node.js** | 18.x or higher | Frontend runtime | [nodejs.org](https://nodejs.org) |
| **npm** | 9.x or higher | Frontend package manager | Included with Node.js |
| **Python** | 3.11 or higher | Backend runtime | [python.org](https://python.org) |
| **pip** | 23.x or higher | Python package manager | Included with Python |
| **Git** | Any recent version | Version control | [git-scm.com](https://git-scm.com) |

### Required Accounts

1. **Neon PostgreSQL Account**
   - Sign up at [neon.tech](https://neon.tech)
   - Create a new project
   - Copy the connection string from the dashboard

### Verify Installations

```bash
# Check Node.js version
node --version
# Expected: v18.x.x or higher

# Check npm version
npm --version
# Expected: 9.x.x or higher

# Check Python version
python --version
# Expected: Python 3.11.x or higher

# Check pip version
pip --version
# Expected: pip 23.x.x or higher
```

---

## Project Setup

### 1. Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd todo_phase2

# Checkout the feature branch
git checkout 001-fullstack-web-app
```

### 2. Generate Shared Secret

Generate a cryptographically secure secret for JWT token signing/verification:

```bash
# Generate 32-byte random secret (base64 encoded)
openssl rand -base64 32
```

**Example output**:
```
7xK9mP2qR8vN4bW6tY1sL0cE3hF5gJ8dA7zX9wU2oI4=
```

**IMPORTANT**: Copy this secret exactly. You'll use it in both frontend and backend `.env` files.

### 3. Configure Backend Environment

Create backend environment file:

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` with your values:

```env
# Database Configuration
DATABASE_URL="postgresql+asyncpg://user:password@host.region.aws.neon.tech/dbname?sslmode=require"

# JWT Secret (MUST match frontend)
BETTER_AUTH_SECRET="7xK9mP2qR8vN4bW6tY1sL0cE3hF5gJ8dA7zX9wU2oI4="

# Backend Configuration
HOST="0.0.0.0"
PORT=8000
```

**Getting DATABASE_URL from Neon**:
1. Go to [Neon Dashboard](https://console.neon.tech)
2. Select your project
3. Go to "Connection Details"
4. Copy the connection string
5. **IMPORTANT**: Change `postgresql://` to `postgresql+asyncpg://` for asyncpg driver

### 4. Configure Frontend Environment

Create frontend environment file:

```bash
cd ../frontend
cp .env.example .env.local
```

Edit `frontend/.env.local` with your values:

```env
# JWT Secret (MUST match backend)
BETTER_AUTH_SECRET="7xK9mP2qR8vN4bW6tY1sL0cE3hF5gJ8dA7zX9wU2oI4="

# Backend API URL
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

**CRITICAL**: Ensure `BETTER_AUTH_SECRET` is **EXACTLY** the same in both files (including quotes/whitespace).

### 5. Install Dependencies

**Backend**:
```bash
cd backend
pip install -r requirements.txt
```

Expected packages:
- fastapi
- uvicorn[standard]
- sqlmodel
- asyncpg
- python-jose[cryptography]
- passlib[bcrypt]
- better-auth (if used on backend)

**Frontend**:
```bash
cd ../frontend
npm install
```

Expected packages:
- next@16+
- react@18+
- better-auth
- tailwindcss

---

## Running the Application

### Start Backend Server

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify backend is running**:
```bash
curl http://localhost:8000/
# Expected: {"message": "Todo API is running"}
```

### Start Frontend Server

In a **new terminal**:

```bash
cd frontend
npm run dev
```

**Expected output**:
```
▲ Next.js 16.x.x
- Local:        http://localhost:3000
- Ready in 2.5s
```

**Verify frontend is running**:
Open browser to [http://localhost:3000](http://localhost:3000)

---

## Testing the Application

### Test 1: User Signup

1. Navigate to http://localhost:3000/signup
2. Enter email: `testuser@example.com`
3. Enter password: `testpassword123`
4. Click "Sign Up"

**Expected Result**:
- Account created successfully
- Automatically signed in
- Redirected to dashboard at `/dashboard`
- Dashboard shows "Welcome, testuser@example.com"

**Troubleshooting**:
- **Error: "Email already registered"** → Email exists, use different email or go to signin
- **Error: "Password too short"** → Use minimum 8 characters
- **Error: "Database connection failed"** → Check `DATABASE_URL` in backend `.env`
- **Error: "JWT verification failed"** → Ensure `BETTER_AUTH_SECRET` matches in both `.env` files

### Test 2: Create Task

1. On dashboard, click "Add Task" (or similar button)
2. Enter title: `Complete project documentation`
3. Enter description: `Write comprehensive docs for Phase II`
4. Click "Create" or "Save"

**Expected Result**:
- Task appears in task list
- Task shows title, description, and incomplete status
- Task has checkbox or toggle for completion

**Troubleshooting**:
- **Error: "Title is required"** → Enter a title
- **Error: "Unauthorized"** → Token expired, sign in again
- **Task doesn't appear** → Check browser console for API errors

### Test 3: Mark Task Complete

1. Click checkbox or toggle next to task
2. Wait for UI update

**Expected Result**:
- Task visually changes (e.g., strikethrough, different color, checkmark)
- Task completion status persists on page refresh

**Troubleshooting**:
- **Task reverts to incomplete** → Check network tab for failed API request
- **No visual change** → Check frontend implementation of completion styles

### Test 4: Edit Task

1. Click "Edit" button on task (or click task to open detail view)
2. Change title to: `Updated project documentation`
3. Change description to: `Updated description with more details`
4. Click "Save"

**Expected Result**:
- Task updates with new title and description
- Changes persist on page refresh

### Test 5: Delete Task

1. Click "Delete" button on task
2. Confirm deletion (if confirmation dialog exists)

**Expected Result**:
- Task disappears from list
- Task is permanently removed (doesn't reappear on refresh)

### Test 6: Data Persistence

1. Refresh the page (F5 or Cmd+R)

**Expected Result**:
- User remains signed in
- All tasks still visible with correct data
- No data loss

### Test 7: Sign Out and Sign In

1. Click "Sign Out" button
2. Verify redirected to signin page at `/signin`
3. Enter email: `testuser@example.com`
4. Enter password: `testpassword123`
5. Click "Sign In"

**Expected Result**:
- Successfully signed in
- Redirected to dashboard
- All previously created tasks visible

### Test 8: Multi-User Isolation

1. Open a **new incognito/private browser window**
2. Navigate to http://localhost:3000/signup
3. Create a second account: `testuser2@example.com` / `password123`
4. Create a task: `User 2's task`
5. Switch back to first browser window (still signed in as testuser@example.com)

**Expected Result**:
- First user (testuser@example.com) sees ONLY their tasks
- Second user (testuser2@example.com) sees ONLY their tasks
- No cross-user data visibility

**Security Test** (Advanced):
1. While signed in as User 1, note the task ID in URL or network tab
2. Try to access User 2's task by manipulating URL or API request
3. Example: Change `user_id` in URL from `123` to `456`

**Expected Result**:
- API returns `403 Forbidden` error
- Message: "Cannot access other user's tasks"
- No data leakage

---

## Common Issues and Solutions

### Issue 1: Backend Won't Start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
cd backend
pip install -r requirements.txt
```

---

### Issue 2: Database Connection Failed

**Error**: `sqlalchemy.exc.OperationalError: could not connect to server`

**Solution**:
1. Verify `DATABASE_URL` in `backend/.env`
2. Ensure connection string starts with `postgresql+asyncpg://`
3. Check Neon dashboard for correct host/port/credentials
4. Test connection:
   ```bash
   psql "postgresql://user:pass@host/db?sslmode=require"
   ```

---

### Issue 3: JWT Verification Failed

**Error**: `401 Unauthorized: Token validation failed`

**Solution**:
1. Ensure `BETTER_AUTH_SECRET` is **identical** in both `.env` files
2. Check for extra spaces, quotes, or newlines
3. Regenerate secret and update both files:
   ```bash
   openssl rand -base64 32
   ```

---

### Issue 4: Frontend Can't Reach Backend

**Error**: `Network Error` or `Failed to fetch`

**Solution**:
1. Verify backend is running on port 8000
2. Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
3. Ensure no CORS errors in browser console
4. Test backend directly:
   ```bash
   curl http://localhost:8000/
   ```

---

### Issue 5: Tasks Not Persisting

**Symptoms**: Tasks disappear on page refresh

**Solution**:
1. Check database connection (see Issue 2)
2. Verify tables were created:
   ```bash
   psql "postgresql://..." -c "\dt"
   # Should show: users, tasks
   ```
3. Check backend logs for SQL errors
4. Ensure `init_db()` runs on startup

---

## Development Workflow

### Making Changes

**Backend Changes**:
1. Edit Python files in `backend/`
2. Server auto-reloads (thanks to `--reload` flag)
3. Test changes via API or frontend

**Frontend Changes**:
1. Edit TypeScript/React files in `frontend/`
2. Next.js auto-reloads (Hot Module Replacement)
3. Changes appear immediately in browser

### Running Tests

**Backend** (future):
```bash
cd backend
pytest
```

**Frontend** (future):
```bash
cd frontend
npm test
```

### Database Migrations

**Current (Phase II)**: Auto-create tables on startup

**Future (Alembic)**:
```bash
# Generate migration
alembic revision --autogenerate -m "Add due_date column"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

---

## API Testing (Optional)

### Using curl

**Signup**:
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"apitest@example.com","password":"password123"}'
```

**Expected response**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "apitest@example.com"
  }
}
```

**Create Task**:
```bash
# Save token from signup response
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X POST http://localhost:8000/api/1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"API test task","description":"Created via curl"}'
```

**Get Tasks**:
```bash
curl http://localhost:8000/api/1/tasks \
  -H "Authorization: Bearer $TOKEN"
```

### Using Postman

1. Import OpenAPI specs from `specs/001-fullstack-web-app/contracts/`
2. Create environment with variables:
   - `base_url`: `http://localhost:8000`
   - `token`: (set after signup/signin)
3. Run requests from collection

---

## Environment Variables Reference

### Backend (`backend/.env`)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | ✅ Yes | `postgresql+asyncpg://user:pass@host/db` | Neon PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | ✅ Yes | `7xK9mP2qR8vN4bW6tY1sL0cE3hF5gJ8d...` | JWT signing secret (min 32 chars) |
| `HOST` | ❌ No | `0.0.0.0` | Backend host (default: 0.0.0.0) |
| `PORT` | ❌ No | `8000` | Backend port (default: 8000) |

### Frontend (`frontend/.env.local`)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `BETTER_AUTH_SECRET` | ✅ Yes | `7xK9mP2qR8vN4bW6tY1sL0cE3hF5gJ8d...` | JWT signing secret (MUST match backend) |
| `NEXT_PUBLIC_API_URL` | ✅ Yes | `http://localhost:8000` | Backend API base URL |

---

## Production Deployment (Future)

### Backend Deployment

**Recommended**: Vercel, Railway, Render, or Fly.io

**Environment Variables**:
- `DATABASE_URL`: Production Neon connection string
- `BETTER_AUTH_SECRET`: Production secret (different from dev)
- `ALLOWED_ORIGINS`: Frontend production URL (for CORS)

### Frontend Deployment

**Recommended**: Vercel (optimized for Next.js)

**Environment Variables**:
- `BETTER_AUTH_SECRET`: Production secret (MUST match backend)
- `NEXT_PUBLIC_API_URL`: Production backend URL

---

## Next Steps

After completing this quickstart:

1. ✅ Verify all 8 tests pass
2. ✅ Confirm multi-user isolation works
3. ✅ Review API contracts in `specs/001-fullstack-web-app/contracts/`
4. ✅ Read data model in `specs/001-fullstack-web-app/data-model.md`
5. 🚀 Ready to run `/sp.tasks` to generate implementation tasks

---

## Support and Troubleshooting

**Common Resources**:
- Feature Spec: `specs/001-fullstack-web-app/spec.md`
- Implementation Plan: `specs/001-fullstack-web-app/plan.md`
- Data Model: `specs/001-fullstack-web-app/data-model.md`
- API Contracts: `specs/001-fullstack-web-app/contracts/`

**If Stuck**:
1. Check error messages in browser console (F12)
2. Check backend terminal for errors
3. Verify environment variables match exactly
4. Test API directly with curl/Postman
5. Review constitution: `.specify/memory/constitution.md`

---

**Quickstart Status**: ✅ COMPLETE
**Date Completed**: 2026-01-17
**Validated By**: Claude Code (Spec-Driven Development Agent)
