from config.db import db
from sqlalchemy import orm, String, ForeignKey, UniqueConstraint, Boolean
import uuid
from sqlalchemy.dialects.postgresql import UUID
# Importamos el modelo Franquicia para usarlo en el tipado de la relación
from models.Franquicia import Franquicia


class PuntoVenta(db.Model):
    __tablename__ = 'puntos_venta'

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True),
                                                  primary_key=True,
                                                  nullable=False,
                                                  default=uuid.uuid4)

    descripcion: orm.Mapped[str] = orm.mapped_column(String(100), nullable=False)

    # Clave Foránea
    id_franquicia: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True),
                                                             ForeignKey('franquicias.id'),
                                                             nullable=False)

    activo: orm.Mapped[bool] = orm.mapped_column(Boolean, nullable=False, default=True)

    script: orm.Mapped[str] = orm.mapped_column(String(150))

    # Restricción Única Compuesta (UniqueConstraint)
    # Define que no puede haber dos puntos de venta con la misma descripción en la misma franquicia
    __table_args__ = (
        UniqueConstraint('descripcion', 'id_franquicia', name='un_pv'),
    )

    # Relación con Franquicia
    # Esto te permite hacer: mi_punto_venta.franquicia
    franquicia: orm.Mapped["Franquicia"] = orm.relationship("Franquicia", backref="puntos_venta")

    def __repr__(self) -> str:
        return f'<PuntoVenta {self.descripcion}>'
