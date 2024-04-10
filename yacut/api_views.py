import re
from http import HTTPStatus

from flask import jsonify, request
from settings import Config

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    data_custom_id = data.get('custom_id')
    if data_custom_id and not re.match(Config.PATTERN, data.get('custom_id')):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if not data_custom_id or data_custom_id == '':
        data_custom_id = get_unique_short_id()
    if URLMap.query.filter_by(short=data.get('custom_id')).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.')
    short = URLMap(original=data.get('url'), short=data_custom_id)
    short.from_dict(data)
    db.session.add(short)
    db.session.commit()
    return jsonify(short.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    original_url = URLMap.query.filter_by(short=short_id).first()
    if original_url is None:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            HTTPStatus.NOT_FOUND)
    return jsonify({'url': original_url.original}), HTTPStatus.OK
