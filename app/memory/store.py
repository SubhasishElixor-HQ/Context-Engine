"""Save and list a user's memories."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import MemoryRecord


def save_memories(
    session: Session,
    user_id: str,
    candidates: list[tuple[str, str]],
) -> list[MemoryRecord]:
    """Save new memories, skipping duplicates for this user."""

    if not candidates:
        return []

    statement = select(MemoryRecord.content).where(
        MemoryRecord.user_id == user_id
    )
    existing_contents = set(session.scalars(statement))
    known_contents = {
        content.casefold()
        for content in existing_contents
    }

    new_records: list[MemoryRecord] = []

    for content, category in candidates:
        normalized = content.casefold()

        if normalized in known_contents:
            continue

        known_contents.add(normalized)

        new_records.append(
            MemoryRecord(
                user_id=user_id,
                content=content,
                category=category,
            )
        )

    if new_records:
        session.add_all(new_records)
        session.commit()

        for record in new_records:
            session.refresh(record)

    return new_records


def list_user_memories(
    session: Session,
    user_id: str,
) -> list[MemoryRecord]:
    """Return this user's memories, newest first."""

    statement = (
        select(MemoryRecord)
        .where(MemoryRecord.user_id == user_id)
        .order_by(
            MemoryRecord.created_at.desc(),
            MemoryRecord.id.desc(),
        )
    )

    return list(session.scalars(statement))