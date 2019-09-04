__author__ = 'Salton'


class MessageError(Exception):
    def __init__(self, message):
        self.message = message


class ChannelNotExistsError(MessageError):
    pass


class UserNotPermittedError(MessageError):
    pass


class UserNotExistError(MessageError):
    pass




