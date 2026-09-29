from uuid import UUID
from datetime import datetime, timezone

from agent.agent import run_agent
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from rag.query import rewrite_query
from dependencies import get_db
from models.user import User
from models.conversation import Conversation
from models.message import Message

from schemas import (
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
    AssistantMessageResponse,
    SourceResponse,
    ArtifactResponse,
)


router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)


# ============================================================
# Create conversation
# ============================================================

@router.post("", response_model=ConversationResponse)
def create_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db),
):
    # Make sure the user exists
    user = db.get(User, data.user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    conversation = Conversation(
        user_id=data.user_id,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return {
        "conversation_id": conversation.id
    }


# ============================================================
# Create message
# ============================================================

@router.post(
    "/{conversation_id}/messages",
    response_model=AssistantMessageResponse,
)
def create_message(
    conversation_id: UUID,
    data: MessageCreate,
    db: Session = Depends(get_db),
):
    conversation = db.get(
        Conversation,
        conversation_id,
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    # --------------------------------------------------------
    # Get previous conversation messages
    # --------------------------------------------------------
    #
    # This happens BEFORE saving the current user message.
    # Therefore, history contains only previous messages.
    #

    previous_messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(
            Message.created_at.asc()
        )
        .all()
    )

    conversation_history = []

    for message in previous_messages:
        conversation_history.append(
            f"{message.role.upper()}: {message.content}"
        )

    history = "\n".join(conversation_history)

    # --------------------------------------------------------
    # Save current user message
    # --------------------------------------------------------

    user_message = Message(
        conversation_id=conversation_id,
        role="user",
        content=data.content,
    )

    db.add(user_message)

    # --------------------------------------------------------
    # Set conversation title from first user message
    # --------------------------------------------------------

    if conversation.title is None:
        conversation.title = data.content[:60]

    # --------------------------------------------------------
    # Update conversation activity time
    # --------------------------------------------------------

    conversation.updated_at = datetime.now(timezone.utc)

    db.commit()
    #db.refresh(user_message)

    try:
        # ----------------------------------------------------
        # Build contextual retrieval query
        # ----------------------------------------------------
        #
        # For a follow-up such as:
        #
        # "What does he recommend?"
        #
        # the previous conversation helps rewrite_query()
        # understand who "he" refers to and what topic we
        # are discussing.
        #

        retrieval_query = rewrite_query(
            question=data.content,
            history=history,
        )

        # ----------------------------------------------------
        # Run Pi agent
        # ----------------------------------------------------
        #
        # The agent:
        #
        # 1. Receives the application-controlled search query
        # 2. Calls search_lenny exactly once
        # 3. Retrieves relevant Lenny transcript content
        # 4. Generates the grounded answer
        # 5. Returns the answer and source metadata
        #

        agent_result = run_agent(
            question=data.content,
            search_query=retrieval_query,
            history=history,
        )

        answer = agent_result["answer"]
        retrieved_sources = agent_result["sources"]
        artifact = agent_result.get("artifact")

        # ----------------------------------------------------
        # Build API source objects
        # ----------------------------------------------------
        #
        # Sources come from actual retrieval results.
        # The LLM does not generate these.
        #

        sources = [
            SourceResponse(
                title=source["title"],
                source=source["source"],
                chunk=source["chunk"],
            )
            for source in retrieved_sources
        ]

        # ----------------------------------------------------
        # Save assistant message
        # ----------------------------------------------------

        assistant_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
            sources=[
                {
                    "title": source.title,
                    "source": source.source,
                    "chunk": source.chunk,
                }
                for source in sources
            ],
        )

        db.add(assistant_message)

        # ----------------------------------------------------
        # Update conversation activity time again
        # ----------------------------------------------------

        conversation.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(assistant_message)
        db.refresh(conversation)

        # ----------------------------------------------------
        # Return assistant response
        # ----------------------------------------------------

        return AssistantMessageResponse(
            id=assistant_message.id,
            conversation_id=assistant_message.conversation_id,
            role=assistant_message.role,
            content=assistant_message.content,
            created_at=assistant_message.created_at,
            sources=sources,
            artifact=(
                ArtifactResponse(**artifact)
                if artifact
                else None
            ),
        )

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate answer: {str(e)}",
        )


# ============================================================
# Get user's conversations
# ============================================================

@router.get(
    "/user/{user_id}",
    response_model=list[ConversationResponse],
)
def get_user_conversations(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    conversations = (
        db.query(Conversation)
        .filter(
            Conversation.user_id == user_id
        )
        .order_by(
            Conversation.updated_at.desc()
        )
        .all()
    )

    return [
        {
            "conversation_id": conversation.id,
            "title": conversation.title,
        }
        for conversation in conversations
    ]


# ============================================================
# Get one conversation
# ============================================================

@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def get_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
):
    conversation = db.get(
        Conversation,
        conversation_id,
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return {
        "conversation_id": conversation.id,
        "title": conversation.title,
    }


# ============================================================
# Get conversation messages
# ============================================================

@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
def get_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db),
):
    conversation = db.get(
        Conversation,
        conversation_id,
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(
            Message.created_at.asc()
        )
        .all()
    )

    return messages