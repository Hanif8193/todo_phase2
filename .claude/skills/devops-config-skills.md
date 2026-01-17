# DevOps & Configuration Skills

## Overview
This document defines DevOps and configuration management skills for full-stack applications, covering environment variable management, secure secrets handling, monorepo organization, and Neon PostgreSQL setup. These skills ensure proper configuration across development, staging, and production environments.

---

## 1. Environment Variable Management

### Purpose
Manage configuration across different environments (development, staging, production) using environment variables, ensuring separation of concerns and preventing configuration drift.

### Key Capabilities
- **Environment Separation**: Maintain distinct configs for dev/staging/production
- **Variable Validation**: Ensure required variables are present and valid
- **Type Safety**: Leverage TypeScript for environment variable typing
- **Fallback Handling**: Provide sensible defaults where appropriate
- **Runtime vs Build-time**: Understand when variables are resolved

### Environment File Structure

```text
Project Root
├── .env.example          # Template with all required variables (committed)
├── .env                  # Local development (gitignored)
├── .env.local            # Local overrides (gitignored)
├── .env.development      # Development defaults (optional, committed)
├── .env.production       # Production defaults (optional, committed)
│
├── backend/
│   ├── .env.example      # Backend-specific template
│   └── .env              # Backend local config (gitignored)
│
└── frontend/
    ├── .env.example      # Frontend-specific template
    ├── .env.local        # Frontend local config (gitignored)
    └── .env.production   # Frontend prod config (gitignored)
```

### .gitignore Configuration

```gitignore
# Environment files
.env
.env.local
.env.*.local
.env.development.local
.env.test.local
.env.production.local

# Exception: Allow templates and defaults
!.env.example
!.env.development
!.env.production
```

### Backend Environment Variables (FastAPI)

```bash
# backend/.env.example
# Copy this to .env and fill in actual values

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
# For Neon PostgreSQL:
# DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.neon.tech/dbname?sslmode=require

# Authentication
JWT_SECRET_KEY=your-secret-key-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Environment
ENVIRONMENT=development  # development, staging, production

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Feature Flags
ENABLE_EMAIL_VERIFICATION=false
ENABLE_RATE_LIMITING=false

# External Services (if needed)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=

# Monitoring (production)
SENTRY_DSN=
```

### Backend Environment Validation (Python)

```python
# backend/config.py
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Literal
import os

class Settings(BaseSettings):
    """Application settings with validation"""

    # Environment
    environment: Literal["development", "staging", "production"] = "development"

    # Database
    database_url: str = Field(..., min_length=10)

    # JWT
    jwt_secret_key: str = Field(..., min_length=32)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    allowed_origins: List[str] = ["http://localhost:3000"]

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # Feature Flags
    enable_email_verification: bool = False
    enable_rate_limiting: bool = False

    # External Services
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""

    # Monitoring
    sentry_dsn: str = ""

    @validator("database_url")
    def validate_database_url(cls, v):
        """Ensure database URL is properly formatted"""
        if not v.startswith(("postgresql://", "postgresql+asyncpg://")):
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
        return v

    @validator("allowed_origins", pre=True)
    def parse_cors_origins(cls, v):
        """Parse comma-separated CORS origins"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @validator("jwt_secret_key")
    def validate_jwt_secret(cls, v, values):
        """Warn if using weak secret in production"""
        if values.get("environment") == "production" and len(v) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters in production")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Singleton instance
settings = Settings()

# Validate on import
if __name__ == "__main__":
    print("Environment configuration:")
    print(f"  Environment: {settings.environment}")
    print(f"  Database: {settings.database_url.split('@')[1] if '@' in settings.database_url else 'configured'}")
    print(f"  CORS Origins: {settings.allowed_origins}")
    print(f"  Log Level: {settings.log_level}")
```

### Using Settings in Application

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
import logging

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Task API",
    debug=settings.environment == "development"
)

# CORS configuration from settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.environment,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development"
    )
```

### Frontend Environment Variables (Next.js)

```bash
# frontend/.env.example
# Public variables (exposed to browser, prefix with NEXT_PUBLIC_)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development

# Private variables (server-side only, no prefix)
API_SECRET_KEY=backend-api-secret
```

```bash
# frontend/.env.local (development)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
```

```bash
# frontend/.env.production
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_ENVIRONMENT=production
```

### Frontend Environment Validation (TypeScript)

```typescript
// frontend/lib/env.ts
import { z } from 'zod'

