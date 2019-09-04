__author__ = 'salton'


from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.users.user import User
from src.models.cinvitations.cinvitation import Cinvitation
import src.models.cinvitations.errors as CinvitationErrors
from src.models.channels.channel import Channel




cinvitation_blueprint = Blueprint('cinvitations', __name__)


@cinvitation_blueprint.route('cinvitations/accept/<string:cinvid>', methods=['GET'])
def accept_invitation(cinvid):
    Cinvitation.accept_invitation(cinvid)
    return render_template("cinvitations/accept.jinja2")

@cinvitation_blueprint.route('cinvitations/join/public/<string:cid>', methods=['GET'])
def join_public(cid):
    email = session['email']
    user_data = User.find_by_email(email)
    user_id = user_data._id
    try:
        if Cinvitation.join_public(user_id, cid):
            return redirect(url_for('message.list_messa', cid=cid))
    except CinvitationErrors.CinvitationError as e:
        return e.message
