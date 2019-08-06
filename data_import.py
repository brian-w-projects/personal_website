from app import create_app, db
from app.models import Tags, Project_tags, Projects, Certifications, Certificates
import os
import csv
from slugify import slugify
from datetime import datetime


print('Entering...')
app = create_app(os.environ.get('CONFIG') or 'development')
with app.app_context():
    db.drop_all()
    db.create_all()

    folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
    file = os.path.abspath(os.path.join(folder, 'projects.csv'))

    with open(os.path.abspath(file), encoding='utf-8') as file:

        for row in csv.reader(file):
            try:
                p = Projects(title=row[1], published=datetime.strptime(row[2], '%m/%d/%y'),
                             link=row[3], slug=slugify(row[1]), small=row[4], description=row[5],
                             abstract=row[6], discussion=row[7], video=row[8])
                db.session.add(p)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

    print('Projects completed...')

    file = os.path.abspath(os.path.join(folder, 'tags.csv'))
    with open(os.path.abspath(file), encoding='utf-8') as file:

        for row in csv.reader(file):
            try:
                t = Tags(tag=row[1])
                db.session.add(t)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

    print('Tags completed...')

    file = os.path.abspath(os.path.join(folder, 'project_tags.csv'))
    with open(os.path.abspath(file), encoding='utf-8') as file:

        for row in csv.reader(file):
            try:
                p = Project_tags(project_id=row[0], tag_id=row[1])
                db.session.add(p)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

    print('Poject Tags completed...')

    file = os.path.abspath(os.path.join(folder, 'certifications.csv'))
    with open(os.path.abspath(file), encoding='utf-8') as file:

        for row in csv.reader(file):
            try:
                c = Certifications(name=row[0], image=row[1], topic=row[2],
                                   certificate=row[3], date=datetime.strptime(row[4], '%m/%d/%y'),
                                   info=row[5], description=row[6])
                db.session.add(c)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

    print('Certifications completed...')

    file = os.path.abspath(os.path.join(folder, 'certificates.csv'))
    with open(os.path.abspath(file), encoding='utf-8') as file:

        for row in csv.reader(file):
            try:
                c = Certificates(name=row[0], company=row[1], image=row[2],
                                   date=datetime.strptime(row[3], '%m/%d/%y'),
                                   certificate=row[4], info=row[5])
                db.session.add(c)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

    print('Certifications completed...')

    print('Finished...')