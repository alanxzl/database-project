__author__ = 'salton'
# Thanks layoutit.com

from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.users.user import User
from src.models.winvitations.winvitation import Winvitation
import src.models.winvitations.errors as WinvitationErrors
from src.models.cinvitations.cinvitation import Cinvitation
import src.models.cinvitations.errors as CinvitationErrors



winvitation_blueprint = Blueprint('winvitations', __name__)


@winvitation_blueprint.route('/winvitation/create', methods=['GET', 'POST'])
def create_winvitation():
    if request.method == 'POST':
        user = User.find_by_email(session['email'])
        adminid = user._id
        inviteid = request.form.get('inviteid')
        wid = session['wid']
        try:
            if Winvitation.new_winvitation(adminid, inviteid, wid):
                return redirect(url_for(".invite_send"))
        except WinvitationErrors.WinvitationError as e:
            return e.message
    return render_template("winvitations/create.jinja2")


@winvitation_blueprint.route('/winvitation/success', methods=['GET'])
def invite_send():
    return render_template("winvitations/success.jinja2")


@winvitation_blueprint.route('/winvitation/list', methods=['GET'])
def list_winvitation():
    email = session["email"]
    user = User.find_by_email(email)
    lists = Winvitation.list_winvitation(user._id)
    clists = Cinvitation.list_cinvitation(user._id)

    return render_template("winvitations/list.jinja2", lists=lists, clists=clists, unick=user.unick)


@winvitation_blueprint.route('winvitations/accept/<string:winvid>', methods=['GET'])
def accept_invitation(winvid):
    Winvitation.accept_invitation(winvid)
    return render_template("winvitations/accept.jinja2")

