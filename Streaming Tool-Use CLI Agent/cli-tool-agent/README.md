# Streaming Tool-Use CLI Agent

A terminal chat agent powered by Claude that streams replies live and can use tools to check the time or save study notes.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then paste your real API key into .env
```

## Run

```bash
python main.py
```

## Things to try

- `Explain photosynthesis simply.` — streams a plain answer using the tutor persona
- `What time is it right now?` — triggers the `get_current_time` tool
- `Save a note: review chapter 3 tonight.` — triggers `save_note`, then check `notes.txt`

## Structure

```
cli-tool-agent/
├── agent/
│   ├── client.py     # Anthropic SDK client
│   ├── config.py     # model, system prompt, tool schemas
│   ├── messages.py   # helpers to build the messages list
│   ├── tools.py      # tool functions + router
│   └── loop.py       # stream_turn and agent_turn logic
├── main.py           # entry point, chat loop
├── requirements.txt
├── .env.example
└── .gitignore
```
