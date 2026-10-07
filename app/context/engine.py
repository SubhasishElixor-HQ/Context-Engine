"""Coordinate collection and context assembly."""

from app.context.builder import ContextBuilder
from app.context.collector import ContextCollector
from app.context.schema import ContextRequest, ContextResponse


class ContextEngine:
    """Orchestrate the V1 context-building pipeline."""

    def __init__(self) -> None:
        self.collector = ContextCollector()
        self.builder = ContextBuilder()

    def build(self, request: ContextRequest) -> ContextResponse:
        user = self.collector.get_user_profile(request.user_id)
        memories = self.collector.get_memories(request.user_id)
        documents = self.collector.get_documents(request.user_id)
        return self.builder.build(request, user, memories, documents)
