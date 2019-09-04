__author__ = 'Salton'


class ChannelError(Exception):
    def __init__(self, message):
        self.message = message


class ChannelExistsError(ChannelError):
    pass


class ChannelAlreadyExist(ChannelError):
    pass


class ChannelNotExistsError(ChannelError):
    pass


class ChannelTypeError(ChannelError):
    pass


class InputTooLongError(ChannelError):
    pass
