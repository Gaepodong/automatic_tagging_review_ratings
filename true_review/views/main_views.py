from flask import Blueprint
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/movie')
def movie():
    return 'movie page!'


@bp.route('/')
def index():
    return 'main page'
