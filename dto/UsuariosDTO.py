from config.ma import ma
from models.Usuario import Usuario


class UsuarioShema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        exclude = ("contra",)


usuarioSchema = UsuarioShema()
usuariosSchema = UsuarioShema(many=True)
