from typing import Any, Dict, List


def filter_by_state(operations_list: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список операций по статусу (по умолчанию выбирает 'EXECUTED')

    Параметры:
        operations_list - список словарей с операциями
        state - статус операций для отбора (по умолчанию 'EXECUTED')

    Возвращает:
        Новый список только с операциями указанного статуса
    """

    # Создаем пустой список для результатов
    result = []

    # Перебираем все операции в списке
    for operation in operations_list:
        # Проверяем есть ли в операции ключ 'state'
        if "state" in operation:
            # Если статус операции совпадает с нужным
            if operation["state"] == state:
                # Добавляем операцию в результат
                result.append(operation)

    # Возвращаем отфильтрованный список
    return result


def sort_by_date(operations_list: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате

    Параметры:
        operations_list - список словарей с операциями
        reverse - порядок сортировки (True - новые сначала, False - старые сначала)

    Возвращает:
        Новый список с операциями, отсортированными по дате
    """

    # Создаем копию списка, чтобы не менять оригинал
    sorted_list: List[Dict[str, Any]] = operations_list.copy()

    # Функция для получения даты из операции
    def get_date(operation: Dict[str, Any]) -> str:
        """Вспомогательная функция для извлечения даты из операции"""
        return operation["date"]

    # Сортируем список по дате
    sorted_list.sort(key=get_date, reverse=reverse)

    # Возвращаем отсортированный список
    return sorted_list
