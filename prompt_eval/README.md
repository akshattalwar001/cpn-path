# Prompt Evaluation

A five-step workflow for measuring and improving prompts through objective scoring.

## The Workflow

### 1. Draft a Prompt

Write an initial prompt to use as your baseline:

```python
prompt = f"""
Please answer the user's question:

{question}
"""
```

### 2. Create an Eval Dataset

Assemble sample inputs that represent real production queries. Example:

- "What's 2+2?"
- "How do I make oatmeal?"
- "How far away is the Moon?"

Build these by hand or generate them with Claude.

### 3. Run Through the Model

Merge each input into your prompt template and send it to Claude. Collect all responses.

### 4. Grade the Responses

Use a grader (another Claude call) to score each response 1-10. Average the scores for an objective baseline.

| Question | Score |
|---|---|
| What's 2+2? | 10 |
| How do I make oatmeal? | 4 |
| How far away is the Moon? | 9 |

**Average: 7.66**

### 5. Iterate

Modify the prompt and repeat steps 3-4. Compare average scores across versions to confirm improvements.

```python
prompt = f"""
Please answer the user's question:

{question}

Answer with ample detail.
"""
# New average: 8.7
```

## Key Benefit

Numeric scores let you compare prompt versions objectively, removing guesswork from prompt engineering.
