import uuid
import os
from models.Carga import Carga, CargaStatus
from models.Operador import Operador
from utils.uploader import upload_to_s3
from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from dto.FranquiciaDTO import franquiciasSchema
from models.Franquicia import Franquicia
from sqlalchemy import text
from config.db import db
import datetime

upload_file_bp = Blueprint('upload_file', __name__, url_prefix='/upload_file',
                           template_folder='templates')


ALLOWED_EXTENSIONS = {'txt', 'csv', 'xlsx'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def subir_carga(id_usuario: uuid,
                id_franquicia: uuid,
                nombre_archivo: str,
                periodo: str,
                status: CargaStatus,
                id_punto_venta: uuid):
    operador: Operador = Operador.query.filter_by(id_usuario=id_usuario, id_franquicia=id_franquicia).first()
    fecha_dt = datetime.datetime.strptime(periodo, '%Y-%m')
    periodo_date = fecha_dt.date()

    new_carga: Carga = Carga(id_operador=operador.id,
                             fecha_carga=datetime.datetime.now(),
                             ult_fecha_status=datetime.datetime.now(),
                             nombre_archivo=nombre_archivo,
                             periodo=periodo_date,
                             status=status,
                             id_punto_venta=id_punto_venta)

    db.session.add(new_carga)
    db.session.commit()


@upload_file_bp.route('/', methods=['GET', 'POST'])
def upload_file():
    # --- MÉTODO GET: Renderizar la vista ---
    if request.method == 'GET':
        sql = text("SELECT * FROM obtener_franq_por_usuario(:id_u)")

        result = db.session.execute(
            db.select(Franquicia).from_statement(sql),
            {"id_u": session.get('user_id')}
        )

        franquicias = result.scalars().all()
        franquicias_dto = franquiciasSchema.dump(franquicias)

        return render_template('upload_file.html', franquicias=franquicias_dto, module='Cargar archivos')

    # --- MÉTODO POST: Procesar el archivo ---

    if request.method == 'POST':
        # 1. Validar existencia del archivo
        if 'file_to_upload' not in request.files:
            flash('Error: No se envió ningún archivo.', 'error')
            return redirect(url_for('upload_file.upload_file'))

        file = request.files['file_to_upload']
        id_franq = request.form.get('id_franquicia')
        id_pv = request.form.get('id_pv')
        periodo = request.form.get('periodo')

        if file.filename == '':
            flash('Error: No seleccionaste ningún archivo.', 'warning')
            return redirect(url_for('upload_file.upload_file'))

        # 2. VALIDACIÓN DE EXTENSIÓN (Aquí está la magia)
        if not allowed_file(file.filename):
            flash('Error: Tipo de archivo no permitido. Usa solo .csv, .txt o .xlsx', 'error')
            return redirect(url_for('upload_file.upload_file'))

        try:
            extension = os.path.splitext(file.filename)[1].lower()
            namefile = f'{id_franq}/{periodo}/{uuid.uuid4()}{extension}'
            # Si pasa la validación, procedemos a S3
            status = upload_to_s3(file, namefile)

            if status:
                subir_carga(session.get('user_id'), id_franq, namefile, periodo, CargaStatus('RAW'), id_pv)
                flash(f'Archivo "{file.filename}" cargado exitosamente.', 'success')
            else:
                flash('Error al subir a S3.', 'error')

        except Exception as e:
            print(f"Error: {e}")
            flash('Error interno del servidor.', 'error')

        return redirect(url_for('upload_file.upload_file'))
