from src.widget import get_date, mask_account_card


def test_mask_account_card(name_number):
    number_in, number_out = name_number
    assert mask_account_card(number_in) == number_out


def test_get_date(datetime_new):
    data_in, data_out = datetime_new
    assert get_date(data_in) == data_out
