# Lesson 8: Tool Use with Streaming

## How Streaming Works with Tools
With streaming, Claude sends events as it generates. For tool arguments you get a new event type: `InputJsonEvent`, which has two properties:
- **partial_json** — the latest chunk
- **snapshot** — everything received so far, cumulative

## Why You See Delays in Streaming
The API buffers chunks and waits for a complete top-level key-value pair to be valid before sending anything. So instead of smooth streaming, you get bursts — one burst per completed key. This is by design to ensure valid JSON.

## Fine-Grained Tool Calling
Disables the API-side JSON validation so you get chunks immediately as Claude generates them. The tradeoff: you may receive invalid JSON and must handle it yourself.

Use it when:
- You want real-time progress shown to users
- Buffering delays hurt the experience
- You're okay writing JSON error handling

## When to Stick with Default
For most apps, default buffered streaming is fine. Only reach for fine-grained when responsiveness is critical.
