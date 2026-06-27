# PROJECT GUIDE — Streaming Tool-Use CLI Agent

> A multi-turn conversational command-line agent built on the Anthropic API,
> demonstrating streaming responses and tool calling (function calling) in a loop.

> **This file is instructions for Claude Code.** Read it top to bottom, then build the
> project exactly as described. Do not add features beyond what is listed here. The goal
> is a small, readable teaching project — simplicity matters more than cleverness.

---

## 0. What we are building (read this first)

A command-line conversational agent: a terminal chat program where a student talks to
Claude, who acts as a friendly tutor. The conversation remembers what was said (multi-turn),
Claude's replies appear live on screen as they are written (streaming), and Claude can
use two small tools — telling the time and saving a study note to a file.

It is one Python file plus a `.env` and a `requirements.txt`. A student should be able to
read the whole thing in one sitting and understand every line.

### Concepts this project demonstrates (for the presentation)

- Basic API requests with the Anthropic Python SDK
- Loading the API key from `.env` with `python-dotenv`
- Message structure (`role` + `content`) and the stateless, send-the-whole-history rule
- Helper functions (`add_user_message`, `add_assistant_message`)
- Multi-turn conversation (appending each reply back to the list)
- System prompts (the tutor persona)
- Streaming responses to the terminal
- Tool use / function calling (tool schema, `ToolUseBlock`, `tool_result`)
- The multi-tool conversation loop driven by `stop_reason == "tool_use"`
- A tool router (a dict, not an if/else chain)
- Error handling with `is_error: True`

### Deliberately OUT of scope (do NOT build these)

- No prompt-evaluation loop, no Claude-as-judge grader, no `asyncio`
- No FastAPI / web server
- No fine-grained tool streaming (the beta flag)
- No database, no external packages beyond the two listed below

---

## 1. Prerequisites

- Python 3.10 or newer.
- An Anthropic API key (the student already has one; it goes in `.env`).
- Two packages only: `anthropic` and `python-dotenv`.

Authoritative SDK and API reference, in case any detail here needs checking:
https://docs.claude.com/en/api/overview

---

## 2. Final file structure

Create exactly these files in the project root:

```
cli-tool-agent/
├── agent.py        # the entire program
├── requirements.txt      # the two dependencies
├── .env                  # holds ANTHROPIC_API_KEY (do NOT commit real key)
├── .env.example          # a template showing the variable name
└── README.md             # how to run it
```

---

## 3. Build steps

Build the project in the order below. Each step says **what** to write and **why**, so the
comments you put in the code can teach the same lesson.

### Step 1 — `requirements.txt`

Two lines only:

```
anthropic
python-dotenv
```

### Step 2 — `.env.example` and `.env`

`.env.example` (this one is safe to share):

```
ANTHROPIC_API_KEY=your-key-here
```

`.env` (real key lives here; identical shape):

```
ANTHROPIC_API_KEY=your-key-here
```

Also create a `.gitignore` containing `.env` so the real key is never committed.

### Step 3 — Imports and setup at the top of `agent.py`

Explain in a comment: the API is **stateless**, so we keep a Python list called `messages`
and send the whole thing every turn. That list is the agent's only "memory".

```python
import os
import json
import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

# Load ANTHROPIC_API_KEY from the .env file into the environment.
load_dotenv()

# The SDK reads the key from the environment automatically.
client = Anthropic()

# The one model we use everywhere in this project.
MODEL = "claude-sonnet-4-6"
```

### Step 4 — The system prompt (the tutor persona)

A plain string constant. Keep it short and clear. This is the "standing instructions" that
apply to every turn — students should see that we write it once, not in every message.

```python
SYSTEM_PROMPT = (
    "You are a friendly and patient tutor for students. "
    "Explain things simply, in small steps, and use short examples. "
    "Encourage the student. When the student wants to remember something, "
    "offer to save it as a note using your save_note tool. "
    "When asked about the date or time, use your get_current_time tool."
)
```

### Step 5 — Message helper functions

These keep list-management out of the main logic. Teach the `role` / `content` shape here.

```python
def add_user_message(messages, content):
    """Append a user turn. `content` can be a string or a list of blocks."""
    messages.append({"role": "user", "content": content})

def add_assistant_message(messages, content):
    """Append an assistant turn (Claude's reply or the blocks it returned)."""
    messages.append({"role": "assistant", "content": content})
```

### Step 6 — The two tool functions (plain Python, no Claude involved)

These are ordinary functions. Claude never runs them — it only *asks* us to. They return
strings, because tool results must be sent back as text.

```python
def get_current_time(format):
    """Return the current local time formatted with a strftime string."""
    return datetime.datetime.now().strftime(format)

def save_note(text):
    """Append a study note to notes.txt and return a confirmation message."""
    with open("notes.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")
    return f"Saved note: {text}"
```

### Step 7 — The tool schemas

This is what Claude reads to decide whether and how to call each tool. The `description`
fields matter a lot — write them precisely. Note `input_schema` mirrors each function's
arguments.

```python
tools = [
    {
        "name": "get_current_time",
        "description": "Returns the current local date/time. Use when the student asks "
                       "what time or date it is.",
        "input_schema": {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "description": "A Python strftime format string, e.g. '%Y-%m-%d %H:%M'."
                }
            },
            "required": ["format"]
        }
    },
    {
        "name": "save_note",
        "description": "Saves a short study note to a file so the student can review it "
                       "later. Use when the student wants to remember something.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The note text to save."
                }
            },
            "required": ["text"]
        }
    }
]
```

