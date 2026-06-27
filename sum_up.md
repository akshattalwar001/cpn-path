# Theory Summary

A condensed reference of every concept covered across the notebooks and directories in this project.

---

## 1. Basic API Requests

**SDK setup:** Initialize the Anthropic client, load your API key from `.env` via `python-dotenv`.

**Message structure:** Every request is a list of messages, each with a `role` (`user` or `assistant`) and `content`. The API is stateless, so you send the full history every turn.

**Single-turn vs. multi-turn:** A single-turn call sends one user message and reads the response. Multi-turn means appending each assistant response back onto the message list before the next call, which is how Claude remembers what was said.

**Helper pattern:** Small functions like `add_user_message` and `add_assistant_message` keep message list management out of your main logic.

---

## 2. System Prompts

**What they are:** An optional top-level `system` field sent alongside messages. Claude reads it as standing instructions that apply to the entire conversation.

**Effect:** They control persona, tone, response style, and constraints without you having to repeat instructions in every user message.

**Persistence:** The system prompt is in scope for every turn of the conversation automatically.

**Example use case:** Setting a pirate persona, restricting topics, telling Claude to always respond in JSON, etc.

---

## 3. Streaming

**Problem solved:** By default the API waits until the full response is generated before sending anything back. For long outputs this creates an awkward blank pause for users.

**How streaming works:** With `client.messages.stream()`, the API sends response chunks as they are generated. You iterate over those chunks and display each piece immediately.

**Event types (raw stream):**
- `RawMessageStartEvent` — signals the start of a new message
- `RawContentBlockStartEvent` — signals the start of a content block
- `RawContentBlockDeltaEvent` — carries an incremental text chunk
- `RawMessageStopEvent` — signals completion

**Text stream shortcut:** `stream.text_stream` is a convenience iterator that yields only the text deltas, hiding the lower-level event wrappers.

**Key detail:** Use `print(..., end="", flush=True)` to render each chunk immediately instead of waiting for a newline.

---

## 4. Structured Data / JSON Output

**Why you need it:** LLM outputs are prose by default. Applications often need a machine-readable format like JSON to feed into downstream code.

**How to request it:** Tell Claude explicitly in the prompt to return only raw JSON with no explanation and no code fences.

**The fence problem:** Claude frequently wraps JSON in ` ```json ... ``` ` even when asked not to. Strip those fences before calling `json.loads()`.

**Stop sequences:** You can set `stop_sequences` to a sentinel like `"```"` to make Claude stop before adding a closing fence.

**Prefill trick:** Pass an `assistant` message that starts with `{` or ` ```json` to guide Claude into the right format from the first token.

---

## 5. Prompt Engineering

Prompt engineering is the practice of writing and iterating on prompts to improve Claude's output quality in a measurable way.

### The Six-Step Evaluation Loop

1. Write a baseline prompt.
2. Generate a test dataset (diverse, representative inputs).
3. Run the prompt against every test case.
4. Grade each output with Claude as the judge (score 1-10).
5. Average the scores into a single metric.
6. Change one thing in the prompt, repeat steps 3-5, compare.

This loop turns prompt improvement from guesswork into a measured process.

### Lesson 1: Clear First Line

The first sentence of the prompt should state the primary task directly. Claude infers intent from context, but an ambiguous opening forces it to guess, which degrades output quality.

Example improvement: Adding "Create a weekly meal plan" as the opening line raised scores from 2.0 to 3.92/10.

### Lesson 2: Output Guidelines

After the task statement, list specific qualities the output must have: format, length, tone, required elements. Without this, Claude picks defaults that may not match your needs.

Example improvement: Adding a six-point guidelines block raised scores from 3.92 to 7.86/10.

### Lesson 3: XML Tags for Structure

When a prompt mixes instructions with data (user-supplied content, examples, field specs), use XML tags to mark boundaries. This prevents instructions from bleeding into data and vice versa.

Use specific tag names (`<athlete_information>`) rather than generic ones (`<data>`).

Example improvement: Wrapping structured athlete data in named XML tags raised scores from 7.86 to 8.20/10.

### Process Steps

For complex analytical tasks, spell out the exact steps Claude should follow rather than leaving the approach open. This ensures comprehensive coverage instead of a quick one-angle answer.

### Parallel Evaluation with asyncio

Running evaluations sequentially is slow. Use `asyncio` with a `Semaphore` to evaluate many test cases concurrently while staying under API rate limits. In Jupyter, use `await` directly at the top level (not `asyncio.run()`, which fails because the event loop is already running).

---

## 6. Prompt Evaluation

Prompt evaluation is the infrastructure side of prompt engineering: the tooling and process that make measurement repeatable.

### Five-Step Workflow

1. Draft a prompt.
2. Assemble an eval dataset of representative inputs (hand-written or AI-generated).
3. Run every input through the prompt template and collect outputs.
4. Grade each output with a Claude-powered grader that returns strengths, weaknesses, reasoning, and a 1-10 score.
5. Iterate: modify the prompt, re-run, compare the average score to the previous version.

### Dataset Generation

You can ask Claude to generate the eval dataset itself. Give it the task description and field spec, use a prefill and stop sequence to get clean JSON back, and parse the result into test cases.

### The Grader

The grader is a separate Claude call that takes a test case and an output and returns a structured JSON object:

```json
{
  "strengths": "...",
  "weaknesses": "...",
  "reasoning": "...",
  "score": 8
}
```

The grader is itself a prompt that must be engineered carefully, as it sets the standard for what "good" means.

### Score Parsing

Claude often returns scores as "8/10" rather than "8". Split on "/" before converting to a number.

---

## 7. Tool Use (Function Calling)

Tool use lets Claude request that your code execute a function on its behalf, then incorporates the result into its response. Claude itself never runs code; it only asks.

### Tool Schema

Each tool is described with a `ToolParam` dict:

```python
{
    "name": "get_current_time",
    "description": "Returns the current local time in the specified format.",
    "input_schema": {
        "type": "object",
        "properties": {
            "format": {"type": "string", "description": "strftime format string"}
        },
        "required": ["format"]
    }
}
```

The description is what Claude reads to decide whether and how to use the tool. Write it precisely.

### Three-Step Process

1. Send Claude the tool schema alongside the messages.
2. Claude responds with a `ToolUseBlock` that contains the tool name and the input parameters it wants to pass.
3. Your code runs the function, then sends back a `tool_result` block containing the output.

### Tool Result Block

Three required fields:

- `tool_use_id`: must match the ID from Claude's `ToolUseBlock` so Claude knows which result maps to which request.
- `content`: the function's return value, as a string.
- `is_error`: boolean, set to `True` if the function threw an exception.

---

## 8. Multi-Tool Conversation Loop

When Claude might use tools multiple times across a conversation, you need a loop that handles this automatically.

### Core Loop Pattern

```python
while True:
    response = chat(messages, tools=tools)
    add_assistant_message(messages, response)

    if response.stop_reason != "tool_use":
        break  # Claude is done, final answer is ready

    tool_result_blocks = run_tools(response)
    add_user_message(messages, tool_result_blocks)
