"""V1 data source for profile, memories, and documents."""

from app.context.schema import UserProfile


class ContextCollector:
    """Collect context inputs; V1 uses a sample profile and empty stores."""

    def get_user_profile(self, user_id: str) -> UserProfile:
        """Return the sample profile, assigning the requested user ID."""
        return UserProfile(
            id=user_id,
            name="Subhasish",
            education="B.Tech CS-AIML",
            skills=["Python", "Machine Learning", "Deep Learning"],
            projects=["RAG Research Paper Assistant"],
        )

    def get_memories(self, user_id: str) -> list[str]:
        """Return no memories until a memory store is added in a later version."""
        return []

    def get_documents(self, user_id: str) -> list[str]:
        """Return no documents until document ingestion is added later."""
        return []
