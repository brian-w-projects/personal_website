from . import db
from datetime import datetime
from sqlalchemy.orm import backref
from flask import current_app, url_for
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

    def to_json(self):
        return {
            'id': self.id,
            'author': 'Brian Weinfeld',
            'title': self.title,
            'published': self.published,
            'repo': self.link,
            'url': url_for('main.display_project', slug=self.slug, _external=True),
            'description': self.description,
            'abstract': self.abstract,
            'discussion': self.discussion,
            'video': self.video.replace('embed/', 'watch?v='),
            'tags': {ele.tag.id: ele.tag.tag for ele in self.tag_list}
        }


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


class Certifications(db.Model):
    __tablename__ = 'certifications'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    image = db.Column(db.String(50))
    topic = db.Column(db.String(50))
    certificate = db.Column(db.Text)
    date = db.Column(db.Date)
    info = db.Column(db.Text)
    description = db.Column(db.Text)

    def to_json(self):
        return {
            'name': self.name,
            'topic': self.topic,
            'certificate': self.certificate,
            'date': self.date,
            'info': self.info,
            'description': self.description
        }


class Certificates(db.Model):
    __tablename__ = 'certificates'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    company = db.Column(db.String(50))
    image = db.Column(db.String(50))
    date = db.Column(db.Date)
    certificate = db.Column(db.Text)
    info = db.Column(db.Text)

    def to_json(self):
        return {
            'name': self.name,
            'company': self.company,
            'date': self.date,
            'info': self.info
        }
