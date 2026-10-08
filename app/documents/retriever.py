"""Retrieve document chunks with keyword and embedding similarity."""

import re

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database.models import DocumentChunkRecord, DocumentRecord
from app.documents.embeddings import embed_texts


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


def _cosine_similarity(first: list[float], second: list[float]) -> float:
    if not first or len(first) != len(second):
        return 0.0

    dot_product = sum(left * right for left, right in zip(first, second))
    first_length = sum(value * value for value in first) ** 0.5
    second_length = sum(value * value for value in second) ** 0.5

    if first_length == 0 or second_length == 0:
        return 0.0

    return dot_product / (first_length * second_length)


def retrieve_document_chunks(
    session: Session,
    user_id: str,
    query: str,
    limit: int = 5,
) -> list[str]:
    """Return chunks ranked by a weighted keyword and semantic score."""
    statement = (
        select(DocumentChunkRecord, DocumentRecord)
        .options(joinedload(DocumentChunkRecord.embedding))
        .join(DocumentRecord, DocumentChunkRecord.document_id == DocumentRecord.id)
        .where(DocumentRecord.user_id == user_id)
    )
    rows = list(session.execute(statement))
    if not rows:
        return []

    has_embeddings = any(chunk.embedding is not None for chunk, _ in rows)
    query_vector = embed_texts([query])[0] if has_embeddings else None
    query_words = _keywords(query)
    scored_chunks = []

    for chunk, document in rows:
        chunk_words = _keywords(chunk.content)
        keyword_score = len(query_words & chunk_words) / max(len(query_words), 1)

        if query_vector is not None and chunk.embedding is not None:
            semantic_score = max(
                0.0,
                _cosine_similarity(query_vector, chunk.embedding.vector),
            )
            score = 0.4 * keyword_score + 0.6 * semantic_score
        else:
            # V4 documents without saved vectors continue to use keyword search.
            score = keyword_score

        if score > 0:
            scored_chunks.append((score, chunk, document))

    scored_chunks.sort(
        key=lambda item: (item[0], item[2].id, item[1].chunk_index),
        reverse=True,
    )

    return [
        f"Source: {document.title} (chunk {chunk.chunk_index + 1})\n{chunk.content}"
        for _, chunk, document in scored_chunks[:limit]
    ]
