__author__ = 'salton'

from src.common.database import Database
from src.common.utils import Utils
from src.models.users.user import User
from src.models.workspaces.workspace import Workspace
import src.models.channels.constants as ChannelConstants
import src.models.channels.errors as ChannelError
import src.models.users.errors as UserError
import src.models.workspaces.errors as WorkspaceError

class Channel(object):
    def __init__(self, cname, cdescript, wid, ctype, creatorid, stamp, _id = None):
        self.cname = cname
        self.cdescript = cdescript
        self.wid = wid
        self.ctype = ctype
        self.creatorid = creatorid
        self.stamp = stamp
        self._id = _id

    """
    ctype:{0:public} {1:private} {2:direct}
    """

    def __repr__(self):
        return "<Channel {}, Type: {}>".format(self.cname, self.ctype)

    @classmethod
    def find_by_cid(cls, cid):
        if not Channel.exist_channel(cid):
            raise ChannelError.ChannelNotExistsError("This Channel doesn't exist")
        sql = "select * from {} where cid = {}".format(ChannelConstants.COLLECTION, cid)
        tup = Database.fetchone(sql)
        _id = tup[0]
        cname = tup[1]
        cdescript = tup[2]
        wid = tup[3]
        ctype = tup[4]
        creatorid = tup[5]
        stamp = tup[6]
        return cls(cname, cdescript, wid, ctype, creatorid, stamp, _id)

    @staticmethod
    def list_channels_by_wid(wid):
        sql = "select {} from {} where wid = {}".format('cid', ChannelConstants.COLLECTION, wid)
        tup = Database.fetchall(sql)
        print(tup)

        jsonlist = []
        for cid in tup:
            temp_channel = Channel.find_by_cid(cid[0])
            jsonlist.append(temp_channel.json())
        return jsonlist

    @staticmethod
    def list_channels_by_uid(user_id):
        sql = "select {} from {} where uid = {}".format('cid', ChannelConstants.INCLUDE, user_id)
        tup = Database.fetchall(sql)
        jsonlist = []
        for cid in tup:
            temp_channel = Channel.find_by_cid(cid[0])
            jsonlist.append(temp_channel.json())
        return jsonlist

    @staticmethod
    def list_channels_by_uid_and_wid(user_id, wid, ctype):
        """

        :param user_id:  user id
        :param wid: wid
        :param ctype: 0-public, 1-private, 2-direct
        :return: public channels
        """
        sql = "select cid from {} natural join {} where uid='{}' and wid='{}' and ctype='{}'".format(
            ChannelConstants.COLLECTION, ChannelConstants.INCLUDE, user_id, wid, ctype)
        tup = Database.fetchall(sql)
        jsonlist = []
        for cid in tup:
            temp_channel = Channel.find_by_cid(cid[0])
            jsonlist.append(temp_channel.json())
        return jsonlist

    @staticmethod
    def list_public_channels_by__wid(wid):
        """

        :param user_id:  user id
        :param wid: wid
        :param ctype: 0-public, 1-private, 2-direct
        :return: public channels
        """
        sql = "select cid from {} where wid='{}' and ctype='{}'".format(
            ChannelConstants.COLLECTION, wid, 0)
        tup = Database.fetchall(sql)
        jsonlist = []
        for cid in tup:
            temp_channel = Channel.find_by_cid(cid[0])
            jsonlist.append(temp_channel.json())
        return jsonlist

    @staticmethod
    def exist_channel(cid):
        sql = "select * from {} where cid='{}'".format(ChannelConstants.COLLECTION, cid)
        channel_data = Database.fetchone(sql)
        if not channel_data:
            return False
        else:
            return True

    @staticmethod
    def new_channel(user_id, cname, cdescript, ctype, wid):
        if not User.exist_user(user_id):
            raise UserError.UserNotExistsError("The admin_id doesn't exist")
        if not Workspace.exist_workspace(wid):
            raise WorkspaceError.WorkspaceNotExistsError("The workspace you want to created channel in doesn't exist")
        if ctype < 0 or ctype > 2:
            raise ChannelError.ChannelTypeError("The Channel Type from your input is invalid")
        if len(cname) > 50:
            raise ChannelError.InputTooLongError("The input of channel name is too long")
        if len(cdescript) > 100:
            raise ChannelError.InputTooLongError("The input of channel description is too long")

        sql = "select * from {} where cname='{}' and wid='{}'".format(ChannelConstants.COLLECTION, cname, wid)
        channel_data = Database.fetchone(sql)

        if channel_data is not None:
            raise ChannelError.ChannelAlreadyExist("The channel exists.")
        sql = "insert into {}(cname, cdescript, wid, ctype, creatorid, stamp)values('{}', '{}', '{}', '{}', '{}', now())".format(
            ChannelConstants.COLLECTION, cname, cdescript, wid, ctype, user_id)
        Database.execute(sql)

        # add creator into channel
        sql = "select * from {} where cname='{}' and wid='{}'".format(ChannelConstants.COLLECTION, cname, wid)
        tup = Database.fetchone(sql)
        cid = tup[0]
        sql = "insert into {}(cid, uid)values({}, {})".format(
            ChannelConstants.INCLUDE, cid, user_id)
        Database.execute(sql)
        return True

    @staticmethod
    def user_in_channel(user_id, cid):
        """
        should detect whether wid or user id exist before judgement
        :param user_id: id of user
        :param cid: channel id
        :return:  True if user is in the workspace
        """
        sql = "select * from {} where cid='{}' and uid='{}'".format(ChannelConstants.INCLUDE, cid, user_id)
        channel_data = Database.fetchall(sql)
        if not Channel.exist_channel(cid):
            raise ChannelError.ChannelNotExistsError("Channel doesn't exist")
        if len(channel_data) == 0:
            print("user {} not in channel {}".format(user_id, cid))  # I/O could be deleted later
            return False
        else:
            print("user {} is in channel {}".format(user_id, cid))  # I/O could be deleted later
            return True

    @staticmethod
    def invitation_for_private_channel(from_id, to_id, cid):
        pass

    @staticmethod
    def join_for_public_channel(user_id, cid):
        pass

    @staticmethod
    def build_a_direct_channel(user_id_1, user_id_2, cid):
        pass

    @staticmethod
    def delete_user_from_channel(user_id, user_to_delete_id, cid):
        pass

    def json(self):
        return {
            "_id": self._id,
            "cname": self.cname,
            "cdescript":self.cdescript,
            "wid": self.wid,
            "ctype": self.ctype,
            "creatorid": self.creatorid,
            "stamp": self.stamp
        }
