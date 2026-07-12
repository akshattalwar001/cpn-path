import sys
import json
import re

# Read all of stdin (Claude Code sends the tool call data here)
data = json.load(sys.stdin)
command = data["tool_input"]["command"]

# Rules from Step 1
dangerous_patterns = [
    r"rm\s+-rf",
    r"git\s+push\s+(--force|-f)",
    r"sudo",
    r"chmod\s+777",
    r">\s*/dev/",
]

for pattern in dangerous_patterns:
    if re.search(pattern, command):
        print(f"Blocked: command matched dangerous pattern ({pattern})", file=sys.stderr)
        sys.exit(2)  # deny

sys.exit(0)  # allow