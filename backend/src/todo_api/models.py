import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, Field as PydanticField
from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field


# --- SQLModel Table ---


class Task(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )


# --- Pydantic Request Models ---


class TaskCreate(BaseModel):
    title: str = PydanticField(min_length=1, max_length=200)
    description: str = PydanticField(default="", max_length=1000)


class TaskUpdate(BaseModel):
    title: str = PydanticField(min_length=1, max_length=200)
    description: str = PydanticField(default="", max_length=1000)


# --- Pydantic Response Models ---


class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    completed: bool
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]


class MessageResponse(BaseModel):
    message: str


# --- Phase 3: Chat Models ---


class Conversation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(index=True)
    title: str | None = Field(default=None, max_length=200)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )


class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(index=True)
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )


# --- Chat Request/Response ---


class ChatRequest(BaseModel):
    message: str = PydanticField(min_length=1)
    conversation_id: uuid.UUID | None = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: uuid.UUID
