import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def ask(prompt: str) -> str:
    result_text = ""
    async for message in query(prompt=prompt, options=ClaudeAgentOptions(allowed_tools=[])):
        if hasattr(message, "content"):
            for block in message.content:
                if hasattr(block, "text"):
                    result_text += block.text
    return result_text

async def main():
    # Step 1: just write, no constraints enforced strictly
    write_prompt = """Write a short (150 word) article about the benefits of automating repetitive tasks at work.
    Do not mention you're an AI. Avoid emojis. Avoid clichéd or overly casual language. Write in a professional, technical tone."""

    draft = await ask(write_prompt)
    print("=== DRAFT (Step 1) ===")
    print(draft)
    print()

    # Step 2: focused revision pass
    fix_prompt = f"""Revise the article below. Follow these steps exactly:
1. Identify any location where the text identifies the author as an AI and remove it
2. Find and remove all emojis
3. Locate any cringey or overly casual writing and replace it with text a technical writer would use

Article:
{draft}"""

    final = await ask(fix_prompt)
    print("=== FINAL (Step 2) ===")
    print(final)

asyncio.run(main())