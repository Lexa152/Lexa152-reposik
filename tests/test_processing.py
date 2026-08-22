from collections import Counter
from datetime import datetime

import pytest

from src.processing import filter_by_rub, filter_by_state, find_by_description, sort_by_date, stat_descr


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-05-10T12:00:00",
            "description": "Оплата интернета",
            "operationAmount": {"currency": {"code": "RUB"}},
            "currency_code": "RUB",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2024-06-01T09:30:00",
            "description": "Перевод другу",
            "operationAmount": {"currency": {"code": "USD"}},
            "currency_code": "USD",
        },
        {
            "id": 3,
            "state": "CANCELED",
            "date": "2024-04-20T15:20:00",
            "description": "Покупка продуктов",
            "operationAmount": {"currency": {"code": "RUB"}},
            "currency_code": "RUB",
        },
        {
            "id": 4,
            "state": "EXECUTED",
            "date": "invalid-date",
            "description": "Оплата ЖКХ",
            "operationAmount": {"currency": {"code": "RUB"}},
            "currency_code": "RUB",
        },
        "not-a-dict",  # мусор для проверки устойчивости
    ]


@pytest.fixture
def rub_json_data():
    """Данные в формате JSON (вложенная структура)"""
    return [
        {"id": 10, "operationAmount": {"currency": {"code": "RUB"}}},
        {"id": 11, "operationAmount": {"currency": {"code": "EUR"}}},
        {"id": 12, "operationAmount": None},
        {"id": 13, "operationAmount": {}},
        {"id": 14, "operationAmount": {"currency": {}}},
    ]


@pytest.fixture
def rub_normal_data():
    """Данные в «нормальном» формате (прямой currency_code)"""
    return [
        {"id": 20, "currency_code": "RUB"},
        {"id": 21, "currency_code": "USD"},
        {"id": 22},  # нет currency_code
    ]


@pytest.fixture
def stat_data():
    return [
        {"description": "Оплата интернета"},
        {"description": "Перевод другу"},
        {"description": "Оплата интернета"},
        {"description": "Покупка продуктов"},
        {"description": "Перевод другу"},
        {"description": "Перевод другу"},
    ]


# --- Тесты filter_by_state ---

def test_filter_by_state_executed(sample_transactions):
    result = filter_by_state(sample_transactions, "EXECUTED")
    assert len(result) == 3
    assert all(t["state"] == "EXECUTED" for t in result)
    ids = {t["id"] for t in result}
    assert ids == {1, 2, 4}


def test_filter_by_state_canceled(sample_transactions):
    result = filter_by_state(sample_transactions, "CANCELED")
    assert len(result) == 1
    assert result[0]["id"] == 3


def test_filter_by_state_empty_list():
    assert filter_by_state([], "EXECUTED") == []
    assert filter_by_state(None, "EXECUTED") == []  # функция корректно обработает None


# --- Тесты sort_by_date ---

def test_sort_by_date_ascending(sample_transactions):
    result = sort_by_date(sample_transactions, reverse=False)
    # Извлекаем даты только из словарей, мусор оставляем как есть
    dates = []
    for t in result:
        if isinstance(t, dict) and "date" in t:
            raw = t["date"]
            if isinstance(raw, str):
                try:
                    dates.append(datetime.fromisoformat(raw))
                except ValueError:
                    dates.append(datetime.min)
            else:
                dates.append(datetime.min)
    assert dates == sorted(dates)


def test_sort_by_date_descending(sample_transactions):
    result = sort_by_date(sample_transactions, reverse=True)
    dates = []
    for t in result:
        if isinstance(t, dict) and "date" in t:
            raw = t["date"]
            if isinstance(raw, str):
                try:
                    dates.append(datetime.fromisoformat(raw))
                except ValueError:
                    dates.append(datetime.min)
            else:
                dates.append(datetime.min)
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_invalid_and_non_dict(sample_transactions):
    # Функция не должна падать на невалидных датах и не-словарях
    result = sort_by_date(sample_transactions)
    assert len(result) == len(sample_transactions)


# --- Тесты filter_by_rub ---

def test_filter_by_rub_json_rub_only(rub_json_data):
    result = filter_by_rub("JSON", rub_json_data)
    assert len(result) == 1
    assert result[0]["id"] == 10


def test_filter_by_rub_normal_rub_only(rub_normal_data):
    result = filter_by_rub("OTHER", rub_normal_data)  # ветка else
    assert len(result) == 1
    assert result[0]["id"] == 20


def test_filter_by_rub_none_or_empty():
    assert filter_by_rub("JSON", None) == []
    assert filter_by_rub("JSON", []) == []


def test_filter_by_rub_robust_against_broken_structure(rub_json_data):
    data = rub_json_data + [
        {"id": 99, "operationAmount": {}},
        {"id": 100, "operationAmount": {"currency": {}}},
        {"id": 101, "operationAmount": "not-a-dict"},
        {"id": 102},  # вообще нет operationAmount
    ]
    result = filter_by_rub("JSON", data)
    assert len(result) == 1  # только один валидный RUB
    assert result[0]["id"] == 10


# --- Тесты find_by_description ---

def test_find_by_description_case_insensitive(sample_transactions):
    result = find_by_description(sample_transactions, "оплата")
    assert len(result) == 2
    ids = {t["id"] for t in result}
    assert ids == {1, 4}


def test_find_by_description_no_match(sample_transactions):
    result = find_by_description(sample_transactions, "не_существует")
    assert result == []


def test_find_by_description_special_chars(sample_transactions):
    data = sample_transactions + [
        {
            "id": 5,
            "state": "EXECUTED",
            "date": "2024-07-01T10:00:00",
            "description": "Оплата счета 100.00 руб.",
            "operationAmount": {"currency": {"code": "RUB"}},
            "currency_code": "RUB",
        }
    ]
    result = find_by_description(data, "100.00")
    assert len(result) == 1
    assert result[0]["id"] == 5


def test_find_by_description_skips_non_dict_and_bad_types(sample_transactions):
    data = sample_transactions + [
        {"id": 6, "state": "EXECUTED", "description": None, "operationAmount": {"currency": {"code": "RUB"}}},
        {"id": 7, "state": "EXECUTED", "description": 12345, "operationAmount": {"currency": {"code": "RUB"}}},
    ]
    result = find_by_description(data, "оплата")
    # Не-dict и не-строковые описания не должны ломать функцию и не должны попадать в результат
    assert len(result) == 2


# --- Тесты stat_descr ---

def test_stat_descr_count_categories(stat_data):
    categories = ["Оплата интернета", "Перевод другу"]
    result = stat_descr(stat_data, categories)
    assert isinstance(result, Counter)
    assert dict(result) == {"Оплата интернета": 2, "Перевод другу": 3}


def test_stat_descr_no_matches(stat_data):
    categories = ["Не существующая категория"]
    result = stat_descr(stat_data, categories)
    assert dict(result) == {}


def test_stat_descr_partial_match(stat_data):
    categories = ["Оплата интернета", "Не существующая"]
    result = stat_descr(stat_data, categories)
    assert dict(result) == {"Оплата интернета": 2}
