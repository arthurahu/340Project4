import dns.resolver


class IP_Lookup:
    def __init__(self):
        self.res = dns.resolver.Resolver(configure=False)
        self.nameservers = ["208.67.222.222", "1.1.1.1", "8.8.8.8", "8.26.56.26", "9.9.9.9", "64.6.65.6", "185.228.168.168", "77.88.8.7", "156.154.70.1", "176.103.130.130"]

    def ipv4(self, address):
        ips = []
        for ns in self.nameservers:
            self.res.nameservers = ns
            answers = self.res.resolve(address, "A", lifetime=2)
            for a in answers:
                ips.append(a)
        return ips

    def ipv6(self, address):
        ips = []
        for ns in self.nameservers:
            self.res.nameservers = ns
            answers = self.res.resolve(address, "AAAA", lifetime=2)
            for a in answers:
                ips.append(a)
        return ips

