from datetime import datetime

from domain_checker.domain_checker import DomainChecker
from domain_checker.ip_validator import *
from requests_operator.perfomance_socket import PerfomanceSocket
from rtt_finder.rtt_finder import RTTFinder


class DNSGetIPException(Exception):
    """
    Исключение, возникающее при невозможности получить IP адрес по доменному имени
    """
    pass


class CheckResultPerfomance:
    """
    Класс для хранения результатов проверки
    """
    def __init__(self, ip: str, port: int | None, check_end_time: datetime,
                 domain: str | None = None, rtt_ms: float | None = None, port_status: bool | None = None):
        self._ip: str = ip
        self._port: int | None = port
        self._check_end_datetime: datetime = check_end_time
        self._domain: str | None = domain
        self._rtt_ms: float | None = rtt_ms
        self._port_status: bool | None = port_status

    def __str__(self):
        """
        Возвращает строковое представление объекта
        :return:
        """
        result_str = f"{self._check_end_datetime.strftime('%Y-%m-%d %H:%M:%S:%f')} | " \
                     f"{self._domain if self._domain is not None else '???'} | " \
                     f"{self._ip} | " \
                     f"{self._rtt_ms if self._rtt_ms else '???'} ms | " \
                     f"{self._port if self._port else -1} | "
        if self._port_status is not None:
            result_str += f"{'Opened' if self._port_status else 'Not opened'}"
        else:
            result_str += f"{'???'}"
        return result_str


class CheckTask:
    """
    Класс Задачи для проверки IP адреса и порта
    """
    def __init__(self, ip: str, port: int, from_domain: str | None = None):
        self._ip = ip
        self._from_domain = from_domain
        self._port = port
        if port == -1:
            port_to_test = 80
        else:
            port_to_test = port
        self._ps = PerfomanceSocket(ip, port_to_test)
        self._rtt_finder = RTTFinder(self._ip, port_to_test, a=0)

    @property
    def ip(self):
        """
        IP адрес для проверки
        :return:
        """
        return self._ip

    @property
    def port(self):
        """
        Порт для проверки
        :return:
        """
        return self._port

    @property
    def domain(self):
        """
        Доменное имя, из которого был получен IP адрес
        :return:
        """
        return self._from_domain

    def check_connection(self) -> CheckResultPerfomance:
        """
        Проверка соединения
        :return: Результат проверки в виде объекта CheckResultPerfomance
        """
        is_ok = self._ps.check_socket_connection()
        self._rtt_finder.a = 0 if is_ok else 1
        rtt = self._rtt_finder.find_roundtriptime(1)
        res = CheckResultPerfomance(self._ip, self._port, datetime.now(),
                                    self._from_domain, rtt.total_seconds()*1000, is_ok if self._port != -1 else None)
        return res

    def __repr__(self):
        """
        Возвращает строковое представление объекта
        """
        return f"CheckTask({self._ip}, {self._port}, {self._from_domain})"


class CheckTaskFactory:
    """
    Фабрика для создания задач для проверки
    """
    def __init__(self):
        self._domain_checker = DomainChecker()

    def create_check_tasks_for_address(self, address: str, ports: list[int] | None = None) -> list[CheckTask]:
        """
        Создает задачи для проверки по адресу и портам
        :param address: адрес для проверки
        :param ports: список портов для проверки
        :return: список задач для проверки
        """
        if ports is None or len(ports) == 0:
            ports = [-1]
        if is_valid_ipv4_address(address) or is_valid_ipv6_address(address):
            ip = address
            return [CheckTask(ip, port) for port in ports]
        ips = self._domain_checker.dns_lookup(address)
        if len(ips) is None:
            raise DNSGetIPException()
        from_domain = address
        return [CheckTask(ip, port, from_domain) for port in ports for ip in ips]
