# sdk-demo

A small practice project for learning the **Claude Agent SDK** — running Claude Code from a Python script instead of typing in a terminal.

## What is the Agent SDK?

- Claude Code CLI = you type in a terminal, Claude responds
- Agent SDK = same Claude "brain," but controlled **from your own code**
- Useful when you want a script (not a human) to run Claude and handle its output

## Structure

    sdk-demo/
    ├── main.py
    └── README.md

## Requirements

- Python 3
- `claude-agent-sdk` package

---

## Step 1 — Install

```bash
pip install claude-agent-sdk --break-system-packages
```

**What it does:** downloads the SDK package so Python can import it.

**What it teaches:** `pip install` is Python's way of adding external tools to a project — same idea as `npm install` in JavaScript.

---

## Step 2 — Write the script

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    prompt = "List the files in the current directory"

    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Glob"]
    )

    async for message in query(prompt=prompt, options=options):
        print(message)

asyncio.run(main())
```

**What each part does:**

| Line | Does |
|---|---|
| `import asyncio` | lets Python run code that waits without freezing |
| `from claude_agent_sdk import ...` | pulls in the SDK's main tools |
| `async def main():` | wraps our program so it can "wait" properly |
| `prompt = "..."` | the instruction we're giving Claude |
| `ClaudeAgentOptions(allowed_tools=[...])` | limits which tools Claude can use |
| `async for message in query(...)` | loops through Claude's response, piece by piece |
| `print(message)` | shows each piece as it arrives |
| `asyncio.run(main())` | actually starts the program |

**What it teaches:**
- Claude doesn't give one big answer — it **streams** a sequence of messages (thinking, tool use, tool result, final answer)
- `async`/`await` is Python's way of handling things that take time (like waiting for Claude) without freezing the whole program

---

## Step 3 — Run it

```bash
python main.py
```

**What it does:** sends the prompt to Claude and prints everything Claude does, step by step, live.

**What it teaches:** this is the same loop the CLI runs — you're just watching it directly instead of through the terminal UI.

---

## Step 4 — Read the output

A run prints messages in this order:

| # | Message type | What it means |
|---|---|---|
| 1 | `SystemMessage` (init) | session started — shows folder, model, available tools |
| 2 | `AssistantMessage` (thinking) | Claude deciding what to do |
| 3 | `AssistantMessage` (tool use) | Claude asks to use a tool (e.g. `Read`) |
| 4 | `UserMessage` (tool result) | the tool's result gets fed back in |
| 5 | `AssistantMessage` (text) | Claude's final human-readable answer |
| 6 | `ResultMessage` | summary — cost, time taken, tokens used |

**What it teaches:** this 6-stage pattern — think → act → react → answer — is the exact same loop that `PreToolUse`/`PostToolUse` hooks intercept in the CLI. The SDK just lets you watch (and control) it directly from code.

---

## Step 5 — Restrict tools

```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob"]
)
```

**What it does:** Claude can *only* use `Read` and `Glob` — nothing else (no `Bash`, no `Write`, no `Edit`), even if it wants to.

**What it teaches:** two different ways to control Claude, and when to use each:

| Method | How it controls Claude | Example |
|---|---|---|
| `allowed_tools` | Blocks whole tools before Claude can even try them | "Claude can never use Bash" |
| Hooks (`PreToolUse`) | Lets Claude try, then checks the specific request | "Claude can use Bash, but not `rm -rf`" |

**Simple analogy:**
- `allowed_tools` = a guest list — you're just not on it, no entry
- Hooks = a bouncer — you're let in, then checked at the door

---

## Summary

| Step | Topic |
|---|---|
| 1 | Installing the SDK |
| 2 | Writing a script that calls Claude |
| 3 | Running it |
| 4 | Understanding the message stream |
| 5 | Restricting which tools Claude can use |