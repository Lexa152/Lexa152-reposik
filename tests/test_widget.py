from src.widget import mask_account_card, get_date


# test_get_mask_account on
def test_mask_account_card(name_number):
    number_in, number_out = name_number
    assert mask_account_card(number_in) == number_out
# test_get_mask_account off


# test_data on
def test_get_date(datetime_new):
    data_in, data_out = datetime_new
    assert get_date(data_in) == data_out
# test_data off

