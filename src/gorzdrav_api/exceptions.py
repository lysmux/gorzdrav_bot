class GorZdravError(ConnectionError):
    def __init__(self, message: str) -> None:
        self.message = message


class ServerConnectionError(GorZdravError):
    def __str__(self) -> str:
        return f"Server returned message: {self.message}"


class ApiError(GorZdravError):
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        super().__init__(message)

    def __str__(self) -> str:
        return f"API returned {self.code} code, message: {self.message}"


class ResponseParseError(GorZdravError):
    def __str__(self):
        return f"Response parse error, message: {self.message}"
