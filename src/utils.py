"""Utility functions for playlist shuffler."""
import random
from typing import Iterator

def extract_playlist_id(url_or_id: str) -> str:
    """Extract playlist ID from URL or raw ID."""
    s = url_or_id.strip()
    if "playlist/" in s:
        s = s.split("playlist/")[1].split("?")[0].strip("/")
    return s

def chunked(iterable, size: int) -> Iterator[list]:
    """Yield chunks of iterable in given size."""
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

def set_random_seed(seed_input: str | None) -> None:
    """Set random seed from input or use random."""
    if not seed_input:
        return
    try:
        random.seed(int(seed_input))
    except ValueError:
        random.seed(seed_input)
