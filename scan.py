import sys
import json
import time
from scanners import ip_addresses


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
                self.scan(address.strip())

        with open(file_out, "w") as f:
            json.dump(self.out, f, sort_keys=True, indent=4)

        return

    def scan(self, address):
        self.out[address] = {}

        self.out[address]["scan_time"] = time.time()

        dns = ip_addresses.IP_Lookup()
        self.out[address]["ipv4_addresses"] = dns.ipv4(address)
        self.out[address]["ipv6_addresses"] = dns.ipv6(address)

        return


if __name__ == '__main__':
    Scan()
