import asyncio
from claude_agent_sdk import query

async def main():
    prompt = "List the files in the current directory"

    async for message in query(prompt=prompt):
        print(message)

asyncio.run(main())