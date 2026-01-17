# Phase II - Todo Full-Stack Web Application

A secure, multi-user web-based todo application with full authentication, database persistence, and user-scoped data isolation.

## Overview

This project implements a modern todo application using:
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS, Better Auth
- **Backend**: FastAPI (Python), SQLModel ORM, JWT authentication
- **Database**: Neon Serverless PostgreSQL

## Features

- User account creation and secure authentication (JWT-based)
- Full CRUD operations on tasks (Create, Read, Update, Delete)
- Task completion tracking with visual feedback
- Multi-user data isolation (users can only access their own tasks)
- Responsive web interface for desktop and mobile
- Persistent task storage in PostgreSQL

## Project Structure

```
todo_phase2/
├── backend/                 # FastAPI backend
│   ├── main.py             # Application entry point
│   ├── db.py               # Database connection
│   ├── models.py           # SQLModel schemas (User, Task)
│   ├── auth.py             # JWT middleware
│   ├── config.py           # Environment configuration
│   ├── routes/             # API endpoints
│   │   ├── auth.py         # Authentication routes
│   │   └── tasks.py        # Task CRUD routes
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Backend environment variables (create from .env.example)
│
├── frontend/                # Next.js frontend
│   ├── app/                # Next.js App Router
│   │   ├── layout.tsx      # Root layout with auth provider
│   │   ├── page.tsx        # Landing page
│   │   ├── signin/         # Sign-in page
│   │   ├── signup/         # Sign-up page
│   │   └── dashboard/      # Task management dashboard (protected)
│   ├── components/         # React components
│   │   ├── TaskList.tsx    # Task list display
│   │   ├── TaskForm.tsx    # Task create/edit form
│   │   └── TaskItem.tsx    # Individual task item
│   ├── lib/                # Utilities
│   │   ├── api.ts          # API client with JWT injection
│   │   └── auth.ts         # Better Auth configuration
│   ├── package.json        # Node dependencies
│   └── .env.local          # Frontend environment variables (create from .env.example)
│
├── specs/                   # Design documentation
│   └── 001-fullstack-web-app/
│       ├── spec.md         # Feature specification
│       ├── plan.md         # Implementation plan
│       ├── tasks.md        # Task breakdown
│       ├── data-model.md   # Database schema
│       ├── quickstart.md   # Testing guide
│       └── contracts/      # API contracts
│
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Neon PostgreSQL account (free tier available at https://neon.tech)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd todo_phase2
```

### 2. Configure Environment Variables

```bash
# Copy the example file
cp .env.example backend/.env
cp .env.example frontend/.env.local

# Generate a secure secret (run this command)
openssl rand -base64 32

# Edit both files and set:
# - BETTER_AUTH_SECRET (use the same value in both files!)
# - DATABASE_URL (from your Neon dashboard)
# - Other variables as needed
```

**CRITICAL**: The `BETTER_AUTH_SECRET` MUST be identical in both `backend/.env` and `frontend/.env.local`.

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at http://localhost:8000

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Frontend will be available at http://localhost:3000

## Usage

### First-Time Setup

1. Navigate to http://localhost:3000
2. Click "Sign Up" to create a new account
3. Enter email and password (minimum 8 characters)
4. You'll be automatically signed in after registration
5. Start creating tasks on the dashboard

### Creating Tasks

1. Sign in to your account
2. On the dashboard, use the task form to create new tasks
3. Enter a title (required) and optional description
4. Click "Add Task" to save

### Managing Tasks

- **Edit**: Click the edit button on any task to modify its details
- **Complete**: Check the checkbox to mark a task as complete
- **Delete**: Click the delete button to remove a task
- **View**: All your tasks are displayed in a list with completion status

### Data Isolation

- Each user's tasks are completely isolated
- You can only see and modify your own tasks
- The backend enforces user authentication on every API request
- Attempting to access another user's tasks will return a 403 Forbidden error

## API Endpoints

### Authentication

- `POST /auth/signup` - Create new account
- `POST /auth/signin` - Sign in with credentials
- `POST /auth/signout` - Sign out (invalidate token)

