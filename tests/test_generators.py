import pytest
from src.generators import filter_by_currency
from src.generators import transaction_descriptions
from src.generators import card_number_generator

@pytest.mark.parametrize(
    "currency_code,expected_count",
    [
        ("USD", 3),
        ("RUB", 2),
        ("EUR", 0),
    ],
)
def test_filter_by_currency_counts(transactions, currency_code, expected_count):
    result = list(filter_by_currency(transactions, currency_code))
    assert len(result) == expected_count


def test_filter_by_currency_returns_iterator(transactions):
    usd_transactions = filter_by_currency(transactions, "USD")
    # Проверяем, что это итератор (не список сразу)
    assert hasattr(usd_transactions, "__next__")
    first = next(usd_transactions)
    assert first["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_empty_list(transactions):
    empty_transactions = []
    result = list(filter_by_currency(empty_transactions, "USD"))
    assert result == []


def test_filter_by_currency_malformed_transaction():
    malformed_transactions = [
        {"id": 1, "operationAmount": {}},  # нет currency
        {"id": 2},  # вообще нет operationAmount
        {
            "id": 3,
            "operationAmount": {"currency": {"code": "USD"}}
        },
    ]
    result = list(filter_by_currency(malformed_transactions, "USD"))
    # Должна вернуться только третья транзакция
    assert len(result) == 1
    assert result[0]["id"] == 3

# генераторы

def test_transaction_descriptions_yields_correct_values(transactions):
    descriptions = transaction_descriptions(transactions)
    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации"
    ]
    result = list(descriptions)
    assert result == expected


def test_transaction_descriptions_returns_iterator(transactions):
    descriptions = transaction_descriptions(transactions)
    # Проверяем, что это итератор (есть __next__)
    assert hasattr(descriptions, "__next__")
    first = next(descriptions)
    assert first == "Перевод организации"


def test_transaction_descriptions_empty_list():
    empty_transactions = []
    descriptions = transaction_descriptions(empty_transactions)
    result = list(descriptions)
    assert result == []


def test_transaction_descriptions_missing_description():
    transactions_with_missing = [
        {"id": 1},  # нет поля description
        {"id": 2, "description": "Есть описание"},
        {"description": None},  # description явно None
    ]
    descriptions = transaction_descriptions(transactions_with_missing)
    result = list(descriptions)
    # По нашей реализации будет "Без описания" для отсутствующих/None
    assert result == ["Без описания", "Есть описание", None]


def test_card_number_generator_basic():
    result = list(card_number_generator(1, 5))
    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]
    assert result == expected


def test_card_number_generator_single_value():
    result = list(card_number_generator(123, 123))
    assert result == ["0000 0000 0000 0123"]


def test_card_number_generator_boundary_values():
    # Проверка граничных значений (начало и конец допустимого диапазона)
    result_start = list(card_number_generator(1, 1))
    result_end = list(card_number_generator(9999_9999_9999_9999, 9999_9999_9999_9999))

    assert result_start == ["0000 0000 0000 0001"]
    assert result_end == ["9999 9999 9999 9999"]


def test_card_number_generator_returns_iterator():
    gen = card_number_generator(1, 3)
    # Проверяем, что это итератор
    assert hasattr(gen, "__next__")
    first = next(gen)
    assert first == "0000 0000 0000 0001"


def test_card_number_generator_invalid_start_less_than_one():
    with pytest.raises(ValueError):
        list(card_number_generator(0, 5))


def test_card_number_generator_invalid_start_negative():
    with pytest.raises(ValueError):
        list(card_number_generator(-10, 5))


def test_card_number_generator_start_greater_than_end():
    with pytest.raises(ValueError):
        list(card_number_generator(10, 5))


def test_card_number_generator_exceeds_max_value():
    with pytest.raises(ValueError):
        list(card_number_generator(1, 10_000_0000_0000_0000))


