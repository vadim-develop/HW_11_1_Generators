import pytest
from typing import Union
from src.masks import get_mask_card_number, get_mask_account

# Фикстуры для тестовых данных
@pytest.fixture
def valid_card_number() -> str:
    """Генерирует валидный номер карты (16 цифр)"""
    return "4000123456789010"

@pytest.fixture
def card_number_with_spaces() -> str:
    """Генерирует номер карты с пробелами"""
    return "4000 1234 5678 9010"

@pytest.fixture
def card_number_with_dashes() -> str:
    """Генерирует номер карты с дефисами"""
    return "4000-1234-5678-9010"

@pytest.fixture
def short_card_number() -> str:
    """Генерирует короткий номер карты (15 цифр)"""
    return "400012345678901"

@pytest.fixture
def long_card_number() -> str:
    """Генерирует длинный номер карты (17 цифр)"""
    return "40001234567890101"

@pytest.fixture
def non_digit_card_number() -> str:
    """Генерирует номер карты с буквами"""
    return "4000abcd56789010"

# Параметризованные тесты для валидных номеров карт
@pytest.mark.parametrize("input_card, expected", [
    ("4000123456789010", "4000 12** **** 9010"),
    (4000123456789010, "4000 12** **** 9010"),  # Как число
    (" 4000123456789010 ", "4000 12** **** 9010"),  # С пробелами
    ("4000-1234-5678-9010", "4000 12** **** 9010"),  # С дефисами
    ("4000.1234.5678.9010", "4000 12** **** 9010"),  # С точками
])
def test_valid_card_masking(input_card: Union[str, int], expected: str):
    """Тестирование корректного маскирования валидных номеров карт"""
    assert get_mask_card_number(input_card) == expected

# Параметризованные тесты для невалидных номеров карт
@pytest.mark.parametrize("input_card, expected_error", [
    ("400012345678901", "Ошибка: Номер карты должен содержать 16 цифр (получено 15)."),  # 15 цифр
    ("40001234567890101", "Ошибка: Номер карты должен содержать 16 цифр (получено 17)."),  # 17 цифр
    ("", "Ошибка: Номер карты должен содержать 16 цифр (получено 0)."),  # Пустая строка
    ("abcd", "Ошибка: Номер карты должен содержать только цифры."),  # Только буквы
    (None, "Ошибка: Номер карты должен содержать только цифры."),  # None
    (12345.67, "Ошибка: Номер карты должен содержать только цифры."),  # Число с плавающей точкой
    ("4000 12x4 5678 9010", "Ошибка: Номер карты должен содержать только цифры."),  # Буква среди цифр
])
def test_invalid_card_input(input_card: Union[str, int, None], expected_error: str):
    """Тестирование обработки невалидных входных данных"""
    assert get_mask_card_number(input_card) == expected_error

# Тесты с использованием фикстур
def test_fixture_valid_card(valid_card_number: str):
    """Тест с использованием фикстуры для валидного номера карты"""
    assert get_mask_card_number(valid_card_number) == "4000 12** **** 9010"

def test_fixture_card_with_spaces(card_number_with_spaces: str):
    """Тест с использованием фикстуры для номера с пробелами"""
    assert get_mask_card_number(card_number_with_spaces) == "4000 12** **** 9010"

def test_fixture_short_card(short_card_number: str):
    """Тест с использованием фикстуры для короткого номера"""
    assert "15" in get_mask_card_number(short_card_number)  # Проверяем сообщение об ошибке

# Тест для проверки граничного случая (ровно 16 символов)
def test_exact_16_digits():
    """Тестирование граничного случая - ровно 16 цифр"""
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"

# Тест для проверки обработки пробелов
def test_whitespace_handling():
    """Тестирование обработки строк с пробелами"""
    assert get_mask_card_number("  1234567890123456  ") == "1234 56** **** 3456"



# Фикстура для генерации валидного номера счета
@pytest.fixture
def valid_account_number() -> str:
    return "73654108430135874305"  # 20 цифр

# Параметризованные тесты для проверки корректного маскирования
@pytest.mark.parametrize("input_account, expected", [
    ("73654108430135874305", "**4305"),  # Стандартный номер
    (73654108430135874305, "**4305"),    # Номер как число
    (" 73654108430135874305 ", "**4305"),  # Номер с пробелами
    ("7365-4108-4301-3587-4305", "**4305"),  # Номер с разделителями
    ("7"*16 + "4305", "**4305"),  # Граничный случай (первые 16 любых цифр)
])
def test_valid_account_masking(input_account: Union[str, int], expected: str):
    assert get_mask_account(input_account) == expected

# Параметризованные тесты для проверки обработки ошибок
@pytest.mark.parametrize("input_account, expected_error", [
    ("1234567890123456789", "Ошибка: Номер счета должен содержать 20 цифр (получено 19)."),  # 19 цифр
    ("123456789012345678901", "Ошибка: Номер счета должен содержать 20 цифр (получено 21)."),  # 21 цифра
    ("", "Ошибка: Номер счета должен содержать 20 цифр (получено 0)."),  # Пустая строка
    ("abcdefghijklmnopqrst", "Ошибка: Номер счета должен содержать только цифры."),  # Буквы
    ("1234 5678 9012 3456 7890", "Ошибка: Номер счета должен содержать только цифры."),  # Буквы и пробелы
    (None, "Ошибка: Номер счета должен содержать только цифры."),  # None
    (12345.67, "Ошибка: Номер счета должен содержать только цифры."),  # Число с плавающей точкой
])
def test_invalid_account_input(input_account: Union[str, int, None], expected_error: str):
    assert get_mask_account(input_account) == expected_error

# Тест для проверки обработки пробелов
def test_whitespace_handling(valid_account_number: str):
    assert get_mask_account(f"  {valid_account_number}  ") == "**4305"

# Тест для проверки граничного случая (ровно 20 символов)
def test_exact_20_digits(valid_account_number: str):
    assert get_mask_account(valid_account_number) == "**4305"
