from flask_wtf import FlaskForm
# from wtforms import StringField
from wtforms import StringField, TextField
# from wtforms.validators import DataRequired
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    # TODO 코멘트 댓글 길이 제한하기, Error message(alert) 추가하기?
    # content = StringField('내용', validators=[DataRequired('내용을 입력해주세요!')])
    # DataRequired는 데이터가 'true' 인지 체크한다.
    # 만약 데이터 타입이 문자열이고 문자열에 whitespace만 있다면 False로 간주
    # 인자로 들어오는 값은 message로 alert 경고문에 출력되는 내용인듯
    # Length 입력값의 길이 체크
    content = TextField('내용', validators=[DataRequired('내용을 입력해주세요!'), Length(
        min=20, max=200, message="Comment needs at least 20 characters")])
