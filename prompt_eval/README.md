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

## Progress: 001_prompt_evals.ipynb

The notebook implements a prompt eval pipeline for AWS-related code generation tasks.

### What's built

**Client setup:** Uses `claude-haiku-4-5` with `python-dotenv` for API key management.

**Helper functions:** `add_user_message`, `add_assistant_message`, and a `chat` wrapper supporting system prompts, temperature, and stop sequences.

**Dataset generation:** `generate_dataset()` prompts Claude to produce an eval dataset of AWS tasks (Python, JSON, or Regex). Uses prefill (`assistant: "```json"`) and a stop sequence to extract clean JSON output.

**Generated dataset** (saved to `dataset.json`):

| # | Task |
|---|---|
| 1 | Validate an AWS S3 bucket name with a Python function |
| 2 | Create an IAM policy JSON for read-only S3 access |
| 3 | Write a regex matching valid EC2 instance IDs |

### Next steps
- Run prompts through the model against the dataset
- Grade responses with a second Claude call (1-10 scoring)
- Compare prompt versions by average score
