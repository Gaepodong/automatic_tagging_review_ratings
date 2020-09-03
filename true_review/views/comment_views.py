from datetime import datetime

from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from true_review import db
from true_review.models import Comments, Movies

from true_review.forms import CommentForm

bp = Blueprint('comment', __name__, url_prefix='/comment')


@bp.route('/create/<int:movie_id>', methods=('GET', 'POST'))
def create(movie_id):
    movie = Movies.query.get_or_404(movie_id)
    form = CommentForm()
    if request.method == 'POST' and form.validate_on_submit():
        # TODO rating 받아오기
        movie_rating = 1
        comment = Comments(movie_id=movie_id, content=form.content.data,
                           movie_rating=movie_rating, create_date=datetime.now())
        movie.comment_set.append(comment)
        db.session.commit()
        return redirect(url_for('movies.movie', movie_code=movie.code))
    print(form.errors)
    # return redirect(url_for('movies.movie', movie_code=movie.code, form=form))

    return render_template('movies/movie_detail.html', movie=movie, form=form)
