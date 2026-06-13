# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate virtual environment
venv\Scripts\Activate.ps1          # PowerShell
venv\Scripts\activate.bat          # CMD

# Start dev server
venv\Scripts\uvicorn main:app --reload

# Install dependencies
venv\Scripts\pip install -r requirements.txt

# Run tests
venv\Scripts\python .claude/skills/add-endpoint/scripts/run_tests.py
```

## Architecture

This is a FastAPI app with in-memory data loaded from `mock_students.json` at startup. There is no database — all mutations (POST, PUT, DELETE) modify the in-process list and are lost on restart.

**Data flow:** `mock_students.json` → loaded into `students: List[dict]` in `main.py` → all endpoints read/write directly against that list.

**Models:** `Student` is the response model, `StudentRequest` is the input model (no `id` field). Both are defined at the top of `main.py`.

**Route ordering matters:** `/students/major/{major}` must be defined before `/students/{student_id}` to avoid FastAPI matching `major` as an integer student ID.

## Writing Style

Avoid em dashes (—). Use commas, colons, parentheses, or split into separate sentences instead.

## Project Skills

- `/add-endpoint` — scaffolds a new FastAPI endpoint following project conventions
- `/update-exp-readme` — updates README.md to reflect current project state
