"""Retrieve document chunks using basic keyword overlap."""

import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import DocumentChunkRecord, DocumentRecord


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "for", "from", "i",
    "in", "is", "it", "me", "my", "of", "on", "or", "the", "to", "with",
    "you",
}


def _keywords(text: str) -> set[str]:
    return {
        word
        for word in re.findall(r"[a-z0-9]+", text.casefold())
        if len(word) > 1 and word not in STOP_WORDS
    }


def retrieve_document_chunks(
    session: Session,
    user_id: str,
    query: str,
    limit: int = 5,
) -> list[str]:
    """Return the user's most relevant chunks with their document titles."""
    query_words = _keywords(query)
    statement = (
        select(DocumentChunkRecord, DocumentRecord)
        .join(DocumentRecord, DocumentChunkRecord.document_id == DocumentRecord.id)
        .where(DocumentRecord.user_id == user_id)
    )

    scored_chunks = []
    for chunk, document in session.execute(statement):
        overlap = len(query_words & _keywords(chunk.content))
        if overlap:
            scored_chunks.append((overlap, chunk, document))

    scored_chunks.sort(
        key=lambda item: (item[0], item[2].id, item[1].chunk_index),
        reverse=True,
    )

    return [
        f"Source: {document.title} (chunk {chunk.chunk_index + 1})\n{chunk.content}"
        for _, chunk, document in scored_chunks[:limit]
    ]
