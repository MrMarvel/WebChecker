from check_task.check_task import CheckTaskFactory, CheckTask
from csv_operator.csv_operator import CsvOperator, DataTable


class ColumnsCountException(Exception):
    pass


class AddressNotFoundException(Exception):
    pass


class TaskLoader:
    def __init__(self, filename: str):
        self._filename = filename
        self._csv = CsvOperator()
        self._factory = CheckTaskFactory()

    def load(self) -> list[CheckTask]:
        dt: DataTable = self._csv.read_csv(self._filename)
        if len(dt.get_columns()) != 2:
            raise ColumnsCountException("Неверный формат файла!")
        tasks = []
        for i, row in enumerate(dt.get_rows()):
            address = str(row[0]).strip()
            if row[1] is None:
                ports = None
            else:
                ports = [int(x) if x is not None else None for x in str(row[1]).split(',')]

            if address is None or address == 'None' or address == '':
                raise AddressNotFoundException(f"Не указан адрес в \"{i+1}\" строке значений!")
            tasks += self._factory.create_check_tasks_for_address(address, ports)
        return tasks


if __name__ == '__main__':
    t = TaskLoader('../input.csv')
    t.load()
