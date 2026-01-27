from config.db import db
from sqlalchemy import orm
import uuid
from sqlalchemy.dialects.postgresql import UUID, VARCHAR


class Script(db.Model):
    __tablename__ = 'scripts'

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True),
                                                  primary_key=True,
                                                  nullable=False,
                                                  default=uuid.uuid4)

    descripcion: orm.Mapped[str] = orm.mapped_column(VARCHAR(120), nullable=False)

    validacion: orm.Mapped[str] = orm.mapped_column(VARCHAR(120), nullable=False)

    transformacion: orm.Mapped[str] = orm.mapped_column(VARCHAR(120), nullable=True)
