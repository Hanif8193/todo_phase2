---
id: "004"
title: "Run Backend in WSL"
stage: general
date: 2026-02-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: PMLS
command: none
labels: ["backend","wsl","uvicorn","startup","debugging"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/main.py
  - backend/venv/pyvenv.cfg
tests:
  - curl http://localhost:8000/ → 200 OK
  - curl http://localhost:8000/health → {"status":"healthy","database":"connected"}
---

## Prompt

run the backend in WSL

## Response snapshot

Started the FastAPI backend in WSL. Root challenge: 32-bit Git Bash (MINGW32) cannot execute `wsl` directly — `wsl.exe` is only accessible via `/c/Windows/Sysnative/wsl.exe`. Background jobs launched via that path died immediately due to Git Bash process tree limitations.

Solution: Used `cmd.exe /c "start /b wsl.exe bash -c ..."` to launch WSL in a detached Windows process, which persisted correctly.

Backend confirmed running:
- `GET http://localhost:8000/` → `{"status":"ok","message":"Todo Application API","version":"2.0.0"}`
- `GET http://localhost:8000/health` → `{"status":"healthy","database":"connected"}`

## Outcome

- ✅ Impact: Backend running at http://localhost:8000; "Failed to fetch" error resolved
- 🧪 Tests: curl health and root endpoints — both 200 OK, database connected
- 📁 Files: no files modified
- 🔁 Next prompts: Test full auth flow (signup/signin) and task CRUD from the frontend
- 🧠 Reflection: 32-bit MINGW Git Bash requires `Sysnative/wsl.exe` and `cmd.exe start /b` pattern to launch persistent WSL processes; direct `wsl` or background `&` from Git Bash kills the process immediately.

## Evaluation notes (flywheel)

- Failure modes observed: WSL process died when launched as background job from 32-bit Git Bash; `nohup` inside WSL also failed to persist
- Graders run and results (PASS/FAIL): curl health check — PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Add START.bat or run_server.py wrapper that uses `cmd /c start wsl.exe ...` for repeatable one-click startup
