__author__ = 'salton'


from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.users.user import User
from src.models.messages.message import Message
from src.models.channels.channel import Channel
import src.models.messages.errors as MessageErrors



message_blueprint = Blueprint('messages', __name__)


@message_blueprint.route('messages/list/<string:cid>', methods=['GET'])
def list_message(cid):
    email = session['email']
    user_data = User.find_by_email(email)
    session['cid'] = cid
    channel_data = Channel.find_by_cid(cid)
    cname = channel_data.cname
    lists = Message.list_messages_by_uid_and_cid(user_data._id, cid)
    return render_template("messages/list.jinja2", lists=lists, unick=user_data.unick, cname=cname)


@message_blueprint.route('messages/new', methods=['GET', 'POST'])
def new_message():
    if request.method == 'POST':
        email = session['email']
        user_data = User.find_by_email(email)
        user_id = user_data._id
        cid = session['cid']
        mcontext = request.form.get('mcontext')
        try:
            if Message.new_message(user_id, cid, mcontext):
                print('New Message posted!')
                return redirect(url_for('.list_message', cid=cid))
        except MessageErrors.MessageError as e:
            return e.message
    cid = session['cid']
    return redirect(url_for('.list_message', cid=cid))
