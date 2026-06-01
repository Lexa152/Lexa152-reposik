from masks import *
from datetime import datetime


def mask_account_card(str_in: str) -> str:
    """Функция для наложения маски на номер счета или карты"""
    if len(str_in) > 0:
        if str_in[0:4] != 'Счет': #КАРТА
            return str_in[0:(len(str_in)-17)]+' '+get_mask_card_number(str_in[(len(str_in)-16):])
        if str_in[0:4] == 'Счет': #СЧЁТ
            return 'Счет '+get_mask_account(str_in[5:])
    else:
        return 'нет данных'


def get_date(date_string):
    '''Дата'''
    dt = datetime.fromisoformat(date_string)
    return dt.strftime("%d.%m.%Y")
