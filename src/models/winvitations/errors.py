__author__ = 'Salton'


class WinvitationError(Exception):
    def __init__(self, message):
        self.message = message


class InviteYourSelf(WinvitationError):
    pass


class UserAlreadyInWorkspace(WinvitationError):
    pass


class WorkspaceNotExistsError(WinvitationError):
    pass


class UserNotExistsError(WinvitationError):
    pass
