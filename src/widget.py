from typing import Union

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(user_data: str) -> str:
    """Функция, которая обрабатывает информацию о картах и счетах, используя существующие функции маскировки"""

    # Разделяем строку на название и номер
    parts = user_data.rsplit(" ", 1)
    if len(parts) != 2:
        return user_data

    name, number = parts

    # Определяем тип и применяем соответствующую маскировку
    if "счет" in name.lower():
        # Используем функцию для счетов
        masked_number = get_mask_account(number)
        if masked_number.startswith("Ошибка"):
            return user_data  # или можно вернуть ошибку
        return f"{name} {masked_number}"
    else:
        # Используем функцию для карт
        masked_number = get_mask_card_number(number)
        if masked_number.startswith("Ошибка"):
            return user_data  # или можно вернуть ошибку
        return f"{name} {masked_number}"


def get_date(date_str: Union[str]) -> Union[str]:
    """Функция, которая преобразует дату из формата '2024-03-11T02:26:18.671407' в 'ДД.ММ.ГГГГ'"""
    return date_str[8:10] + "." + date_str[5:7] + "." + date_str[:4]
