__author__ = 'salton'

from src.common.database import Database
from src.models.users.user import User
from src.models.channels.channel import Channel
import src.models.messages.constants as MessageConstants
import src.models.messages.errors as MessageError



class Message(object):
    def __init__(self, cid, uid, mcontext, stamp, _id = None, unick = None):
        self.cid = cid
        self.uid = uid
        self.mcontext = mcontext
        self.stamp = stamp
        self._id = _id
        self.unick = unick

    def __repr__(self):
        return "<Message {}>".format(self._id)

    @classmethod
    def find_by_msid(cls, msid):
        sql = "select * from {} where msid = {}".format(MessageConstants.COLLECTION, msid)
        tup = Database.fetchone(sql)
        _id = tup[0]
        cid = tup[1]
        uid = tup[2]
        mcontext = tup[3]
        stamp = tup[4]
        user_data = User.find_by_uid(uid)
        return cls(cid, uid, mcontext, stamp, _id, user_data.unick)

    @staticmethod
    def list_messages_by_uid_and_cid(user_id, cid):
        # check whether the user is in the channel
        if not Channel.user_in_channel(user_id, cid):
            raise MessageError.UserNotPermittedError("You are not permitted for this Channel")
        sql = "select {} from {} where cid = {} order by stamp asc".format('msid', MessageConstants.COLLECTION, cid)
        tup = Database.fetchall(sql)
        print(tup)

        jsonlist = []
        for msid in tup:
            temp_message = Message.find_by_msid(msid[0])
            jsonlist.append(temp_message.json())
        return jsonlist

    @staticmethod
    def new_message(user_id, cid, mcontext):
        channel_data = Channel.find_by_cid(cid)
        if not channel_data:
            raise MessageError.ChannelNotExistsError("The Channel you trying to post message doesn't exist")
        user_data = User.find_by_uid(user_id)
        if not user_data:
            raise MessageError.UserNotExistError("The user trying to post message doesn't exist")
        # check whether the user is in the channel
        if not Channel.user_in_channel(user_id, cid):
            raise MessageError.UserNotPermittedError("you are not included in this channel")
        sql = "insert into {}(cid, uid, mcontext, stamp)values('{}', '{}', '{}', now())".format(
            MessageConstants.COLLECTION, cid, user_id, mcontext)
        Database.execute(sql)
        return True

    def json(self):
        return {
            "cid": self.cid,
            "uid": self.uid,
            "mcontext": self.mcontext,
            "stamp": self.stamp,
            "_id": self._id,
            "unick": self.unick
        }