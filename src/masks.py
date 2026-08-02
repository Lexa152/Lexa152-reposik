import logging
import os

# файл-менеджмент
current_dir = os.getcwd()  # раб
parent_dir = os.path.dirname(current_dir)  # род

# создание логгирования
logger = logging.getLogger('masks')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(parent_dir + "/logs/masks.log", encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# чистка лога
with open(parent_dir + "/logs/masks.log", 'w'):
    pass


def get_mask_card_number(num_k: str) -> str:
    """Функция для наложения маски на номер банковой карты"""
    if len(num_k) == 16:
        num_km = num_k[0:6] + "******" + num_k[12:16]
        logger.info('Номер карты прикрыт УСПЕШНО!')
        return num_km[0:4] + " " + num_km[4:8] + " " + num_km[8:12] + " " + num_km[12:16]
    else:
        logger.error('Упс! Неверно считан номер карты (кол-во символов не равно 16)')
        return 'номер карты с ошибкой'


def get_mask_account(num_s: str) -> str:
    """Функция для наложения маски на номер счета"""
    if len(num_s) >= 4:
        logger.info('Номер cчёта прикрыт УСПЕШНО!')
        return "**" + num_s[-4:]
    else:
        logger.error('Упс! Неверно считан номер счёта (кол-во символов меньше 4)')
        return 'номер счёта с ошибкой'
