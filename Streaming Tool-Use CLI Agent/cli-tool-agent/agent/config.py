MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = (
    "You are a friendly and patient tutor for students. "
    "Explain things simply, in small steps, and use short examples. "
    "Encourage the student. When the student wants to remember something, "
    "offer to save it as a note using your save_note tool. "
    "When asked about the date or time, use your get_current_time tool."
)

TOOLS = [
    {
        "name": "get_current_time",
        "description": (
            "Returns the current local date/time. "
            "Use when the student asks what time or date it is."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "description": "A Python strftime format string, e.g. '%Y-%m-%d %H:%M'.",
                }
            },
            "required": ["format"],
        },
    },
    {
        "name": "save_note",
        "description": (
            "Saves a short study note to a file so the student can review it later. "
            "Use when the student wants to remember something."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The note text to save.",
                }
            },
            "required": ["text"],
        },
    },
]
