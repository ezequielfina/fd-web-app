import uuid
from config.db import db
from sqlalchemy import Column, String, Boolean, orm, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False,
                                                  default=uuid.uuid4)
    usuario: orm.Mapped[str] = orm.mapped_column(String(30), nullable=False, unique=True)
    contra: orm.Mapped[str] = orm.mapped_column(String(150), nullable=False)
    activo: orm.Mapped[bool] = orm.mapped_column(Boolean, nullable=False, default=True)
    rol: orm.Mapped[str] = orm.mapped_column(String(30), nullable=False, default='OPERADOR')

    __table_args__ = (
        CheckConstraint(rol.in_(['SUPERADMIN', 'GESTOR', 'OPERADOR']), name='ch_usu_rol'),
    )

    def set_password(self, password):
        self.contra = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contra, password)

    def __repr__(self):
        return f'Usuario: {self.usuario}'
