from models.Franquicia import Franquicia
from config.ma import ma


class FranquiciaShema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Franquicia


franquiciaSchema = FranquiciaShema()
franquiciasSchema = FranquiciaShema(many=True)
