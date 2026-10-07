"""Coordinate PostgreSQL collection and context assembly."""

from sqlalchemy.orm import Session

from app.context.builder import ContextBuilder
from app.context.collector import ContextCollector
from app.context.schema import ContextRequest, ContextResponse


class ContextEngine:
    def __init__(self) -> None:
        self.builder = ContextBuilder()

    def build(self, request: ContextRequest, session: Session) -> ContextResponse | None:
        collector = ContextCollector(session)
        user = collector.get_user_profile(request.user_id)
        if user is None:
            return None
        memories = collector.get_memories(request.user_id)
        documents = collector.get_documents(request.user_id)
        return self.builder.build(request, user, memories, documents)