const envSchema = z.object({
  // Public variables (available in browser)
  NEXT_PUBLIC_API_URL: z.string().url(),
  NEXT_PUBLIC_ENVIRONMENT: z.enum(['development', 'staging', 'production']),

  // Private variables (server-side only)
  API_SECRET_KEY: z.string().optional(),
})

type Env = z.infer<typeof envSchema>

// Validate environment variables
function validateEnv(): Env {
  try {
    return envSchema.parse({
      NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
      NEXT_PUBLIC_ENVIRONMENT: process.env.NEXT_PUBLIC_ENVIRONMENT,
      API_SECRET_KEY: process.env.API_SECRET_KEY,
    })
  } catch (error) {
    console.error('❌ Invalid environment variables:', error)
    throw new Error('Invalid environment variables')
  }
}

// Export validated environment
export const env = validateEnv()

// Type-safe environment access
export function getApiUrl(): string {
  return env.NEXT_PUBLIC_API_URL
}

export function isDevelopment(): boolean {
  return env.NEXT_PUBLIC_ENVIRONMENT === 'development'
}

export function isProduction(): boolean {
  return env.NEXT_PUBLIC_ENVIRONMENT === 'production'
}
```

### Using Environment Variables in Next.js

```typescript
// frontend/lib/api-client.ts
import { getApiUrl } from './env'

export class ApiClient {
  private baseUrl: string

  constructor() {
    this.baseUrl = getApiUrl()
  }

  async request(endpoint: string, options?: RequestInit) {
    const url = `${this.baseUrl}${endpoint}`
    // ... rest of implementation
  }
}

// frontend/app/page.tsx
import { env } from '@/lib/env'

export default function HomePage() {
  return (
    <div>
      <p>Environment: {env.NEXT_PUBLIC_ENVIRONMENT}</p>
      <p>API: {env.NEXT_PUBLIC_API_URL}</p>
    </div>
  )
}
```

### Environment Variable Checklist

```text
✅ .env.example committed with all required variables (values as placeholders)
✅ .env and .env.local in .gitignore
✅ All required variables validated on startup
✅ Type-safe access to environment variables
✅ Sensible defaults for optional variables
✅ Public vs private variables clearly separated (NEXT_PUBLIC_ prefix)
✅ No secrets hardcoded in source code
✅ Documentation explains each variable's purpose
```

### Success Criteria
- All environments have validated configuration
- No hardcoded configuration in source code
- Type-safe environment variable access
- Clear separation between public and private variables
- .env.example provides complete template
- Application fails fast with clear error if config invalid

---

## 2. Secure Secrets Handling

### Purpose
Protect sensitive credentials (API keys, database passwords, JWT secrets) from exposure in source control, logs, and error messages while ensuring they're available to the application at runtime.

### Key Capabilities
- **Secret Rotation**: Change secrets without application downtime
- **Access Control**: Limit who can view/modify secrets
- **Audit Logging**: Track secret access and modifications
- **Encryption at Rest**: Store secrets encrypted
- **Separation of Concerns**: Secrets never in source code or logs

### Secret Storage Options

```text
Environment          | Recommended Solution
---------------------|---------------------
Local Development    | .env file (gitignored)
CI/CD                | GitHub Secrets, GitLab CI/CD Variables
Staging/Production   | Vercel Environment Variables, Railway Secrets,
                     | AWS Secrets Manager, HashiCorp Vault
```

### Secrets Categories

```text
Category             | Examples                           | Storage
---------------------|------------------------------------|---------
Database Credentials | DATABASE_URL, DB_PASSWORD          | Env vars
API Keys             | JWT_SECRET_KEY, STRIPE_SECRET_KEY  | Env vars
Service Credentials  | AWS_ACCESS_KEY_ID, SENDGRID_API_KEY| Env vars
OAuth Credentials    | GOOGLE_CLIENT_ID, GITHUB_SECRET    | Env vars
```

### Never Commit These to Git

```bash
# ❌ NEVER DO THIS
# config.py
DATABASE_URL = "postgresql://user:hunter2@neon.tech/db"  # Hardcoded!
JWT_SECRET_KEY = "super-secret-key-123"  # In source code!

