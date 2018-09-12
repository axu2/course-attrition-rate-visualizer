import requests
import datetime
from bs4 import BeautifulSoup
from course import Enrollment, Session

session = Session()

url = "https://registrar.princeton.edu/course-offerings/search_results.xml?submit=Search&term=1192&coursetitle=&instructor=&distr_area=&level=&cat_number=&subject=COS&sort=SYN_PS_PU_ROXEN_SOC_VW.SUBJECT%2C+SYN_PS_PU_ROXEN_SOC_VW.CATALOG_NBR%2CSYN_PS_PU_ROXEN_SOC_VW.CLASS_SECTION%2CSYN_PS_PU_ROXEN_SOC_VW.CLASS_MTG_NBR"
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

for row in soup.table.findAll('tr')[1:]:
    cols = [list(col.stripped_strings) for col in row.findAll('td')]
    enroll = Enrollment(date=datetime.date.today(), enroll=cols[8][0], course_id=cols[0][0])
    session.add(enroll)

session.commit()
