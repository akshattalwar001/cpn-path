import datetime


def get_current_time(format):
    return datetime.datetime.now().strftime(format)


def save_note(text):
    with open("notes.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")
    return f"Saved note: {text}"


tool_functions = {
    "get_current_time": get_current_time,
    "save_note": save_note,
}


def run_tool(name, tool_input):
    func = tool_functions[name]
    return func(**tool_input)
