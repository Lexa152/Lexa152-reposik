from datetime import datetime


# фильтр по state:
def filter_by_state(data_list, state='EXECUTED'):
    """Фильтр списка словарей по state"""
    if data_list != []:
        return [item for item in data_list if (item.get('state') == state)]
    else:
        return 'нет данных'


# сортировка по датевремени:
def sort_by_date(data, reverse=True):
    """ Сортирует список словарей по дате """
    valid_items = []
    invalid_items = []

    for item in data:
        date_str = item.get("date")
        if date_str is None:
            invalid_items.append(item)
            continue

        try:
            # Парсим дату в формате ISO (например, '2019-07-03T18:35:29.512364')
            date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            valid_items.append((date_obj, item))
        except (ValueError, TypeError):
            invalid_items.append(item)

    # Сортируем корректные элементы по дате
    sorted_valid = [item for _, item in sorted(valid_items, key=lambda x: x[0], reverse=reverse)]

    # Возвращаем отсортированные корректные элементы, затем некорректные
    return sorted_valid + invalid_items


from typing import List, Dict


def filter_by_state(data: List[Dict[str, any]], state: str = 'EXECUTED') -> List[Dict[str, any]]:
    """ Фильтрует список словарей по значению ключа """
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: List[Dict[str, any]], reverse: bool = True) -> List[Dict[str, any]]:
    """ Сортирует список словарей по значению ключа """
    return sorted(data, key=lambda item: item['date'], reverse=reverse)
