import pytest
from datetime import datetime
from typing import Any, Dict, List
from src.processing import filter_by_state, sort_by_date  # Замените src.operations на ваш модуль

# Фикстуры для тестовых данных
@pytest.fixture
def sample_operations() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T12:00:00.000000"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-10T08:30:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-20T15:45:00.000000"},
        {"id": 4, "state": "PENDING", "date": "2023-01-05T09:15:00.000000"},
        {"id": 5, "state": "EXECUTED", "date": "2023-01-18T11:20:00.000000"},
    ]

@pytest.fixture
def operations_with_same_date() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T12:00:00.000000"},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-15T12:00:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-15T12:00:00.000000"},
    ]

@pytest.fixture
def operations_with_invalid_dates() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15"},
        {"id": 2, "state": "EXECUTED", "date": "15-01-2023"},
        {"id": 3, "state": "EXECUTED", "date": "invalid_date"},
    ]

# Тесты для функции filter_by_state
@pytest.mark.parametrize("state, expected_ids", [
    ("EXECUTED", [1, 3, 5]),
    ("CANCELED", [2]),
    ("PENDING", [4]),
    ("UNKNOWN", []),
])
def test_filter_by_state(sample_operations: List[Dict[str, Any]], state: str, expected_ids: List[int]):
    """Параметризованный тест фильтрации по разным состояниям"""
    filtered = filter_by_state(sample_operations, state)
    assert [op["id"] for op in filtered] == expected_ids

def test_filter_default_state(sample_operations: List[Dict[str, Any]]):
    """Тест фильтрации со значением состояния по умолчанию"""
    filtered = filter_by_state(sample_operations)
    assert all(op["state"] == "EXECUTED" for op in filtered)

def test_filter_empty_list():
    """Тест фильтрации пустого списка"""
    assert filter_by_state([]) == []

# Тесты для функции sort_by_date
def test_sort_descending(sample_operations: List[Dict[str, Any]]):
    """Тест сортировки по убыванию (новые сначала)"""
    sorted_ops = sort_by_date(sample_operations)
    dates = [op["date"] for op in sorted_ops]
    assert dates == sorted(dates, reverse=True)

def test_sort_ascending(sample_operations: List[Dict[str, Any]]):
    """Тест сортировки по возрастанию (старые сначала)"""
    sorted_ops = sort_by_date(sample_operations, reverse=False)
    dates = [op["date"] for op in sorted_ops]
    assert dates == sorted(dates)

def test_sort_same_date(operations_with_same_date: List[Dict[str, Any]]):
    """Тест сортировки при одинаковых датах"""
    sorted_ops = sort_by_date(operations_with_same_date)
    assert [op["id"] for op in sorted_ops] == [1, 2, 3]

@pytest.mark.parametrize("reverse", [True, False])
def test_sort_invalid_dates(operations_with_invalid_dates: List[Dict[str, Any]], reverse: bool):
    """Тест сортировки с некорректными датами"""
    with pytest.raises((ValueError, TypeError)):
        sort_by_date(operations_with_invalid_dates, reverse=reverse)

def test_sort_empty_list():
    """Тест сортировки пустого списка"""
    assert sort_by_date([]) == []