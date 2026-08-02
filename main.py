from src.utils import load_operations
from src.dataimport import import_data_csv, import_data_xlsx
from src.processing import filter_by_state, sort_by_date
from src.dataselects import find_RUB_recursive, find_description, get_unique_values
from src.widget import get_date, mask_account_card

# вводные данные
data_path1 = r'D:\Python_HomeWork\pythonProject2\data\operations.json'
data_path2 = r'D:\Python_HomeWork\pythonProject2\data\transactions.csv'
data_path3 = r'D:\Python_HomeWork\pythonProject2\data\transactions_excel.xlsx'


def find_by_key_partial(obj, partial_key):
    """
    Возвращает первое значение, чей ключ содержит partial_key. Ищет рекурсивно
    """
    partial_key = partial_key.lower()

    if isinstance(obj, dict):
        for k, v in obj.items():
            if partial_key in k.lower():
                return v
            # Рекурсия вглубь
            result = find_by_key_partial(v, partial_key)
            if result is not None:
                return result

    elif isinstance(obj, (list, tuple)):
        for item in obj:
            result = find_by_key_partial(item, partial_key)
            if result is not None:
                return result

    return None


def get_info_for_print(datalist):
    """
    Фунцкия - основной цикл вывода информации (перебор списка словарей)
    """
    for i in datalist:
        tranz_date = ''
        tranz_amount = ''
        tranz_cur_name = ''
        tranz_from = ''
        tranz_to = ''
        tranz_descript = ''

        if (get_date(find_by_key_partial(i, 'date')) is not None):
            tranz_date = get_date(find_by_key_partial(i, 'date'))
        if (find_by_key_partial(i, 'amount') is not None):
            tranz_amount = find_by_key_partial(i, 'amount')
        if (find_by_key_partial(i, 'code') is not None):
            tranz_cur_name = find_by_key_partial(i, 'name')
            if tranz_cur_name in ['RUB', 'Ruble']:
                tranz_cur_name = 'руб.'
        if (mask_account_card(find_by_key_partial(i, 'from')) is not None):
            tranz_from = mask_account_card(find_by_key_partial(i, 'from'))
        if (mask_account_card(find_by_key_partial(i, 'to')) is not None):
            tranz_to = mask_account_card(find_by_key_partial(i, 'to'))
        if (find_by_key_partial(i, 'description') is not None):
            tranz_descript = find_by_key_partial(i, 'description')

        print(tranz_date + ' ' + tranz_descript)  # строка-1

        if tranz_from not in ['', 'нет данных']:
            print(tranz_from + ' -> ' + tranz_to)  # строка-2
        else:
            print(tranz_to)

        print('Сумма: ' + str(tranz_amount) + ' ' + tranz_cur_name)  # строка-3
        print()  # строка-4


def main():
    """
    Главная функция
    """
    print('Привет! \n'
          'Добро пожаловать в программу работы с банковскими транзакциями. \n'
          'Выберите необходимый пункт меню: \n'
          '1. Получить информацию о транзакциях из JSON-файла; \n'
          '2. Получить информацию о транзакциях из CSV-файла;  \n'
          '3. Получить информацию о транзакциях из XLSX-файла. ')
    datatip = ''
    while datatip not in ['1', '2', '3']:
        datatip = input('Ваш выбор: ')
        if datatip not in ['1', '2', '3']:
            print('Вы должны ввести один из следующих вариантов: ')
            print(['1', '2', '3'])

    # file loud
    if datatip == '1':
        print('Для обработки выбран JSON-файл. ')
        datalist = load_operations(data_path1)
    if datatip == '2':
        print('Для обработки выбран CSV-файл. ')
        datalist = import_data_csv(data_path2)
    if datatip == '3':
        print('Для обработки выбран XLSX-файл. ')
        datalist = import_data_xlsx(data_path3)

    # Filter STATE
    stateforyoulist = get_unique_values(datalist, "state")  # выборка всех статусов
    stateforyou = ''
    stateforyoulist_lower = [i.lower() for i in stateforyoulist]
    while stateforyou.lower() not in stateforyoulist_lower:
        print('Введите статус, по которому необходимо выполнить фильтрацию. \n'
              'Доступные для фильтровки статусы: ')
        print(stateforyoulist)  # вывод всех доступных статусов
        stateforyou = input('Ваш выбор: ')

        if stateforyou.lower() not in stateforyoulist_lower:
            print(f'Статус операции "{stateforyou}" недоступен. ')
        else:
            for i in range(0, len(stateforyoulist)):
                if stateforyou.lower() == stateforyoulist[i].lower():
                    stateforyou = stateforyoulist[i]
                    break

    datalist = filter_by_state(datalist, stateforyou)
    print(f'Операции отфильтрованы по статусу "{stateforyou}". ')

    # Other sorts
    sortdata = ''
    sortgrow = ''
    sortrubl = ''
    sortword = ''
    sortword_text = ''

    while sortdata not in ['да', 'нет']:
        print('Отсортировать операции по дате? Да/Нет ')
        sortdata = input('Ваш выбор: ').lower()
        if sortdata not in ['да', 'нет']:
            print('можно выбирать только из вариантов: "Да" или "Нет" ')

    if sortdata == 'да':
        # сортир по времени и возрастанию / убыванию
        while sortgrow not in ['по возрастанию', 'по убыванию']:
            print('Отсортировать по возрастанию или по убыванию? ')
            sortgrow = input('Ваш выбор: ').lower()
            if sortgrow not in ['по возрастанию', 'по убыванию']:
                print('можно выбирать только из вариантов: "по возрастанию" или "по убыванию" ')
        if sortgrow == 'по возрастанию':
            datalist = sort_by_date(datalist, reverse=False)
        else:
            datalist = sort_by_date(datalist, reverse=True)

    # sort RUB
    while sortrubl not in ['да', 'нет']:
        print('Выводить только рублевые транзакции? Да/Нет ')
        sortrubl = input('Ваш выбор: ').lower()
        if sortrubl not in ['да', 'нет']:
            print('можно выбирать только из вариантов: "Да" или "Нет" ')

    if sortrubl == 'да':
        datalist = find_RUB_recursive(datalist, 'RUB')

    # word
    while sortword not in ['да', 'нет']:
        print('Отфильтровать список транзакций по определенному слову в описании? Да/Нет ')
        sortword = input('Ваш выбор: ').lower()
        if sortword not in ['да', 'нет']:
            print('можно выбирать только из вариантов: "Да" или "Нет" ')

    # word text
    if sortword == 'да':
        print('Введите слово, которое должно присутствовать в описаниях транзакций ')
        sortword_text = input('Ваше слово: ').lower()
        datalist = find_description(datalist, sortword_text)

    # принтинг результатов
    if len(datalist) > 0:
        print('')
        print('Распечатываю итоговый список транзакций... ')
        print('Всего банковских операций в выборке: ' + str(len(datalist)))
        print('')
        get_info_for_print(datalist)
    else:
        print('Не найдено ни одной транзакции, подходящей под ваши условия фильтрации ')


main()
