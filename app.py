from flask import Flask, request, session, redirect, url_for
from config.config import Config
from config.db import db
from config.ma import ma
from modules.health.health_controller import health_bp
from modules.auth.auth_controller import auth_bp
from modules.upload_file.upload_file_controller import upload_file_bp
from modules.main.main import main_bp
from modules.operadores.routes import operadores_bp
from modules.usuarios.routes import usuarios_bp
from modules.franquicias.routes import franquicias_bp
from modules.punto_venta.routes import punto_venta_bp
from modules.cargas.routes import cargas_bp
from modules.scripts.routes import scripts_bp

from models.Usuario import Usuario

app = Flask(__name__)

app.register_blueprint(health_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(upload_file_bp)
app.register_blueprint(main_bp)
app.register_blueprint(operadores_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(franquicias_bp)
app.register_blueprint(punto_venta_bp)
app.register_blueprint(cargas_bp)
app.register_blueprint(scripts_bp)


app.config.from_object(Config)

# Inicializamos la base de datos y Marshmallow con la app
db.init_app(app)
ma.init_app(app)


@app.before_request
def verificar_acceso():
    rutas_publicas = ['auth.login', 'auth.register', 'static']
    if request.endpoint in rutas_publicas:
        return None

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if 'user_id' in session:
        user: Usuario = db.session.get(Usuario, session.get('user_id'))
        if not user or not user.activo:
            session.clear()
            return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, port=8080)
