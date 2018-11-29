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
import dash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') or 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)

    dept = db.Column(db.String(3))
    num = db.Column(db.String(4))
    title = db.Column(db.String)

    max = db.Column(Integer)

    def __repr__(self):
        return "<Course(code={})>".format(self.dept + " " + self.num)

class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    enroll = db.Column(db.Integer)

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    course = db.relationship("Course", back_populates="enrollments")

    def __repr__(self):
        return "<Enrollment(course={} {}, date={}, enroll={})>".format(self.course.dept, self.course.num, self.date, self.enroll)

Course.enrollments = db.relationship("Enrollment", order_by=Enrollment.id, back_populates="course")

db.create_all()

def main():
    from enroll import soup

    seen = set()

    for row in soup.table.findAll('tr')[1:]:
        cols = [list(col.stripped_strings) for col in row.findAll('td')]
        id = cols[0][0]
        if id not in seen:
            dept, num = cols[1][0].split()
            max_enroll = None
            if cols[9]:
                max_enroll = cols[9][0]

            course = Course(id=cols[0][0], dept=dept, num=num, title=cols[2][0], max=max_enroll)
            db.session.add(course)
            seen.add(id)

    db.session.commit()

if __name__ == '__main__':
    main()