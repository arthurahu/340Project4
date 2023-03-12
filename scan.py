import sys
import json
import time
from scanners import dns_lookup, server_info


class Scan:

    def __init__(self):
        if len(sys.argv) != 3:
            sys.stderr.write("number of args")
            return -1

        file_in = sys.argv[1]
        file_out = sys.argv[2]

        self.out = {}

        with open(file_in, "r") as f:
            for address in f:
                if address[0] == "#":
                    continue
                self.scan(address.strip())

        with open(file_out, "w") as f:
            json.dump(self.out, f, sort_keys=True, indent=4)

        return

    def scan(self, address):
        self.out[address] = {}

        self.out[address]["scan_time"] = time.time()

        dns = dns_lookup.DNSLookup()
        self.out[address]["ipv4_addresses"] = dns.ipv4(address)
        self.out[address]["ipv6_addresses"] = dns.ipv6(address)

        server = server_info.ServerInfo(address)

        self.out[address]["http_server"] = server.server_type()
        self.out[address]["insecure_http"] = server.insecure()
        self.out[address]["redirect_to_https"] = server.redirect_to_https()
        self.out[address]["hsts"] = server.hsts()
        self.out[address]["tls_versions"] = server.tls_versions()
        self.out[address]["root_ca"] = server.root_ca()

        return


if __name__ == '__main__':
    Scan()
