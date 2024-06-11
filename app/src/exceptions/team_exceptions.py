class TeamServiceError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class TeamCreationError(TeamServiceError):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, status_code)
