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
    FLASKS3_BUCKET_NAME = 'brian-website'
    AWS_ACCESS_KEY_ID = 'AKIAIRKYLG7FE27K5HNQ'
    AWS_SECRET_ACCESS_KEY = '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'


class DeploymentConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    FLASKS3_BUCKET_NAME = 'brian-website'


config = {
    'development': DevelopmentConfig,
    'deployment': DeploymentConfig
}