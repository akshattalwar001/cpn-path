import json
import os

with open(".claude/settings.example.json") as f:
    content = f.read()

abs_path = os.getcwd()  # absolute path to wherever this project currently sits
content = content.replace("$PWD", abs_path)

with open(".claude/settings.local.json", "w") as f:
    f.write(content)

print("Created .claude/settings.local.json with your absolute paths.")