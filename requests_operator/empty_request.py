import requests


class EmptyRequest:

    def __init__(self, status_code: int, text: str):
        self.status_code = status_code
        self.text = text

    @staticmethod
    def get(url, timeout=2):
        r = requests.get(url, timeout=timeout, verify=False)
        return EmptyRequest(r.status_code, r.text)