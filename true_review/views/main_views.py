from flask import Blueprint, render_template, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
import config
from true_review.models import Movies
from true_review.update import update_movies, update_reviews


bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/update')
def update_movies_and_reviews():
    """
    update movies and reviews from 'ranked_reviews' folder
    :return redirect to movie_.list
    """
    new_movie_code_list = update_movies()
    for movie_code in new_movie_code_list:
        update_reviews(movie_code)
    return redirect(url_for('movies._list'))


@bp.route('/')
def index():
    """
    # TODO: domain redirect 주소 포함한 주석으로 수정할 것
    :return redirect to movies._list
    """
    return redirect(url_for('movies._list'))
