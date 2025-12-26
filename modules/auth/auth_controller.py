from flask import Blueprint, request, render_template, redirect, url_for, session
from models.Usuario import Usuario
from config.db import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        usuario = request.form['usuario']
        contra = request.form['password']

        user: Usuario = Usuario.query.filter_by(usuario=usuario).first()

        if user and user.check_password(contra) and user.activo is True:
            session['user_id'] = user.id
            session['usuario'] = user.usuario
            session['rol'] = user.rol

            return redirect(url_for('main.home'))
        else:
            return redirect(url_for('auth.login'))
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        contra = request.form.get('password')

        exist_user = Usuario.query.filter_by(usuario=usuario).first()
        if exist_user:
            return redirect(url_for('auth.register'))

        new_user = Usuario(usuario=usuario)
        new_user.set_password(contra)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

