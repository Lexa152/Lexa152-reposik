from typing import List, Dict


def filter_by_state(data: List[Dict[str, any]], state: str = 'EXECUTED') -> List[Dict[str, any]]:
    """ Фильтрует список словарей по значению ключа """
    return [item for item in data if item.get("state") == state]




