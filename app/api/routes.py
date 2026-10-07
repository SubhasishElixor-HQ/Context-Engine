"""User profile CRUD and context-building endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.context.engine import ContextEngine
from app.context.schema import (
    ContextRequest,
    ContextResponse,
    UserCreate,
    UserProfile,
    UserUpdate,
)
from app.database.connection import get_db_session
from app.database.crud import (
    create_user_record,
    delete_user_record,
    get_user_record,
    update_user_record,
)

router = APIRouter(tags=["context and users"])
context_engine = ContextEngine()


def to_user_profile(record) -> UserProfile:
    return UserProfile(
        id=record.id,
        name=record.profile.name,
        education=record.profile.education,
        skills=[skill.name for skill in record.skills],
        projects=[project.name for project in record.projects],
    )


@router.post("/users", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate, session: Session = Depends(get_db_session)
) -> UserProfile:
    if get_user_record(session, data.id) is not None:
        raise HTTPException(status_code=409, detail="A user with this ID already exists")
    try:
        record = create_user_record(session, data)
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="User data conflicts with an existing record") from exc
    return to_user_profile(record)


@router.get("/users/{user_id}", response_model=UserProfile)
def read_user(user_id: str, session: Session = Depends(get_db_session)) -> UserProfile:
    record = get_user_record(session, user_id)
    if record is None:
        raise HTTPException(status_code=404, detail="User not found")
    return to_user_profile(record)


@router.put("/users/{user_id}", response_model=UserProfile)
def edit_user(
    user_id: str,
    data: UserUpdate,
    session: Session = Depends(get_db_session),
) -> UserProfile:
    try:
        record = update_user_record(session, user_id, data)
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="User data conflicts with an existing record") from exc
    if record is None:
        raise HTTPException(status_code=404, detail="User not found")
    return to_user_profile(record)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: str, session: Session = Depends(get_db_session)) -> Response:
    if not delete_user_record(session, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/context/build", response_model=ContextResponse)
def build_context(
    request: ContextRequest,
    session: Session = Depends(get_db_session),
) -> ContextResponse:
    context = context_engine.build(request, session)
    if context is None:
        raise HTTPException(status_code=404, detail="User not found")
    return context
