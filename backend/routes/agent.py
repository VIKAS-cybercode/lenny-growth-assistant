from fastapi import APIRouter
from pydantic import BaseModel

from agent.tools import search_lenny


router = APIRouter(
    prefix="/agent",
    tags=["agent"],
)


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


@router.post("/search")
def agent_search(data: SearchRequest):
    return search_lenny(
        query=data.query,
        limit=data.limit,
    )