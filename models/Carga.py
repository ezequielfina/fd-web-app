import uuid
import datetime
from enum import Enum as PyEnum

from sqlalchemy import orm, ForeignKey, String, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, DATE
from sqlalchemy.ext.associationproxy import association_proxy  # <--- 1. IMPORTAR ESTO
from config.db import db

# Importamos PuntoVenta para el tipado (o usa string "PuntoVenta" si te da error circular)
from models.PuntoVenta import PuntoVenta


class CargaStatus(str, PyEnum):
    RAW = "RAW"
    VALIDATED = "VALIDATED"
    TRANSFORMED = "TRANSFORMED"
    LOADED = "LOADED"
    VALIDATION_FAILED = "VALIDATION FAILED"
    TRANSFORM_FAILED = "TRANSFORM FAILED"
    LOAD_FAILED = "LOAD FAILED"


class Carga(db.Model):
    __tablename__ = 'cargas'

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4
    )

    id_operador: orm.Mapped[uuid.UUID] = orm.mapped_column(
        UUID(as_uuid=True),
        ForeignKey('operadores.id'),
        nullable=False
    )

    fecha_carga: orm.Mapped[datetime.datetime] = orm.mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    nombre_archivo: orm.Mapped[str] = orm.mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

    periodo: orm.Mapped[datetime.date] = orm.mapped_column(
        DATE,
        nullable=False
    )

    status: orm.Mapped[CargaStatus] = orm.mapped_column(
        String(30),
        nullable=False,
        default=CargaStatus.RAW
    )

    id_punto_venta: orm.Mapped[uuid.UUID] = orm.mapped_column(
        UUID(as_uuid=True),
        ForeignKey('puntos_venta.id'),
        nullable=False
    )

    ult_fecha_status: orm.Mapped[datetime.datetime] = orm.mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    # --- NUEVAS LÍNEAS AQUÍ ---

    # 2. Definimos la relación con PuntoVenta para que SQLAlchemy pueda "navegar"
    punto_venta: orm.Mapped["PuntoVenta"] = orm.relationship("PuntoVenta", backref="cargas")

    # 3. Creamos el atajo directo a Franquicia
    # Sintaxis: association_proxy('nombre_relacion_local', 'nombre_atributo_remoto')
    franquicia = association_proxy('punto_venta', 'franquicia')

    # --------------------------

    __table_args__ = (
        ForeignKeyConstraint(['id_operador'], ['operadores.id'], name='fk_car_ope'),
        ForeignKeyConstraint(['id_punto_venta'], ['puntos_venta.id'], name='fk_car_pv'),
        CheckConstraint(
            "status IN ('RAW', 'VALIDATED', 'TRANSFORMED', 'LOADED', 'VALIDATION FAILED', 'TRANSFORM FAILED', 'LOAD FAILED')",
            name='check_car_sta'
        ),
    )