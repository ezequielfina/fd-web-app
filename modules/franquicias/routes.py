from flask import Blueprint, render_template, request, flash, redirect, url_for
from config.db import db
from models.Franquicia import Franquicia
from dto.FranquiciaDTO import franquiciasSchema, franquiciaSchema

franquicias_bp = Blueprint('franquicias', __name__, url_prefix='/franquicias', template_folder='templates')


@franquicias_bp.route('/')
def get():
    franquicias: [Franquicia] = Franquicia.query.all()
    franquicias_dto: [franquiciasSchema] = franquiciasSchema.dump(franquicias)

    return render_template('franquicias.html', module='Franquicias', franquicias=franquicias_dto)


@franquicias_bp.route('/api/get/<uuid:id_franq>')
def get_info_json(id_franq):
    franquicia = db.session.get(Franquicia, id_franq)
    if not franquicia:
        return {"error": "No encontrado"}, 404

    return franquiciaSchema.dump(franquicia)


@franquicias_bp.route('/update', methods=['POST'])
def update():
    # Obtenemos el ID del select y los nuevos datos de los inputs
    id_fran = request.form.get('id_modificar')
    nuevo_cuit = request.form.get('mf_cuit')
    nueva_razon = request.form.get('mf_razon_social')

    if not id_fran:
        flash('Debes seleccionar una franquicia para modificar', 'error')
        return redirect(url_for('franquicias.get'))

    # Buscamos la franquicia en la DB
    franquicia = db.session.get(Franquicia, id_fran)

    if franquicia:
        try:
            # Actualizamos los campos
            franquicia.cuit = nuevo_cuit
            franquicia.razon_social = nueva_razon

            db.session.commit()
            flash(f'Franquicia "{nueva_razon}" actualizada con éxito', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar: El CUIT o Razón Social ya existen', 'error')
    else:
        flash('Franquicia no encontrada', 'error')

    return redirect(url_for('franquicias.get'))


@franquicias_bp.route('/', methods=['POST'])
def new():
    cuit = request.form.get('nf_cuit')
    razon_social = request.form.get('nf_razon_social')

    fran_exist = Franquicia.query.filter((Franquicia.cuit == cuit) | (Franquicia.razon_social == razon_social)).first()
    if fran_exist:
        flash('Ya existe una franquicia con ese CUIT o Razón Social', 'error')
        return redirect(url_for('franquicias.get'))

    new_fran: Franquicia = Franquicia(cuit=cuit, razon_social=razon_social)
    db.session.add(new_fran)
    db.session.commit()

    flash(f'Franquicia CUIT: {new_fran.cuit} - Razón social: {new_fran.razon_social} creado correctamente', 'created')
    return redirect(url_for('franquicias.get'))
