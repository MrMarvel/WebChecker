import pandas as pd

from csv_operator.data_table import DataTable


class CsvOperator:
    @staticmethod
    def read_csv(from_file: str, sep=';'):
        """

        :param from_file:
        :param sep:
        :return:
        """
        df: pd.DataFrame = pd.read_csv(from_file, sep=sep)
        df[df.isna()] = None

        columns_name = [str(x) for x in df.columns]
        rows = [list(x) for x in df.values]
        t = DataTable(columns_name, rows)
        return t


if __name__ == '__main__':
    CsvOperator.read_csv('input.csv')
