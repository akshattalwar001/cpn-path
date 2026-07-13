# Guardrail

A Claude Code hooks project that adds four safety/automation layers:

## What it does

1. **Block Dangerous Bash Commands** (`PreToolUse`, matcher: `Bash`)
   Denies risky shell commands before they run — `rm -rf`, `git push --force`,
   `sudo`, `chmod 777`, redirects into `/dev/`.

2. **Protect Sensitive Files** (`PreToolUse`, matcher: `Write|Edit`)
   Denies edits to protected files — `.env`, `secrets.json`, `*.pem`, `*.key`,
   `package-lock.json`, `yarn.lock`.

3. **Inspect Input** (`PostToolUse`, matcher: `*`)
   Logs every tool call's input and response to `post-log.json` for
   debugging and auditing.

4. **Auto-Format Edited Files** (`PostToolUse`, matcher: `Write|Edit`)
   Runs Prettier on `.js/.jsx/.ts/.tsx` files and Black on `.py` files
   automatically after Claude writes or edits them.

## Structure

    guardrail/
    ├── .claude/
    │   └── settings.json          # hook config
    ├── hooks/
    │   ├── block-dangerous-bash-commands.py
    │   ├── protect-sensitive-files.py
    │   ├── inspect_input.py
    │   └── auto-format-edited-files.py
    ├── test/                      # sample files for manual testing
    │   ├── sample.js
    │   ├── sample.py
    │   └── .env.test
    ├── post-log.json              # output log from inspect_input hook
    └── README.md

## How hooks work here

- **PreToolUse** hooks can block a tool call by exiting with code `2` and
  printing a reason to stderr. Claude receives that reason and can adapt.
- **PostToolUse** hooks run after the tool already executed — they can't
  block, only react (e.g. run a formatter).

## Manual testing

Each hook reads JSON from stdin, so you can test it directly without
Claude Code:

    echo '{"tool_input": {"command": "rm -rf /tmp/test"}}' | python hooks/block-dangerous-bash-commands.py
    echo "Exit code: $LASTEXITCODE"

Exit code `2` = blocked, `0` = allowed.

## Requirements

- Python 3
- `prettier` (via `npx`) for JS/TS formatting
- `black` for Python formatting