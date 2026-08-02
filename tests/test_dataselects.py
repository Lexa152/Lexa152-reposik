import pytest
import re
from collections import Counter

from src.dataselects import (
    _contains_rub,
    find_RUB_recursive,
    get_descriptions_non_empty,
    get_unique_values,
)


@pytest.fixture
def sample_data_with_descriptions():
    return [
        {"description": "Оплата RUB"},
        {"description": "Покупка продуктов"},
        {"description": "Перевод в рублях"},
        {"amount": 100},  # без description
    ]


@pytest.fixture
def sample_nested_data():
    return [
        {"details": {"currency": "RUB", "note": "test"}},
        {"details": {"currency": "USD", "note": "no rub"}},
        {"items": [{"currency": "rub"}, {"other": "value"}]},
        {"plain": "just text"},
    ]


@pytest.fixture
def sample_states_data():
    return [
        {"state": "EXECUTED"},
        {"state": "PENDING"},
        {"state": "EXECUTED"},
        {"state": None},
        {"state": ""},
        {"no_state_key": "value"},
    ]


@pytest.fixture
def pattern_rub():
    return re.compile("RUB", re.IGNORECASE)


@pytest.mark.parametrize(
    "obj,expected",
    [
        ("Оплата RUB", True),
        ({"currency": "RUB"}, True),
        ({"nested": {"deep": {"value": "rub"}}}, True),
        ([{"c": "USD"}, {"c": "rub"}], True),
        (("no", "rub", "ok"), True),
        ({"a": {"b": {"c": "USD"}}}, False),
        ({"value": 12345, "flag": None}, False),
        (123, False),
    ],
    ids=[
        "str_match",
        "dict_top_level",
        "dict_deep_nested",
        "list_with_match",
        "tuple_with_match",
        "deep_no_match",
        "non_string_no_match",
        "int_no_match",
    ],
)
def test_contains_rub_parametrized(obj, expected, pattern_rub):
    assert _contains_rub(obj, pattern_rub) is expected


@pytest.mark.parametrize(
    "data,search_string,expected_count",
    [
        ([{"description": "RUB OK"}], "RUB", 1),
        ([{"description": "No match"}], "RUB", 0),
        ([], "RUB", 0),
        ([{"details": {"currency": "rub"}}], "rub", 1),
        ([{"items": [{"c": "RUB"}, {"x": "y"}]}, {"items": [{"c": "USD"}]}], "RUB", 1),
    ],
    ids=["simple_match", "simple_no_match", "empty_list", "nested_dict", "nested_list"],
)
def test_find_RUB_recursive_parametrized(data, search_string, expected_count):
    result = find_RUB_recursive(data, search_string=search_string)
    assert len(result) == expected_count


@pytest.mark.parametrize(
    "datalist,descrlist0,expected_counter",
    [
        (
            [
                {"description": "A"},
                {"description": "B"},
                {"description": "A"},
                {"no_desc": "X"},
            ],
            ["A", "B", "C"],
            Counter({"A": 2, "B": 1}),
        ),
        (
            [{"description": "X"}, {"description": "Y"}],
            ["A", "B"],
            Counter(),
        ),
        (
            [{"amount": 10}, {"no_desc": 20}],
            ["any"],
            Counter(),
        ),
    ],
    ids=["basic_filter_and_count", "no_matches", "missing_description"],
)
def test_get_descriptions_non_empty_parametrized(datalist, descrlist0, expected_counter):
    counter = get_descriptions_non_empty(datalist, descrlist0)
    assert isinstance(counter, Counter)
    assert counter == expected_counter


@pytest.mark.parametrize(
    "key,expected_result",
    [
        ("state", ["EXECUTED", "PENDING"]),
        ("missing_key", []),
    ],
    ids=["valid_key", "missing_key"],
)
def test_get_unique_values_parametrized(sample_states_data, key, expected_result):
    result = get_unique_values(sample_states_data, key)
    assert result == expected_result


def test_get_unique_values_order_and_filters(sample_states_data):
    # тест проверки порядка и фильтрации None/пустых
    result = get_unique_values(sample_states_data, "state")
    assert result == ["EXECUTED", "PENDING"]
    assert None not in result
    assert "" not in result


def test_get_unique_values_empty_data():
    assert get_unique_values([], "state") == []
