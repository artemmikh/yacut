import random
import string
from urllib.parse import urlparse

from flask import render_template, request, redirect, url_for, flash, session

from . import app, db
from .models import URLMap
from .forms import YacutForm

LENGTH_SHORT_LINK = 6
ENDPOINT = 'http://127.0.0.1:5000/'


def get_unique_short_id():
    symbols = string.digits + string.ascii_letters
    short_link = ''.join(
        random.choice(symbols) for _ in range(LENGTH_SHORT_LINK))
    if URLMap.query.filter_by(short=short_link).first() is None:
        return short_link
    else:
        return get_unique_short_id()


@app.route('/', methods=['GET', 'POST'])
def index_view(short=None):
    form = YacutForm()
    if form.validate_on_submit():
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
        return redirect(url_for('index_view', short=short))
    if session.get('short'):
        short_link = ENDPOINT + session.pop('short')
        return render_template('index.html',
                               form=form,
                               short=short_link)
    else:
        return render_template('index.html', form=form)
    # short_link = ENDPOINT + session.pop('short', '') if session.get(
    #     'short') else ''
    # return render_template('index.html',
    #                        form=form,
    #                        short=short_link)


@app.route('/<string:short>')
def redirection(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    parsed_url = urlparse(url.original)
    if parsed_url.scheme:
        return redirect(url.original)
    else:
        return redirect('http://' + url.original)