# ✅ DO THIS INSTEAD
# config.py
import os
DATABASE_URL = os.getenv("DATABASE_URL")  # From environment
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # From environment
```

### Preventing Secret Leaks

```python
# backend/config.py
from pydantic_settings import BaseSettings
import logging

class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str

    def __repr__(self):
        """Override repr to hide secrets in logs"""
        return f"Settings(database_url='***', jwt_secret_key='***')"

    class Config:
        env_file = ".env"

settings = Settings()

# ❌ BAD: Secrets will appear in logs
logging.info(f"Settings: {settings}")

# ✅ GOOD: Secrets masked
logging.info(f"Settings loaded successfully")
```

### Masking Secrets in Logs

```python
# backend/utils/logging.py
import re
import logging

class SecretMaskingFormatter(logging.Formatter):
    """Formatter that masks secrets in log output"""

    # Patterns to detect and mask
    SECRET_PATTERNS = [
        (re.compile(r'password["\']?\s*[:=]\s*["\']?([^"\'}\s]+)', re.I), 'password=***'),
        (re.compile(r'token["\']?\s*[:=]\s*["\']?([^"\'}\s]+)', re.I), 'token=***'),
        (re.compile(r'api[_-]?key["\']?\s*[:=]\s*["\']?([^"\'}\s]+)', re.I), 'api_key=***'),
        (re.compile(r'secret["\']?\s*[:=]\s*["\']?([^"\'}\s]+)', re.I), 'secret=***'),
        (re.compile(r'postgresql://[^:]+:([^@]+)@', re.I), 'postgresql://user:***@'),
    ]

    def format(self, record):
        """Format log record and mask secrets"""
        original = super().format(record)
        masked = original

        for pattern, replacement in self.SECRET_PATTERNS:
            masked = pattern.sub(replacement, masked)

        return masked

