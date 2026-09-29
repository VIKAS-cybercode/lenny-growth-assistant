from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from models.user import User
from schemas import AnonymousUserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/anonymous", response_model=AnonymousUserResponse)
def create_anonymous_user(db: Session = Depends(get_db)):
    user = User()

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"user_id": user.id}