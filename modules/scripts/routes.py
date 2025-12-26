from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.Franquicia import Franquicia
from dto.FranquiciaDTO import franquiciasSchema
from models.PuntoVenta import PuntoVenta
from config.db import db


scripts_bp = Blueprint('scripts', __name__, template_folder='templates', url_prefix='/scripts')


@scripts_bp.get('/')
def get():
    franquicias: [Franquicia] = Franquicia.query.all()
    franquicias_dto = franquiciasSchema.dump(franquicias)

    return render_template('scripts.html', module='Scripts', franquicias=franquicias_dto)


@scripts_bp.post('/')
def setear_script_pv():
    id_pv = request.form.get('id_pv')
    script = request.form.get('algo')

    pv: PuntoVenta = PuntoVenta.query.filter_by(id=id_pv).first()
    pv.script = script

    db.session.add(pv)
    db.session.commit()

    flash('Script seteado correctamente', 'success')
    return redirect(url_for('scripts.get'))

