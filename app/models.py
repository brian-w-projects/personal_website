from . import db
from datetime import datetime
from sqlalchemy.orm import backref
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as TimedSerializer
# from . import login_manager
from sqlalchemy.sql.expression import or_, desc
import re
from slugify import slugify

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    published = db.Column(db.Date, default=datetime.utcnow)
    link = db.Column(db.TEXT)
    slug = db.Column(db.String(100), unique=True)
    small = db.Column(db.INTEGER)
    description = db.Column(db.TEXT)
    abstract = db.Column(db.TEXT)
    discussion = db.Column(db.TEXT)
    video = db.Column(db.TEXT)

class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.INTEGER, primary_key=True)
    tag = db.Column(db.String(100), unique=True)


class Project_tags(db.Model):
    __tablename__ = 'project_tags'
    id = db.Column(db.INTEGER, primary_key=True)
    project_id = db.Column(db.INTEGER, db.ForeignKey('projects.id'))
    tag_id = db.Column(db.INTEGER, db.ForeignKey('tags.id'))

    project = db.relationship('Projects', backref=backref('tag_list', lazy='dynamic'))
    tag = db.relationship('Tags', backref=backref('project_list', lazy='dynamic'))

