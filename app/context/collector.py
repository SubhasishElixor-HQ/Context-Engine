"""Read context data from PostgreSQL through SQLAlchemy."""

from sqlalchemy.orm import Session

from app.context.schema import UserProfile
from app.database.crud import get_user_record
from app.documents.retriever import retrieve_document_chunks
from app.memory.retriever import retrieve_relevant_memories


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

    def get_memories(self, user_id: str, query: str) -> list[str]:
        return retrieve_relevant_memories(
            self.session,
            user_id,
            query,
        )

    def get_documents(self, user_id: str, query: str) -> list[str]:
        return retrieve_document_chunks(
            self.session,
            user_id,
            query,
        )