# Usage
handler = logging.StreamHandler()
handler.setFormatter(SecretMaskingFormatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

logger = logging.getLogger(__name__)
logger.addHandler(handler)
```

### GitHub Secrets (CI/CD)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to production
        env:
          # Access GitHub Secrets
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          JWT_SECRET_KEY: ${{ secrets.JWT_SECRET_KEY }}
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
        run: |
          # Deploy commands here
          echo "Deploying with secrets from GitHub"
```

### Vercel Environment Variables

```bash
# Install Vercel CLI
npm i -g vercel

# Add production secret
vercel env add DATABASE_URL production
# Paste secret value when prompted

# Add secret for all environments
vercel env add JWT_SECRET_KEY

# Pull environment variables to local
vercel env pull .env.local
```

### Railway Secrets

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Add variable to current project
railway variables set DATABASE_URL="postgresql://..."
railway variables set JWT_SECRET_KEY="your-secret-key"

# List variables
railway variables

# Link to project
railway link
```

### Docker Secrets (for containerized apps)

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    secrets:
      - db_password
      - jwt_secret

secrets:
  db_password:
    file: ./secrets/db_password.txt
  jwt_secret:
    file: ./secrets/jwt_secret.txt
```

```python
# backend/config.py (reading Docker secrets)
import os
from pathlib import Path

def get_secret(secret_name: str) -> str:
    """Read secret from Docker secret or environment variable"""
    # Try Docker secrets first
    secret_path = Path(f"/run/secrets/{secret_name}")
    if secret_path.exists():
        return secret_path.read_text().strip()

    # Fall back to environment variable
    return os.getenv(secret_name.upper(), "")

class Settings(BaseSettings):
    database_url: str = Field(default_factory=lambda: get_secret("database_url"))
    jwt_secret_key: str = Field(default_factory=lambda: get_secret("jwt_secret_key"))
```

### Secret Rotation Strategy

```python
# backend/auth.py
import os
from datetime import datetime

class JWTManager:
    """JWT manager with secret rotation support"""

    def __init__(self):
        # Current secret
        self.primary_secret = os.getenv("JWT_SECRET_KEY")

        # Old secret (for grace period during rotation)
        self.secondary_secret = os.getenv("JWT_SECRET_KEY_OLD", "")

    def verify_token(self, token: str):
        """Verify token with primary secret, fall back to secondary"""
        try:
            # Try primary secret
            return jwt.decode(token, self.primary_secret, algorithms=["HS256"])
        except jwt.InvalidSignatureError:
            if self.secondary_secret:
                # Try old secret during rotation grace period
                return jwt.decode(token, self.secondary_secret, algorithms=["HS256"])
            raise

    def create_token(self, data: dict):
        """Always create tokens with primary secret"""
        return jwt.encode(data, self.primary_secret, algorithm="HS256")
```

### Secret Scanning Prevention

```bash
# Install git-secrets (prevents committing secrets)
git clone https://github.com/awslabs/git-secrets
cd git-secrets
make install

# Initialize in your repo
cd /path/to/your/repo
git secrets --install
git secrets --register-aws  # Add AWS patterns

# Add custom patterns
git secrets --add 'password\s*=\s*.+'
git secrets --add 'api[_-]?key\s*=\s*.+'

# Scan existing commits
git secrets --scan-history
```

### Pre-commit Hook (prevent secret commits)

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Check for common secret patterns
if git diff --cached | grep -E '(password|secret|api_key|token)\s*=\s*["\'][^"\']+["\']'; then
    echo "❌ ERROR: Possible secret detected in staged files!"
    echo "Please remove secrets and use environment variables instead."
    exit 1
fi

echo "✅ No secrets detected"
exit 0
```

### Security Checklist

```text
✅ No secrets in source code
✅ No secrets in git history
✅ Secrets masked in logs and error messages
✅ .env files in .gitignore
✅ Secrets rotated periodically
✅ Access to production secrets restricted
✅ Secrets encrypted at rest (platform-specific)
✅ Pre-commit hooks prevent accidental commits
✅ Secret scanning in CI/CD pipeline
```

### Success Criteria
- No secrets ever committed to git
- Secrets stored in environment variables or secret managers
- Logs never contain plaintext secrets
- Pre-commit hooks prevent accidental exposure
- Secret rotation possible without downtime
- Clear documentation of which secrets are needed

---

## 3. Monorepo Navigation

### Purpose
Efficiently organize and navigate a monorepo structure with multiple packages (frontend, backend, shared libraries) while maintaining clear boundaries and dependencies.

### Key Capabilities
- **Package Organization**: Logical separation of concerns
- **Dependency Management**: Shared dependencies and workspace configs
- **Script Coordination**: Run commands across multiple packages
- **Path Resolution**: Import from other packages easily
- **Independent Versioning**: Version packages separately

### Monorepo Structure

```text
project-root/
├── .git/
├── .github/
│   └── workflows/
│       ├── backend-ci.yml
│       ├── frontend-ci.yml
│       └── deploy.yml
│
├── packages/               # Alternative: apps/ and packages/
│   ├── backend/
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── models/
│   │   │   ├── routers/
│   │   │   └── services/
│   │   ├── tests/
│   │   ├── .env.example
│   │   ├── pyproject.toml
│   │   └── README.md
│   │
│   ├── frontend/
│   │   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   ├── public/
│   │   ├── .env.example
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── README.md
│   │
│   └── shared/            # Shared types, utilities
│       ├── types/
│       │   ├── user.ts
│       │   └── task.ts
│       ├── utils/
│       └── package.json
│
├── docs/                  # Documentation
│   ├── api.md
│   ├── setup.md
│   └── architecture.md
│
├── scripts/               # Helper scripts
│   ├── setup.sh
│   ├── deploy.sh
│   └── migrate.sh
│
├── .gitignore
├── package.json           # Root package.json (workspace config)
├── pnpm-workspace.yaml    # or npm workspaces
├── turbo.json             # if using Turborepo
└── README.md
```

### npm/pnpm Workspaces Configuration

```json
// package.json (root)
{
  "name": "task-manager-monorepo",
  "version": "1.0.0",
  "private": true,
  "workspaces": [
    "packages/*"
  ],
  "scripts": {
    "dev": "pnpm --parallel run dev",
    "dev:frontend": "pnpm --filter frontend dev",
    "dev:backend": "cd packages/backend && uvicorn main:app --reload",
    "build": "pnpm --recursive run build",
    "test": "pnpm --recursive run test",
    "lint": "pnpm --recursive run lint",
    "clean": "pnpm --recursive run clean"
  },
  "devDependencies": {
    "turbo": "^1.10.0"
  }
}
```

```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'
```

### Frontend Package Configuration

```json
// packages/frontend/package.json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "jest"
  },
  "dependencies": {
    "next": "14.0.0",
    "react": "18.2.0",
    "shared": "workspace:*"
  }
}
```

### Shared Package

```typescript
// packages/shared/types/task.ts
export interface Task {
  id: number
  title: string
  description: string | null
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  user_id: number
  created_at: string
  updated_at: string
}

