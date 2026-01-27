from models.Script import Script
from config.ma import ma


class ScriptSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Script


scriptSchema = ScriptSchema
scriptsSchema = ScriptSchema(many=True)
