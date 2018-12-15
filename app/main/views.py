from flask import render_template, request, jsonify, session, flash, redirect, url_for, current_app
from . import main
from .forms import ContactForm
from ..models import Tags, Project_tags, Projects, Certifications
from .. import db
from sqlalchemy.sql.expression import desc
import os
from ..email import send_email
import boto3


@main.route('/')
def index():
    form = ContactForm(request.form)
    form.next.data = url_for('main.index')
    return render_template('main/index.html', form=form)


@main.route('/about-me')
def about_me():
    form = ContactForm(request.form)
    form.next.data = url_for('main.about_me')
    return render_template('main/about-me.html', form=form)


@main.route('/resume')
def resume():
    form = ContactForm(request.form)
    form.next.data = url_for('main.resume')
    return render_template('main/resume.html', form=form)


@main.route('/projects')
def projects():
    form = ContactForm(request.form)
    form.next.data = url_for('main.projects')
    small = db.session.query(Projects) \
        .filter(Projects.small == 1) \
        .order_by(desc(Projects.id))
    large = db.session.query(Projects) \
        .filter(Projects.small == 0) \
        .order_by(desc(Projects.id))
    tags = db.session.query(Tags) \
        .order_by(Tags.tag)
    return render_template('main/projects.html', small=small, large=large, form=form, tags=tags)


@main.route('/projects/<string:slug>')
def display_project(slug):
    form = ContactForm(request.form)
    form.next.data = url_for('main.display_project', slug=slug)
    project = db.session.query(Projects) \
        .filter(Projects.slug == slug) \
        .one()
    next = db.session.query(Projects) \
        .get(project.id + 1)
    prev = db.session.query(Projects) \
        .get(project.id - 1)
    return render_template(f'main/single_project.html', project=project, next=next, prev=prev, form=form)


@main.route('/api')
def api1():
    form = ContactForm(request.form)
    form.next.data = url_for('main.api1')
    return render_template('main/api1.html', form=form)


@main.route('/certifications')
def certifications():
    form = ContactForm(request.form)
    form.next.data = url_for('main.certifications')
    certs = db.session.query(Certifications) \
        .order_by(desc(Certifications.date)) \
        .all()
    return render_template('main/certifications.html', form=form, certifications=certs)


@main.route('/form-validate', methods=['POST'])
def validate():
    form = ContactForm(request.form)
    if form.validate():
        if os.environ.get('CONFIG'):
            send_email(name=form.name.data, email=form.email.data, information=form.information.data)
        flash('Success! I will be in touch shortly', 'success')
    else:
        flash('Sorry, there was an error. I can be reached at brian.weinfeld@gmail.com Sorry for the inconvenience.',
              'error')
    return redirect(form.next.data or url_for('main.resume'))


@main.route('/download')
def resume_download():
    s3 = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
    )

    url = s3.generate_presigned_url('get_object',
                                    Params={'Bucket': current_app.config['FLASKS3_BUCKET_NAME'], 'Key': 'static/downloads/resume.pdf'},
                                    ExpiresIn=100)
    return redirect(url, code=302)