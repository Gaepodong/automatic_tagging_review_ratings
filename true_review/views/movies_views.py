from flask import Blueprint, render_template, url_for

from werkzeug.utils import redirect
from true_review.models import Movies, Reviews
from .. import db

from werkzeug.utils import redirect
import requests
from bs4 import BeautifulSoup

from true_review.forms import CommentForm

bp = Blueprint('movies', __name__, url_prefix='/movies')


def getImageUrl(code):
    # make Url
    # https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=
    url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=' + \
        str(code)
    response = requests.get(url.format(1))
    if response.status_code == 500:
        print("Movie code error")
    soup = BeautifulSoup(response.text, 'html.parser')
    imageUrl = soup.find('img')
    return imageUrl['src']


@bp.route('/movie/<int:movie_code>/<int:isFirstRender>/')
def movie(movie_code, isFirstRender):
    movie = db.session.query(Movies).filter_by(code=movie_code).first()
    review_list = Reviews.query.filter_by(
        movie_id=movie.id).order_by(Reviews.text_rank.desc())
    form = CommentForm()
    if movie == None:
        return redirect(url_for('movies._list'))
    return render_template('movies/movie_detail.html', movie=movie, form=form, isFirstRender=isFirstRender, review_list=review_list)


@bp.route('/list/')
def _list():
    movie_list = Movies.query.order_by(Movies.create_date.desc())
    for movie in movie_list:
        if movie.image_path == None:
            movie.image_path = getImageUrl(movie.code)
            db.session.commit()
    return render_template('movies/movie_list.html', movie_list=movie_list)
