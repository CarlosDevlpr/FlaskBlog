from source import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)  # primary_key define o usuário como único
    username = database.Column(database.String, nullable=False)  # nullable serve para não ser vazio
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    profile_pic = database.Column(database.String, default='default.jpg', nullable=False)
    posts = database.relationship('Post', backref='author', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='Não informado')

    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String, nullable=False)
    body = database.Column(database.Text, nullable=False)
    creation_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    user_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
