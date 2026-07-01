from typing import Iterable, Dict, Any

def filter_by_currency(transactions: list[Dict[str, Any]], currency_code: str) -> Iterable[Dict[str, Any]]:
    """
    Возвращает итератор по транзакциям
    """
    for transaction in transactions:
        # Защита от некорректной структуры транзакции
        operation_amount = transaction.get("operationAmount", {})
        currency = operation_amount.get("currency", {})
        code = currency.get("code")

        if code == currency_code:
            yield transaction


def transaction_descriptions(transactions: list[Dict[str, Any]]) -> Iterable[str]:
    """
    Генератор
    """
    for transaction in transactions:
        description = transaction.get("description", "Без описания")
        yield description


def card_number_generator(start: int, end: int) -> Iterable[str]:
    """
    Генератор номеров карт XXXX XXXX XXXX XXXX.
    """
    if start < 1 or end < 1:
        raise ValueError("start и end должны быть >= 1")
    if start > end:
        raise ValueError("start не может быть больше end")
    if end > 9999_9999_9999_9999:
        raise ValueError("end не может превышать 9999999999999999")

    for number in range(start, end + 1):
        # Форматируем число как 16-значную строку с ведущими нулями
        number_str = f"{number:016d}"
        # Разбиваем на группы по 4 символа через пробел
        card_number = f"{number_str[0:4]} {number_str[4:8]} {number_str[8:12]} {number_str[12:16]}"
        yield card_number

