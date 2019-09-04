__author__ = 'salton'

from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.users.user import User
from src.models.workspaces.workspace import Workspace
from src.models.channels.channel import Channel
import src.models.channels.errors as ChannelErrors

channel_blueprint = Blueprint('channels', __name__)


@channel_blueprint.route('/channel/create', methods=['GET', 'POST'])
def create_channel():
    if request.method == 'POST':
        user = User.find_by_email(session['email'])
        cname = request.form.get('cname')
        print(cname)
        cdescript = request.form.get('cdescript')
        print(cdescript)
        ctype = int(request.form.get('ctype'))
        print(ctype)
        wid = session['wid']
        try:
            if Channel.new_channel(user._id, cname, cdescript, ctype, wid):
                print("New channel created!")
                return redirect(url_for(".channel_list_by_wid_and_uid", wid=wid))
        except ChannelErrors.ChannelError as e:
            return e.message

    return render_template("channels/create.jinja2")


@channel_blueprint.route('/channel/list_by_uid', methods=['GET'])
def channel_list_by_uid():
    email = session["email"]
    user = User.find_by_email(email)
    lists = Channel.list_channels_by_uid(user._id)

    return render_template("channels/list_by_uid.jinja2", lists=lists, unick=user.unick)


@channel_blueprint.route('/channel/list_by_wid_and_uid/<string:wid>', methods=['GET'])
def channel_list_by_wid_and_uid(wid):

    session['wid']=wid
    email = session["email"]
    workspace_id = wid
    workspace = Workspace.find_by_wid(wid)
    user = User.find_by_email(email)
    public_list = Channel.list_public_channels_by__wid(wid)
    private_list = Channel.list_channels_by_uid_and_wid(user._id, workspace_id, 1)
    direct_list = Channel.list_channels_by_uid_and_wid(user._id, workspace_id, 2)

    return render_template("channels/list_by_wid_and_uid.jinja2", public_list=public_list,
                           private_list=private_list, direct_list=direct_list, unick=user.unick, wname=workspace.wname)

