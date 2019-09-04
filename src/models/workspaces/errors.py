__author__ = 'Salton'


class WorkspaceError(Exception):
    def __init__(self, message):
        self.message = message


class WorkspaceExistsError(WorkspaceError):
    pass


class WorkspaceAlreadyExist(WorkspaceError):
    pass

class WorkspaceNotExistsError(WorkspaceError):
    pass