from typing import Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date  # Замените src.operations на ваш модуль


# Фикстура с тестовыми данными
@pytest.fixture
def sample_operations() -> List[Dict[str, str]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T12:00:00.000000"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-10T08:30:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-20T15:45:00.000000"},
        {"id": 4, "date": "2023-01-05T09:15:00.000000"},  # Операция без статуса
    ]


def test_filter_by_state_default(sample_operations):
    """Тест фильтрации по умолчанию (EXECUTED)"""
    result = filter_by_state(sample_operations)
    assert len(result) == 2
    assert all(op["state"] == "EXECUTED" for op in result)


def test_filter_by_state_canceled(sample_operations):
    """Тест фильтрации по статусу CANCELED"""
    result = filter_by_state(sample_operations, "CANCELED")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_empty_list():
    """Тест фильтрации пустого списка"""
    assert filter_by_state([]) == []


def test_sort_by_date_descending(sample_operations):
    """Тест сортировки по убыванию даты (новые сначала)"""
    result = sort_by_date(sample_operations)
    dates = [op["date"] for op in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(sample_operations):
    """Тест сортировки по возрастанию даты (старые сначала)"""
    result = sort_by_date(sample_operations, reverse=False)
    dates = [op["date"] for op in result]
    assert dates == sorted(dates)


def test_sort_with_same_dates():
    """Тест сортировки при одинаковых датах"""
    ops = [
        {"id": 1, "date": "2023-01-01T00:00:00.000000"},
        {"id": 2, "date": "2023-01-01T00:00:00.000000"},
    ]
    result = sort_by_date(ops)
    assert [op["id"] for op in result] == [1, 2]
