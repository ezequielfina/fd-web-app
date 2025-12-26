from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from models.PuntoVenta import PuntoVenta
from dto.FranquiciaDTO import franquiciasSchema
from dto.PuntoVentaDTO import puntosVentaSchema
from models.Franquicia import Franquicia
from sqlalchemy import text
from config.db import db


punto_venta_bp = Blueprint('punto_venta', __name__, template_folder='templates', url_prefix='/punto_venta')


@punto_venta_bp.route('/')
def get():
    # 1. Preparamos la consulta SQL
    # Nota: En Postgres las funciones que retornan tablas se llaman con SELECT
    sql = text("SELECT * FROM obtener_franq_por_usuario(:id_u)")

    # 2. Ejecutamos vinculando al modelo Franquicia
    # Usamos db.session.execute en lugar de session.scalars para mayor compatibilidad
    result = db.session.execute(
        db.select(Franquicia).from_statement(sql),
        {"id_u": session.get('user_id')}
    )

    # 3. Obtenemos los objetos
    franquicias: [Franquicia] = result.scalars().all()
    franquicias_dto: [franquiciasSchema] = franquiciasSchema.dump(franquicias)

    return render_template('punto_venta.html', module='Puntos de venta', franquicias=franquicias_dto)


@punto_venta_bp.route('/nuevo', methods=['POST'])
def nuevo_punto_venta():
    id_franquicia = request.form.get('npv_id_franquicia')
    descripcion = request.form.get('npv_descripcion')

    nuevo_pv: PuntoVenta = PuntoVenta(id_franquicia=id_franquicia, descripcion=descripcion, activo=True)
    db.session.add(nuevo_pv)
    db.session.commit()

    flash('Nuevo punto de venta agregado correctamente', 'success')
    return redirect(url_for('punto_venta.get'))


@punto_venta_bp.get('/por-franquicia/<uuid:id_franq>')
def get_pv_por_franquicia(id_franq):
    puntos_venta: [PuntoVenta] = PuntoVenta.query.filter_by(id_franquicia=id_franq, activo=True)
    pvs_dto = puntosVentaSchema.dump(puntos_venta)

    return pvs_dto

