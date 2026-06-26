# Lesson 7: Building a Robust Conversation Loop

## Detecting When Claude is Done
`stop_reason` tells you if Claude wants a tool or is finished. If it's `"tool_use"`, keep looping. Anything else means Claude has the final answer.

## Handling Multiple Tool Calls
Claude can request several tools in one response. Filter all `tool_use` blocks and process each one separately, sending back a result block for every single one.

## Error Handling
Even if a tool fails, you must send a result block back. Set `is_error: True` and include the error message so Claude knows what went wrong and can respond accordingly.

## Scalable Tool Routing
Instead of putting all logic inside the loop, create a separate `run_tool` function that maps tool names to their implementations. This makes adding new tools clean and simple.

> **Continue in the same notebook**

```python
import json

def run_tool(tool_name, tool_input):
    if tool_name == "get_current_datetime":
        return get_current_datetime(**tool_input)
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

def run_tools(message):
    tool_requests = [block for block in message.content if block.type == "tool_use"]
    tool_result_blocks = []
    
    for tool_request in tool_requests:
        try:
            tool_output = run_tool(tool_request.name, tool_request.input)
            tool_result_blocks.append({
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": json.dumps(tool_output),
                "is_error": False
            })
        except Exception as e:
            tool_result_blocks.append({
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": f"Error: {e}",
                "is_error": True
            })
    
    return tool_result_blocks

def run_conversation(messages):
    while True:
        response = chat(messages, tools=[get_current_datetime_schema])
        add_assistant_message(messages, response)
        print(text_from_message(response))
        
        if response.stop_reason != "tool_use":
            break
        
        tool_results = run_tools(response)
        add_user_message(messages, tool_results)
    
    return messages
```

```python
messages = []
add_user_message(messages, "What is the exact time, formatted as HH:MM:SS?")
run_conversation(messages)
```