from true_review import db

# TODO: db 야매 느낌 덜나게 변경하기 https://edykim.com/ko/post/getting-started-with-sqlalchemy-part-1/ <-- 참고


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Integer, nullable=True, unique=True)
    create_date = db.Column(db.DateTime(), nullable=False)
    image_path = db.Column(db.Text(), nullable=True)

# 긍부정 리뷰 텍스트랭크 매긴 것 5개씩 영화별로 저장


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movies.id', ondelete='CASCADE'))
    text_rank = db.Column(db.Float, nullable=True)
    content = db.Column(db.Text(), nullable=False)
    movie_rating = db.Column(db.Integer, nullable=False)
    emotion = db.Column(db.Boolean, nullable=False)
    reviews = db.relationship('Movies', backref=db.backref('review_set'))

# 새로 다는 리뷰


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movies.id', ondelete='CASCADE'))
    movie = db.relationship('Movies', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    movie_rating = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
