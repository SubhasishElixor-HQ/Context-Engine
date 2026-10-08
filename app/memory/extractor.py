"""Extract simple, explicit memories from conversation text without an LLM."""

import re


MEMORY_CUES = re.compile(
    r"\b(i want|i hope|my goal is|i plan to|i prefer|i like|i love|i avoid|"
    r"i am|i'm|i have|i know|i study|i work|my name is|remember that)\b",
    re.IGNORECASE,
)


def extract_memory_candidates(conversation_text: str) -> list[tuple[str, str]]:
    """Return (content, category) pairs for statements with known memory cues."""
    sentences = re.split(r"(?<=[.!?])\s+|\r?\n+", conversation_text.strip())
    candidates: list[tuple[str, str]] = []
    seen: set[str] = set()

    for sentence in sentences:
        content = sentence.strip(" \t\r\n\"'")
        if not content or not MEMORY_CUES.search(content):
            continue

        normalized = content.casefold()
        if normalized in seen:
            continue
        seen.add(normalized)

        lowered = content.casefold()
        if any(cue in lowered for cue in ("want", "hope", "goal", "plan")):
            category = "goal"
        elif any(cue in lowered for cue in ("prefer", "like", "love", "avoid")):
            category = "preference"
        else:
            category = "fact"

        candidates.append((content[:2000], category))

    return candidates
