from models.Usuario import Usuario
from models.Operador import Operador
from dto.UsuariosDTO import usuariosSchema
from dto.FranquiciaDTO import franquiciasSchema
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from config.db import db
from models.Franquicia import Franquicia
from dto.OperadorDTO import operadorSchema

operadores_bp = Blueprint('operadores', __name__, url_prefix='/operadores', template_folder='templates')


@operadores_bp.route('/')
def get():
    # 1. Cargamos las listas como siempre
    usuarios = Usuario.query.all()
    usuarios_dto = usuariosSchema.dump(usuarios)

    franquicias = Franquicia.query.all()
    franquicias_dto = franquiciasSchema.dump(franquicias)

    # 2. Lógica NUEVA: Verificamos si venimos de una redirección con parámetros
    id_usuario_sel = request.args.get('id_usuario')
    id_franquicia_sel = request.args.get('id_franquicia')

    operador_seleccionado = None

    if id_usuario_sel and id_franquicia_sel:
        # Buscamos la relación específica para pintarla en el template
        operador_seleccionado = Operador.query.filter_by(
            id_usuario=id_usuario_sel,
            id_franquicia=id_franquicia_sel
        ).first()

    return render_template(
        'operadores.html',
        module='Operadores',
        usuarios=usuarios_dto,
        franquicias=franquicias_dto,
        # Pasamos las variables nuevas al HTML
        sel_usu=id_usuario_sel,
        sel_fran=id_franquicia_sel,
        operador=operador_seleccionado
    )


@operadores_bp.route('/franquicias/<uuid:id_usu>')
def get_franquicias_operador(id_usu):
    # Hacemos un JOIN: "Selecciona Franquicias unidas con Operadores donde..."
    franquicias = (
        db.session.query(Franquicia)
        .join(Operador)
        .filter(Operador.id_usuario == id_usu, Operador.activo == True)
        .all()
    )

    # Convertimos directamente la lista de franquicias
    return franquiciasSchema.dump(franquicias)


@operadores_bp.route('/es-operador/check', methods=['GET'])
def check_es_operador():
    id_usuario = request.args.get('id_usuario')
    id_franquicia = request.args.get('id_franquicia')

    if not id_usuario or not id_franquicia:
        return jsonify({'error': 'Faltan datos'}), 400

    # CORRECCIÓN: Usamos filter_by para argumentos con nombre
    operador = Operador.query.filter_by(
        id_usuario=id_usuario,
        id_franquicia=id_franquicia,
        activo=True
    ).first()

    # Devolvemos un JSON. bool(operador) será True si existe, False si es None.
    return jsonify({'es_operador': bool(operador)})


@operadores_bp.route('/modificar-status', methods=['POST'])
def modificar_status():
    # 1. Obtenemos datos del Form
    id_usuario = request.form.get('id_usuario')
    id_franquicia = request.form.get('id_franquicia')

    # Validamos que lleguen
    if not id_usuario or not id_franquicia:
        flash('Faltan datos para realizar la operación', 'error')
        return redirect(url_for('operadores.get'))

    operador = Operador.query.filter_by(id_usuario=id_usuario, id_franquicia=id_franquicia).first()

    mensaje = ""
    categoria = "success"

    # 2. Lógica de Negocio (Toggle)
    if operador:
        # Si ya existe, invertimos el estado
        if operador.activo:
            operador.activo = False
            mensaje = "Franquicia desasociada correctamente."
            categoria = "warning"  # Color amarillo/naranja
        else:
            operador.activo = True
            mensaje = "Franquicia re-asociada correctamente."
            categoria = "success"  # Color verde
    else:
        # Si no existe, creamos uno nuevo
        operador = Operador(id_usuario=id_usuario, id_franquicia=id_franquicia, activo=True)
        db.session.add(operador)
        mensaje = "Nueva asociación creada correctamente."
        categoria = "success"

    db.session.commit()

    # 3. Flasheamos el mensaje
    flash(mensaje, categoria)

    # 4. REDIRECCIÓN CON PARÁMETROS
    # Pasamos los IDs de vuelta para que la página 'get' sepa mantenerlos seleccionados
    return redirect(url_for('operadores.get', id_usuario=id_usuario, id_franquicia=id_franquicia))
