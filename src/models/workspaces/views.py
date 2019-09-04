__author__ = 'salton'

from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.users.user import User
from src.models.workspaces.workspace import Workspace
import src.models.workspaces.errors as WorkspaceErrors


workspace_blueprint = Blueprint('workspaces', __name__)


@workspace_blueprint.route('/workspace/create', methods=['GET', 'POST'])
def create_workspace():
    if request.method == 'POST':
        user = User.find_by_email(session['email'])
        wname = request.form.get('wname')
        print(wname)
        wdescript = request.form.get('wdescript')
        print(wdescript)
        try:
            if Workspace.new_workspace(user._id, wname, wdescript):
                print("Created!")
                return redirect(url_for(".workspace_list"))
        except WorkspaceErrors.WorkspaceError as e:
            return e.message

    return render_template("workspaces/create.jinja2")


@workspace_blueprint.route('/workspace_list', methods=['GET'])
def workspace_list():
    email = session["email"]
    user = User.find_by_email(email)
    lists = Workspace.list_workspaces(user._id)

    return render_template("workspaces/list.jinja2", lists = lists, unick=user.unick)
