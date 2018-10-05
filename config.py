import os


class Config:
    pass

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'asdlfasdflkjsdf'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:cosmic joke@localhost/site'


class DeploymentConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # REDIS_URL = os.environ.get('REDIS_URL')
    # CELERY_BROKER_URL = os.environ.get('REDIS_URL')
    # CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'deployment': DeploymentConfig
}