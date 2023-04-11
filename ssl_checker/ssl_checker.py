# -*- encoding: utf-8 -*-
# requires a recent enough python with idna support in socket
# pyopenssl, cryptography and idna
from collections import namedtuple
from datetime import datetime
from socket import socket
from typing import Union

import idna
from OpenSSL import SSL


class NoSSLException(Exception):
    """
    Исключение, возникающее при невозможности получить SSL сертификат
    """
    pass


class SSLChecker:
    """
    Класс для проверки SSL сертификата
    Также является оберткой для работой с pyopenssl и idna
    """
    def __init__(self, ip: str, port: int = 443):
        """
        Конструктор
        :param ip: IP адрес
        :param port: Порт, обычно 443
        """
        self._ip = ip
        self._port = port

    def verify_cert(self) -> bool:
        """
        Проверка SSL сертификата
        :return: True, если сертификат валиден, иначе False
        """
        # verify notAfter/notBefore, CA trusted, servername/sni/hostname
        cert_info = self.get_certificate_info()
        if cert_info is None:
            return False
        if cert_info.cert is None:
            return False
        return cert_info.cert.not_valid_after >= datetime.now()
        # service_identity.pyopenssl.verify_hostname(client_ssl, hostname)
        # issuer

    def get_certificate_info(self) -> Union[namedtuple, None]:
        """
        Получение информации о сертификате
        :return: namedtuple с информацией о сертификате или None, если сертификат не удалось получить
        """
        hostname, port = self._ip, self._port
        HostInfo = namedtuple(field_names='cert hostname peername', typename='HostInfo')
        hostname_idna = idna.encode(hostname)
        try:
            with socket() as sock:
                sock.connect((hostname, port))
                peername = sock.getpeername()
                ctx = SSL.Context(SSL.SSLv23_METHOD)  # most compatible
                ctx.check_hostname = False
                ctx.verify_mode = SSL.VERIFY_NONE

                sock_ssl = SSL.Connection(ctx, sock)
                sock_ssl.set_connect_state()
                sock_ssl.set_tlsext_host_name(hostname_idna)
                sock_ssl.do_handshake()
                cert = sock_ssl.get_peer_certificate()
                crypto_cert = cert.to_cryptography()
                sock_ssl.close()
        except Exception as _:
            return None
            # raise NoSSLException("No SSL on {hostname}:{port}".format(hostname=hostname, port=port))

        return HostInfo(cert=crypto_cert, peername=peername, hostname=hostname)





def run_as_main():
    HOSTS = [
        ('yandex.ru', 443),
        ('projectvoid.play.ai', 443),
    ]
    ssl_checker = SSLChecker('5.255.255.77', 443)
    certificate = ssl_checker.get_certificate_info()
    print(certificate)


if __name__ == '__main__':
    run_as_main()
