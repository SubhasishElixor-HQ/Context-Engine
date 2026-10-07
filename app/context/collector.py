"""Read context data from PostgreSQL through SQLAlchemy."""

from sqlalchemy.orm import Session

from app.context.schema import UserProfile
from app.database.crud import get_user_record


class ContextCollector:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_user_profile(self, user_id: str) -> UserProfile | None:
        user = get_user_record(self.session, user_id)
        if user is None or user.profile is None:
            return None
        return UserProfile(
            id=user.id,
            name=user.profile.name,
            education=user.profile.education,
            skills=[skill.name for skill in user.skills],
            projects=[project.name for project in user.projects],
        )

    def get_memories(self, user_id: str) -> list[str]:
        """Memory storage is a later version; V2 returns an empty list."""
        return []

    def get_documents(self, user_id: str) -> list[str]:
        """Document retrieval is a later version; V2 returns an empty list."""
        return []
