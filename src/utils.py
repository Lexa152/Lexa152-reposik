import json
from typing import Any, Dict, List


# целевая функция
def load_operations(file_path: str) -> List[Dict[str, Any]]:
    """  Загруж транзакции из файла """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as ex:
        # ошибка при загрузке
        return []

    if isinstance(data, list):
        # загруженное - это точно список
        return data
    else:
        # загружанные — это не список
        return []

