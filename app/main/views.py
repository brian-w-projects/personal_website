from flask import render_template, request, jsonify, session, flash, redirect, url_for, current_app
from . import main
# from .forms import
# from ..models import
from .. import db


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/about-me')
def about_me():
    return render_template('main/about-me.html')


@main.route('/resume')
def resume():
    return render_template('main/resume.html')


@main.route('/projects')
def projects():
    return render_template('main/projects.html')


@main.route('/projects-<int:id>')
def display_project(id):
    return render_template(f'main/projects-{id}.html', id=id)