export interface TaskCreate {
  title: string
  description?: string
  priority?: Task['priority']
}

export interface TaskUpdate {
  title?: string
  description?: string
  status?: Task['status']
  priority?: Task['priority']
}
```

```json
// packages/shared/package.json
{
  "name": "shared",
  "version": "0.1.0",
  "main": "index.ts",
  "types": "index.ts",
  "exports": {
    "./types": "./types/index.ts",
    "./utils": "./utils/index.ts"
  }
}
```

### Using Shared Package in Frontend

```typescript
// packages/frontend/lib/api/tasks.ts
import type { Task, TaskCreate, TaskUpdate } from 'shared/types'

export async function getTasks(): Promise<Task[]> {
  // Implementation
}
```

### TypeScript Path Mapping

```json
// packages/frontend/tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"],
      "shared/*": ["../shared/*"]
    }
  }
}
```

### Backend Python Package Structure

```text
packages/backend/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── task_service.py
│   └── utils/
│       ├── __init__.py
│       └── security.py
├── tests/
├── alembic/              # Database migrations
├── pyproject.toml
└── requirements.txt
```

```toml
# packages/backend/pyproject.toml
[project]
name = "backend"
version = "0.1.0"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "sqlmodel>=0.0.14",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "httpx>=0.25.0",
]
```

### Turborepo Configuration (optional)

```json
// turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**"]
    },
    "test": {
      "dependsOn": ["build"]
    },
    "lint": {},
    "dev": {
      "cache": false
    }
  }
}
```

### Cross-Package Scripts

```bash
# scripts/dev-all.sh
#!/bin/bash

# Start backend and frontend concurrently
echo "Starting backend and frontend..."

# Terminal 1: Backend
(cd packages/backend && uvicorn main:app --reload --port 8000) &
BACKEND_PID=$!

# Terminal 2: Frontend
(cd packages/frontend && pnpm dev) &
FRONTEND_PID=$!

# Trap Ctrl+C and cleanup
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT

# Wait for both processes
wait
```

```bash
# scripts/setup.sh
#!/bin/bash

echo "Setting up monorepo..."

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd packages/frontend
pnpm install

# Setup backend
echo "Setting up backend..."
cd ../backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e .

# Copy environment templates
echo "Creating .env files from templates..."
cd ../frontend
cp .env.example .env.local

cd ../backend
cp .env.example .env

echo "✅ Setup complete!"
echo "Run 'pnpm dev' from root to start all services"
```

### Navigation Tips

```bash
# Quick navigation aliases (add to ~/.bashrc or ~/.zshrc)
alias cdfe='cd /path/to/project/packages/frontend'
alias cdbe='cd /path/to/project/packages/backend'
alias cdroot='cd /path/to/project'

# Run commands from root
pnpm --filter frontend dev      # Run frontend dev server
pnpm --filter shared build      # Build shared package

# Run backend from root
cd packages/backend && source venv/bin/activate && uvicorn main:app --reload
```

### Monorepo Best Practices

```text
✅ Clear package boundaries (frontend, backend, shared)
✅ Shared types in shared package
✅ Root-level scripts for common tasks
✅ Each package has its own README
✅ Consistent naming conventions
✅ Independent package versioning
✅ Clear dependency graph
✅ Workspace-aware dependency installation
```

### Success Criteria
- Clear package organization with logical separation
- Shared code reused via workspace packages
- Scripts to run/build/test all packages from root
- TypeScript path mapping for easy imports
- Documentation for navigating the structure
- Fast dependency installation with workspaces

---

## 4. Neon PostgreSQL Configuration

### Purpose
Configure and connect to Neon PostgreSQL, a serverless Postgres platform with autoscaling, branching, and built-in connection pooling.

### Key Capabilities
- **Connection Management**: Configure async database connections
- **Connection Pooling**: Use Neon's built-in pooling
- **SSL/TLS**: Secure connections required
- **Branching**: Use database branches for development
- **Migrations**: Manage schema changes with Alembic
- **Monitoring**: Track query performance and connection health

### Neon Connection String Format

```text
# Standard format
postgresql://[user]:[password]@[endpoint]/[dbname]?sslmode=require

