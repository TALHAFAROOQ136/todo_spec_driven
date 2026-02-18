"""MCP Server exposing task management tools for the AI agent."""

import asyncio
import uuid
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP
from sqlmodel import select

from todo_api.db import async_session
from todo_api.models import Task

mcp = FastMCP("todo-tasks")


@mcp.tool()
async def add_task(user_id: str, title: str, description: str = "") -> str:
    """Create a new task for the user.

    Args:
        user_id: The ID of the user who owns the task.
        title: The title of the task.
        description: Optional description for the task.
    """
    async with async_session() as session:
        task = Task(
            title=title.strip(),
            description=description,
            user_id=user_id,
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return f"Task created: '{task.title}' (id: {task.id})"


@mcp.tool()
async def list_tasks(user_id: str) -> str:
    """List all tasks for the user.

    Args:
        user_id: The ID of the user whose tasks to list.
    """
    async with async_session() as session:
        result = await session.exec(
            select(Task).where(Task.user_id == user_id)
        )
        tasks = result.all()
        if not tasks:
            return "No tasks found. The task list is empty."
        lines = []
        for i, t in enumerate(tasks, 1):
            status = "done" if t.completed else "pending"
            desc = f" — {t.description}" if t.description else ""
            lines.append(f"{i}. [{status}] {t.title}{desc} (id: {t.id})")
        return "\n".join(lines)


@mcp.tool()
async def complete_task(user_id: str, task_id: str) -> str:
    """Toggle the completion status of a task.

    Args:
        user_id: The ID of the user who owns the task.
        task_id: The UUID of the task to toggle.
    """
    async with async_session() as session:
        task = await session.get(Task, uuid.UUID(task_id))
        if not task or task.user_id != user_id:
            return "Task not found or access denied."
        task.completed = not task.completed
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        await session.commit()
        status = "completed" if task.completed else "incomplete"
        return f"Task '{task.title}' marked as {status}."


@mcp.tool()
async def delete_task(user_id: str, task_id: str) -> str:
    """Delete a task.

    Args:
        user_id: The ID of the user who owns the task.
        task_id: The UUID of the task to delete.
    """
    async with async_session() as session:
        task = await session.get(Task, uuid.UUID(task_id))
        if not task or task.user_id != user_id:
            return "Task not found or access denied."
        title = task.title
        await session.delete(task)
        await session.commit()
        return f"Task '{title}' has been deleted."


@mcp.tool()
async def update_task(
    user_id: str,
    task_id: str,
    title: str | None = None,
    description: str | None = None,
) -> str:
    """Update the title and/or description of a task.

    Args:
        user_id: The ID of the user who owns the task.
        task_id: The UUID of the task to update.
        title: New title for the task (optional).
        description: New description for the task (optional).
    """
    async with async_session() as session:
        task = await session.get(Task, uuid.UUID(task_id))
        if not task or task.user_id != user_id:
            return "Task not found or access denied."
        if title is not None:
            task.title = title.strip()
        if description is not None:
            task.description = description
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        await session.commit()
        return f"Task updated: '{task.title}'."


if __name__ == "__main__":
    mcp.run(transport="stdio")
