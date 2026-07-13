import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    prompt = "List the files in the current directory"

    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Glob"]
    )

    async for message in query(prompt=prompt, options=options):
        print(message)

asyncio.run(main())