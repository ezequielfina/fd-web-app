from config.ma import ma
from models.Carga import Carga


class CargaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Carga
        include_fk = True


cargaSchema = CargaSchema()
cargasSchema = CargaSchema(many=True)
