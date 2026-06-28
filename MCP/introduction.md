What is MCP?

## The Problem
Building a GitHub chatbot means writing schemas and function implementations for every GitHub feature — repos, PRs, issues, projects, and more. That's a massive amount of code to write, test, and maintain.

## What MCP Does
MCP shifts that burden away from you to a dedicated MCP server. Someone else has already written all the tool definitions and implementations. You just connect to the MCP server and use them.

## Key Concepts
- **MCP Client** — your server/application
- **MCP Server** — a pre-built integration that wraps an outside service (GitHub, AWS, etc.)
- **What's inside an MCP server** — tool schemas, tool implementations, prompts, and resources

## Common Misconceptions

**"Isn't MCP just tool use?"** — No. Tool use is the mechanism. MCP is about *who writes the tools*. Without MCP, you write them. With MCP, someone else already did.

**"Who builds MCP servers?"** — Anyone. Often the service providers themselves (e.g. AWS releasing an official MCP server for their services).

## One Line Summary
MCP = pre-packaged integrations so you don't have to write tool definitions from scratch.