import pytest


#test_card_number
@pytest.fixture(params=[
    ('7000792289606361', '7000 79** **** 6361'),
    ('7000792289606362', '7000 79** **** 6362')
])
def test_card_numbers(request):
    return request.param
#test_card_number off


#test_get_mask_account on
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
#test_get_mask_account off


#test_card_namenumber on
@pytest.fixture(params=[
    ('Maestro 1596837868705199', 'Maestro 1596 83** **** 5199'),
    ('Счет 64686473678894779589', 'Счет **9589')
])
def name_number(request):
    return request.param
#test_card_namenumber off


#test_data on
@pytest.fixture(params=[
    ('2024-03-11T02:26:18.671407', '11.03.2024'),
    ('2024-03-11T02:26:18.671407', '11.03.2024')
])
def datetime_new(request):
    return request.param
#test_data off