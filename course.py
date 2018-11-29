from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import datetime
import os

host = os.getenv('DATABASE_URL') or 'sqlite:////tmp/test.db'

engine = create_engine(host)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)

    dept = Column(String(3))
    num = Column(String(4))
    title = Column(String)

    max = Column(Integer)

    def __repr__(self):
        return "<Course(code={})>".format(self.dept + " " + self.num)

class Enrollment(Base):
    __tablename__ = 'enrollments'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    enroll = Column(Integer)

    course_id = Column(Integer, ForeignKey('courses.id'))

    course = relationship("Course", back_populates="enrollments")

    def __repr__(self):
        return "<Enrollment(course={} {}, date={}, enroll={})>".format(self.course.dept, self.course.num, self.date, self.enroll)

Course.enrollments = relationship("Enrollment", order_by=Enrollment.id, back_populates="course")

Base.metadata.create_all(engine)

def main():
    from enroll import soup

    session = Session()
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
            session.add(course)
            seen.add(id)

    session.commit()

if __name__ == '__main__':
    main()
