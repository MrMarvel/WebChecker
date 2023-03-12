import requests


class EmptyRequest:
    """
    Адаптер для requests, чтобы можно было возвращать запрос
    """

    def __init__(self, status_code: int, text: str):
        self.status_code = status_code
        self.text = text

    @staticmethod
    def get(url, timeout=2):
        """
        Получить запрос
        :param url: адрес в виде строки http://ip:port
        :param timeout: таймаут в секундах
        :return: EmptyRequest
        """
        r = requests.get(url, timeout=timeout, verify=False)
        return EmptyRequest(r.status_code, r.text)