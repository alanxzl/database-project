__author__ = 'salton'
from src.common.database import Database
from flask import Flask, render_template




app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = "123"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.jinja2')


from src.models.users.views import user_blueprint
from src.models.workspaces.views import workspace_blueprint
from src.models.channels.views import channel_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(workspace_blueprint, url_prefix="/workspaces")
app.register_blueprint(channel_blueprint, url_prefix="/channels")

from src.models.winvitations.views import winvitation_blueprint
app.register_blueprint(winvitation_blueprint, url_prefix="/winvitations")

from src.models.cinvitations.views import cinvitation_blueprint
app.register_blueprint(cinvitation_blueprint, url_prefix="/cinvitations")

from src.models.messages.views import message_blueprint
app.register_blueprint(message_blueprint, url_prefix="/messages")


