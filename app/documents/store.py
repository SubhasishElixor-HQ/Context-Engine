"""Save documents and their chunks, and list a user's documents."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import DocumentChunkRecord, DocumentRecord
from app.documents.chunker import chunk_text


def create_document(
    session: Session,
    user_id: str,
    title: str,
    content: str,
) -> DocumentRecord:
    document = DocumentRecord(
        user_id=user_id,
        title=title,
        content=content,
    )
    document.chunks = [
        DocumentChunkRecord(chunk_index=index, content=chunk)
        for index, chunk in enumerate(chunk_text(content))
    ]

    session.add(document)
    session.commit()
    session.refresh(document)
    return document


def list_user_documents(
    session: Session,
    user_id: str,
) -> list[DocumentRecord]:
    statement = (
        select(DocumentRecord)
        .where(DocumentRecord.user_id == user_id)
        .order_by(DocumentRecord.created_at.desc(), DocumentRecord.id.desc())
    )
    return list(session.scalars(statement))
