class GorZdravError(Exception):
    pass


class ServerError(GorZdravError):
    def __init__(self, message, code=None):
        self.message = message
        self.code = code

    def __str__(self):
        return f"Server returned {self.code}, message: {self.message}"


class ApiError(GorZdravError):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f"API returned {self.code} code, message: {self.message}"


class ResponseParseError(GorZdravError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"Response parse error, message: {self.message}"
