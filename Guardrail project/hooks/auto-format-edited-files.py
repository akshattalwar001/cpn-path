import sys
import json
import subprocess

data = json.load(sys.stdin)
file_path = data["tool_input"]["file_path"]

if file_path.endswith((".js", ".jsx", ".ts", ".tsx")):
    subprocess.run(["npx", "prettier", "--write", file_path])
elif file_path.endswith(".py"):
    subprocess.run(["black", file_path])

# PostToolUse can't block anyway, so we just always exit 0
sys.exit(0)