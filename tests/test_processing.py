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
    data_in, data_out = data_filter_null
    assert filter_by_state(data_in) == data_out


# test-sorted-1
def test_data_sorted1(data_sorted1):
    data_in, data_out = data_sorted1
    assert sort_by_date(data_in) == data_out


# test-sorted-2
def test_data_sorted2(data_sorted2):
    data_in, data_out = data_sorted2
    assert sort_by_date(data_in, False) == data_out

