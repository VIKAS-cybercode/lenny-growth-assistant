from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AnonymousUserResponse(BaseModel):
    user_id: UUID


class ConversationCreate(BaseModel):
    user_id: UUID


class ConversationResponse(BaseModel):
    conversation_id: UUID
    title: str | None = None


class MessageCreate(BaseModel):
    content: str


class SourceResponse(BaseModel):
    title: str
    source: str
    chunk: int


class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    created_at: datetime
    sources: list[SourceResponse] | None = None

    model_config = {
        "from_attributes": True
    }


class ArtifactResponse(BaseModel):
    type: str
    title: str
    content: str


class AssistantMessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    created_at: datetime
    sources: list[SourceResponse]
    artifact: ArtifactResponse | None = None

    model_config = {
        "from_attributes": True
    }