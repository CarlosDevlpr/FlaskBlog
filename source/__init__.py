from flask import Flask  # usa-se o url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)  # Cria uma instância de Classe

app.config['SECRET_KEY'] = '83ff4782709a6f2fd8f827e5573f6d68'  # Criado um token pelo código do python: secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bancodedados.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_criarconta'
login_manager.login_message_category = 'alert-info'

from source import routes
