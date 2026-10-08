"""Save documents and their chunks, and list a user's documents."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import (
    DocumentChunkRecord,
    DocumentEmbeddingRecord,
    DocumentRecord,
)
from app.documents.chunker import chunk_text
from app.documents.embeddings import embed_texts


def create_document(
    session: Session,
    user_id: str,
    title: str,
    content: str,
) -> DocumentRecord:
    chunks = chunk_text(content)
    vectors = embed_texts([f"{title}\n{chunk}" for chunk in chunks])

    document = DocumentRecord(
        user_id=user_id,
        title=title,
        content=content,
    )
    document.chunks = []
    for index, (chunk, vector) in enumerate(zip(chunks, vectors)):
        document.chunks.append(
            DocumentChunkRecord(
                chunk_index=index,
                content=chunk,
                embedding=DocumentEmbeddingRecord(vector=vector),
            )
        )

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
