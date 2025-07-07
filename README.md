# Домашняя работа Pytest
# Обработка банковских операций

Модуль для фильтрации и сортировки банковских операций.

## Установка
1. Скопируйте файл `processing.py` в ваш проект
2. Импортируйте нужные функции:
```python
from processing import filter_by_state, sort_by_date
```

## Использование

### Функция `filter_by_state`
Фильтрует операции по статусу:
```python
operations = [
    {'id': 1, 'state': 'EXECUTED'},
    {'id': 2, 'state': 'CANCELED'}
]

# Фильтрация выполненных операций
executed_ops = filter_by_state(operations)

# Фильтрация отмененных операций
canceled_ops = filter_by_state(operations, 'CANCELED')
```

### Функция `sort_by_date`
Сортирует операции по дате:
```python
operations = [
    {'date': '2019-07-03T18:35:29.512364'},
    {'date': '2018-06-30T02:08:58.425572'}
]

# Сортировка по убыванию (новые сначала)
sorted_desc = sort_by_date(operations)

# Сортировка по возрастанию (старые сначала)
sorted_asc = sort_by_date(operations, reverse=False)
```

## Примеры работы
```python
from processing import filter_by_state, sort_by_date

data = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
]

# Фильтрация + сортировка
filtered = filter_by_state(data, 'EXECUTED')
result = sort_by_date(filtered)
```