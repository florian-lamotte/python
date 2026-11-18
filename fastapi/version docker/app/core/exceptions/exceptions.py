from http import HTTPStatus

class AppException(Exception):
    """ Classe de base des erreurs """

    def __init__(
        self,
        message: str = "An application error occurred",
        status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
    ) -> None:
        self.message = message
        self.status_code = status_code
        
        super().__init__(message)

class BadRequestException(AppException):
    def __init__(self, message: str = "Invalid data") -> None:
        super().__init__(message, HTTPStatus.BAD_REQUEST)

class UnauthorizedException(AppException):
    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(message, HTTPStatus.UNAUTHORIZED)

class ForbiddenException(AppException):
    def __init__(self, message: str = "Access forbidden") -> None:
        super().__init__(message, HTTPStatus.FORBIDDEN)

class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, HTTPStatus.NOT_FOUND)

class MethodNotAllowedException(AppException):
    def __init__(self, message: str = "Method not allowed") -> None:
        super().__init__(message, HTTPStatus.METHOD_NOT_ALLOWED)

class ConflictException(AppException):
    def __init__(self, message: str = "Resource conflict") -> None:
        super().__init__(message, HTTPStatus.CONFLICT)

class UnprocessableEntityException(AppException):
    def __init__(self, message: str = "Unable to process request") -> None:
        super().__init__(message, HTTPStatus.UNPROCESSABLE_ENTITY)

class TooManyRequestsException(AppException):
    def __init__(self, message: str = "Too many requests") -> None:
        super().__init__(message, HTTPStatus.TOO_MANY_REQUESTS)

class InternalServerException(AppException):
    def __init__(self, message: str = "Internal server error") -> None:
        super().__init__(message, HTTPStatus.INTERNAL_SERVER_ERROR)

class ServiceUnavailableException(AppException):
    def __init__(self, message: str = "Service temporarily unavailable") -> None:
        super().__init__(message, HTTPStatus.SERVICE_UNAVAILABLE)