from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import datetime
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') or 'sqlite:///:memory:'
db = SQLAlchemy(app)

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.String)
    title = db.Column(db.String)

    max = db.Column(Integer)

    def __repr__(self):
        return "<Course(code={})>".format(self.code)

class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    enroll = db.Column(db.Integer)

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    course = db.relationship("Course", back_populates="enrollments")

    def __repr__(self):
        return "<Enrollment(enroll={})>".format(self.enroll)

Course.enrollments = db.relationship("Enrollment", order_by=Enrollment.id, back_populates="course")

db.create_all()

if __name__ == '__main__':
    import requests
    from bs4 import BeautifulSoup

    url = "https://registrar.princeton.edu/course-offerings/search_results.xml?submit=Search&term=1192&coursetitle=&instructor=&distr_area=&level=&cat_number=&subject=COS&sort=SYN_PS_PU_ROXEN_SOC_VW.SUBJECT%2C+SYN_PS_PU_ROXEN_SOC_VW.CATALOG_NBR%2CSYN_PS_PU_ROXEN_SOC_VW.CLASS_SECTION%2CSYN_PS_PU_ROXEN_SOC_VW.CLASS_MTG_NBR"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    for row in soup.table.findAll('tr')[1:]:
        cols = [list(col.stripped_strings) for col in row.findAll('td')]
        course = Course(id=cols[0][0], code=cols[1][0], title=cols[2][0], max=cols[9][0])
        db.session.add(course)

    db.session.commit()
