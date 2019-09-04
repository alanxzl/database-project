__author__ = 'salton'

from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.users.user import User
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators


user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for(".login_success"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/login.jinja2")  # Send the user an error if their login was invalid


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        uname = request.form['uname']
        unick = request.form['unick']

        try:
            if User.register_user(email, password, uname, unick):
                session['email'] = email
                return redirect(url_for(".login_success"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/register.jinja2")  # Send the user an error if their login was invalid

@user_blueprint.route('/user_center')
@user_decorators.requires_login
def login_success():
    user = User.find_by_email(session['email'])
    return render_template("users/login_success.jinja2", email=session['email'], unick=user.unick, user_id = user._id)


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))


@user_blueprint.route('/personal/center')
def personal_center():
    user = User.find_by_email(session['email'])
    return render_template("users/login_success.jinja2", email=session['email'], unick=user.unick, user_id = user._id)

