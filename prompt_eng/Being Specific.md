# Lesson 3: Being Specific

---

## The Core Idea

Vague prompt = Claude picks everything (length, format, content, angle).
Specific prompt = you control the output.

Two tools to do this:

```
1. Output guidelines  — what the result should look like
2. Process steps      — how Claude should think before answering
```

---

## Tool 1: Output Guidelines

List the qualities you want in the output.

```
VAGUE:
"Write a short story about someone discovering a hidden talent."

SPECIFIC:
"Write a short story about someone discovering a hidden talent.
Guidelines:
- Under 1,000 words
- Include one clear moment that reveals the talent
- At least one supporting character
- Third person, past tense"
```

Use for controlling: length, format, tone, required elements.

---

## Tool 2: Process Steps

Tell Claude HOW to think before answering. Good for complex tasks.

```
VAGUE:
"Analyze why our sales dropped."

WITH STEPS:
"Analyze why our sales dropped. Follow these steps:
1. Examine market-level metrics first
2. Check industry trends
3. Review individual rep performance
4. Look for organizational changes
5. Summarize the most likely root cause"
```

Without steps, Claude picks one angle and runs with it.
With steps, it covers all angles before concluding.

---

## When to use which

```
Output guidelines  → almost every prompt (format, length, content)
Process steps      → complex problems, decisions, analysis tasks
Both together      → professional/production prompts
```

---

## Applied to Meal Plan

```
SCORE SO FAR: 3.92/10

What's still missing: no calorie numbers, no macros,
no portion weights, no meal timing — Claude is guessing
what "meal plan" means.

FIX: add output guidelines that spell it out explicitly.
```

---

## Cell 17 — Add output guidelines

```python
def run_prompt(prompt_inputs):
    prompt = f"""Generate a one-day meal plan for an athlete \
that meets their dietary restrictions.

- Height: {prompt_inputs["height"]}
- Weight: {prompt_inputs["weight"]}
- Goal: {prompt_inputs["goal"]}
- Dietary restrictions: {prompt_inputs["restrictions"]}

Guidelines:
1. Include accurate daily calorie amount
2. Show protein, fat, and carb amounts
3. Specify when to eat each meal
4. Use only foods that fit restrictions
5. List all portion sizes in grams
6. Keep budget-friendly if mentioned
"""
    messages = []
    add_user_message(messages, prompt)
    return chat(messages)
```

**What changed:** Added the 6-point guidelines block. First line untouched.

---

## Cell 18 — Evaluate

```python
results = evaluator.run_evaluation(
    run_prompt_function=run_prompt,
    dataset_file="dataset.json",
    extra_criteria="""
The output should include:
- Daily caloric total
- Macronutrient breakdown
- Meals with exact foods, portions, and timing
"""
)
```

```
# Expected output:
Average Score: 7.86/10
Individual scores: [7.5, 8.0, 8.0]
```

**3.92 → 7.86. More than doubled. From adding 6 lines.**

---

## The Pattern

```
Lesson 2 fix (clear first line):   2.32 → 3.92
Lesson 3 fix (specific guidelines): 3.92 → 7.86

Each lesson = one targeted addition to the same prompt.
Nothing removed. Just more signal given to Claude.
```

```
SCORE PROGRESS:
2/10  [##        ]  naive baseline
4/10  [####      ]  + clear first line
8/10  [########  ]  + specific guidelines  <-- you are here
```