from flask import Blueprint
from config.db import db
from models.Health import Health
from dto.HealthDTO import health_schema

health_bp = Blueprint('health', __name__, url_prefix='/health')


@health_bp.route('/')
def health():
    nuevo_check = Health()
    db.session.add(nuevo_check)
    db.session.commit()

    return health_schema.jsonify(nuevo_check)
