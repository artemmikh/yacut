import random
import string

from flask import render_template, request, redirect, url_for

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
    else:
        return get_unique_short_id()


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if request.method == 'POST':
        pass

    return render_template('index.html')
