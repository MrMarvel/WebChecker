from copy import deepcopy


class DataTable:
    """
    Класс для хранения с таблицей данных
    """
    def __init__(self, columns_name: list[str | None], rows: list[list] = None):
        """
        Конструктор таблицы данных.
        Количество имен столбцов должно совпадать с количеством столбцов
        :param columns_name: Имена столбцов list[str]
        :param rows: Строки данных list[list]
        """
        if type(columns_name) is not list:
            raise Exception("columns_name - не список!")
        if len(columns_name) < 1:
            raise Exception("Таблица не содержит столбцов!")

        self._columns_name = columns_name
        if rows is not None:
            if type(rows) is not list:
                raise Exception("rows - не список!")
            if len(rows) > 0:
                if False in [type(x) is list for x in rows]:
                    raise Exception("rows не соответствует формату list[list]")
                if False in [len(x) == len(self._columns_name) for x in rows]:
                    raise Exception(f"rows не соответствует формату количеству столбцов в данных")

        self._rows = rows

    def get_columns(self) -> list[str]:
        return self._columns_name.copy()

    def get_row(self, pos: int):
        return self._rows[0].copy()

    def get_rows_count(self) -> int:
        return len(self._rows)

    def get_rows(self) -> list[list]:
        return deepcopy(self._rows)