### Tasks

All task endpoints require JWT authentication via `Authorization: Bearer <token>` header.

- `GET /api/{user_id}/tasks` - List all user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get single task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status

See `specs/001-fullstack-web-app/contracts/` for detailed API specifications.

## Testing

### Manual Testing Workflow

1. **Create Account**
   - Navigate to signup page
   - Enter valid email and password
   - Verify automatic signin after registration

2. **Task CRUD Operations**
   - Create a new task
   - Edit the task title and description
   - Mark the task as complete
   - Mark it incomplete again
   - Delete the task

3. **Data Persistence**
   - Create several tasks
   - Refresh the browser
   - Verify all tasks are still present

4. **Multi-User Isolation (Two-User Test)**
   - Open a second browser (or incognito window)
   - Create a second account with different email (e.g., user2@example.com)
   - Create tasks in both accounts (e.g., "User 1 Task" and "User 2 Task")
   - Verify that tasks are completely isolated:
     - User 1 should only see tasks created by User 1
     - User 2 should only see tasks created by User 2
     - Neither user can see the other's tasks in the UI
   - **API Manipulation Test** (Advanced):
     - While signed in as User 1, try to access User 2's tasks by:
       - Manually changing the `user_id` in API requests
       - Attempting to GET /api/{user_2_id}/tasks with User 1's token
     - Verify that the API returns 403 Forbidden error
     - Confirm that User 1's JWT token cannot access User 2's resources

See `specs/001-fullstack-web-app/quickstart.md` for detailed testing scenarios.

## Security Features

- **JWT Authentication**: Stateless token-based authentication with 7-day expiry
- **Password Hashing**: Passwords are hashed using bcrypt (never stored in plaintext)
- **User Isolation**: Database queries are filtered by authenticated user ID
- **CORS Protection**: Backend only accepts requests from configured frontend origin
- **SQL Injection Prevention**: SQLModel ORM provides parameterized queries
- **Authorization Checks**: Every API endpoint validates JWT and user ownership

## Development

### Running Tests

```bash
# Backend tests (when available)
cd backend
pytest

# Frontend tests (when available)
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
flake8 .

# Frontend linting
cd frontend
npm run lint
```

### Database Migrations

Database schema is automatically created on first run via SQLModel's `create_all()` function. For production deployments, consider using Alembic for migrations.

## Troubleshooting

### Backend won't start

- Verify `DATABASE_URL` is correctly formatted in `backend/.env`
- Ensure Neon database is accessible and SSL is enabled
- Check that all Python dependencies are installed

### Frontend won't start

- Run `npm install` in the frontend directory
- Verify Node.js version is 18 or higher
- Clear `.next` cache: `rm -rf .next && npm run dev`

### Authentication fails

- Ensure `BETTER_AUTH_SECRET` is identical in both `.env` files
- Check that the secret is at least 32 characters long
- Verify backend is running and accessible at the configured API URL

### CORS errors

- Check that `CORS_ORIGINS` in `backend/.env` matches your frontend URL
- For development, should be `http://localhost:3000`
- For production, update to your deployed frontend domain

## Production Deployment

### Backend Deployment

1. Set environment variables on your hosting platform
2. Use a production WSGI server like Gunicorn:
   ```bash
   gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
   ```
3. Enable HTTPS (required for secure authentication)
4. Update CORS_ORIGINS to your frontend domain

### Frontend Deployment

1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Deploy to Vercel, Netlify, or similar platform
3. Set environment variables in deployment settings
4. Update `NEXT_PUBLIC_API_URL` to your production backend URL

## Documentation

- Full specification: `specs/001-fullstack-web-app/spec.md`
- Implementation plan: `specs/001-fullstack-web-app/plan.md`
- Task breakdown: `specs/001-fullstack-web-app/tasks.md`
- Database schema: `specs/001-fullstack-web-app/data-model.md`
- API contracts: `specs/001-fullstack-web-app/contracts/`
- Testing guide: `specs/001-fullstack-web-app/quickstart.md`

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please refer to the project documentation in the `specs/` directory.
