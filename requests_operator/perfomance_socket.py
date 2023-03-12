import socket
from datetime import datetime, timedelta, time
import requests


class PerfomanceSocket:
    def __init__(self, ip: str, port: int, timeout: int = 2):
        self._ip = ip
        self._port = port
        self._timeout = timeout

    def check_socket_connection(self) -> bool:
        ip = self._ip
        port = self._port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(self._timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                return True
            else:
                return False

    def find_socket_perfomance(self) -> timedelta:
        sock_params = (self._ip, self._port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Set the timeout in the event that the host/port we are pinging doesn't send information back
            sock.settimeout(self._timeout)
            # Open a TCP Connection
            sock.connect(sock_params)
            # Time prior to sending 1 byte
            t1 = datetime.now()
            sock.sendall(b'1')
            data = sock.recv(1)
            # Time after receiving 1 byte
            t2 = datetime.now()
            # RTT
            return t2 - t1


if __name__ == '__main__':
    # print(check_socket_connection('', 80))
    pass