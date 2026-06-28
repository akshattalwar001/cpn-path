# Claude API: Learning Experiments

A personal learning repo for exploring the Claude API hands-on. Each notebook covers one concept, building up from basic API calls to RAG pipelines and extended thinking.

## Setup

```bash
python -m venv venv
venv\Scripts\Activate.ps1

pip install -r requirements.txt
venv\Scripts\pip install jupyter ipykernel sentence-transformers rank-bm25
venv\Scripts\python -m ipykernel install --user --name exp-venv --display-name "Python (exp-venv)"
```

Open notebooks in VS Code and select the **Python (exp-venv)** kernel.

## What's Covered

### Claude API Basics
- `001_requests.ipynb`: first API call, message structure
- `002_system_prompts.ipynb`: shaping model behavior with system prompts
- `003_streaming.ipynb`: streaming responses
- `004_structured_data.ipynb`: extracting structured output

### Prompt Engineering
- `prompt_eng/001_prompting.ipynb`: prompting techniques and patterns
- `prompt_eval/001_prompt_evals.ipynb`: evaluating and comparing prompts

### Tool Use
- `tool_use/001_tool_use.ipynb`: giving Claude tools to call
- `tool_use/001_multi_tools.ipynb`: multiple tools in one turn
- `tool_use/Fine-Grained Tool Calling/`: streaming tool calls with fine-grained control
- `tool_use/001_text_editor_tool.ipynb`: Claude's built-in text editor tool for file editing

### RAG (Retrieval-Augmented Generation)
- `RAG/001_chunking.ipynb`: four chunking strategies (character, section, sentence, semantic)
- `RAG/002_searching-n-embeddings.ipynb`: semantic search with sentence-transformers
- `RAG/003_unified_hybrid_search.ipynb`: hybrid search combining BM25 and vector search via Reciprocal Rank Fusion (RRF)

### Thinking and Caching
- `Thinking and Caching/001_extended_thinking.ipynb`: extended thinking, how it works, when to use it, redacted thinking

## FastAPI App

A small student data API lives alongside the notebooks, used to practice endpoint generation with Claude Code.

```bash
venv\Scripts\uvicorn main:app --reload
# Docs at http://127.0.0.1:8000/docs
```
