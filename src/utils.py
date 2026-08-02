import json
import os
from typing import Any, Dict, List

current_dir = os.getcwd()  # раб
parent_dir = os.path.dirname(current_dir)  # род


def load_operations(file_path: str) -> List[Dict[str, Any]]:
    """  Загруж транзакции из файла """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as ex:
        return []

    if isinstance(data, list):
        return data
    else:
        return []
