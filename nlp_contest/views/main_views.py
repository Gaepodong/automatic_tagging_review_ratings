from flask import Blueprint
bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/movie')
def movie():
    return 'movie page!'


@bp.route('/')
def index():
    return 'main page'
