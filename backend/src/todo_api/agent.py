"""OpenAI Agents SDK agent for conversational task management."""

import os
import sys

from agents import Agent, Runner
from agents.mcp import MCPServerStdio

from todo_api.config import OPENAI_API_KEY

# Ensure OpenAI API key is set for the SDK
os.environ.setdefault("OPENAI_API_KEY", OPENAI_API_KEY)

SYSTEM_PROMPT = """You are a friendly and helpful task management assistant. You help users manage their to-do list through natural language conversation.

You can:
- Add new tasks
- List all tasks
- Mark tasks as complete or incomplete
- Delete tasks
- Update task titles and descriptions

Guidelines:
- Always confirm actions you take (e.g., "Done! I've added 'Buy groceries' to your task list.")
- When listing tasks, format them in a clear, readable way.
- If a user's request is ambiguous, ask for clarification.
- Be concise but friendly in your responses.
- When a user refers to a task by name or number, use the list_tasks tool first to find the correct task ID, then perform the requested action.
- The user_id parameter is already set for all tools — just pass it as provided.
"""


def _get_mcp_server() -> MCPServerStdio:
    """Create an MCP server subprocess pointing to our mcp_server.py."""
    return MCPServerStdio(
        params={
            "command": sys.executable,
            "args": ["-m", "todo_api.mcp_server"],
            "cwd": os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "env": {
                **os.environ,
                "PYTHONPATH": os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            },
        },
        name="todo-tasks",
    )


async def run_agent(user_id: str, messages: list[dict]) -> str:
    """Run the AI agent with conversation history and return the response.

    Args:
        user_id: The authenticated user's ID (passed to MCP tools).
        messages: List of {"role": "user"|"assistant", "content": "..."} dicts.

    Returns:
        The assistant's response text.
    """
    mcp_server = _get_mcp_server()

    # Inject user_id into the system prompt so the agent knows which user it's operating for
    system_with_user = (
        f"{SYSTEM_PROMPT}\n\n"
        f"IMPORTANT: For all tool calls, use user_id=\"{user_id}\". "
        f"This is the authenticated user you are helping."
    )

    agent = Agent(
        name="Todo Assistant",
        instructions=system_with_user,
        mcp_servers=[mcp_server],
    )

    # Build input from conversation history
    input_messages = []
    for msg in messages:
        input_messages.append({
            "role": msg["role"],
            "content": msg["content"],
        })

    async with mcp_server:
        result = await Runner.run(agent, input=input_messages)

    return result.final_output
