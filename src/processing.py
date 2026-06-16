from typing import List, Dict


def filter_by_state(data: List[Dict[str, any]], state: str = 'EXECUTED') -> List[Dict[str, any]]:
    """ Фильтрует список словарей по значению ключа """
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: List[Dict[str, any]], reverse: bool = True) -> List[Dict[str, any]]:
    """ Сортирует список словарей по значению ключа """
    return sorted(data, key=lambda item: item['date'], reverse=reverse)
