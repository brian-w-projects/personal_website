from app import create_app, db
from app.models import Tags, Project_tags, Projects
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
                p = Projects(id=row[0], title=row[1], published=datetime.strptime(row[2], '%m/%d/%y'),
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
                t = Tags(id=row[0], tag=row[1])
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
                p = Project_tags(id=row[0], project_id=row[1], tag_id=row[2])
                db.session.add(p)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

    print('Poject Tags completed...')
    print('Finished...')