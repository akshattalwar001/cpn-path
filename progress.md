# Project Progress

## Claude Partner Network Course

### Setup
- Created virtual environment with `venv`
- Installed FastAPI and Uvicorn via `requirements.txt`
- Deleted `index.js` and migrated project to Python/FastAPI

### API
- Built `main.py` with a full student CRUD API
- Created `mock_students.json` with 5 mock students (name, age, grade, major)
- Endpoints built:
  - `GET /students` — list all students
  - `GET /students/{student_id}` — get by ID
  - `GET /students/major/{major}` — get by major (case-insensitive)
  - `POST /students` — create student
  - `PUT /students/{student_id}` — update student
  - `DELETE /students/{student_id}` — delete student

### Claude Code Skills
- Created global personal skill: `no-em-dashes`
- Created project skills:
  - `add-endpoint` — scaffolds FastAPI endpoints with model + route format, uses Sonnet 4.7, includes allowedTools
  - `update-exp-readme` — updates README with What/Installation/Usage/Endpoints/Project Structure format
- Added supporting directories to `add-endpoint` skill:
  - `scripts/run_tests.py` — pytest runner
  - `references/status_codes.md` — HTTP status code reference
  - `assets/router_template.py` — full FastAPI router boilerplate

### Agents
- Created `.claude/agents/readme-updater-agent.md` — documentation specialist agent that delegates README updates using the `update-readme` skill

### Documentation
- `CLAUDE.md` — project guidance for Claude Code (commands, architecture, writing style)
- `README.md` — kept in sync with project via the `update-exp-readme` skill and readme-updater-agent
- `.gitignore` — covers venv, pycache, .env, IDE, OS files

### GitHub
- Repo created: `akshattalwar001/cpn-path`
- All changes committed and pushed to `main`