# With connection pooling (recommended)
postgresql://[user]:[password]@[endpoint]/[dbname]?sslmode=require&connect_timeout=10

# Example
postgresql://user:abc123@ep-cool-darkness-12345678.us-east-2.aws.neon.tech/neondb?sslmode=require

# For SQLAlchemy async (asyncpg driver)
postgresql+asyncpg://user:abc123@ep-cool-darkness-12345678.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### Environment Variables for Neon

```bash
# backend/.env
# Get this from Neon dashboard: https://console.neon.tech

# Connection string with asyncpg driver
DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# Alternative: Separate components
NEON_HOST=ep-xxx.region.aws.neon.tech
NEON_DATABASE=dbname
NEON_USER=user
NEON_PASSWORD=password

# Pool configuration
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
```

### SQLAlchemy Configuration for Neon

```python
# backend/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from config import settings
import logging

logger = logging.getLogger(__name__)

# Create async engine with Neon-optimized settings
engine = create_async_engine(
    settings.database_url,
    echo=settings.environment == "development",  # Log SQL in dev
    pool_size=10,              # Number of persistent connections
    max_overflow=20,           # Additional connections when pool exhausted
    pool_timeout=30,           # Wait time for connection from pool
    pool_pre_ping=True,        # Verify connections before use
    pool_recycle=3600,         # Recycle connections after 1 hour
    connect_args={
        "ssl": "require",      # Neon requires SSL
        "server_settings": {
            "application_name": "task-manager-backend",
            "jit": "off",      # Disable JIT for better cold start performance
        },
        "timeout": 10,         # Connection timeout
        "command_timeout": 30, # Query timeout
    },
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database initialized")

async def close_db():
    """Close database connections"""
    await engine.dispose()
    logger.info("Database connections closed")

async def get_session() -> AsyncSession:
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()
```

### Health Check with Neon

```python
# backend/routers/health.py
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
import time

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)):
    """Health check with database connectivity"""
    try:
        start = time.time()

        # Simple query to check DB connection
        result = await session.execute(text("SELECT 1"))
        result.scalar()

        db_latency = round((time.time() - start) * 1000, 2)

        return {
            "status": "healthy",
            "database": "connected",
            "db_latency_ms": db_latency,
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
        }
```

### Alembic Configuration for Neon

```bash
# Install Alembic
pip install alembic
alembic init alembic
```

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from config import settings
from models import SQLModel  # Import all models

# Alembic Config object
config = context.config

# Override sqlalchemy.url with environment variable
config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode"""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,  # No pooling for migrations
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
```

```ini
# alembic.ini
[alembic]
script_location = alembic
prepend_sys_path = .

# Database URL (overridden by env.py)
sqlalchemy.url = postgresql+asyncpg://localhost/db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
```

### Running Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Add tasks table"

# Review the generated migration
# alembic/versions/xxx_add_tasks_table.py

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current version
alembic current

# Show migration history
alembic history
```

### Example Migration

```python
# alembic/versions/001_initial_schema.py
"""Initial schema

Revision ID: 001
Create Date: 2026-01-17
"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_email', 'users', ['email'])

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('priority', sa.String(length=50), nullable=False, server_default='medium'),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('ix_tasks_status', 'tasks', ['status'])

def downgrade():
    op.drop_index('ix_tasks_status', table_name='tasks')
    op.drop_index('ix_tasks_user_id', table_name='tasks')
    op.drop_table('tasks')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
```

### Neon Database Branching

```bash
# Neon allows creating database branches for development/testing

# Using Neon CLI
npm install -g neonctl

# Authenticate
neonctl auth

# Create a branch from main
neonctl branches create --name dev-feature-x --parent main

# Get connection string for branch
neonctl connection-string dev-feature-x

# Use branch connection string in development
# .env.development
DATABASE_URL=postgresql+asyncpg://[branch-connection-string]

# Delete branch when done
neonctl branches delete dev-feature-x
```

### Connection Pooling Best Practices

```python
# For Neon, connection pooling is built-in
# Use pooled connection for better performance

# Standard connection (direct to database)
postgresql://user:pass@ep-xxx.neon.tech/db

