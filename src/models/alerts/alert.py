import uuid
from src.common.database import Database
import src.models.alerts.constants as AlertConstants



class Alert(object):
    def __init__(self, user_email, _id=None):
        self.user_email = user_email
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Alert for {}>".format(self.user_email)

    def json(self):
        return {
            "_id": self._id,
            "user_email": self.user_email,
            "active": self.active
        }


