---
name: update-exp-readme
description: Updates the README.md for the exp project. Use when updating README, reflecting recent changes, or when the user asks to sync README with the current state of this project.
---

When updating the README.md:

1. Run `git diff main...HEAD` to see all changes on this branch
2. Run `git log --oneline -20` to see recent commit history
3. Read the existing README.md to understand current structure
4. Update the README following this format:

## What
One sentence describing what this project does.

## Installation
Steps to install and set up the project.

## Usage
How to run or use the project, with examples.

## Endpoints
- List all FastAPI endpoints with method and path
- Brief description of each

## Project Structure
- Bullet points of key files and directories
- Brief description of each