```

`stop_reason == "tool_use"` means Claude wants to call a tool. Any other stop reason means it has a final answer.

### Parallel Tool Calls

Claude can request multiple tools in a single response. Filter all `tool_use` blocks from `response.content`, execute each one, and include a result block for every request. You must never leave a tool request unanswered, even if the tool fails.

### Tool Router

Instead of if-else chains, use a dispatch dict or a `run_tool(name, input)` function that maps tool names to implementations. This keeps the loop clean and makes adding new tools trivial.

### Error Handling

Wrap each tool execution in try-except. On failure, send back a result block with `is_error: True` and the exception message as the content. This lets Claude acknowledge the failure and respond gracefully.

---

## 9. Streaming with Tool Use

### Default (Buffered) Streaming

When streaming is combined with tool use, the API buffers tool input chunks until it has assembled valid JSON for each parameter, then flushes. Text blocks stream smoothly; tool inputs stream in bursts (one burst per completed parameter).

### Fine-Grained Tool Streaming (Beta)

Enabled with the beta flag `"fine-grained-tool-streaming-2025-05-14"`. This disables the API-side JSON validation buffer and sends tool input chunks immediately as they are generated.

Tradeoff: You get real-time progress, but you may receive partial or invalid JSON mid-stream and must handle parsing errors yourself.

Use this only when responsiveness is critical and the extra error-handling complexity is acceptable. For most apps, buffered streaming is sufficient.

---

## Key Parameters Reference

| Parameter | What it controls |
|---|---|
| `model` | Which Claude model to use (`claude-sonnet-4-6`, `claude-haiku-4-5`, etc.) |
| `max_tokens` | Hard cap on response length |
| `temperature` | Randomness: 0 = deterministic, 1 = default creative |
| `system` | Standing instructions for the whole conversation |
| `stop_sequences` | List of strings at which Claude stops generating |
| `tools` | List of tool schemas Claude can request |
| `stream` | Whether to stream the response incrementally |

---

## Common Pitfalls

**JSON wrapped in fences:** Claude adds ` ```json ... ``` ` even when told not to. Strip before parsing.

**Score format:** Claude returns "7/10" not "7". Split on "/" before `float()`.

**`asyncio.run()` in Jupyter:** Fails because an event loop is already running. Use `await` directly or `nest_asyncio`.

**Missing tool results:** Every tool request in a response must have a corresponding result block. Omitting one corrupts the conversation state.

**Route ordering in FastAPI:** Literal path segments (e.g., `/students/major/{major}`) must be defined before parameterized segments (e.g., `/students/{id}`) or FastAPI will match the wrong route.
