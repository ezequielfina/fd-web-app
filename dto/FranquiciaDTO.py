from config.ma import ma
from models.Franquicia import Franquicia


class FranquiciaShema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Franquicia


franquiciaSchema = FranquiciaShema()
franquiciasSchema = FranquiciaShema(many=True)
