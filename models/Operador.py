from config.db import db
from sqlalchemy import orm, Boolean, ForeignKey, UniqueConstraint
import uuid
from sqlalchemy.dialects.postgresql import UUID
# Asegúrate de que estas importaciones no generen referencias circulares
from models.Usuario import Usuario
from models.Franquicia import Franquicia


class Operador(db.Model):
    __tablename__ = 'operadores'

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True),
                                                  primary_key=True,
                                                  nullable=False,
                                                  default=uuid.uuid4)

    # CORRECCIÓN 1: ForeignKey se pasa como objeto, no como parámetro 'ForeignKey='
    id_usuario: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True),
                                                          ForeignKey('usuarios.id'),
                                                          nullable=False)

    id_franquicia: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True),
                                                             ForeignKey('franquicias.id'),
                                                             nullable=False)

    activo: orm.Mapped[bool] = orm.mapped_column(Boolean, nullable=False, default=True)

    # CORRECCIÓN 2: Es __table_args__, no __tableargs__
    __table_args__ = (
        UniqueConstraint('id_usuario', 'id_franquicia', name='un_ope'),
    )

    # Relaciones
    usuario: orm.Mapped["Usuario"] = orm.relationship("Usuario", backref="operadores")
    franquicia: orm.Mapped["Franquicia"] = orm.relationship("Franquicia", backref="operadores")

    def __repr__(self) -> str:
        return f'<Operador User ID: {self.id_usuario} - Franq ID: {self.id_franquicia}>'