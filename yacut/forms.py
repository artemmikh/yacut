from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional, EqualTo


class YacutForm(FlaskForm):
    original_link = TextAreaField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 16)])
    submit = SubmitField('Создать')

# TODO Валидация совпадения с оригинальной ссылкой.

# EqualTo('original_link', message=
# 'Не может совпадать с оригинальной ссылкой')]
