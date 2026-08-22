import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(data, state="EXECUTED"):
    """
    Фильтр по статусу транзакции без использования .get()
    """
    if not isinstance(data, (list, tuple)):
        return []

    result = []
    for item in data:
        # Пропускаем всё, что не словарь
        if not isinstance(item, dict):
            continue

        # Проверяем наличие ключа и совпадение значения
        if "state" in item and item["state"] == state:
            result.append(item)

    return result


def sort_by_date(data, reverse=False):
    """
    Сортировка данных по дате туда-сюда (без .get())
    """
    def parse_date(item):
        # Сначала убедимся, что это словарь — иначе не сможем безопасно проверять ключи
        if not isinstance(item, dict):
            return datetime.min

        # Проверяем наличие ключа "date"
        if "date" not in item:
            return datetime.min

        raw = item["date"]

        # Дата должна быть строкой
        if not isinstance(raw, str):
            return datetime.min

        try:
            return datetime.fromisoformat(raw)
        except (ValueError, TypeError):
            return datetime.min

    # Защита от передачи не-итерируемого объекта (None, число и т.п.)
    if not isinstance(data, (list, tuple)):
        return []

    return sorted(data, key=parse_date, reverse=reverse)


def filter_by_rub(filetype, datalist):
    """
    Фильтрация данных по рублю с безопасными проверками.
    """
    new_datalist = []

    # Защита от None и не-списков
    if not isinstance(datalist, list):
        return new_datalist

    if filetype == 'JSON':
        for i in datalist:
            # Пропускаем, если элемент не словарь
            if not isinstance(i, dict):
                continue

            # Безопасное получение operationAmount
            op_amount = i.get('operationAmount')
            if not isinstance(op_amount, dict):
                continue

            currency = op_amount.get('currency')
            if not isinstance(currency, dict):
                continue

            code = currency.get('code')
            if code == 'RUB':
                new_datalist.append(i)

    else:
        # «Нормальный» формат
        for i in datalist:
            if not isinstance(i, dict):
                continue

            code = i.get('currency_code', '')
            if code == 'RUB':
                new_datalist.append(i)

    return new_datalist


def find_by_description(datalist: List[Dict[str, Any]], word: str) -> List[Dict[str, Any]]:
    """
    Фильтр-Re по слову в описании
    """
    new_datalist = []

    # список пустой или None
    if not datalist:
        return new_datalist

    # Компилируем с IGNORECASE и экранированием спецсимволов
    pattern = re.compile(re.escape(word), re.IGNORECASE)

    for i in datalist:
        # если элемент не словарь
        if not isinstance(i, dict):
            continue

        txt_descr = i.get('description')

        # Ищу
        if isinstance(txt_descr, str) and pattern.search(txt_descr):
            new_datalist.append(i)

    return new_datalist


def stat_descr(data: list[dict], categories: list) -> dict:
    '''
    подсчёт количества транзакций по каждому description
    '''
    list_operations = []
    for item in data:
        # Пропускаем, если не словарь или нет description
        if not isinstance(item, dict):
            continue
        desc = item.get("description")
        if desc is None:
            continue
        if desc in categories:
            list_operations.append(desc)
    category_count = Counter(list_operations)
    return category_count

