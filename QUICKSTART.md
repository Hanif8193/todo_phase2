# 🚀 Quick Start - Phase II Todo App

## ✅ COMPLETED SETUP
- ✅ Backend code ready
- ✅ Frontend code ready
- ✅ Python dependencies installed
- ✅ Auth secret generated (same in both .env files)

## 🔴 REQUIRED: Get Database Connection

### Step 1: Create Neon Database (2 minutes)

1. Go to https://neon.tech/
2. Click "Sign Up" (free tier available)
3. Create new project
4. Copy the connection string that looks like:
   ```
   postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require
   ```

### Step 2: Configure Backend

Edit `backend/.env` and replace line 6:

**FROM:**
```
DATABASE_URL=postgresql://user:password@your-neon-host.neon.tech/your-database?sslmode=require
```

**TO:**
```
DATABASE_URL=postgresql://your-actual-connection-string-from-neon
```

### Step 3: Start Backend

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Backend will start at:** http://localhost:8000

**Test it:** Open http://localhost:8000/docs (should see API documentation)

---

## 🎨 Frontend (Optional - Requires Disk Space)

**Current disk space:** 279MB free  
**Needed:** ~3GB for node_modules

### If You Have Space:

```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

**Frontend will start at:** http://localhost:3000

### If Low on Disk Space:

**Test backend API only** using http://localhost:8000/docs

Or free space:
1. Empty Recycle Bin
2. Clear `C:\Users\PMLS\AppData\Local\Temp`
3. Run Windows Disk Cleanup

---

## 🧪 Test the Backend API

Once backend is running, visit http://localhost:8000/docs and try:

### 1. Create User (Sign Up)
```json
POST /auth/signup
{
  "email": "test@example.com",
  "password": "testpassword123"
}
```

### 2. Sign In
```json
POST /auth/signin
{
  "email": "test@example.com",
  "password": "testpassword123"
}
```
Copy the `token` from response.

### 3. Create Task
```json
POST /api/{user_id}/tasks
Authorization: Bearer {your_token}
{
  "title": "My first task",
  "description": "Testing the API"
}
```

### 4. Get All Tasks
```json
GET /api/{user_id}/tasks
Authorization: Bearer {your_token}
```

---

## 📁 Configuration Summary

### backend/.env
```bash
DATABASE_URL=postgresql://...  # ⚠️ YOU MUST SET THIS
BETTER_AUTH_SECRET=8Hy2Et+f5MyiCJckbs8leUTAVfc4YdoOIvurEWmtKaY=  # ✅ Already set
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

### frontend/.env.local
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000  # ✅ Already set
BETTER_AUTH_SECRET=8Hy2Et+f5MyiCJckbs8leUTAVfc4YdoOIvurEWmtKaY=  # ✅ Already set
```

---

## ⚡ Next Steps

1. **Now:** Get Neon database connection string
2. **Then:** Update `backend/.env` with DATABASE_URL
3. **Finally:** Run `uvicorn main:app --reload` in backend directory

**That's it!** Your backend will be fully functional.

Frontend can wait until you free disk space.
