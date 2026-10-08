"""Find memories that share keywords with the user's current task."""

import re

from sqlalchemy.orm import Session

from app.memory.store import list_user_memories


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "for",
    "from",
    "i",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
    "you",
}


def _keywords(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.casefold())

    return {
        word
        for word in words
        if len(word) > 1 and word not in STOP_WORDS
    }


def retrieve_relevant_memories(
    session: Session,
    user_id: str,
    query: str,
    limit: int = 5,
) -> list[str]:
    """Return memories with the most keyword matches."""

    query_words = _keywords(query)
    memories = list_user_memories(session, user_id)

    scored_memories = []

    for memory in memories:
        overlap = len(query_words & _keywords(memory.content))

        if overlap > 0:
            scored_memories.append((overlap, memory))

    scored_memories.sort(
        key=lambda item: (item[0], item[1].id),
        reverse=True,
    )

    return [
        memory.content
        for _, memory in scored_memories[:limit]
    ]