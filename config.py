import os

BASE_PATH = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # TODO: configure broker (Redis/Rabbitmq)
    BROKER_URL = None
    CELERY_RESULT_BACKEND = None

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql:///urlshortener"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
                                             "postgresql:///urlshortener_test"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql:///urlshortener"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
