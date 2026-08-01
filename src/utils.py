from typing import List, Dict, Any
import json
import logging
import os

# файл-менеджмент
current_dir = os.getcwd() # раб
parent_dir = os.path.dirname(current_dir) # род

# создание логгирования
logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(parent_dir + "/logs/utils.log", encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# чистка лога
with open(parent_dir + "/logs/utils.log", 'w'):
    pass

# целевая функция
def load_operations(file_path: str) -> List[Dict[str, Any]]:
    """  Загруж транзакции из файла """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as ex:
        # ошибка при загрузке
        logger.error(f'Упс! Ошибка при загрузке файла: {ex}')
        return []

    if isinstance(data, list):
        # загруженное - это точно список
        logger.info(f'Загрузка данных прошла успешно! Файл: {file_path}')
        return data
    else:
        # загружанные — это не список
        logger.warning(f'Упс! Содержимое файла не является списком. Вывожу пустой список. Файл: {file_path}')
        return []

