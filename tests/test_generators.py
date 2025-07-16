from typing import Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

# Тесты для функции filter_by_currency


# Фикстура с тестовыми транзакциями
@pytest.fixture
def sample_transactions() -> List[Dict]:
    return [
        {"id": 1, "operationAmount": {"amount": "100.00", "currency": {"code": "USD", "name": "Доллар"}}},
        {"id": 2, "operationAmount": {"amount": "200.00", "currency": {"code": "EUR", "name": "Евро"}}},
        {"id": 3, "operationAmount": {"amount": "300.00", "currency": {"code": "USD", "name": "Доллар"}}},
        {"id": 4, "operationAmount": {"amount": "400.00", "currency": {"code": "GBP", "name": "Фунт"}}},
        {"id": 5, "operationAmount": {}},  # Некорректная транзакция
        {"id": 6},  # Транзакция без operationAmount
    ]


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


# Фикстура с тестовыми данными
@pytest.fixture
def sample_transactions() -> List[Dict]:
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод со счета на счет"},
        {"id": 3},  # Транзакция без описания
        {"id": 4, "description": "Оплата услуг"},
        {"id": 5, "other_field": "Нет описания"},  # Тоже без описания
    ]


# Параметризованный тест для разных случаев
@pytest.mark.parametrize(
    "input_data, expected_descriptions",
    [
        # Тест 1: Обычные транзакции с описаниями
        ([{"description": "Зарплата"}, {"description": "Аренда"}], ["Зарплата", "Аренда"]),
        # Тест 2: Транзакции без описаний
        ([{"amount": 100}, {"date": "2023-01-01"}], []),
        # Тест 3: Пустой список
        ([], []),
        # Тест 4: Смешанные транзакции
        ([{"description": "Покупка"}, {"amount": 200}, {"description": "Продажа"}], ["Покупка", "Продажа"]),
    ],
)
def test_transaction_descriptions_parametrized(input_data, expected_descriptions):
    """Параметризованный тест для разных случаев ввода"""
    result = list(transaction_descriptions(input_data))
    assert result == expected_descriptions


def test_with_fixture(sample_transactions):
    """Тест с использованием фикстуры"""
    gen = transaction_descriptions(sample_transactions)

    # Проверяем порядок и содержание описаний
    assert next(gen) == "Перевод организации"
    assert next(gen) == "Перевод со счета на счет"
    assert next(gen) == "Оплата услуг"

    # Проверяем, что генератор закончился
    with pytest.raises(StopIteration):
        next(gen)


def test_empty_list():
    """Тест с пустым списком транзакций"""
    gen = transaction_descriptions([])
    with pytest.raises(StopIteration):
        next(gen)


# тесты для фунции card_number_generator


# Фикстура с тестовыми диапазонами
@pytest.fixture(
    params=[
        (1, 5),  # Маленький диапазон
        (9995, 9999),  # Близко к границе
        (1, 1),  # Один номер
        (9999999999999995, 9999999999999999),  # Максимальные значения
    ]
)
def number_ranges(request):
    """Фикстура возвращает разные диапазоны для тестирования"""
    return request.param


# Параметризованные тесты для проверки форматирования
@pytest.mark.parametrize(
    "number, expected",
    [
        (1, "0000 0000 0000 0001"),
        (1234567890123456, "1234 5678 9012 3456"),
        (9999999999999999, "9999 9999 9999 9999"),
        (10000, "0000 0000 0001 0000"),  # Проверка чисел больше 9999
    ],
)
def test_card_number_formatting(number, expected):
    """Тест правильного форматирования номеров карт"""
    gen = card_number_generator(number, number)
    assert next(gen) == expected


def test_generator_with_fixture(number_ranges):
    """Тест генератора с использованием фикстуры"""
    start, end = number_ranges
    gen = card_number_generator(start, end)

    # Проверяем первый элемент
    first_number = next(gen)
    assert (
        first_number
        == f"{start:016d}"[:4]
        + " "
        + f"{start:016d}"[4:8]
        + " "
        + f"{start:016d}"[8:12]
        + " "
        + f"{start:016d}"[12:16]
    )

    # Проверяем количество элементов
    count = end - start + 1
    if count > 1:
        # Пропускаем промежуточные элементы
        for _ in range(count - 2):
            next(gen)
        # Проверяем последний элемент
        last_number = next(gen)
        assert (
            last_number
            == f"{end:016d}"[:4] + " " + f"{end:016d}"[4:8] + " " + f"{end:016d}"[8:12] + " " + f"{end:016d}"[12:16]
        )

    # Проверяем завершение генератора
    with pytest.raises(StopIteration):
        next(gen)


def test_invalid_range():
    """Тест на некорректный диапазон (start > end)"""
    gen = card_number_generator(10, 5)
    with pytest.raises(StopIteration):
        next(gen)


def test_edge_cases():
    """Тест граничных случаев"""
    # Минимальное значение
    gen = card_number_generator(1, 1)
    assert next(gen) == "0000 0000 0000 0001"

    # Максимальное значение
    gen = card_number_generator(9999999999999999, 9999999999999999)
    assert next(gen) == "9999 9999 9999 9999"

    # Диапазон из одного элемента
    gen = card_number_generator(1234567890123456, 1234567890123456)
    assert next(gen) == "1234 5678 9012 3456"
