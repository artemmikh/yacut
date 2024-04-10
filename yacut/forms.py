from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Regexp, Optional
from settings import Config


class YacutForm(FlaskForm):
    original_link = TextAreaField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Regexp(Config.PATTERN,
                   message='Указано недопустимое имя для короткой ссылки')])
    submit = SubmitField('Создать')
