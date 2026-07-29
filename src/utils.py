from typing import List, Dict, Any
import json


def load_operations(file_path: str) -> List[Dict[str, Any]]:
    """  Загруж транзакции из файла """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        # Файл не найден, битый JSON или невалидные данные — возвращаем пустой список
        return []
    # Пров что загружанные — это список
    if isinstance(data, list):
        return data
    else:
        # Если загружанные — это не список
        return []

