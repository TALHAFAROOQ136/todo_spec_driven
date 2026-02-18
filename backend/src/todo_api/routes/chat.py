"""Chat endpoint for AI-powered task management."""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from todo_api.auth import get_current_user_id
from todo_api.db import get_session
from todo_api.models import ChatRequest, ChatResponse, Conversation, Message
from todo_api.agent import run_agent

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> ChatResponse:
    # 1. Get or create conversation
    if body.conversation_id:
        conversation = await session.get(Conversation, body.conversation_id)
        if not conversation or conversation.user_id != user_id:
            conversation = None

    if not body.conversation_id or not conversation:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

    # 2. Load conversation history from DB
    result = await session.exec(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)  # type: ignore[arg-type]
    )
    history = result.all()

    messages = [{"role": m.role, "content": m.content} for m in history]
    messages.append({"role": "user", "content": body.message})

    # 3. Store user message
    user_msg = Message(
        conversation_id=conversation.id,
        role="user",
        content=body.message,
    )
    session.add(user_msg)
    await session.commit()

    # 4. Run agent
    response_text = await run_agent(user_id, messages)

    # 5. Store assistant response
    assistant_msg = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=response_text,
    )
    session.add(assistant_msg)

    # Update conversation timestamp and title
    conversation.updated_at = datetime.now(timezone.utc)
    if not conversation.title and len(body.message) > 0:
        conversation.title = body.message[:100]
    session.add(conversation)
    await session.commit()

    # 6. Return response
    return ChatResponse(
        response=response_text,
        conversation_id=conversation.id,
    )
