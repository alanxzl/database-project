__author__ = 'salton'


class CinvitationError(Exception):
    def __init__(self, message):
        self.message = message


class InviteYourSelf(CinvitationError):
    pass


class UserAlreadyInChannel(CinvitationError):
    pass


class ChannelNotExistsError(CinvitationError):
    pass


class UserNotExistsError(CinvitationError):
    pass


class ChannelTypeError(CinvitationError):
    pass


class DirectChannelOverflow(CinvitationError):
    pass

