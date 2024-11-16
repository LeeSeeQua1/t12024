from api import TaskStatus


def status(status_field: str) -> TaskStatus:
    if status_field in ['Закрыто', 'Выполнено']:
        return TaskStatus.CLOSED
    elif status_field in ['В работе', 'Тестирование', 'Анализ', 'Исправление', 'Подтверждение исправления',
                          'Разработка', 'Локализация']:
        return TaskStatus.IN_PROGRESS
    elif status_field in ['Создано', 'Готово к разработке', 'В ожидании']:
        return TaskStatus.TO_DO
    else:
        return TaskStatus.OTHER
