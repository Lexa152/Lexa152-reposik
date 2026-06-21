from src.masks import get_mask_card_number
from src.masks import get_mask_account

#test_get_mask_card_number on
def test_get_mask_card_number(test_card_numbers):
    card_number_in, card_number_out = test_card_numbers
    assert get_mask_card_number(card_number_in) == card_number_out
#test_get_mask_card_number off


#test_get_mask_account on
def test_get_mask_account(test_mask_account):
    number_in, number_out = test_mask_account
    assert get_mask_account(number_in) == number_out
#test_get_mask_account off

