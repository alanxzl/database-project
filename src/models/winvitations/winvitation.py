__author__ = 'salton'


from src.common.database import Database
from src.models.users.user import User
from src.common.utils import Utils
import src.models.winvitations.constants as WinvitatioinConstant
import src.models.winvitations.errors as WinvitationError


class Winvitation(object):
    def __init__(self, adminid, inviteid, wid, stamp, is_read=False, is_accpeted=False, wname=None, adminname=None, _id=None):
        self.adminid = adminid
        self.inviteid = inviteid
        self.wid = wid
        self.stamp = stamp
        self.is_read = is_read
        self.is_accepted = is_accpeted
        self.wname=wname
        self.adminname=adminname
        self._id = _id


    def __repr__(self):
        return "<Invitation from {} to {} in workspace {}>".format(self.adminid, self.inviteid, self.wid)

    @classmethod
    def find_by_winvid(cls, winvid):
        sql = "select * from {} where winvid = {}".format(WinvitatioinConstant.COLLECTION, winvid)
        tup = Database.fetchone(sql)
        _id = tup[0]
        adminid = tup[1]
        inviteid = tup[2]
        wid = tup[3]
        stamp = tup[4]
        is_read = tup[5]
        is_accepted = tup[6]
        # workspace name
        sql = "select wname from workspaces where wid = {}".format(wid)
        tup = Database.fetchone(sql)
        wname = tup[0]

        #invitatior name
        sql = "select uname from users where uid = {}".format(adminid)
        tup = Database.fetchone(sql)
        adminname = tup[0]
        return cls(adminid, inviteid, wid, stamp,is_read, is_accepted, wname, adminname, _id)

    @staticmethod
    def new_winvitation(adminid, inviteid, wid):
        # check if adminid == inviteid
        if adminid == inviteid:
            raise WinvitationError.InviteYourSelf("The user you invite shouldn't be yourself")

        # check if workspace exist
        sql = "select * from {} where wid='{}'".format(WinvitatioinConstant.WORKSPACE, wid)
        workspace_data = Database.fetchone(sql)
        if workspace_data is None:
            raise WinvitationError.WorkspaceNotExistsError("The workspace in this request doesn't exist")

        # check whether the user invited is already in the workspace
        sql = "select * from {} where wid='{}' and uid='{}'".format(WinvitatioinConstant.INCLUDE, wid, inviteid)
        invitation_data = Database.fetchone(sql)
        if invitation_data is not None:
            raise WinvitationError.UserAlreadyInWorkspace("The user you invite is already in the workspace")

        # check whether the user invited exist
        if not User.exist_user(inviteid):
            raise WinvitationError.UserNotExistsError("The user you are inviting doesn't exist")

        # update table : winvite
        sql = "insert into {}(adminid, inviteid, wid, stamp, is_read, is_accepted)values('{}', '{}', '{}',now(), {}, {})".format(
            WinvitatioinConstant.COLLECTION, adminid, inviteid, wid, 'False', 'False')
        Database.execute(sql)
        return True

    @staticmethod
    def read_invitation(winvid):
        sql = "update {} set is_read=True where winvid={}".format(WinvitatioinConstant.COLLECTION, winvid)
        Database.execute(sql)
        return True

    @staticmethod
    def accept_invitation(winvid):
        sql = "update {} set is_accepted=True where winvid={}".format(WinvitatioinConstant.COLLECTION, winvid)
        Database.execute(sql)
        sql = "select * from {} where {} = {}".format(WinvitatioinConstant.COLLECTION, "winvid", winvid)
        tup = Database.fetchone(sql)
        _id = tup[0]
        adminid = tup[1]
        inviteid = tup[2]
        wid = tup[3]
        stamp = tup[4]
        is_read = tup[5]
        is_accepted = tup[6]
        sql = "insert into {} (wid, uid) values ({}, {})".format(WinvitatioinConstant.INCLUDE, wid , inviteid)
        Database.execute(sql)
        return True

    @staticmethod
    def list_winvitation(user_id):
        sql = "select winvid from {} where inviteid = {} order by stamp desc".format(WinvitatioinConstant.COLLECTION, user_id)
        tup = Database.fetchall(sql)
        print(tup)

        jsonlist = []
        for winvid in tup:
            temp_winvitation = Winvitation.find_by_winvid(winvid[0])
            jsonlist.append(temp_winvitation.json())
        return jsonlist

    def json(self):
        return {
            "_id": self._id,
            "adminid": self.adminid,
            "inviteid":self.inviteid,
            "wid": self.wid,
            "stamp": self.stamp,
            "is_read": self.is_read,
            "is_accepted": self.is_accepted,
            "wname": self.wname,
            "adminname": self.adminname
        }




