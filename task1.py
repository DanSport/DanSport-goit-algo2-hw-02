from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    # Перетворення вхідних даних у відповідні dataclass
    printer_constraints = PrinterConstraints(**constraints)
    jobs = [PrintJob(**job) for job in print_jobs]
    
    # Сортуємо завдання за пріоритетом (1 — найвищий, потім 2, потім 3)
    jobs_sorted = sorted(jobs, key=lambda job: job.priority)
    
    groups = []         # Список груп для одночасного друку
    current_group = []  # Поточна група завдань
    current_volume = 0  # Сумарний об'єм поточної групи
    
    # Жадібний підхід: намагаємося додати завдання до поточної групи,
    # не порушуючи обмеження по об'єму та кількості моделей.
    for job in jobs_sorted:
        # Якщо до поточної групи можна додати завдання:
        if (len(current_group) < printer_constraints.max_items and 
            current_volume + job.volume <= printer_constraints.max_volume):
            current_group.append(job)
            current_volume += job.volume
        else:
            # Фіксуємо групу та починаємо нову
            groups.append(current_group)
            current_group = [job]
            current_volume = job.volume

    # Додаємо останню групу, якщо вона не порожня
    if current_group:
        groups.append(current_group)
    
    total_time = 0
    print_order = []
    # Для кожної групи час друку визначається як максимальний час серед моделей у групі
    for group in groups:
        group_time = max(job.print_time for job in group)
        total_time += group_time
        # Додаємо ідентифікатори завдань згідно з порядком друку в групі
        print_order.extend([job.id for job in group])
    
    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},   # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}   # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()
