from flask import Blueprint, render_template

from true_review.models import Movies
import requests
from bs4 import BeautifulSoup

bp = Blueprint('movies', __name__, url_prefix='/movies')

def getImageUrl(code):
    # make Url
    #https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=190010
    url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=' + str(code)
    response = requests.get(url.format(1))
    if response.status_code == 500:
        print("Movie code error")
    soup = BeautifulSoup(response.text, 'html.parser')
    imageUrl = soup.find('img')
    return imageUrl['src']

@bp.route('/movie/<int:movie_id>/')
def movie(movie_id):
    movie = Movies.query.get_or_404(movie_id)
    return render_template('movies/movie_detail.html', movie=movie)


@bp.route('/list/')
def _list():
    movie_list = Movies.query.order_by(Movies.create_date.desc())
    for movie in movie_list:
        movie.image_path = getImageUrl(movie.code)
    return render_template('movies/movie_list.html', movie_list=movie_list)
