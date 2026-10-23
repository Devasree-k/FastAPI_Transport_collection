# Base exception for application-specific errors with an HTTP status code.

class AppException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code


class NotFoundException(AppException):
    def __init__(self, message: str):
        super().__init__(message, 404)

# Represents invalid input or a request that cannot be processed.
class BadRequestException(AppException):
    def __init__(self, message: str):
        super().__init__(message, 400)

# To check duplicate phone number 
class ConflictException(AppException):
    def __init__(self, message: str):
        super().__init__(message, 409)
