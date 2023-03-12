import requests
import socket


class ServerInfo:
    def __init__(self, address):
        self.name = address
        self.url = "http://" + address
        try:
            self.r = requests.get(self.url, timeout=2, allow_redirects=False)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            self.r = None

    def server_type(self):
        if self.r is None:
            return None
        try:
            return self.r.headers["server"]
        except KeyError:
            return None

    def insecure(self):
        if self.r is None:
            return False
        try:
            ip_address = socket.gethostbyname(self.name)
            with socket.create_connection((ip_address, 80), timeout=2) as sock:
                return True

        except (socket.timeout, ConnectionRefusedError, requests.exceptions.ConnectionError):
            return False

    def redirect_to_https(self):
        if self.r is None:
            return False
        redirects = 0
        while redirects < 10:
            if self.r.status_code in [301, 302]:
                self.url = self.r.headers["Location"]
                if self.url.startswith("https://"):
                    try:
                        self.r = requests.get(self.url, timeout=2)
                        return True
                    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                        self.r = None
                        return False
                self.r = requests.get(self.url, timeout=2, allow_redirects=False)
                redirects += 1
            return False
        return False

            # if self.r.status_code // 100 != 3:
            #     return False
            # if self.url.startswith("https://"):
            #     return True
            # self.url = self.r.headers["Location"]
            # try:
            #     self.r = requests.get(f"http://{self.url}", allow_redirects=False, timeout=2)
            #     redirects += 1
            # except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            #     return False

        return False

    def hsts(self):
        if self.r is None:
            return False
        return "Strict-Transport-Security" in self.r.headers

    def tls_versions(self):
        if self.r is None:
            return []
        return []

    def root_ca(self):
        if self.r is None:
            return ""
        return ""
