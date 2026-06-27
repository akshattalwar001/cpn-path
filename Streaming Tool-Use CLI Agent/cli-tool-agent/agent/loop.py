from .client import client
from .config import MODEL, SYSTEM_PROMPT, TOOLS
from .messages import add_assistant_message, add_user_message
from .tools import run_tool
from . import ui


def stream_turn(messages):
    header_printed = False
    with client.messages.stream(
        model=MODEL,
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        tools=TOOLS,
        messages=messages,
    ) as stream:
        for chunk in stream.text_stream:
            if not header_printed:
                ui.tutor_start()
                header_printed = True
            ui.tutor_chunk(chunk)
        final = stream.get_final_message()
    if header_printed:
        ui.tutor_end()
    return final


def agent_turn(messages):
    while True:
        response = stream_turn(messages)
        add_assistant_message(messages, response.content)

        if response.stop_reason != "tool_use":
            break

        result_blocks = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            ui.tool_call(block.name, block.input)
            try:
                result = run_tool(block.name, block.input)
                is_error = False
            except Exception as e:
                result = f"Error running {block.name}: {e}"
                is_error = True
            ui.tool_result(str(result), is_error)
            result_blocks.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(result),
                "is_error": is_error,
            })

        add_user_message(messages, result_blocks)
