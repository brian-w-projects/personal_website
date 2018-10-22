from flask import request, jsonify, url_for, send_from_directory, current_app, render_template
from . import api1
from ..models import Tags, Project_tags, Projects
from .. import db
from sqlalchemy.sql.expression import desc
import os


@api1.route('/contact')
def contact():
    response = jsonify({'name_first': 'Brian',
                        'name_last': 'Weinfeld',
                        'api': '1',
                        'phone': '9084511746',
                        'email': 'brian.weinfeld@gmail.com',
                        'github': 'https://github.com/brian-w-projects',
                        'linkedin': 'https://www.linkedin.com/in/brian-weinfeld/',
                        'location': 'Vancouver',
                        'resume': url_for('static', filename='downloads/resume.pdf', _external=True)})
    response.code = 200
    return response


@api1.route('/projects/')
def projects():
    query = db.session.query(Projects) \
        .all()
    response = jsonify({ele.id: ele.to_json() for ele in query})
    response.code = 200
    return response


@api1.route('/projects/<int:id>')
def project_id(id):
    query = db.session.query(Projects) \
        .get(id)
    response = jsonify(query.to_json())
    response.code = 200
    return response


@api1.route('/projects/tags/<int:id>')
def project_tag_id(id):
    query = db.session.query(Projects) \
        .join(Project_tags) \
        .filter(Project_tags.tag_id == id) \
        .all()
    response = jsonify({ele.id: ele.to_json() for ele in query})
    response.code = 200
    return response


@api1.route('/projects/tags/<string:tag>')
def project_tag(tag):
    query = db.session.query(Projects) \
        .join(Project_tags) \
        .join(Tags) \
        .filter(Tags.tag == tag) \
        .all()
    response = jsonify({ele.id: ele.to_json() for ele in query})
    response.code = 200
    return response


@api1.route('/tags')
def tags():
    response = jsonify({tag.id: tag.tag for tag in db.session.query(Tags).all()})
    response.code = 200
    return response


@api1.route('/tags/<int:tag_id>')
def tags_id(tag_id):
    query = db.session.query(Projects) \
        .join(Project_tags) \
        .filter(Project_tags.tag_id == tag_id) \
        .order_by(Projects.id)
    response = jsonify({project.id: project.title for project in query})
    response.code = 200
    return response


@api1.route('/resume')
def resume():
    directory = os.path.join(current_app.root_path, 'static/downloads')
    return send_from_directory(directory, 'resume.pdf')


@api1.route('/certifications')
def certifications():
    response = jsonify({})
    response.code = 200
    return response


@api1.route('/<path:path>')
def bad_request(path):
    response = jsonify({'error': 'poorly formed request',
                        'valid_pathways': {
                            'api1/resume': 'PDF of resume',
                            'api1/certifications': 'PDF of certifications',
                            'api1/projects': 'All projects and associated data',
                            'api1/projects/<int:id>': 'Project of the specified ID',
                            'api1/projects/tags/<string:tag>': 'All projects that contain specified tag by tag name',
                            'api1/projects/tags/<int:id>': 'All projects that contain specified tag by tag ID',
                            'api1/tags': 'All tags and associated tag names',
                            'api1/tags/<int:id>': 'All project ID and names that contain tag',
                            'api1/contact': 'All relevant contact information',
                        }})
    response.code = 404
    return response
