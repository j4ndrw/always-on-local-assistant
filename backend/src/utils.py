from difflib import SequenceMatcher
from typing import Callable, Iterable


def levenshtein_distance(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def find_similar(xs: Iterable[str], key: str, mapper: Callable[[str], str] = lambda x: x) -> tuple[str | None, float | None]:
    if len([*xs]) == 0:
        return None, None

    similarities: list[tuple[str, float]] = []
    for app in xs:
        similarities.append((app, levenshtein_distance(key, mapper(app))))

    return sorted(similarities, key=lambda x: x[1])[-1]
