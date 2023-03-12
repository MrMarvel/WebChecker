from unittest import TestCase

from check_task.check_task import CheckTaskFactory


class TestCheckTask(TestCase):
    def test_check_connection(self):
        fac = CheckTaskFactory()
        c = fac.create_check_tasks_for_address('ya.ru', [80])
        results = [c.check_connection() for c in c]
        print(c)
        print('\n'.join([str(x) for x in results]))
