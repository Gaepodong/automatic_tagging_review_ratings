from flask import Blueprint, render_template

from true_review.models import Movies

bp = Blueprint('movies', __name__, url_prefix='/movies')


@bp.route('/movie/<int:movie_id>/')
def movie(movie_id):
    movie = Movies.query.get_or_404(movie_id)
    return render_template('movies/movie_detail.html', movie=movie)


@bp.route('/list/')
def _list():
    movie_list = Movies.query.order_by(Movies.create_date.desc())
    return render_template('movies/movie_list.html', movie_list=movie_list)
