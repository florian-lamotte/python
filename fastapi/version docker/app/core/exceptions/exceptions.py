class AppException(Exception):
    """ Personnalisation des erreurs """
    
    def __init__(
        self,
        message: str = "An application error occurred",
        status_code: int = 500,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundException(AppException):
    def __init__(
        self, 
        message="Resource not found"
    ) -> None:
        super().__init__(message, 404)

class ValidationException(AppException):
    def __init__(
        self, 
        message="Invalid data"
    ) -> None:
        super().__init__(message, 400)

class UnauthorizedException(AppException):
    def __init__(
        self,
        message: str = "Authentication required",
    ) -> None:
        super().__init__(message, 401)

class ForbiddenException(AppException):
    def __init__(
        self,
        message: str = "Access forbidden",
    ) -> None:
        super().__init__(message, 403)

class ConflictException(AppException):
    def __init__(
        self,
        message: str = "Resource conflict",
    ) -> None:
        super().__init__(message, 409)