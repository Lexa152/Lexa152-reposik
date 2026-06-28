from src.processing import filter_by_state, sort_by_date


# test-filter-1
def test_data_filter1(data_filter_normal):
    data_in, data_out = data_filter_normal
    assert filter_by_state(data_in) == data_out


# test-filter-2
def test_data_filter2(data_filter_pending):
    data_in, data_out = data_filter_pending
    assert filter_by_state(data_in, 'PENDING') == data_out


# test-filter-3
def test_data_filter3(data_filter_null):
    data_in, expected = data_filter_null
    assert filter_by_state(data_in) == expected


# test-sorted
def test_sort_by_date_ascending(sample_data):
    result = sort_by_date(sample_data, reverse=False)
    # Ожидаем порядок по возрастанию: 2018 -> 2019 -> 2020
    assert [item["id"] for item in result] == [3, 1, 2]


def test_sort_by_date_descending(sample_data):
    result = sort_by_date(sample_data, reverse=True)
    # По убыванию: 2020 -> 2019 -> 2018
    assert [item["id"] for item in result] == [2, 1, 3]


def test_sort_with_invalid_dates():
    data = [
        {"id": 1, "date": "2019-07-03T18:35:29"},
        {"id": 2},                         # нет date
        {"id": 3, "date": "not-a-date"},   # невалидная дата
        {"id": 4, "date": "2020-01-01T00:00:00"},
    ]
    result = sort_by_date(data, reverse=True)

    # Валидные (1 и 4) должны быть отсортированы по дате (по убыванию)
    valid_ids = [item["id"] for item in result if "date" in item and item["date"] != "not-a-date"]
    assert valid_ids == [4, 1]

    # Невалидные (2 и 3) должны идти после валидных, в исходном порядке
    invalid_ids = [item["id"] for item in result if item["id"] not in valid_ids]
    assert invalid_ids == [2, 3]


def test_sort_empty_list():
    assert sort_by_date([]) == []


def test_sort_all_invalid():
    data = [
        {"id": 1},
        {"id": 2, "date": "bad"},
        {"id": 3},
    ]
    result = sort_by_date(data)
    # Все элементы невалидны, порядок должен сохраниться
    assert [item["id"] for item in result] == [1, 2, 3]


def test_sort_iso_with_z_suffix():
    data = [
        {"id": 1, "date": "2020-01-01T10:00:00Z"},
        {"id": 2, "date": "2019-12-31T23:00:00Z"},
    ]
    result = sort_by_date(data, reverse=True)
    assert [item["id"] for item in result] == [1, 2]

