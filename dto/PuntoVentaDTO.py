from models.PuntoVenta import PuntoVenta
from config.ma import ma


class PuntoVentaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PuntoVenta


puntoVentaSchema = PuntoVentaSchema()
puntosVentaSchema = PuntoVentaSchema(many=True)
