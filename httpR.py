class HttpRequest:
    def __init__(self, method, url, headers, body):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        headers_str = "\r\n".join([f"{k}: {v}" for k, v in self.headers.items()])
        request_line = f"{self.method} {self.url} HTTP/1.1\r\n"
        return f"{request_line}{headers_str}\r\n\r\n{self.body}".encode()

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> 'HttpRequest':
        data = binary_data.decode()
        headers_end = data.find("\r\n\r\n")
        headers = data[:headers_end].split("\r\n")
        method, url, _ = headers[0].split(" ")
        headers_dict = dict(line.split(": ", 1) for line in headers[1:])
        body = data[headers_end + 4:]
        return cls(method, url, headers_dict, body)

class HttpResponse:
    def __init__(self, status_code, headers, body):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        headers_str = "\r\n".join([f"{k}: {v}" for k, v in self.headers.items()])
        status_line = f"HTTP/1.1 {self.status_code}\r\n"
        return f"{status_line}{headers_str}\r\n\r\n{self.body}".encode()

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> 'HttpResponse':
        data = binary_data.decode()
        headers_end = data.find("\r\n\r\n")
        headers = data[:headers_end].split("\r\n")
        status_code = int(headers[0].split(" ")[1])
        headers_dict = dict(line.split(": ", 1) for line in headers[1:])
        body = data[headers_end + 4:]
        return cls(status_code, headers_dict, body)