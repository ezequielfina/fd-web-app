from sqlalchemy import text
from config.db import db
from flask import Blueprint, render_template, session
from models.Carga import Carga
from models.Franquicia import Franquicia
from dto.FranquiciaDTO import franquiciasSchema
from dto.CargaDTO import cargasSchema, cargaSchema


cargas_bp = Blueprint('cargas', __name__, template_folder='templates', url_prefix='/cargas')


@cargas_bp.get('/')
def get():
    sql = text("SELECT * FROM obtener_franq_por_usuario(:id_u)")

    result = db.session.execute(
        db.select(Franquicia).from_statement(sql),
        {"id_u": session.get('user_id')}
    )

    franquicias = result.scalars().all()
    franquicias_dto = franquiciasSchema.dump(franquicias)

    return render_template('carga.html', module='Detalle cargas', franquicias=franquicias_dto)


@cargas_bp.get('/cargas/<uuid:id_franq>')
def get_cargas_por_franq_y_usu(id_franq):
    sql = text("SELECT * FROM cargas_por_franquicia(:id_franq, :id_u)")

    result = db.session.execute(
        db.select(Carga).from_statement(sql),
        {"id_franq": id_franq, "id_u": session.get('user_id')}
    )

    cargas = result.scalars().all()
    cargas_dto = cargasSchema.dump(cargas)

    return cargas_dto


@cargas_bp.get('/<uuid:id_carga>')
def get_details(id_carga):
    carga: Carga = Carga.query.filter_by(id=id_carga).first()
    carga_dto = cargaSchema.dump(carga)

    return carga_dto
