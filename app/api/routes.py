"""HTTP endpoints for building context."""

from fastapi import APIRouter

from app.context.engine import ContextEngine
from app.context.schema import ContextRequest, ContextResponse

router = APIRouter(prefix="/context", tags=["context"])
context_engine = ContextEngine()


@router.post("/build", response_model=ContextResponse)
def build_context(request: ContextRequest) -> ContextResponse:
    """Collect and assemble the context for a user's current task."""
    return context_engine.build(request)
