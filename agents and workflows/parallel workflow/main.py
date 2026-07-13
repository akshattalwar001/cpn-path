import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

TEXT = """
Our product helps teams ship faster by automating repetitive tasks.
It's simple, it works, and people like it a lot honestly.
"""

async def evaluate(criterion: str, instructions: str) -> str:
    prompt = f"Evaluate this text for {criterion}.\n{instructions}\n\nText:\n{TEXT}"
    result_text = ""
    async for message in query(prompt=prompt, options=ClaudeAgentOptions(allowed_tools=[])):
        if hasattr(message, "content"):
            for block in message.content:
                if hasattr(block, "text"):
                    result_text += block.text
    return f"[{criterion.upper()}]\n{result_text}"

async def aggregate(results: list[str]) -> str:
    combined = "\n\n".join(results)
    prompt = f"""Here are 3 independent evaluations of the same text, covering clarity, tone, and grammar:

{combined}

Based on all 3, give a final verdict: is this text ready to publish as-is, or does it need revision? Be specific about what to fix, if anything."""

    final_text = ""
    async for message in query(prompt=prompt, options=ClaudeAgentOptions(allowed_tools=[])):
        if hasattr(message, "content"):
            for block in message.content:
                if hasattr(block, "text"):
                    final_text += block.text
    return final_text

async def main():
    # Step 2+3: run 3 evaluations in parallel
    tasks = [
        evaluate("clarity", "Is the message easy to understand? Rate 1-10 and explain."),
        evaluate("tone", "Is the tone professional and appropriate? Rate 1-10 and explain."),
        evaluate("grammar", "Are there grammar or spelling issues? Rate 1-10 and explain."),
    ]
    results = await asyncio.gather(*tasks)

    for r in results:
        print(r)
        print("---")

    # Step 4: combine into one final verdict
    verdict = await aggregate(results)
    print("\n=== FINAL VERDICT ===")
    print(verdict)

asyncio.run(main())