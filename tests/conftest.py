import pytest


# test_card_number
@pytest.fixture(params=[
    ('7000792289606361', '7000 79** **** 6361'),
    ('70007922896063672', 'номер с ошибкой'),
    ('700079228960633', 'номер с ошибкой'),
    ('404', 'номер с ошибкой'),
    ('', 'номер с ошибкой'),
])
def test_card_numbers(request):
    return request.param


# test_get_mask_account
@pytest.fixture(params=[
    ('73654108430135874305', '**4305'),
    ('736541084301358743056', '**3056'),
    ('7365410843013587437', '**7437'),
    ('73678', '**3678'),
    ('679', 'номер с ошибкой'),
    ('', 'номер с ошибкой')
])
def test_mask_account(request):
    return request.param


# test_card_name_number
@pytest.fixture(params=[
    ('Maestro 1596837868705199', 'Maestro 1596 83** **** 5199'),
    ('Счет 64686473678894779589', 'Счет **9589'),
    ('MasterCard 7158300734726758', 'MasterCard 7158 30** **** 6758'),
    ('Счет 35383033474447895560', 'Счет **5560'),
    ('Visa Classic 6831982476737658', 'Visa Classic 6831 98** **** 7658'),
    ('Visa Platinum 8990922113665229', 'Visa Platinum 8990 92** **** 5229'),
    ('Visa Gold 5999414228426353', 'Visa Gold 5999 41** **** 6353'),
    ('Счет 73654108430135874305', 'Счет **4305')
])
def name_number(request):
    return request.param


# test_data
@pytest.fixture(params=[
    ('2021-01-01T02:26:18.671407', '01.01.2021'),
    ('2022-10-10T02:26:18.671407', '10.10.2022'),
    ('2023-11-11T02:26:18.671407', '11.11.2023'),
    ('', 'нет данных')
])
def datetime_new(request):
    return request.param


# test filter by state-1
@pytest.fixture(params=[
    ([
         {'id': 123455001, 'state': 'EXECUTED', 'date': '2026-01-03T18:35:29.512364'},
         {'id': 123455002, 'state': 'EXECUTED', 'date': '03-02-2026-03T18:35:29.512364'},
         {'id': 123455003, 'state': 'CANCELED', 'date': '2026-03-03T18:35:29.512364'},
         {'id': 123455004, 'state': 'CANCELED', 'date': '2026-05-03T18:35:29.512364'},
         {'id': 123455005, 'state': 'PENDING', 'date': '2026-05-03T18:35:29.512364'},
         {'id': 123455006, 'state': 'PENDING', 'date': '2026-06-03T18:35:29.512364'},
         {'id': 123455006},
         {}
     ],
     [
         {'id': 123455001, 'state': 'EXECUTED', 'date': '2026-01-03T18:35:29.512364'},
         {'id': 123455002, 'state': 'EXECUTED', 'date': '03-02-2026-03T18:35:29.512364'}
     ])
])
def data_filter_normal(request):
    return request.param


# test filter by state-2
@pytest.fixture(params=[
    ([
         {'id': 123455001, 'state': 'EXECUTED', 'date': '2026-01-03T18:35:29.512364'},
         {'id': 123455002, 'state': 'EXECUTED', 'date': '03-02-2026-03T18:35:29.512364'},
         {'id': 123455003, 'state': 'CANCELED', 'date': '2026-03-03T18:35:29.512364'},
         {'id': 123455004, 'state': 'CANCELED', 'date': '2026-05-03T18:35:29.512364'},
         {'id': 123455005, 'state': 'PENDING', 'date': '2026-05-03T18:35:29.512364'},
         {'id': 123455006, 'state': 'PENDING', 'date': '2026-05-03T18:35:29.512364'},
         {}
     ],
     [
         {'id': 123455005, 'state': 'PENDING', 'date': '2026-05-03T18:35:29.512364'},
         {'id': 123455006, 'state': 'PENDING', 'date': '2026-05-03T18:35:29.512364'}
     ])
])
def data_filter_pending(request):
    return request.param


# test filter by state-3
@pytest.fixture(params=[
    ([], []),                         # пустой список → пустой список
    ([{"state": "EXECUTED"}], [{"state": "EXECUTED"}]),
    ([{"state": "PENDING"}], []),     # не совпадает по state
    ([{"state": "EXECUTED"}, {"state": "PENDING"}], [{"state": "EXECUTED"}]),
])
def data_filter_null(request):
    return request.param


# test sorted by data
@pytest.fixture
def sample_data():
    return [
        {"id": 1, "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "date": "2020-01-10T12:00:00"},
        {"id": 3, "date": "2018-12-31T23:59:59"},
    ]

