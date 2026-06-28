---
name: update-exp-readme
description: Updates the README.md for the exp project. Use when updating README, reflecting recent changes, or when the user asks to sync README with the current state of this project.
---

This is a learning and experimentation repo for the Claude API. The README should read as a guide to what's been explored, not a product or project README.

When updating the README.md:

1. Run `git log --oneline -20` to see recent commits and what's been added
2. Glob `**/*.ipynb` to discover all notebooks and their locations
3. Read the existing README.md to understand current structure
4. Update the README following this format:

## Format

```
# Claude API: Learning Experiments

One sentence framing this as a personal learning/experimentation repo.

## Setup
Minimal install steps. Include jupyter/ipykernel/any ML packages needed for notebooks.
Always include the kernel registration command and the note to select "Python (exp-venv)" in VS Code.

## What's Covered
Group notebooks by topic area (e.g. Claude API Basics, Prompt Engineering, Tool Use, RAG, Thinking and Caching).
For each notebook: one line describing the concept it explores.
Write from a learning perspective: "exploring X", "how X works", not "this module does X".

## FastAPI App (if still present)
Keep this section minimal. It's a practice vehicle, not the focus.
```

## Tone guidelines
- Learning-first: what did we explore, not what does the project do
- No "features" or "functionality" language
- Notebook descriptions should name the concept being learned, not describe code
- Keep it concise. This is a personal learning log, not documentation
- Never use em dashes (—). Use commas, colons, or split into separate sentences instead.
