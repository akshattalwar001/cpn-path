import sys
import json

data = json.load(sys.stdin)

with open("post-log.json", "a") as f:
    f.write(json.dumps(data, indent=2) + "\n---\n")

sys.exit(0)