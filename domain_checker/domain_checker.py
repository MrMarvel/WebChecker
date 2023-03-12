from nslookup import Nslookup




class DomainChecker:
    """
    Класс адаптер для работы с nslookup
    """

    def __init__(self, dns_servers: list[str] = None):
        if dns_servers is None:
            dns_servers = ['1.1.1.1']
        self._dns_query = Nslookup(dns_servers=dns_servers, verbose=True)

    def dns_lookup(self, domain: str) -> list[str]:
        ips_record = self._dns_query.dns_lookup(domain)
        ips = [str(x) for x in ips_record.answer]
        return ips

    def get_first_ip_from_domain(self, domain: str) -> str | None:
        ips = self.dns_lookup(domain)
        if len(ips) > 0:
            return ips[0]
        return None


if __name__ == '__main__':
    d = DomainChecker()
    d.dns_lookup('yaasdassdasdasddsd.ru')
