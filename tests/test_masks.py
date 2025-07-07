from src.masks import get_mask_card_number, get_mask_account


# Тесты для get_mask_card_number
def test_valid_card_masking():
    assert get_mask_card_number("1234567812345678") == "1234 56** **** 5678"


def test_card_with_spaces():
    assert get_mask_card_number(" 1234567812345678 ") == "1234 56** **** 5678"


def test_card_as_number():
    assert get_mask_card_number(1234567812345678) == "1234 56** **** 5678"


def test_invalid_short_card():
    result = get_mask_card_number("1234")
    assert "Ошибка" in result and "16 цифр" in result


def test_invalid_long_card():
    result = get_mask_card_number("123456781234567812")
    assert "Ошибка" in result and "16 цифр" in result


def test_card_with_letters():
    result = get_mask_card_number("abcd1234efgh5678")
    assert "Ошибка" in result and "только цифры" in result


# Тесты для get_mask_account
def test_valid_account_masking():
    assert get_mask_account("12345678901234567890") == "**7890"


def test_account_with_spaces():
    assert get_mask_account(" 12345678901234567890 ") == "**7890"


def test_account_as_number():
    assert get_mask_account(12345678901234567890) == "**7890"


def test_invalid_short_account():
    result = get_mask_account("1234567890")
    assert "Ошибка" in result and "20 цифр" in result


def test_invalid_long_account():
    result = get_mask_account("123456789012345678901")
    assert "Ошибка" in result and "20 цифр" in result


def test_account_with_letters():
    result = get_mask_account("abcdefghijklmnopqrst")
    assert "Ошибка" in result and "только цифры" in result
