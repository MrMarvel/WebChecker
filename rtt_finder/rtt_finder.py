from datetime import datetime, timedelta

from requests_operator.empty_request import EmptyRequest
from requests_operator.perfomance_socket import PerfomanceSocket


class RTTFinder:
    """
    Класс для нахождения RTT (Round Trip Time) по заданному IP и порту
    учитывая коэффициент сглаживания a
    """

    def __init__(self, ip: str, port: int, a: float = 1.0, timeout=2):
        """
        Конструктор класса RTTFinder для нахождения RTT (Round Trip Time) по заданному IP и порту
        :param ip: IP адрес заданной в виде строки
        :param port: Порт заданный в виде целого числа (0-65535)
        :param a: Коэффициент сглаживания, заданный в виде числа с плавающей точкой в диапазоне [0, 1]
        """
        self._ip = ip
        self._port = port
        self._old_rtt: timedelta | None = None
        if not (0 <= a <= 1):
            raise ValueError("a должно быть между [0, 1]")
        self._a = a
        self._timeout = timeout
        self._ps = PerfomanceSocket(ip, port, timeout=timeout)
        self._lost_packets = 0

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        if not (0 <= value <= 1):
            raise ValueError("a должно быть между [0, 1]")
        self._a = value

    @property
    def lost_packets(self):
        return self._lost_packets

    def _find_roundtriptime_iteration(self) -> timedelta:
        try:
            interval = self._ps.find_socket_perfomance()
        except Exception as e:
            try:
                first_time = datetime.now()
                EmptyRequest.get("http://" + self._ip + ":" + str(self._port), timeout=self._timeout)
                second_time = datetime.now()
                interval = second_time - first_time
            except Exception as e:
                interval = timedelta(seconds=self._timeout)
                self._lost_packets += 1

        if self._old_rtt is None:
            self._old_rtt = interval
            return interval
        rtt = self._a * self._old_rtt + (1 - self._a) * interval
        self._old_rtt = rtt
        return rtt

    def find_roundtriptime(self, attempts: int = 10) -> timedelta:
        if attempts < 1:
            raise ValueError("Количество попыток должно быть больше 0")
        rtt = None
        for _ in range(attempts):
            rtt = self._find_roundtriptime_iteration()
        return rtt

    def __repr__(self):
        return f"RTTFinder({self._ip}, {self._port}, {self._a})"


if __name__ == '__main__':
    r = RTTFinder('34.96.123.111', 80, 0.9, timeout=2)
    print(r.find_roundtriptime(1).total_seconds())
