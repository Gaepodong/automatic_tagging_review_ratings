from datetime import datetime

from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

import requests as req
import json

from true_review import db
from true_review.models import Comments, Movies, Reviews

from true_review.forms import CommentForm

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/create/<int:movie_id>', methods=('GET', 'POST'))
def create(movie_id):
    movie = Movies.query.get_or_404(movie_id)
    review_list = Reviews.query.filter_by(
        movie_id=movie.id).order_by(Reviews.text_rank.desc())
    form = CommentForm()
    if request.method == 'POST' and form.validate_on_submit():

        # TODO: predict 보낼 사이트 주소는 환경변수로 숨기기
        response = req.post('http://dd8aae8e80ab.ngrok.io/predict',
                            data={'text': form.content.data}).json()
        # TODO rating, emotion_percent 가져오기
        emotion_percent = response['emotion_percent']
        movie_rating = response['movie_rating']
        pos_or_neg = response['pos_or_neg']

        # emotion_percent = 0.1
        # movie_rating = 2
        # pos_or_neg = 1

        comment = Comments(movie_id=movie_id, content=form.content.data,
                           movie_rating=movie_rating, create_date=datetime.now(), emotion_percent=emotion_percent, pos_or_neg=pos_or_neg)
        movie.comment_set.append(comment)
        db.session.commit()
        # return redirect(url_for('movies.movie', movie_code=movie.code, isFirstRender=0))
        return render_template('movies/movie_detail.html', movie=movie, form=form, isFirstRender=0, review_list=review_list, comment=comment)
    # return redirect(url_for('movies.movie', movie_code=movie.code, form=form))
    return render_template('movies/movie_detail.html', movie=movie, form=form, isFirstRender=1, review_list=review_list, comment=None)
