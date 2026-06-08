def get_mask_card_number(num_k):
    '''Функция для наложения маски на номер банковой карты 7000 7922 8960 6361 '''
    if len(num_k) > 5:
        num_km = num_k[1:5],'****',num_k[11:15]
    return num_km
# АБВГ ДЕЁЖ ЗИЙК ЛМНО
my_karta = 'АБВГДЕЁЖЗИЙКЛМНО'
print(get_mask_card_number(my_karta))