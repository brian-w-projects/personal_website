from flask import render_template, request, jsonify, session, flash, redirect, url_for, current_app
from . import main
from .forms import ContactForm
from ..models import Tags, Project_tags, Projects, Certifications, Certificates
from .. import db
from sqlalchemy.sql.expression import desc
import os
from ..email import send_email


@main.route('/')
def index():
    form = ContactForm(request.form)
    form.next.data = url_for('main.index')
    highlights = db.session.query(Projects) \
        .filter(Projects.small == 0) \
        .order_by(desc(Projects.published)) \
        .limit(5)
    return render_template('main/index.html', form=form, highlights=highlights)


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
        .order_by(desc(Projects.published))
    large = db.session.query(Projects) \
        .filter(Projects.small == 0) \
        .order_by(desc(Projects.published))
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
        .filter(Projects.published > project.published) \
        .order_by(Projects.published) \
        .first()

    prev = db.session.query(Projects) \
        .filter(Projects.published < project.published) \
        .order_by(desc(Projects.published)) \
        .first()

    path = os.path.join(current_app.static_folder, 'project_images', str(project.id))
    if os.path.exists(path):
        images = os.listdir(os.path.join(current_app.static_folder, 'project_images', str(project.id)))
    else:
        images = []
    return render_template(f'main/single_project.html', project=project, next=next, prev=prev, images=images, form=form)


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


@main.route('/trainings')
def trainings():
    form = ContactForm(request.form)
    form.next.data = url_for('main.trainings')
    certs = db.session.query(Certificates) \
        .order_by(desc(Certificates.date)) \
        .all()
    return render_template('main/trainings.html', form=form, certificates=certs)


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
