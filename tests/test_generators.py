import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

# Тесты для функции filter_by_currency

# Тестовые данные - 4 простые транзакции
test_data = [
    {  # 1. Транзакция в USD
        "id": 1,
        "operationAmount": {"amount": "100", "currency": {"code": "USD", "name": "Доллар"}},
    },
    {  # 2. Транзакция в EUR
        "id": 2,
        "operationAmount": {"amount": "200", "currency": {"code": "EUR", "name": "Евро"}},
    },
    {  # 3. Еще одна транзакция в USD
        "id": 3,
        "operationAmount": {"amount": "300", "currency": {"code": "USD", "name": "Доллар"}},
    },
    {"id": 4, "operationAmount": {"amount": "400"}},  # 4. Транзакция без указания валюты (неправильная)
]


def test_find_usd_transactions():
    """Тест 1: Находим все USD транзакции"""
    # Получаем итератор с USD транзакциями
    usd_transactions = filter_by_currency(test_data, "USD")

    # Превращаем итератор в список для проверки
    result = list(usd_transactions)

    # Должно найти 2 транзакции (id 1 и 3)
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_find_eur_transactions():
    """Тест 2: Находим EUR транзакцию"""
    eur_transactions = filter_by_currency(test_data, "EUR")
    result = list(eur_transactions)

    # Должна быть 1 транзакция (id 2)
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_not_found_currency():
    """Тест 3: Ищем несуществующую валюту"""
    rub_transactions = filter_by_currency(test_data, "RUB")
    result = list(rub_transactions)

    # Не должно найти ни одной транзакции
    assert len(result) == 0


def test_bad_transaction_structure():
    """Тест 4: Проверяем обработку битой транзакции"""
    # Транзакция с id 4 имеет неправильную структуру
    all_transactions = filter_by_currency(test_data, "USD")
    result = list(all_transactions)

    # Должны быть только id 1 и 3, id 4 не должен мешать
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_empty_input():
    """Тест 5: Проверяем пустой список транзакций"""
    result = list(filter_by_currency([], "USD"))
    assert len(result) == 0


# Тесты для функции transaction_descriptions
def test_returns_correct_descriptions():
    """Тест 1: Проверяем, что функция возвращает правильные описания"""
    # Подготовка тестовых данных
    test_transactions = [
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Оплата услуг"},
    ]

    # Используем генератор
    gen = transaction_descriptions(test_transactions)

    # Проверяем каждое описание по очереди
    assert next(gen) == "Перевод организации"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Оплата услуг"

    # Проверяем, что генератор закончился
    with pytest.raises(StopIteration):
        next(gen)


def test_skips_transactions_without_description():
    """Тест 2: Проверяем, что пропускаются транзакции без описания"""
    test_transactions = [
        {"description": "Первый перевод"},
        {"no_description": "Нет описания"},  # Нет поля description
        {"description": "Второй перевод"},
        {"amount": 100},  # Тоже нет описания
    ]

    gen = transaction_descriptions(test_transactions)

    # Должны получить только транзакции с описанием
    assert next(gen) == "Первый перевод"
    assert next(gen) == "Второй перевод"

    # Больше описаний нет
    with pytest.raises(StopIteration):
        next(gen)


def test_single_transaction():
    """Тест 3: Проверяем работу с одной транзакцией"""
    test_transactions = [{"description": "Одиночный перевод"}]

    gen = transaction_descriptions(test_transactions)
    assert next(gen) == "Одиночный перевод"

    with pytest.raises(StopIteration):
        next(gen)


def test_empty_list():
    """Тест 4: Проверяем работу с пустым списком транзакций"""
    gen = transaction_descriptions([])

    # Генератор должен сразу завершиться
    with pytest.raises(StopIteration):
        next(gen)


def test_mixed_transactions():
    """Тест 5: Проверяем работу со смешанными данными"""
    test_transactions = [
        {"description": "Зарплата"},
        {"amount": 1000},  # Без описания
        {"description": "Аренда"},
        {"date": "2023-01-01"},  # Без описания
        {"description": "Покупка продуктов"},
    ]

    gen = transaction_descriptions(test_transactions)

    # Должны получить только транзакции с описанием
    assert next(gen) == "Зарплата"
    assert next(gen) == "Аренда"
    assert next(gen) == "Покупка продуктов"

    with pytest.raises(StopIteration):
        next(gen)


# тесты для фунции card_number_generator
def test_small_range():
    """Тест небольшого диапазона"""
    generator = card_number_generator(1, 3)
    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"
    assert next(generator) == "0000 0000 0000 0003"

    with pytest.raises(StopIteration):
        next(generator)


def test_large_numbers():
    """Тест больших номеров карт"""
    generator = card_number_generator(9999999999999995, 9999999999999999)
    assert next(generator) == "9999 9999 9999 9995"
    assert next(generator) == "9999 9999 9999 9996"
    assert next(generator) == "9999 9999 9999 9997"
    assert next(generator) == "9999 9999 9999 9998"
    assert next(generator) == "9999 9999 9999 9999"

    with pytest.raises(StopIteration):
        next(generator)


def test_single_number():
    """Тест одного номера карты"""
    generator = card_number_generator(1234567890123456, 1234567890123456)
    assert next(generator) == "1234 5678 9012 3456"

    with pytest.raises(StopIteration):
        next(generator)


def test_invalid_range():
    """Тест неверного диапазона (start > end)"""
    generator = card_number_generator(5, 1)
    with pytest.raises(StopIteration):
        next(generator)
