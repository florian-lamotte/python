class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 500,
    ):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)


class ValidationException(AppException):
    def __init__(self, message="Invalid data"):
        super().__init__(message, 400)