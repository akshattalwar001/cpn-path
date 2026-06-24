# Lesson 4: XML Tags for Structure

---

## The Core Idea

When prompts get long or mix different types of content, Claude can lose track of what's what. XML tags draw clear boundaries.

```
WITHOUT TAGS:
Claude sees one wall of text.
Instructions bleed into data.

WITH TAGS:
Each section has a clear label.
Claude knows exactly what each chunk is.
```

---

## When it matters most

```
- Large amounts of data (20 pages of sales records)
- Mixing types (code + docs + instructions)
- Multiple variables interpolated into one prompt
- Any time you're asking Claude to "use the data above"
```

For short prompts it helps a little. For complex prompts it's essential.

---

## Bad vs Good

```
BAD (no boundaries):
Debug this code. def calculate(x): return x*2
Parameters should be typed. The function should
handle edge cases. Always validate inputs first...
(where does the code end? where do instructions begin?)

GOOD (with tags):
<my_code>
def calculate(x):
    return x * 2
</my_code>

<docs>
Parameters should be typed.
Always validate inputs first.
</docs>

Debug the code using the docs above.
```

---

## Tag naming tip

```
GENERIC (worse):   <data>, <text>, <input>
SPECIFIC (better): <sales_records>, <athlete_information>, <my_code>

Descriptive names = Claude understands purpose, not just boundary.
```

---

## Applied to Meal Plan

```
SCORE SO FAR: 7.86/10

The athlete data (height, weight, goal, restrictions)
is just floating in the prompt as a list.
Wrapping it in a tag makes the boundary explicit.
```

---

## Cell 19 — Add XML tags

```python
def run_prompt(prompt_inputs):
    prompt = f"""Generate a one-day meal plan for an athlete \
that meets their dietary restrictions.

<athlete_information>
- Height: {prompt_inputs["height"]}
- Weight: {prompt_inputs["weight"]}
- Goal: {prompt_inputs["goal"]}
- Dietary restrictions: {prompt_inputs["restrictions"]}
</athlete_information>

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

**What changed:** Wrapped the athlete data in `<athlete_information>` tags. Everything else untouched.

---

## Cell 20 — Evaluate

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
Average Score: 8.20/10
Individual scores: [8.0, 8.5, 8.1]
```

---

## Score progress so far

```
2/10  [##        ]  naive baseline
4/10  [####      ]  + clear first line  (lesson 2)
8/10  [########  ]  + specific guidelines (lesson 3)
8.2/10 [########  ]  + XML tags           (lesson 4)
```

XML tags gave a smaller jump here because the prompt is still simple. The gain grows as prompt complexity grows.

---

## The Rule

```
Small prompt, few variables  → tags help a little
Large prompt, mixed content  → tags are essential

Always ask: "Could Claude confuse my instructions
             with my data?" If yes, add tags.
```