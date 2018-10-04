from . import db
from datetime import datetime
from sqlalchemy.orm import backref
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as TimedSerializer
from . import login_manager
from flask_login import UserMixin
from sqlalchemy.sql.expression import or_, desc


class Ex(db.Model):
    __tablename__ = 'ex'