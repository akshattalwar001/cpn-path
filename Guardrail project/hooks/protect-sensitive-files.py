import sys
import json
import fnmatch

data = json.load(sys.stdin)
file_path = data["tool_input"]["file_path"]

# Rules from Step 1
protected_patterns = [
    ".env",
    ".env.*",
    "secrets.json",
    "*.pem",
    "*.key",
    "package-lock.json",
    "yarn.lock",
]

for pattern in protected_patterns:
    if fnmatch.fnmatch(file_path, f"*{pattern}"):
        print(f"Blocked: '{file_path}' matches protected pattern '{pattern}'", file=sys.stderr)
        sys.exit(2)  # deny

sys.exit(0)  # allow