from config.ma import ma
from models.Health import Health


class HealthSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Health


health_schema = HealthSchema()
healths_schema = HealthSchema(many=True)
