"""Assemble collected context into the API response model."""

from app.context.schema import ContextRequest, ContextResponse, UserProfile


class ContextBuilder:
    """Combine user/task inputs with data collected by ContextCollector."""

    def build(
        self,
        request: ContextRequest,
        user: UserProfile,
        memories: list[str],
        documents: list[str],
    ) -> ContextResponse:
        return ContextResponse(
            user=user,
            goal=request.goal,
            task=request.task,
            memories=memories,
            documents=documents,
        )
