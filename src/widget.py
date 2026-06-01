from masks import *

def mask_account_card(str_in: str) -> str:
    """Функция для наложения маски на номер счета или карты"""
    if len(str_in) > 0:
        if str_in[0:4] != 'Счет': #КАРТА
            return str_in[0:(len(str_in)-17)]+' '+get_mask_card_number(str_in[(len(str_in)-16):])
        if str_in[0:4] == 'Счет': #СЧЁТ
            return 'Счет '+get_mask_account(str_in[5:])


#str0 = ''
#str0 = 'Maestro 1596837868705199'
#str0 = 'Счет 64686473678894779589'
str0 = 'MasterCard 7158300734726758'
#str0 = 'Счет 35383033474447895560'
#str0 = 'Visa Classic 6831982476737658'
#str0 = 'Visa Platinum 8990922113665229'
#str0 = 'Visa Gold 5999414228426353'
#str0 = 'Счет 73654108430135874305'

print(mask_account_card(str0))
#num_sm = "**" + num_s[-4:]