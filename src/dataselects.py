import re
from collections import Counter


def find_description(data, search_string):
    """ Функция для поиска строки в описании """
    pattern = re.compile(search_string, re.IGNORECASE)
    return [item for item in data if pattern.search(item.get('description', ''))]


def _contains_rub(obj, pattern):
    """ Рекурсивно проверяет, есть ли подстрока RUB в объекте -1/2 """
    if isinstance(obj, str):
        return bool(pattern.search(obj))
    elif isinstance(obj, dict):
        return any(_contains_rub(v, pattern) for v in obj.values())
    elif isinstance(obj, list | tuple):
        return any(_contains_rub(item, pattern) for item in obj)
    else:
        return False


def find_RUB_recursive(data, search_string='RUB'):
    """ Возвращает список словарей, в которых встречается RUB (в любом вложенном поле) -2/2 """
    pattern = re.compile(search_string, re.IGNORECASE)
    return [item for item in data if _contains_rub(item, pattern)]


def get_descriptions_non_empty(datalist, descrlist0):
    """ Функция для вывода списка дескрипшинов с подсчётом """
    descrlist1 = [t['description'] for t in datalist if 'description' in t]
    descrlist2 = [x for x in descrlist1 if x in descrlist0]
    return Counter(descrlist2)


def get_unique_values(data, key):
    """
    Возвращает список неповторяющихся значений указанного ключа из списка
    список, имя ключа на выходе list — список уникальных значений
    """
    seen = set()
    result = []

    for item in data:
        value = item.get(key)
        if (value is not None) and (value != '') and (value not in seen):
            seen.add(value)
            result.append(value)

    return result
