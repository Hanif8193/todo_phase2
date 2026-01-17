# Phase II Todo App - Startup Guide

## Current Status

### ✅ COMPLETED
- All backend code files created
- All frontend code files created
- Backend virtual environment created
- Backend dependencies: INSTALLING (in progress)
- Frontend .env.local created

### ⚠️ ISSUES
- **Disk Space**: C: drive has limited space (279MB free)
- Frontend dependencies NOT installed (need ~2-3GB for node_modules)
- Backend .env needs configuration

## Quick Start

### 1. Configure Backend Environment

Edit `backend/.env` and set these values:

```bash
# Get DATABASE_URL from https://console.neon.tech/
DATABASE_URL=postgresql://user:password@your-host.neon.tech/your-db?sslmode=require

# Generate secret: openssl rand -base64 32
BETTER_AUTH_SECRET=your_32_character_secret_here

# Keep these as-is
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

### 2. Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate
# If dependencies not fully installed:
pip install -r requirements.txt

# Start server
uvicorn main:app --reload
```

Backend will run at: http://localhost:8000

### 3. Install Frontend Dependencies (Terminal 2)

**⚠️ REQUIRES 2-3GB FREE DISK SPACE**

If you have space:
```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

Frontend will run at: http://localhost:3000

### 4. Free Disk Space (If Needed)

To install frontend dependencies:
1. Empty Recycle Bin
2. Clear Windows TEMP folder
3. Run Disk Cleanup
4. Remove unused applications

## API Documentation

Once backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables Required

**Backend (.env)**:
- DATABASE_URL (from Neon)
- BETTER_AUTH_SECRET (generate with openssl)

**Frontend (.env.local)** (already created):
- NEXT_PUBLIC_API_URL=http://localhost:8000

## Troubleshooting

### Backend won't start
- Check DATABASE_URL is correct
- Ensure BETTER_AUTH_SECRET is at least 32 characters
- Verify venv is activated

### Frontend won't install
- Check available disk space: `df -h`
- Need ~3GB free on C: drive
- Try: `npm cache clean --force`

### CORS errors
- Ensure CORS_ORIGINS in backend/.env includes frontend URL
- Default: http://localhost:3000

## Files Created

### Backend
- main.py - FastAPI app
- models.py - User & Task models
- auth.py - JWT authentication
- db.py - Database connection
- config.py - Environment config
- routes/auth.py - Auth endpoints
- routes/tasks.py - Task CRUD endpoints

### Frontend
- app/page.tsx - Landing page
- app/layout.tsx - Root layout
- app/signup/page.tsx - User registration
- app/signin/page.tsx - User login  
- app/dashboard/page.tsx - Task management
- components/AuthProvider.tsx - Auth context
- components/TaskList.tsx - Task display
- components/TaskForm.tsx - Task create/edit
- components/TaskItem.tsx - Task actions
- lib/auth.ts - Auth client
- lib/api.ts - API client
- middleware.ts - Route protection

## Next Steps

1. Configure backend/.env with your database credentials
2. Start backend server
3. Free disk space if needed
4. Install frontend dependencies
5. Start frontend server
6. Visit http://localhost:3000

**Implementation is complete. Only configuration and disk space needed.**
