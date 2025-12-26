from flask import Blueprint, render_template


main_bp = Blueprint('main', __name__, url_prefix='/', template_folder='templates')


@main_bp.route('/')
def home():
    return render_template('home.html')
