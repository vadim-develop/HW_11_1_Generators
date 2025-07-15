from typing import Dict, List, Iterator


def filter_by_currency(transactions: List[Dict], currency: str) -> Iterator[Dict]:
    """
    Фильтрует транзакции по валюте и возвращает итератор.

    Параметры:
        transactions: Список словарей с транзакциями
        currency: Код валюты для фильтрации (например, "USD")

    Возвращает:
        Итератор, который поочередно выдает транзакции с заданной валютой
    """
    for transaction in transactions:
        try:
            # Проверяем валюту операции (в operationAmount -> currency -> code)
            if transaction["operationAmount"]["currency"]["code"] == currency:
                yield transaction
        except KeyError:
            # Пропускаем транзакции с некорректной структурой
            continue


def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    """
    Генератор, который возвращает описания транзакций по очереди.

    Параметры:
        transactions: Список словарей с транзакциями

    Возвращает:
        Итератор, который поочередно выдает описания транзакций
    """
    for transaction in transactions:
        # Извлекаем описание, если оно есть
        description = transaction.get("description")
        if description is not None:
            yield description


def card_number_generator(start: int, end: int) -> str:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    Параметры:
        start: начальный номер карты (от 1)
        end: конечный номер карты (до 9999999999999999)

    Возвращает:
        Номера карт в заданном диапазоне в формате XXXX XXXX XXXX XXXX
    """
    for number in range(start, end + 1):
        # Преобразуем число в 16-значную строку с ведущими нулями
        card_number = f"{number:016d}"
        # Форматируем по маске XXXX XXXX XXXX XXXX
        formatted_number = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:16]}"
        yield formatted_number
