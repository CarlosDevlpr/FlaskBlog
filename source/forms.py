from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from source.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):  # Criado a lógica de funcionamento do formulário CriarConta
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Seu melhor e-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirm_password = PasswordField('Confirme a senha', validators=[DataRequired(), EqualTo('password')])
    submit_criarconta = SubmitField('Criar conta')

    def validate_email(self, email):  # OBRIGATORIAMENTE a função tem que começar com 'validate_' pois é assim que o validate_on_submit() no routes.py valida a lógica.
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastra-se com outro e-mail ou faça login para continuar.')


class FormLogin(FlaskForm):  # Criado a lógica de funcionamento do formulário Login
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar dados')
    submit_login = SubmitField('Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    profile_pic = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit_editarperfil = SubmitField('Salvar Alterações')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com este e-mail. Cadastre outro e-mail.')


class FormCriarPost(FlaskForm):
    title = StringField('Título do Post:', validators=[DataRequired(), Length(2, 140)])
    body = TextAreaField('Escreva seu Post aqui:', validators=[DataRequired()])
    submit_criarpost = SubmitField('Criar Post')
