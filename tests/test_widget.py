from src.widget import get_date, mask_account_card


# Тесты для функции mask_account_card
def test_mask_card():
    """Тест маскирования номера карты"""
    assert mask_account_card("Visa Platinum 1234567890123456") == "Visa Platinum 1234 56** **** 3456"


def test_mask_account():
    """Тест маскирования номера счета"""
    assert mask_account_card("Счет 12345678901234567890") == "Счет **7890"


def test_invalid_card():
    """Тест с некорректным номером карты"""
    assert mask_account_card("Visa Platinum 1234") == "Visa Platinum 1234"


def test_invalid_account():
    """Тест с некорректным номером счета"""
    assert mask_account_card("Счет 123") == "Счет 123"


# Тесты для функции get_date
def test_date_conversion():
    """Тест преобразования даты"""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"


def test_short_date():
    """Тест с короткой датой"""
    assert get_date("2024-03-11") == "11.03.2024"  # Сработает, но возможно стоит добавить обработку
