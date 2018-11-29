from flask import Flask
from flask_moment import Moment
from flask_sslify import SSLify
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from config import config
#from flask_redis import Redis
#from flask_celery import Celery


moment = Moment()
db = SQLAlchemy(query_class=BaseQuery)
csrf = CSRFProtect()
# login_manager = LoginManager()
#redis_store = Redis()
#celery = Celery()
# login_manager.session_protection = 'strong'
# login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment.init_app(app)
    #redis_store.init_app(app)
    #celery.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    # login_manager.init_app(app)
    sslify = SSLify(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api1 import api1 as api1_blueprint
    app.register_blueprint(api1_blueprint, url_prefix='/api1')

    return app