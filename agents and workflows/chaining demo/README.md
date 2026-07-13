# Chaining Demo

Exploring prompt chaining with the Claude Agent SDK: splitting one task into a sequence of focused calls, where each step's output feeds the next.

## What it does

`main.py` runs a two-step chain:

1. **Draft**: asks Claude to write a short article, with loose style constraints (no AI disclosure, no emojis, professional tone) that aren't strictly enforced in a single pass.
2. **Revise**: feeds the draft back in with an explicit checklist (remove AI disclosures, remove emojis, replace casual language), so the second call focuses only on cleanup rather than generation.

The idea being tested: a single prompt with many constraints tends to satisfy some and miss others, but breaking it into generate-then-fix steps gets more reliably correct output.

## Running it

```bash
python main.py
```

Prints the draft and the revised final version so the two steps can be compared directly.

## Requirements

- `claude_agent_sdk` installed and configured (Claude Code CLI available on PATH, since the SDK shells out to it)
