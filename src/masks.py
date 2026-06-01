def get_mask_card_number(num_k: str) -> str:
    """Функция для наложения маски на номер банковой карты"""
    if len(num_k) == 16:
        num_km = num_k[0:6] + "******" + num_k[12:16]
        return num_km[0:4] + " " + num_km[4:8] + " " + num_km[8:12] + " " + num_km[12:16]
    else:
        return 'номер с ошибкой'


def get_mask_account(num_s: str) -> str:
    """Функция для наложения маски на номер счета"""
    if len(num_s) >= 4:
        return "**" + num_s[-4:]
    else:
        return 'номер с ошибкой'
