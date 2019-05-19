from flask import request, jsonify, url_for, send_from_directory, current_app, render_template
from . import api1
from ..models import Tags, Project_tags, Projects, Certifications, Certificates
from .. import db
from sqlalchemy.sql.expression import desc
import os


contact_json = { 'name_first': 'Brian',
            'name_last': 'Weinfeld',
            'api': '1',
            'phone': '9084511746',
            'email': 'brian.weinfeld@gmail.com',
            'github': 'https://github.com/brian-w-projects',
            'linkedin': 'https://www.linkedin.com/in/brian-weinfeld/',
            'location': 'Vancouver',
            'website': 'www.BrianDoesDataScience.com',
            'log_line': 'Talented programmer with strong creative vision, robust mathematics and statistics '
                        'background and team driven professional work environment experience. Adept public '
                        'speaker with proficiency crafting persuasive presentations for maximum '
                        'understanding and engagement. Lifelong learner with passion and curiosity for all '
                        'things computer and data science',
            'resume': 'https://www.BrianDoesDataScience.com/static/images/resume.pdf'}


@api1.route('/contact')
def contact():
    response = jsonify(contact_json)
    response.code = 200
    return response


@api1.route('/highlights/')
def highlights():
    query = db.session.query(Projects) \
        .filter(Projects.small == 0) \
        .all()
    response = jsonify({'contact': contact_json, 'projects': [{ele.title: ele.to_json() for ele in query}]})
    response.code = 200
    return response


@api1.route('/projects/')
def projects():
    query = db.session.query(Projects) \
        .all()
    response = jsonify({'contact': contact_json, 'projects': [{ele.title: ele.to_json() for ele in query}]})
    response.code = 200
    return response


@api1.route('/projects/<int:id>')
def project_id(id):
    query = db.session.query(Projects) \
        .get(id)
    response = jsonify({'contact': contact_json, 'projects': [{query.title: query.to_json()}]})
    response.code = 200
    return response


@api1.route('/projects/tags/<int:id>')
def project_tag_id(id):
    query = db.session.query(Projects) \
        .join(Project_tags) \
        .filter(Project_tags.tag_id == id) \
        .all()
    response = jsonify({'contact': contact_json, 'projects': [{ele.title: ele.to_json() for ele in query}]})
    response.code = 200
    return response


@api1.route('/projects/tags/<string:tag>')
def project_tag(tag):
    query = db.session.query(Projects) \
        .join(Project_tags) \
        .join(Tags) \
        .filter(Tags.tag == tag.lower()) \
        .all()
    response = jsonify({'contact': contact_json, 'projects': [{ele.title: ele.to_json() for ele in query}]})
    response.code = 200
    return response


@api1.route('/tags')
def tags():
    response = jsonify({'contact': contact_json, 'tags': [{tag.id: tag.tag for tag in db.session.query(Tags).all()}]})
    response.code = 200
    return response


@api1.route('/tags/<int:tag_id>')
def tags_id(tag_id):
    query = db.session.query(Projects) \
        .join(Project_tags) \
        .filter(Project_tags.tag_id == tag_id) \
        .order_by(Projects.id)
    tag = db.session.query(Tags) \
        .get(tag_id)
    response = jsonify({'contact': contact_json, 'tag': tag.tag,
                        'projects': [{project.id: project.title for project in query}]})
    response.code = 200
    return response


@api1.route('/resume')
def resume():
    directory = os.path.join(current_app.root_path, 'static', 'images')
    print(directory)
    return send_from_directory(directory, 'resume.pdf')


@api1.route('/certifications')
def certifications():
    query = db.session.query(Certifications) \
        .order_by(desc(Certifications.date)) \
        .all()
    response = jsonify({'contact': contact_json, 'certifications': [{cert.id: cert.to_json() for cert in query}]})
    response.code = 200
    return response


@api1.route('/trainings')
def trainings():
    query = db.session.query(Certificates) \
        .order_by(desc(Certificates.date)) \
        .all()
    response = jsonify({'contact': contact_json, 'certificates': [{cert.id: cert.to_json() for cert in query}]})
    response.code = 200
    return response


@api1.route('/<path:path>')
def bad_request(path):
    response = jsonify({'error': 'poorly formed request',
                        'valid_pathways': {
                            'api1/highlights': 'All highlight projects and associated data',
                            'api1/resume': 'PDF of resume',
                            'api1/certifications': 'Certification Details',
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
