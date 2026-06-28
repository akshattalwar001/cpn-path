---
name: git-push
description: Commit and push changes to GitHub. Always generates 4 commit message options in different tones before committing. Use when the user wants to push, commit, or ship changes to GitHub.
---

Follow these steps exactly, in order. Do not skip the message options step.

## Step 1: Understand what changed

Run these in parallel:
- `git status` to see staged and untracked files
- `git diff` to see unstaged changes
- `git diff --staged` to see staged changes
- `git log --oneline -5` to see recent commit style

## Step 2: Stage files if needed

If there are relevant untracked or unstaged files, ask the user which ones to include before staging.

## Step 3: Generate 4 commit message options

Based on what changed, write 4 options in these tones. Use AskUserQuestion with all 4 as options.

- **Casual**: short, lowercase, like a dev dashing off a message ("tweaked the chunking logic")
- **Descriptive**: clear and informative, explains the what and why in one line
- **Concise**: minimal words, just the noun and verb ("add RRF hybrid search")
- **Conventional**: follows conventional commits format, e.g. "feat:", "fix:", "docs:", "refactor:"

Rules for all messages:
- No em dashes (—)
- No trailing periods
- Under 72 characters
- Present tense

## Step 4: Commit with the chosen message

Use PowerShell heredoc syntax:

```
git commit -m @'
<chosen message>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
'@
```

## Step 5: Push

Run `git push` and confirm it succeeded.
