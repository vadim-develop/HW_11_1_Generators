from typing import Union


def get_mask_card_number(user_card: Union[str, int]) -> str:
    """Функция, которая принимает на вход номер карты в виде числа и возвращает маску номера по правилу
    XXXX XX** **** XXXX"""
    # Преобразуем в строку и удаляем возможные пробелы
    card_str = str(user_card).strip()

    # Проверяем, что в номере карты только цифры
    if not card_str.isdigit():
        return "Ошибка: Номер карты должен содержать только цифры."

    if len(card_str) != 16:
        return f"Ошибка: Номер карты должен содержать 16 цифр (получено {len(card_str)})."

    # Форматируем номер карты по маске XXXX XX** **** XXXX
    masked_card = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    return masked_card


def get_mask_account(user_account: Union[int, str]) -> str:
    """Функция, которая принимает на вход номер счета в виде числа и возвращает маску номера по правилу **XXXX"""
    # Преобразуем в строку и удаляем возможные пробелы
    account_str = str(user_account).strip()

    # Проверяем, что в номере счета только цифры
    if not account_str.isdigit():
        return "Ошибка: Номер счета должен содержать только цифры."

    # Проверяем длину номера счета (должно быть 20 цифр)
    if len(account_str) != 20:
        return f"Ошибка: Номер счета должен содержать 20 цифр (получено {len(account_str)})."

    # Форматируем номера счета по маске **XXXX
    masked_account = f"**{account_str[-4:]}"
    return masked_account
