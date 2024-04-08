from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_url(id):
    data = request.get_json()
    if 'original' not in data or 'short' not in data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.')


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    original_url = URLMap.query.filter_by(short_id=short_id).first()
    if original_url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'original_url': original_url.to_dict()}), 200
