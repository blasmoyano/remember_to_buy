class AppErrorBaseClass(Exception):
    def __init__(self, errors: list = None):
        self.errors = [] if errors is None else errors

    def errors(self):
        return self.errors


class RepositoryError(AppErrorBaseClass):
    def __init__(self, errors: list = None):
        super().__init__(errors)


class ServiceError(AppErrorBaseClass):
    def __init__(self, errors: list = None):
        super().__init__(errors)
