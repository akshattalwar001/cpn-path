# Prompt Engineering

Score your prompts. Improve by the numbers.

How to build an eval pipeline that turns prompt guesswork into measurable progress.

---

> A prompt has no grade until you test it. The loop is simple: run your prompt on a fixed dataset, score the outputs, average the scores. Change the prompt. Repeat. The number tells you if it got better.

---

## The Six Steps

**01 — Write a baseline prompt**
Don't overthink it. Write the prompt you think will work. Its only job right now is to give you a starting score to beat.

**02 — Generate a test dataset**
Ask Claude to produce test cases from your task description and a field spec. Faster than writing them by hand, and more varied.
> Watch out: Claude may wrap the JSON in ` ```json ``` ` even when you ask for raw output. Strip the fences before parsing — always.

**03 — Run the prompt on every case**
Loop through the dataset, fill in your prompt template with each input, call the API, collect the responses. Nothing clever here.

**04 — Grade with Claude**
Send each output back to Claude with the original input and your quality criteria. Ask for a score from 1–10 and a reason. This is called *LLM-as-judge* — it's consistent and the reasoning points directly at what to fix.
> Watch out: The model may return `7/10` instead of `7`. Split on `/` before calling `float()`.

**05 — Average the scores**
One number. Write it down. That's your baseline.

**06 — Iterate**
Change one thing in the prompt. Re-run steps 3–5. If the score went up, keep it. If it went down, revert. The loop is the skill — everything else is just setup.

---

## Running in Parallel

Sequential runs wait for each API call to finish before starting the next. With async, all cases run at the same time — total time drops from *sum of all calls* to *slowest single call*.

Cap concurrency with a semaphore to stay under rate limits. In Jupyter, use `await` directly in the cell — `asyncio.run()` fails because Jupyter already has a running event loop.

---

## Quick Reference

| Error | Fix |
|---|---|
| `JSONDecodeError` on dataset parse | Claude wrapped it in ` ```json ``` ` fences — strip them before `json.loads()` |
| `ValueError: could not convert '7/10' to float` | Split on `/` first, then convert the left side |
| `RuntimeError: asyncio.run() cannot be called` | You're in Jupyter — use `await` directly in the cell |
| `BadRequestError 400: prefill not supported` | Newer models reject assistant prefill — prompt for raw output and strip fences instead |
