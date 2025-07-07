import pytest
from typing import Union
from src.widget import mask_account_card, get_date

# Фикстуры для тестовых данных
@pytest.fixture
def valid_card_data() -> str:
    return "Visa Platinum 7000792289606361"

@pytest.fixture
def valid_account_data() -> str:
    return "Счет 73654108430135874305"

@pytest.fixture
def invalid_data() -> str:
    return "Неизвестный тип 1234567890"

@pytest.fixture
def short_data() -> str:
    return "Карта 1234"

@pytest.fixture
def valid_date_str() -> str:
    return "2024-03-11T02:26:18.671407"

# Тесты для функции mask_account_card
@pytest.mark.parametrize("input_data, expected", [
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
    ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
])
def test_valid_masking(input_data: str, expected: str):
    """Тестирование корректного маскирования валидных данных"""
    assert mask_account_card(input_data) == expected

@pytest.mark.parametrize("input_data", [
    "Неизвестный тип 1234567890",
    "Слишкомкороткаястрока",
    "",
    "Visa Platinum",
    "Счет",
])
def test_invalid_input(input_data: str):
    """Тестирование обработки некорректных входных данных"""
    assert mask_account_card(input_data) == input_data

def test_card_with_spaces(valid_card_data: str):
    """Тест с использованием фикстуры для карты с пробелами"""
    assert mask_account_card(f"  {valid_card_data}  ") == "Visa Platinum 7000 79** **** 6361"

def test_account_with_special_chars(valid_account_data: str):
    """Тест для счета со специальными символами"""
    assert mask_account_card("Счет 7365-4108-4301-3587-4305") == "Счет **4305"

# Тесты для функции get_date
@pytest.mark.parametrize("input_date, expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("1999-12-31T23:59:59.999999", "31.12.1999"),
    ("2000-01-01T00:00:00.000000", "01.01.2000"),
])
def test_valid_date_conversion(input_date: str, expected: str):
    """Тестирование корректного преобразования даты"""
    assert get_date(input_date) == expected

@pytest.mark.parametrize("input_date", [
    "",
    "2024-03-11",
    "11.03.2024",
    "не дата",
    None,
])
def test_invalid_date_input(input_date: Union[str, None]):
    """Тестирование обработки некорректных дат"""
    if input_date is None:
        with pytest.raises(Exception):
            get_date(input_date)
    else:
        with pytest.raises((ValueError, IndexError)):
            get_date(input_date)

def test_fixture_date_conversion(valid_date_str: str):
    """Тест с использованием фикстуры для даты"""
    assert get_date(valid_date_str) == "11.03.2024"

def test_short_date_input():
    """Тестирование короткой строки с датой"""
    with pytest.raises(IndexError):
        get_date("2024-03")