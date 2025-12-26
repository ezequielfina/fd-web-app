from config.db import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, DateTime, orm
import uuid
from datetime import datetime


class Health(db.Model):
    __tablename__ = 'health'

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status: orm.Mapped[str] = orm.mapped_column(String(2), nullable=False, default='OK')
    fecha: orm.Mapped[datetime] = orm.mapped_column(DateTime(timezone=True), default=datetime.now)
