__author__ = 'salton'

from src.common.database import Database
from src.models.users.user import User
from src.common.utils import Utils
import src.models.workspaces.constants as WorkspaceConstants
import src.models.workspaces.errors as WorkspaceError
import src.models.users.errors as UserError


class Workspace(object):
    def __init__(self, wname, wdescript, stamp, _id = None):
        self.wname = wname
        self.wdescript = wdescript
        self.stamp = stamp
        self._id = _id

    def __repr__(self):
        return "<Workspace {}>".format(self.wname)

    @classmethod
    def find_by_wname(cls, wname):
        sql = "select * from {} where wname = '{}'".format(WorkspaceConstants.COLLECTION, wname)
        tup = Database.fetchone(sql)
        _id = tup[0]
        wname = tup[1]
        wdescript = tup[2]
        stamp = tup[3]
        return cls(wname, wdescript, stamp, _id)

    @classmethod
    def find_by_wid(cls, wid):
        sql = "select * from {} where wid = {}".format(WorkspaceConstants.COLLECTION, wid)
        tup = Database.fetchone(sql)
        _id = tup[0]
        wname = tup[1]
        wdescript = tup[2]
        stamp = tup[3]
        return cls(wname, wdescript, stamp, _id)

    @staticmethod
    def list_workspaces(user_id):
        """
        :param user_id:
        :return:  a json include all information of workspaces
        """
        sql = "select {} from {} where uid = {}".format('wid', WorkspaceConstants.INCLUDE, user_id)
        tup = Database.fetchall(sql)
        print(tup)

        jsonlist = []
        for wid in tup:
            temp_workspace = Workspace.find_by_wid(wid[0])
            jsonlist.append(temp_workspace.json())
        return jsonlist

    @staticmethod
    def new_workspace(user_id, wname, wdescript):
        # update table : workspace
        sql = "select * from {} where wname='{}'".format(WorkspaceConstants.COLLECTION, wname)
        workspace_data = Database.fetchone(sql)

        if workspace_data is not None:
            raise WorkspaceError.WorkspaceAlreadyExist("The workspace exists.")
        sql = "insert into {}(wname, wdescript, stamp)values('{}', '{}', now())".format(
            WorkspaceConstants.COLLECTION, wname, wdescript)
        Database.execute(sql)
        # update table : admin
        sql = "select * from {} where wname='{}'".format(WorkspaceConstants.COLLECTION, wname)
        tup = Database.fetchone(sql)
        wid = tup[0]
        sql = "insert into {}(adminid, wid)values({}, {})".format(
            WorkspaceConstants.ADMINTABLE, user_id, wid)
        Database.execute(sql)
        # add admin into workspace
        sql = "insert into {}(wid, uid)values({}, {})".format(
            WorkspaceConstants.INCLUDE, wid, user_id)
        Database.execute(sql)
        return True

    @staticmethod
    def user_in_workspace(user_id, wid):
        """
        should detect whether wid or user id exist before judgement
        :param user_id: id of user
        :param wid: workspace id
        :return:  True if user is in the workspace
        """
        sql = "select * from {} where wid='{}' and uid='{}'".format(WorkspaceConstants.INCLUDE, wid, user_id)
        workspace_data = Database.fetchall(sql)
        if not Workspace.exist_workspace(wid):
            raise WorkspaceError.WorkspaceNotExistsError("The workspace you query doesn't exist")
        if len(workspace_data)==0:
            print("user {} not in workspace {}".format(user_id, wid))  # I/O could be deleted later
            return False
        else:
            print("user {} is in workspace {}".format(user_id, wid))  # I/O could be deleted later
            return True

    @staticmethod
    def is_admin_for_workspace(user_id, wid):
        sql = "select * from {} where wid='{}' and adminid='{}'".format(WorkspaceConstants.ADMINTABLE, wid, user_id)
        admin_data = Database.fetchall(sql)
        if len(admin_data)==0:
            return False
        else:
            return True

    @staticmethod
    def promote_user_to_admin(user_id, wid):
        """
        admin user promote a normal user to another admin
        :param user_id: the user id to be promoted
        :param wid: workspace id
        :return:
        """
        if not Workspace.exist_workspace(wid):
            raise WorkspaceError.WorkspaceNotExistsError("This workspace doesn't exists")
        if not User.exist_user(user_id):
            raise UserError.UserNotExistsError("The user you want to promote doesn't exists")

        # update the admintable
        sql = "insert into {}(adminid, wid)values('{}', '{}')".format(
            WorkspaceConstants.ADMINTABLE, user_id, wid)
        Database.execute(sql)
        return True

    @staticmethod
    def exist_workspace(wid):
        sql = "select * from {} where wid='{}'".format(WorkspaceConstants.COLLECTION, wid)
        workspace_data = Database.fetchone(sql)
        if not workspace_data:
            return False
        else:
            return True

    @staticmethod
    def invitation_for_workspace(from_id, to_id, wid):
        pass

    def json(self):
        return {
            "_id": self._id,
            "wname": self.wname,
            "wdescript":self.wdescript,
            "stamp": self.stamp
        }