# Pooled connection (recommended for production)
postgresql://user:pass@ep-xxx-pooler.neon.tech/db

# Update DATABASE_URL to use pooled endpoint
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx-pooler.neon.tech/db?sslmode=require
```

### Query Optimization for Neon

```python
# Use indexes for frequently queried columns
from sqlmodel import Field, SQLModel

class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(index=True)         # ✅ Indexed
    status: str = Field(index=True)          # ✅ Indexed
    title: str = Field(max_length=255)
    created_at: datetime = Field(index=True) # ✅ Indexed for sorting

# Avoid N+1 queries with eager loading
from sqlalchemy.orm import selectinload

statement = (
    select(Task)
    .where(Task.user_id == user_id)
    .options(selectinload(Task.tags))  # Load related tags in one query
)
```

### Monitoring Neon Performance

```python
# Add query timing middleware
from fastapi import Request
import time
import logging

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_db_queries(request: Request, call_next):
    """Log slow database queries"""
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000

    if duration > 1000:  # Log queries slower than 1s
        logger.warning(f"Slow request: {request.url.path} took {duration:.2f}ms")

    return response
```

### Neon Configuration Checklist

```text
✅ DATABASE_URL uses postgresql+asyncpg:// driver
✅ Connection string includes ?sslmode=require
✅ Using pooled connection endpoint (-pooler)
✅ Connection pool configured (pool_size, max_overflow)
✅ pool_pre_ping=True to handle stale connections
✅ Alembic configured for migrations
✅ Database branches used for development/testing
✅ Indexes on frequently queried columns
✅ Health check endpoint tests DB connectivity
✅ Query performance monitored
```

### Success Criteria
- Application connects to Neon PostgreSQL successfully
- SSL/TLS connection enforced
- Connection pooling configured
- Migrations managed with Alembic
- Database health check endpoint implemented
- Development uses database branches
- Production uses pooled connection endpoint

---

## Integration Example: Full Configuration Setup

```bash
# Project structure
project-root/
├── packages/
│   ├── backend/
│   │   ├── .env.example
│   │   ├── .env
│   │   ├── config.py
│   │   ├── database.py
│   │   └── alembic/
│   └── frontend/
│       ├── .env.example
│       └── .env.local
├── scripts/
│   ├── setup.sh
│   └── check-env.sh
└── README.md
```

```bash
# scripts/check-env.sh - Validate environment setup
#!/bin/bash

echo "Checking environment configuration..."

# Check backend .env
if [ ! -f "packages/backend/.env" ]; then
    echo "❌ packages/backend/.env not found"
    echo "   Copy from .env.example and configure"
    exit 1
fi

# Check frontend .env
if [ ! -f "packages/frontend/.env.local" ]; then
    echo "❌ packages/frontend/.env.local not found"
    echo "   Copy from .env.example and configure"
    exit 1
fi

# Validate backend DATABASE_URL
cd packages/backend
if ! python -c "from config import settings; print(settings.database_url)" > /dev/null 2>&1; then
    echo "❌ Backend configuration invalid"
    exit 1
fi

echo "✅ Environment configuration valid"
```

```python
# backend/config.py - Complete configuration
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List

class Settings(BaseSettings):
    # Environment
    environment: str = "development"

    # Database (Neon PostgreSQL)
    database_url: str = Field(..., min_length=10)

    # JWT
    jwt_secret_key: str = Field(..., min_length=32)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    allowed_origins: List[str] = ["http://localhost:3000"]

    @validator("database_url")
    def validate_database_url(cls, v):
        if not v.startswith("postgresql"):
            raise ValueError("DATABASE_URL must be PostgreSQL connection string")
        if "sslmode=require" not in v and "neon.tech" in v:
            raise ValueError("Neon connections require sslmode=require")
        return v

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## References

- Pydantic Settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- Next.js Environment Variables: https://nextjs.org/docs/app/building-your-application/configuring/environment-variables
- Neon Documentation: https://neon.tech/docs/introduction
- SQLAlchemy Async: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- Alembic Migrations: https://alembic.sqlalchemy.org/
- Vercel Environment Variables: https://vercel.com/docs/projects/environment-variables
- Railway Documentation: https://docs.railway.app/
- Git Secrets: https://github.com/awslabs/git-secrets
- `.specify/memory/constitution.md` - Project-specific configuration standards
