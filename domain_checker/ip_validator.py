import socket


def is_valid_ipv4_address(address):
    """
    Проверяет, является ли строка валидным IPv4 адресом
    :param address: Строка с адресом
    :return: True, если адрес валидный, иначе False
    """
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


def is_valid_ipv6_address(address):
    """
    Проверяет, является ли строка валидным IPv6 адресом
    :param address: Строка с адресом
    :return: True, если адрес валидный, иначе False
    """
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True
