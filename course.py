from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import datetime
import os

host = os.getenv('DATEBASE_URL') or 'sqlite:///:memory:'

engine = create_engine(host)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)

    code = Column(String)
    title = Column(String)

    max = Column(Integer)

    def __repr__(self):
        return "<Course(code={})>".format(self.code)

class Enrollment(Base):
    __tablename__ = 'enrollments'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    enroll = Column(Integer)

    course_id = Column(Integer, ForeignKey('courses.id'))

    course = relationship("Course", back_populates="enrollments")

    def __repr__(self):
        return "<Enrollment(enroll={})>".format(self.enroll)

Course.enrollments = relationship("Enrollment", order_by=Enrollment.id, back_populates="course")

Base.metadata.create_all(engine)

if __name__ == '__main__':
    import requests
    from bs4 import BeautifulSoup

    session = Session()

    url = "https://registrar.princeton.edu/course-offerings/search_results.xml?submit=Search&term=1192&coursetitle=&instructor=&distr_area=&level=&cat_number=&subject=COS&sort=SYN_PS_PU_ROXEN_SOC_VW.SUBJECT%2C+SYN_PS_PU_ROXEN_SOC_VW.CATALOG_NBR%2CSYN_PS_PU_ROXEN_SOC_VW.CLASS_SECTION%2CSYN_PS_PU_ROXEN_SOC_VW.CLASS_MTG_NBR"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    for row in soup.table.findAll('tr')[1:]:
        cols = [list(col.stripped_strings) for col in row.findAll('td')]
        course = Course(id=cols[0][0], code=cols[1][0], title=cols[2][0], max=cols[8][0])
        session.add(course)

    session.commit()
