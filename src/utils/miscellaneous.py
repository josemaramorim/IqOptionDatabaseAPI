from typing import List


def normalize_pairs(pairs: List[str], otc: bool) -> List[str]:
    def normalize(pair: str) -> str:
        return f"{pair}-OTC" if otc and "-OTC" not in pair.upper() else pair.upper()

    return [normalize(pair) for pair in pairs]
