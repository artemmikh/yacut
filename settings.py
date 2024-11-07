class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '1234test4321'
    PATTERN = r'^[A-Za-z0-9]{1,16}$'
    ENDPOINT = 'http://127.0.0.1:5000/'
