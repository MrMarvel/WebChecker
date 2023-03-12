import os
from enum import Enum

from check_task.check_task import CheckTask
from task_loader.task_loader import TaskLoader


class FILES(Enum):
    """
    Класс для хранения констант
    """
    INPUT_FILE = 'input.csv'




class App:
    @staticmethod
    def main():
        """
        Точка входа
        Здесь начинается магия
        :return:
        """
        # Проверка условий среды
        # Проверка наличия наличние входного файла
        if not os.path.exists(FILES.INPUT_FILE.value):
            print(f"Файл {FILES.INPUT_FILE.value} не найден!")
            return
        # Создание загрузчика
        task_loader = TaskLoader(FILES.INPUT_FILE.value)
        # Работа в цикле
        while True:
            # Загрузка задачи
            try:
                tasks: list[CheckTask] = task_loader.load()
            except Exception as e:
                print(f"Ошибка при загрузке задачи: {e}")
                return
            # Проверка наличия задач
            if len(tasks) == 0:
                print("Задачи не найдены!")
                return

            last_domain = None
            # Разделение по доменам для вывода
            domains_tasks: dict[str, list[CheckTask]] = {}
            for task in tasks:
                if task.domain is None:
                    if task.ip not in domains_tasks:
                        domains_tasks[task.ip] = []
                    domains_tasks[task.ip].append(task)
                if task.domain not in domains_tasks:
                    domains_tasks[task.domain] = []
                domains_tasks[task.domain].append(task)
            # Проверка сайтов
            for task in tasks:
                # Вывод домена для сохранения формата вывода
                if task.domain is None:
                    print(["???",
                           list(set(x.ip for x in domains_tasks[task.ip])),
                           list(set(x.port for x in domains_tasks[task.ip]))
                           ])
                elif last_domain != task.domain:
                    print([task.domain if task.domain is not None else '???',
                           list(set(x.ip for x in domains_tasks[task.domain])),
                           list(set(x.port for x in domains_tasks[task.domain]))
                           ])
                    last_domain = task.domain
                check_result = task.check_connection()
                print(str(check_result))


if __name__ == '__main__':
    App.main()
