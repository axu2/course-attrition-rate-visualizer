import requests
import datetime
from bs4 import BeautifulSoup
from course import Enrollment, Session

url = "https://registrar.princeton.edu/course-offerings/search_results.xml?submit=Search&term=1192&subject=COS"
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

if __name__ == '__main__':
    session = Session()
    seen = set()

    for row in soup.table.findAll('tr')[1:]:
        cols = [list(col.stripped_strings) for col in row.findAll('td')]
        id = cols[0][0]
        if id not in seen:
            enroll = Enrollment(date=datetime.date.today(), enroll=cols[8][0], course_id=id)
            session.add(enroll)

    session.commit()
