from flask import render_template, request, jsonify, session, flash, redirect, url_for, current_app
from . import main
from .forms import ContactForm
from ..models import Tags, Project_tags, Projects
from .. import db
from sqlalchemy.sql.expression import desc


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/about-me')
def about_me():
    return render_template('main/about-me.html')


@main.route('/resume', methods=['GET', 'POST'])
def resume():
    form = ContactForm(request.form)
    if request.method == 'POST':
        if form.validate():
            print('Success')
            print(form.name.data)
            print(form.email.data)
            print(form.information.data)
            flash('Success! I will be in touch shortly', 'success')
        else:
            flash('Sorry, there was an error. I can be reached at brian.weinfeld@gmail.com Sorry for the inconvenience.', 'error')
            print('Failure')
        return redirect(url_for('main.resume'))
    return render_template('main/resume.html', form=form)


@main.route('/projects')
def projects():
    small = db.session.query(Projects) \
        .filter(Projects.small == 1) \
        .order_by(desc(Projects.id))
    large = db.session.query(Projects) \
        .filter(Projects.small == 0) \
        .order_by(desc(Projects.id))
    return render_template('main/projects.html', small=small, large=large)


@main.route('/projects/<string:slug>', methods=['GET', 'POST'])
def display_project(slug):
    form = ContactForm(request.form)
    if request.method == 'POST':
        if form.validate():
            print('Success')
            print(form.name.data)
            print(form.email.data)
            print(form.information.data)
            flash('Success! I will be in touch shortly', 'success')
        else:
            flash('Sorry, there was an error. I can be reached at brian.weinfeld@gmail.com Sorry for the inconvenience.', 'error')
            print('Failure')
        return redirect(url_for('main.display_project', slug=slug))
    project = db.session.query(Projects) \
        .filter(Projects.slug == slug) \
        .one()
    next = db.session.query(Projects) \
        .get(project.id + 1)
    prev = db.session.query(Projects) \
        .get(project.id - 1)
    return render_template(f'main/single_project.html', project=project, next=next, prev=prev, form=form)