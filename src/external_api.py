import requests
from typing import Dict, Any, Optional
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

CB_RATES_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


def _get_exchange_rates() -> Optional[Dict[str, Decimal]]:
    """
    Получает курсы валют от ЦБ РФ и возвращает словарь:
    {'USD': Decimal('90.5'), 'EUR': Decimal('98.2'), ...}
    Если запрос не удался — возвращает None.
    """
    try:
        resp = requests.get(CB_RATES_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()

    except (requests.RequestException, ValueError, Exception):
        return None

    rates = {}
    valutes = data.get("Valute", {})


    for v in valutes.values():
        char_code = v.get("CharCode")
        if char_code in ("USD", "EUR"):
            try:
                rates[char_code] = Decimal(str(v["Value"]))
            except (TypeError, ValueError, InvalidOperation):
                continue

    return rates


def convert_transaction_to_rubles(transaction: Dict[str, Any]) -> float:
    op_amount = transaction.get("operationAmount")
    if not isinstance(op_amount, dict):
        raise ValueError("В транзакции отсутствует или неверно заполнено поле 'operationAmount'.")

    amount_raw = op_amount.get("amount")
    currency_info = op_amount.get("currency")

    if not isinstance(currency_info, dict):
        raise ValueError("В транзакции неверно заполнено поле 'currency'.")

    currency_code = (currency_info.get("code") or "").strip().upper()

    try:
        amount_decimal = Decimal(str(amount_raw))
    except (TypeError, ValueError, InvalidOperation):
        raise ValueError(f"Поле 'amount' не может быть преобразовано в число: {amount_raw!r}")

    if currency_code == "RUB":
        return float(amount_decimal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

    if currency_code not in ("USD", "EUR"):
        raise ValueError(f"Неподдерживаемая валюта: {currency_code}")

    rates = _get_exchange_rates()
    if rates is None:
        raise RuntimeError("Не удалось получить курсы валют.")

    rate = rates.get(currency_code)
    if rate is None:
        raise RuntimeError(f"Курс для валюты {currency_code} не найден.")

    converted = amount_decimal * rate
    result_decimal = converted.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return float(result_decimal)

