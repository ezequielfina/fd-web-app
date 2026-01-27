from flask import Blueprint, render_template, request, flash, redirect, url_for
import uuid
from models.Franquicia import Franquicia
from models.Script import Script
from dto.FranquiciaDTO import franquiciasSchema
from dto.ScriptDTO import scriptsSchema
from models.PuntoVenta import PuntoVenta
from config.db import db


scripts_bp = Blueprint('scripts', __name__, template_folder='templates', url_prefix='/scripts')


@scripts_bp.get('/')
def get():
    franquicias: list[Franquicia] = Franquicia.query.all()
    franquicias_dto = franquiciasSchema.dump(franquicias)

    return render_template('scripts.html', module='Scripts', franquicias=franquicias_dto)


@scripts_bp.get('/lista')
def get_list():
    scripts: list[Script] = Script.query.all()
    scripts_dto = scriptsSchema.dump(scripts)

    return scripts_dto


@scripts_bp.post('/')
def setear_script_pv():
    id_pv = request.form.get('id_pv')
    script_id = request.form.get('script_id')

    # 1. Validar que los datos existan
    if not id_pv or not script_id:
        flash('Datos incompletos', 'error')
        return redirect(url_for('scripts.get'))

    # 2. Buscar el registro
    pv = PuntoVenta.query.filter_by(id=id_pv).first()

    if not pv:
        flash('Punto de venta no encontrado', 'error')
        return redirect(url_for('scripts.get'))

    try:
        # 3. Convertir strings a UUID antes de asignar
        # Esto soluciona el error: Got 'str | None', expected 'UUID'
        pv.id_script = uuid.UUID(script_id)

        db.session.add(pv)
        db.session.commit()
        flash('Script seteado correctamente', 'success')

    except ValueError:
        # Por si el string no tiene formato de UUID válido
        flash('Formato de ID inválido', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar: {str(e)}', 'error')

    return redirect(url_for('scripts.get'))

