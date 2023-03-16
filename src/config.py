from os import environ

SECRET_KEY = environ.get('SECRET_KEY')
API_KEY = environ.get('API_KEY')
SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
RESTX_VALIDATE = environ.get('RESTX_VALIDATE')
SESSION_PERMANENT = False
SESSION_TYPE = 'sqlalchemy'
