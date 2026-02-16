---
id: "003"
title: "Failed to Fetch Backend Not Running"
stage: general
date: 2026-02-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: PMLS
command: none
labels: ["debugging","backend","venv","cors","localhost"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/main.py
  - backend/config.py
  - backend/.env
  - frontend/lib/api.ts
  - frontend/.env.local
  - backend/venv/pyvenv.cfg
tests:
  - none
---

## Prompt

Failed to fetch

## Response snapshot

Diagnosed "Failed to fetch" error in the frontend application. Root cause: the backend server is not running at `http://localhost:8000`. The venv was created in WSL (`/usr/bin/python3.12`) but the session runs in Git Bash on Windows, making the venv's Python symlink unexecutable.

Provided three fix options:
1. **WSL (recommended):** `cd /mnt/c/.../backend && source venv/bin/activate && uvicorn main:app --reload`
2. **New Windows venv:** `python -m venv venv_win && pip install -r requirements.txt && uvicorn main:app`
3. **Direct Windows Python:** Use `/c/Program Files/Python313/python -m uvicorn main:app`

Frontend env (`NEXT_PUBLIC_API_URL=http://localhost:8000`) and backend CORS (`http://localhost:3000`) are correctly configured — only the backend process needs to be started.

## Outcome

- ✅ Impact: Identified backend not running as root cause of "Failed to fetch"; provided actionable fix paths
- 🧪 Tests: none run
- 📁 Files: backend/main.py, backend/config.py, frontend/lib/api.ts (read only, no changes)
- 🔁 Next prompts: Start the backend using one of the three options; verify connectivity with `curl http://localhost:8000/health`
- 🧠 Reflection: The venv/pyvenv.cfg shows WSL origin (`/usr/bin/python3.12`), which is incompatible with Git Bash on Windows. Always check pyvenv.cfg when a venv fails to activate.

## Evaluation notes (flywheel)

- Failure modes observed: WSL-created venv not compatible with Git Bash environment
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Try `source venv/bin/activate` inside WSL terminal to confirm existing venv works
