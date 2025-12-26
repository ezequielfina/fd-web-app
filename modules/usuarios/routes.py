from flask import Blueprint, render_template, request, redirect, flash, url_for
from models.Usuario import Usuario
from dto.UsuariosDTO import usuarioSchema, usuariosSchema
from config.db import db

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios', template_folder='templates')


@usuarios_bp.route('/')
def get():
    usuarios: [Usuario] = Usuario.query.all()
    usuarios_dto: [usuariosSchema] = usuariosSchema.dump(usuarios)

    roles = [{'nombre': 'OPERADOR'}, {'nombre': 'GESTOR'}, {'nombre': 'SUPERADMIN'}]

    return render_template('usuarios.html', module='Usuarios', usuarios=usuarios_dto, roles=roles)


@usuarios_bp.route('/api/get/<uuid:id_usuario>')
def get_info_json(id_usuario):
    usuario = db.session.get(Usuario, id_usuario)
    if not usuario:
        return {"error": "No encontrado"}, 404

    return usuarioSchema.dump(usuario)


@usuarios_bp.route('/update', methods=['POST'])
def update():
    # Obtenemos el ID del select y los nuevos datos de los inputs
    id_usuario = request.form.get('id_modificar')
    nuevo_usuario = request.form.get('mu_usuario')
    nueva_contra = request.form.get('mu_contra')
    activo_raw = request.form.get('mu_activo')
    esta_activo = True if activo_raw == 'checked' else False
    nuevo_rol = request.form.get('mu_rol')

    if not id_usuario:
        flash('Debes seleccionar un usuario para modificar', 'error')
        return redirect(url_for('usuarios.get'))

    # Buscamos la franquicia en la DB
    usuario: Usuario = db.session.get(Usuario, id_usuario)

    if usuario:
        try:
            # Actualizamos los campos
            usuario.usuario = nuevo_usuario
            if nueva_contra and nueva_contra.strip():
                usuario.set_password(nueva_contra)
            usuario.activo = esta_activo
            usuario.rol = nuevo_rol

            db.session.commit()
            flash(f'Usuario "{nuevo_usuario}" actualizado con éxito', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar: El usuario ya existe', 'error')
    else:
        flash('Usuario no encontrado', 'error')

    return redirect(url_for('usuarios.get'))


@usuarios_bp.route('/', methods=['POST'])
def new():
    usuario = request.form.get('nu_usuario')
    password = request.form.get('nu_password')
    activo_raw = request.form.get('nu_activo')
    esta_activo = True if activo_raw == 'checked' else False
    rol = request.form.get('nu_rol')

    usuario_exist: Usuario = Usuario.query.filter_by(usuario=usuario).first()
    if usuario_exist:
        flash('Ya existe un usuario con ese username', 'error')
        return redirect(url_for('usuarios.get'))

    new_usuario: Usuario = Usuario(usuario=usuario, activo=esta_activo, rol=rol)
    new_usuario.set_password(password)
    db.session.add(new_usuario)
    db.session.commit()

    flash(f'Usuario USERNAME: {new_usuario.usuario} creado correctamente', 'created')
    return redirect(url_for('usuarios.get'))
