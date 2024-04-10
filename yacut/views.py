import random
import string
from urllib.parse import urlparse
from http import HTTPStatus

from flask import render_template, request, redirect, flash, session
from settings import Config

from . import app, db
from .models import URLMap
from .forms import YacutForm

LENGTH_SHORT_LINK = 6


def get_unique_short_id():
    symbols = string.digits + string.ascii_letters
    short_link = ''.join(
        random.choice(symbols) for _ in range(LENGTH_SHORT_LINK))
    if URLMap.query.filter_by(short=short_link).first() is None:
        return short_link
    return get_unique_short_id()


@app.route('/', methods=['GET', 'POST'])
def index_view(short=None):
    form = YacutForm()

    if not form.validate_on_submit():
        return render_template('index.html', form=form)

    if session.get('short'):
        short_link = Config.ENDPOINT + session.pop('short')
        return render_template(
            'index.html',
            form=form,
            short=short_link)

    original_link = request.form['original_link']
    custom_id = form.custom_id.data
    if custom_id:
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        else:
            short = custom_id
    else:
        short = get_unique_short_id()

    new_url = URLMap(original=original_link, short=short)
    db.session.add(new_url)
    db.session.commit()
    session['short'] = short
    return render_template('index.html', form=form,
                           short=Config.ENDPOINT + short), HTTPStatus.OK


@app.route('/<string:short>')
def redirection(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    parsed_url = urlparse(url.original)
    if parsed_url.scheme:
        return redirect(url.original)
    return redirect('http://' + url.original)
