__author__ = 'salton'
# test script for some API

import pymysql
from src.common.database import Database
#from src.models.users.user import User
from src.models.workspaces.workspace import Workspace
from src.models.channels.channel import Channel
#import src.models.workspaces.constants as WorkspaceConstants
from src.models.winvitations.winvitation import Winvitation
from src.models.cinvitations.cinvitation import Cinvitation
from src.models.messages.message import Message
Database.initialize()


message_data = Message.list_messages_by_uid_and_cid(1,4)
print(message_data[0])


#print(user_data)
#data = Channel.list_channels_by_uid(6)


Database.close()






