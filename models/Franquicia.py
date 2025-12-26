from sqlalchemy.dialects.postgresql import UUID
from config.db import db
from sqlalchemy import String, orm
import uuid


class Franquicia(db.Model):
    __tablename__ = 'franquicias'

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True),
                                                  primary_key=True,
                                                  nullable=False,
                                                  default=uuid.uuid4)
    cuit: orm.Mapped[str] = orm.mapped_column(String(11), nullable=False, unique=True)
    razon_social: orm.Mapped[str] = orm.mapped_column(String(120), nullable=False, unique=True)
