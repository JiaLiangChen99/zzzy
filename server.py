import dash
import dash_bootstrap_components as dbc
from flask_login import UserMixin, LoginManager

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions = True
    )

server = app.server

server.secret_key = 'dasdaszjkljkjisadshndklajdlj'

#绑定应用
login_manage = LoginManager()
login_manage.init_app(server)

class User(UserMixin):
    pass

@login_manage.user_loader
def load_user(username):
    new_user = User()
    new_user.id = username
    return new_user