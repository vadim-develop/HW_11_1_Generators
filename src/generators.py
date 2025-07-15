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