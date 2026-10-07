"""Create, read, update, and delete persistent user profile data."""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.context.schema import UserCreate, UserUpdate
from app.database.models import (
    ProfileRecord,
    ProjectRecord,
    SkillRecord,
    UserRecord,
)


def _user_query():
    return select(UserRecord).options(
        selectinload(UserRecord.profile),
        selectinload(UserRecord.skills),
        selectinload(UserRecord.projects),
    )


def get_user_record(session: Session, user_id: str) -> UserRecord | None:
    return session.scalar(_user_query().where(UserRecord.id == user_id))


def create_user_record(session: Session, data: UserCreate) -> UserRecord:
    user = UserRecord(
        id=data.id,
        profile=ProfileRecord(name=data.name, education=data.education),
        skills=[SkillRecord(name=name) for name in data.skills],
        projects=[ProjectRecord(name=name) for name in data.projects],
    )
    session.add(user)
    session.commit()
    saved_user = get_user_record(session, user.id)
    if saved_user is None:
        raise RuntimeError("User was committed but could not be read back")
    return saved_user


def update_user_record(
    session: Session, user_id: str, data: UserUpdate
) -> UserRecord | None:
    user = get_user_record(session, user_id)
    if user is None:
        return None

    changes = data.model_dump(exclude_unset=True)
    if changes.get("name") is not None:
        user.profile.name = changes["name"]
    if changes.get("education") is not None:
        user.profile.education = changes["education"]
    if changes.get("skills") is not None:
        user.skills.clear()
        session.flush()
        user.skills = [SkillRecord(name=name) for name in changes["skills"]]
    if changes.get("projects") is not None:
        user.projects.clear()
        session.flush()
        user.projects = [ProjectRecord(name=name) for name in changes["projects"]]

    session.commit()
    return get_user_record(session, user_id)


def delete_user_record(session: Session, user_id: str) -> bool:
    user = session.get(UserRecord, user_id)
    if user is None:
        return False
    session.delete(user)
    session.commit()
    return True
