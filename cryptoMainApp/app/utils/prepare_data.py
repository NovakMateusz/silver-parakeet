from typing import Dict, List

from app.utils.constans import NAME_CODE_MAPPING


def chunks(items: List, n: int):
    for i in range(0, len(items), n):
        yield items[i:i + n]


def prepare_items(split: int = 5) -> List[List[Dict]]:
    items: List[Dict] = [{'name': key, 'state': 0.0, 'filename': f'images/logos/{key.lower()}.svg'} for key
                         in NAME_CODE_MAPPING.keys()]
    result: List[List[Dict]] = []
    for item in chunks(items, split):
        result.append(item)
    return result
