# Claude Partner Network Course

## What
A FastAPI student data API built as part of the Claude Partner Network (CPN) course, demonstrating Claude Code skills for endpoint generation, project scaffolding, and README management.

## Installation

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\Activate.ps1        # PowerShell
venv\Scripts\activate.bat        # CMD

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
venv\Scripts\uvicorn main:app --reload
```

API docs available at http://127.0.0.1:8000/docs

## Endpoints

- `GET /students` - Return all students
- `GET /students/{student_id}` - Return a student by ID
- `GET /students/major/{major}` - Return all students by major (case-insensitive)
- `POST /students` - Create a new student
- `PUT /students/{student_id}` - Update a student by ID
- `DELETE /students/{student_id}` - Delete a student by ID

## Project Structure

- `main.py` - FastAPI app with all endpoints and Pydantic models
- `mock_students.json` - Mock student data loaded at startup (in-memory, not persisted)
- `requirements.txt` - Python dependencies
- `CLAUDE.md` - Guidance for Claude Code: dev commands, architecture notes, and project conventions
- `.claude/skills/add-endpoint/` - Project skill for scaffolding new FastAPI endpoints
- `.claude/skills/update-exp-readme/` - Project skill for updating this README