### Step 8 — The tool router

A dict mapping tool name → the Python function. This replaces a long if/else chain and
makes adding tools trivial. Also write a `run_tool` helper that calls the right function
with the input Claude provided.

```python
tool_functions = {
    "get_current_time": get_current_time,
    "save_note": save_note,
}

def run_tool(name, tool_input):
    """Call the function named `name`, passing Claude's input dict as keyword args."""
    func = tool_functions[name]
    return func(**tool_input)
```

### Step 9 — Running every tool Claude asked for (with error handling)

Claude may request more than one tool in a single reply. We must answer **every** request,
even if one fails. A failed tool comes back with `is_error: True` so Claude can recover.

Each tool result block needs three fields: `tool_use_id` (must match Claude's request id),
`content` (the string result), and `is_error`.

```python
def run_tools(message):
    """Look through Claude's reply for tool requests, run each, return result blocks."""
    tool_result_blocks = []
    for block in message.content:
        if block.type == "tool_use":
            try:
                result = run_tool(block.name, block.input)
                is_error = False
            except Exception as e:
                result = f"Error running {block.name}: {e}"
                is_error = True

            tool_result_blocks.append({
                "type": "tool_result",
                "tool_use_id": block.id,   # ties this result to that exact request
                "content": str(result),
                "is_error": is_error,
            })
    return tool_result_blocks
```

### Step 10 — One streamed turn to Claude

This sends the current `messages` plus the system prompt and tools, streams the text to the
screen as it arrives, and returns the finished message object (so we can inspect
`stop_reason` and any tool requests).

Teach the streaming detail: we iterate `stream.text_stream` and print with
`end="", flush=True` so each chunk shows instantly. After the stream finishes,
`stream.get_final_message()` gives us the complete message.

```python
def stream_turn(messages):
    """Stream one assistant turn to the terminal and return the final message object."""
    print("\nTutor: ", end="", flush=True)
    with client.messages.stream(
        model=MODEL,
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        tools=tools,
        messages=messages,
    ) as stream:
        for text_chunk in stream.text_stream:
            print(text_chunk, end="", flush=True)
        final_message = stream.get_final_message()
    print()  # newline after the streamed reply
    return final_message
```

### Step 11 — The multi-tool conversation loop

This is the heart of the agent. For one user input, Claude might: answer directly, OR ask
for tools, get results, then answer. We loop until `stop_reason` is no longer `"tool_use"`.

```python
def agent_turn(messages):
    """Handle one full exchange: keep running tools until Claude gives a final answer."""
    while True:
        response = stream_turn(messages)
        add_assistant_message(messages, response.content)

        # If Claude is NOT asking for a tool, it has given its final answer. Stop.
        if response.stop_reason != "tool_use":
            break

        # Otherwise run the requested tool(s) and feed results back as a user turn.
        tool_result_blocks = run_tools(response)
        add_user_message(messages, tool_result_blocks)
```

### Step 12 — The main chat loop (the program entry point)

A simple `while True` that reads typed input, appends it as a user message, runs
`agent_turn`, and repeats. Typing `quit` or `exit` ends the program.

```python
def main():
    print("Tutor agent ready. Type 'quit' to exit.")
    messages = []  # the whole conversation history (the agent's memory)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye! Happy studying.")
            break
        if not user_input:
            continue

        add_user_message(messages, user_input)
        agent_turn(messages)

if __name__ == "__main__":
    main()
```

---

## 4. Assemble the full file

Combine Steps 3–12 into a single `agent.py` in that order: imports/setup, system
prompt, message helpers, tool functions, tool schemas, router, `run_tools`, `stream_turn`,
`agent_turn`, `main`. Keep all the teaching comments.

---

## 5. README.md to generate

Write a short `README.md` containing:

1. One-line description of the project.
2. Setup steps:
   ```
   python -m venv venv
   source venv/bin/activate      # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env          # then paste the real key into .env
   ```
3. Run command: `python agent.py`
4. Three things to try, to show off each concept:
   - "Explain photosynthesis simply." → plain streamed answer (system prompt + streaming)
   - "What time is it right now?" → triggers `get_current_time` (tool use + loop)
   - "Save a note: review chapter 3 tonight." → triggers `save_note`, then check `notes.txt`

---

## 6. Verification checklist (Claude Code: confirm before finishing)

- [ ] `pip install -r requirements.txt` succeeds.
- [ ] Program starts and shows the ready prompt.
- [ ] A normal question streams text live (visible chunk-by-chunk).
- [ ] Asking the time calls `get_current_time` and Claude reports it.
- [ ] Asking to save a note creates/appends `notes.txt` with the text.
- [ ] Typing `quit` exits cleanly.
- [ ] Deliberately break a tool (e.g. temporarily raise an error in `save_note`) and confirm
      the agent reports the failure gracefully instead of crashing — then revert.

---

## 7. Notes for whoever presents this

The story to tell, in order: we send a list of messages → the system prompt sets the
persona once → streaming makes replies feel live → tools let Claude reach outside itself,
but Claude only *asks*; our Python does the work → the loop keeps going while
`stop_reason == "tool_use"` and stops when Claude has a final answer → the router and the
`is_error` flag keep the whole thing tidy and crash-proof.

Keep it simple. Resist adding more tools or features during the demo.