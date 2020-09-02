from true_review import db


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    image_path = db.Column(db.Text(), nullable=True)


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movie.id', ondelete='CASCADE'))
    text_rank = db.Column(db.Float, nullable=True)
    content = db.Column(db.Text(), nullable=False)
    movie_rating = db.Column(db.Integer, nullable=False)
    emotion = db.Column(db.Boolean, nullable=False)
    reviews = db.relationship('Movie', backref=db.backref('review_set'))


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movie.id', ondelete='CASCADE'))
    movie = db.relationship('Movie', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    movie_rating = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
