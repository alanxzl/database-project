__author__ = 'salton'


from src.common.database import Database
from src.models.users.user import User
from src.models.channels.channel import Channel
import src.models.cinvitations.constants as CinvitatioinConstant
import src.models.cinvitations.errors as CinvitationError


class Cinvitation(object):
    def __init__(self, adminid, inviteid, cid, stamp, is_read=False, is_accpeted=False, cname=None, adminname=None, _id=None):
        self.adminid = adminid
        self.inviteid = inviteid
        self.cid = cid
        self.stamp = stamp
        self.is_read = is_read
        self.is_accepted = is_accpeted
        self.cname=cname
        self.adminname=adminname
        self._id = _id


    def __repr__(self):
        return "<Invitation from {} to {} in channel {}>".format(self.adminid, self.inviteid, self.cid)

    @classmethod
    def find_by_cinvid(cls, cinvid):
        sql = "select * from {} where cinvid = {}".format(CinvitatioinConstant.COLLECTION, cinvid)
        tup = Database.fetchone(sql)
        _id = tup[0]
        adminid = tup[1]
        inviteid = tup[2]
        cid = tup[3]
        stamp = tup[4]
        is_read = tup[5]
        is_accepted = tup[6]
        # workspace name
        sql = "select cname from {} where cid = {}".format(CinvitatioinConstant.CHANNELS, cid)
        tup = Database.fetchone(sql)
        cname = tup[0]

        #invitatior name
        sql = "select uname from users where uid = {}".format(adminid)
        tup = Database.fetchone(sql)
        adminname = tup[0]
        return cls(adminid, inviteid, cid, stamp,is_read, is_accepted, cname, adminname, _id)

    @staticmethod
    def new_cinvitation(adminid, inviteid, cid):
        # check if adminid == inviteid
        if adminid == inviteid:
            raise CinvitationError.InviteYourSelf("The user you invite shouldn't be yourself")

        # check if channel exist
        sql = "select * from {} where cid='{}'".format(CinvitatioinConstant.CHANNELS, cid)
        channel_data = Database.fetchone(sql)
        if channel_data is None:
            raise CinvitationError.ChannelNotExistsError("The channel in this request doesn't exist")

        # check whether the user invited is already in the workspace
        sql = "select * from {} where cid='{}' and uid='{}'".format(CinvitatioinConstant.INCLUDE, cid, inviteid)
        invitation_data = Database.fetchone(sql)
        if invitation_data is not None:
            raise CinvitationError.UserAlreadyInChannel("The user you invite is already in the channel")

        # check whether the user invited exist
        if not User.exist_user(inviteid):
            raise CinvitationError.UserNotExistsError("The user you are inviting doesn't exist")

        # update table : cinvite
        sql = "insert into {}(adminid, inviteid, cid, stamp, is_read, is_accepted)values('{}', '{}', '{}',now(), {}, {})".format(
            CinvitatioinConstant.COLLECTION, adminid, inviteid, cid, 'False', 'False')
        Database.execute(sql)
        return True

    @staticmethod
    def read_invitation(cinvid):
        sql = "update {} set is_read=True where cinvid={}".format(CinvitatioinConstant.COLLECTION, cinvid)
        Database.execute(sql)
        return True

    @staticmethod
    def accept_invitation(cinvid):
        sql = "update {} set is_accepted=True where cinvid={}".format(CinvitatioinConstant.COLLECTION, cinvid)
        Database.execute(sql)
        sql = "select * from {} where {} = {}".format(CinvitatioinConstant.COLLECTION, "cinvid", cinvid)
        tup = Database.fetchone(sql)
        _id = tup[0]
        adminid = tup[1]
        inviteid = tup[2]
        cid = tup[3]
        stamp = tup[4]
        is_read = tup[5]
        is_accepted = tup[6]
        sql = "insert into {} (cid, uid) values ({}, {})".format(CinvitatioinConstant.INCLUDE, cid , inviteid)
        Database.execute(sql)
        return True

    @staticmethod
    def list_cinvitation(user_id):
        sql = "select cinvid from {} where inviteid = {} order by stamp desc".format(CinvitatioinConstant.COLLECTION, user_id)
        tup = Database.fetchall(sql)
        print(tup)

        jsonlist = []
        for cinvid in tup:
            temp_cinvitation = Cinvitation.find_by_cinvid(cinvid[0])
            jsonlist.append(temp_cinvitation.json())
        return jsonlist

    @staticmethod
    def invite_for_private(adminid, inviteid, cid):
        # check if channel exist
        sql = "select * from {} where cid='{}'".format(CinvitatioinConstant.CHANNELS, cid)
        channel_data = Database.fetchone(sql)
        if channel_data is None:
            raise CinvitationError.ChannelNotExistsError("The channel in this request doesn't exist")
        # check the type of channel
        sql = "select {} from {} where {} = {}".format('ctype', CinvitatioinConstant.CHANNELS, 'cid', cid)
        tup = Database.fetchone(sql)
        if tup[0] != 1:
            raise CinvitationError.ChannelTypeError("Channel with id {} is not a private channel".format(cid))
        Cinvitation.new_cinvitation(adminid, inviteid, cid)
        return True

    @staticmethod
    def invite_for_direct(adminid, inviteid, cid):
        # check if channel exist
        sql = "select * from {} where cid='{}'".format(CinvitatioinConstant.CHANNELS, cid)
        channel_data = Database.fetchone(sql)
        if channel_data is None:
            raise CinvitationError.ChannelNotExistsError("The channel in this request doesn't exist")

        # check if the channel is type: direct
        ctype = channel_data[4]
        if ctype != 2:
            raise CinvitationError.ChannelTypeError("Channel with id {} is not a direct channel".format(cid))

        # check whether th channel is full
        sql = "select count(uid) from {} where cid={}".format(CinvitatioinConstant.INCLUDE, cid)
        include_data = Database.fetchone(sql)
        count_user = include_data[0]
        if count_user >= 2:
            raise CinvitationError.DirectChannelOverflow("The direct channel in your invitation is full")
        Cinvitation.new_cinvitation(adminid, inviteid, cid)
        return True

    @staticmethod
    def join_public(user_id, cid):
        # check whether the channel exist
        sql = "select * from {} where {} = {}".format(CinvitatioinConstant.CHANNELS, "cid", cid)
        channel_data = Database.fetchone(sql)
        if channel_data is None:
            raise CinvitationError.ChannelNotExistsError("The channel you requested doesn't exist")
        # check whether the channel is public
        ctype = channel_data[4]
        if ctype != 0:
            raise CinvitationError.ChannelTypeError("The channel you are joining is not a public channel")
        # check whether the user is already in the channel
        if Channel.user_in_channel(user_id, cid):
            raise CinvitationError.UserAlreadyInChannel("You are already in the channel")
        # update the table: cinclude
        sql = "insert into {} (cid, uid) values ({}, {})".format(CinvitatioinConstant.INCLUDE, cid, user_id)
        Database.execute(sql)
        return True

    def json(self):
        return {
            "_id": self._id,
            "adminid": self.adminid,
            "inviteid":self.inviteid,
            "cid": self.cid,
            "stamp": self.stamp,
            "is_read": self.is_read,
            "is_accepted": self.is_accepted,
            "cname": self.cname,
            "adminname": self.adminname
        }
