from datetime import datetime

from flask import Blueprint, url_for, request
from werkzeug.utils import redirect

from true_review import db
from true_review.models import Comments, Movies

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/create/<int:movie_id>', methods=('POST',))
def create(movie_id):
    movie = Movies.query.get_or_404(movie_id)
    content = request.form['content']
    # TODO rating 받아오기
    movie_rating = 1
    comment = Comments(movie_id=movie_id, content=content,
                       movie_rating=movie_rating, create_date=datetime.now())
    movie.comment_set.append(comment)
    db.session.commit()
    return redirect(url_for('movies.movie', movie_id=movie_id))
