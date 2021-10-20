from flask import render_template, redirect, request, url_for, flash, abort
from source import app, database, bcrypt
from source.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from source.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image  # Biblioteca para reduzir tamanho de imagens


@app.route('/')  # Decorator para definir a rota da página
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)  # Ele chama uma página HTML. CHAMAR SEMPRE ENTRE ASPAS!!!


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login_criarconta():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'submit_login' in request.form:  # Confirma se o botão que ele apertou é o de login
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()  # O usuário recebe o e-mail que ele acabou de digitar no campo do email no login
        if usuario and bcrypt.check_password_hash(usuario.password, form_login.password.data):  # Confirma se o email e senha são daquele usuário
            login_user(usuario, remember=form_login.lembrar_dados.data)  # Faz o login do usuário no site
            flash(f'Login feito com sucesso no e-mail {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login. E-mail ou senha incorretos.', 'alert-danger')
    elif form_criarconta.validate_on_submit() and 'submit_criarconta' in request.form:  # Confirma se o botão que ele apertou é o de criar conta
        pw_crypt = bcrypt.generate_password_hash(form_criarconta.password.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, password=pw_crypt)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada com sucesso com o e-mail {form_login.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def logout():
    logout_user()
    flash(f'Logout feito com sucesso!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/profile')
@login_required
def profile():
    profile_picture = url_for('static', filename=f'fotos_perfil/{current_user.profile_pic}')
    return render_template('profile.html', profile_picture=profile_picture)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def create_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    cod = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + cod + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.profile_pic.data:
            nome_imagem = salvar_imagem(form.profile_pic.data)
            current_user.profile_pic = nome_imagem
        database.session.commit()
        flash('Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    profile_picture = url_for('static', filename=f'fotos_perfil/{current_user.profile_pic}')
    return render_template('editarperfil.html', profile_picture=profile_picture, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        form = FormCriarPost()
        if request.method == 'GET':
            form.title.data = post.title
            form.body.data = post.body
        elif form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            database.session.commit()
            flash('Post editado com sucesso!', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluído com sucesso.', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
