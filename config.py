import os

basedir = os.path.abspath(os.path.dirname(__file__))

database_url = os.getenv('DATABASE_URL', None)
sqlite_database_url = 'sqlite:///' + os.path.join(basedir, 'sqlite.db')

class Config:
    JWT_SECRET_KEY = os.getenv('SECRET_KEY', '@#$%^&*_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = database_url or sqlite_database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = sqlite_database_url
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = database_url


config_by_env = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

jwt_key = Config.JWT_SECRET_KEY
