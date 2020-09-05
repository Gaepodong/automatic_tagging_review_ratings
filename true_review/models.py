from true_review import db

# TODO: db 야매 느낌 덜나게 변경하기 https://edykim.com/ko/post/getting-started-with-sqlalchemy-part-1/ <-- 참고


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Integer, nullable=True, unique=True)
    create_date = db.Column(db.DateTime(), nullable=False)
    image_path = db.Column(db.Text(), nullable=True)

    def __init__(self, title, code, create_date, image_path):
        self.title = title
        self.code = code
        self.create_date = create_date
        self.image_path = image_path

# 긍부정 리뷰 텍스트랭크 매긴 것 5개씩 영화별로 저장


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movies.id', ondelete='CASCADE'))
    text_rank = db.Column(db.Float, nullable=True)
    content = db.Column(db.Text(), nullable=False)
    # TODO: movie_rating은 삭제할 것
    movie_rating = db.Column(db.Integer, nullable=False)
    # TODO: emotion을 pos_or_neg로 바꿔야함.
    emotion = db.Column(db.Boolean, nullable=False)
    reviews = db.relationship('Movies', backref=db.backref('review_set'))

    def __init__(self, movie_id, text_rank, content, movie_rating, emotion):
        self.movie_id = movie_id
        self.text_rank = text_rank
        self.content = content
        self.movie_rating = movie_rating
        self.emotion = emotion

# 새로 다는 리뷰

# 영화코드.csv  text_rank, content, emotion


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movies.id', ondelete='CASCADE'))
    content = db.Column(db.Text(), nullable=False)
    movie_rating = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    emotion_percent = db.Column(db.Float, nullable=True)
    pos_or_neg = db.Column(db.Boolean, nullable=True)
    movie = db.relationship('Movies', backref=db.backref('comment_set'))

    def __init__(self, movie_id, content, movie_rating, create_date, emotion_percent, pos_or_neg):
        self.movie_id = movie_id
        self.content = content
        self.movie_rating = movie_rating
        self.create_date = create_date
        self.emotion_percent = emotion_percent
        self.pos_or_neg = pos_or_neg
