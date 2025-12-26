from config.ma import ma
from models.Operador import Operador


class OperadorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Operador


operadorSchema = OperadorSchema()
operadoresSchema = OperadorSchema(many=True)
