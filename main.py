from src.dataimport import import_data_csv, import_data_xlsx
from src.processing import filter_by_rub, filter_by_state, find_by_description, sort_by_date, stat_descr
from src.utils import load_operations
from src.widget import get_date, mask_account_card

# вводные данные
data_path1 = r'D:\Python_HomeWork\pythonProject2\data\operations.json'
data_path2 = r'D:\Python_HomeWork\pythonProject2\data\transactions.csv'
data_path3 = r'D:\Python_HomeWork\pythonProject2\data\transactions_excel.xlsx'

def datalist_printer(datalist, filetype):
    """
    Фунцкия вывода транзакций на экран
    """
    if (datalist is not None) and (len(datalist)>0):
        if filetype == 'JSON':
            # работа с жизоном
            for i in datalist:
                i_amount = ''
                i_currency = ''
                i_date = get_date(i.get('date', ''))
                i_from = mask_account_card(i.get('from', ''))
                i_to = mask_account_card(i.get('to', ''))
                i_desc = i.get('description', '')

                if i['operationAmount'] is not None:
                    ii = i['operationAmount']
                    if ii is not None:
                        i_amount = ii.get('amount', '')
                        iii = ii['currency']
                        if iii is not None:
                            i_currency = iii.get('code', '')
                if i_currency == 'RUB':
                    i_currency = 'руб.'
                # печать данных
                print()
                print(f'{i_date} {i_desc} ')
                if (i_from is None) or (i_from == ''):
                    print(f'{i_to} ')
                else:
                    print(f'{i_from} -> {i_to} ')
                print(f'Сумма: {i_amount} {i_currency} ')

        else:
            # работа с нормальными
            for i in datalist:
                i_date = get_date(i.get('date', ''))
                i_amount = i.get('amount', '')
                i_currency = i.get('currency_code', '')
                i_from = mask_account_card(i.get('from', ''))
                i_to = mask_account_card(i.get('to', ''))
                i_desc = i.get('description', '')
                if i_currency == 'RUB':
                    i_currency = 'руб.'
                # печать данных
                print()
                print(f'{i_date} {i_desc} ')
                if (i_from is None) or (i_from == ''):
                    print(f'{i_to} ')
                else:
                    print(f'{i_from} -> {i_to} ')
                print(f'Сумма: {i_amount} {i_currency} ')


def main():
    """
    Главная функция
    """
    filetype = ''
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
        filetype = 'JSON'
        print('Для обработки выбран JSON-файл. ')
        datalist = load_operations(data_path1)
    if datatip == '2':
        filetype = 'CSV'
        print('Для обработки выбран CSV-файл. ')
        datalist = import_data_csv(data_path2)
    if datatip == '3':
        filetype = 'XLSX'
        print('Для обработки выбран XLSX-файл. ')
        datalist = import_data_xlsx(data_path3)

    # Filter STATE
    stateforyoulist = ['EXECUTED', 'CANCELED', 'PENDING']  # выборка всех статусов
    stateforyoulist_lower = ['executed', 'canceled', 'pending']
    stateforyou = ''
    while stateforyou.lower() not in stateforyoulist_lower:
        print('Введите статус, по которому необходимо выполнить фильтрацию. \n'
              'Доступные для фильтровки статусы: ')
        print(stateforyoulist)  # вывод всех доступных статусов
        stateforyou = input('Ваш выбор: ')

        if stateforyou.lower() not in stateforyoulist_lower:
            print(f'Статус операции "{stateforyou}" недоступен. ')
        else:
            for i in range(0, len(stateforyoulist_lower)):
                if stateforyou.lower() == stateforyoulist[i].lower():
                    stateforyou = stateforyoulist[i]
                    break

    datalist = filter_by_state(datalist, stateforyou)   # filter_by_state
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
            print('Можно выбирать только из вариантов: "Да" или "Нет" ')

    if sortdata == 'да':

        # сорт по времени по возрастанию / убыванию
        while sortgrow not in ['по возрастанию', 'по убыванию']:
            print('Отсортировать по возрастанию или по убыванию? ')
            sortgrow = input('Ваш выбор: ').lower()
            if sortgrow not in ['по возрастанию', 'по убыванию']:
                print('Можно выбирать только из вариантов: "по возрастанию" или "по убыванию" ')

        if sortgrow == 'по возрастанию':
            datalist = sort_by_date(datalist, reverse=False)
        else:
            datalist = sort_by_date(datalist, reverse=True)

    # sort RUB
    while sortrubl not in ['да', 'нет']:
        print('Выводить только рублевые транзакции? Да/Нет ')
        sortrubl = input('Ваш выбор: ').lower()
        if sortrubl not in ['да', 'нет']:
            print('Можно выбирать только из вариантов: "Да" или "Нет" ')

    if sortrubl == 'да':
        datalist = filter_by_rub(filetype, datalist)


    while sortword not in ['да', 'нет']:
        print('Отфильтровать список транзакций по определенному слову в описании? Да/Нет ')
        sortword = input('Ваш выбор: ').lower()
        if sortword not in ['да', 'нет']:
            print('Можно выбирать только из вариантов: "Да" или "Нет" ')

    # ввод слова для фильтрации sortword_text
    if sortword == 'да':
        print('Укажите слово, по которому будет произведена фильтрация ')
        sortword_text = input('Ваш выбор: ').lower()
        # фильтрация по слову в описании
        datalist = find_by_description(datalist, sortword_text)

    # принтинг результатов   find_by_description
    if len(datalist) > 0:
        print('')
        print('Распечатываю итоговый список транзакций... ')
        print('Всего банковских операций в выборке: ' + str(len(datalist)))
        print('')
        datalist_printer(datalist, filetype)
    else:
        print('Не найдено ни одной транзакции, подходящей под ваши условия фильтрации ')


main()
