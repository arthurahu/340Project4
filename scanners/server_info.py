import requests
import socket
import ssl
import nmap


class ServerInfo:
    def __init__(self, address):
        self.name = address
        self.url = "http://" + address
        self.secure = False
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
                        self.secure = True
                        return self.secure
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
        if self.r is None or self.secure is False:
            return []

        versions = []

        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_SSLv3
        try:
            with socket.create_connection((self.name, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=self.name) as ssock:
                    versions.append("TLSv1.3")
        except ssl.SSLError:
            pass

        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_SSLv2
        try:
            with socket.create_connection((self.name, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=self.name) as ssock:
                    versions.append("TLSv1.3")
        except ssl.SSLError:
            pass

        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2
        try:
            with socket.create_connection((self.name, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=self.name) as ssock:
                    versions.append("TLSv1.3")
        except ssl.SSLError:
            pass

        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_3
        try:
            with socket.create_connection((self.name, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=self.name) as ssock:
                    versions.append("TLSv1.2")
        except ssl.SSLError:
            pass

        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_TLSv1_3
        try:
            with socket.create_connection((self.name, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=self.name) as ssock:
                    versions.append("TLSv1.1")
        except ssl.SSLError:
            pass

        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.options |= ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_TLSv1_3
        try:
            with socket.create_connection((self.name, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=self.name) as ssock:
                    versions.append("TLSv1")
        except ssl.SSLError:
            pass

        return versions

    def root_ca(self):
        if self.r is None or self.secure is False:
            return ""
        context = ssl.create_default_context()
        with socket.create_connection((self.name, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=self.name) as sslsock:
                cert = sslsock.getpeercert()
        return cert['issuer'][1][0][1]
