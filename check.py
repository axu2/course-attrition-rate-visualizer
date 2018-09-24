# python check.py COS 429
import sys
from course import Course, Enrollment

dept, num = sys.argv[1:3]
course_id = Course.query.filter_by(dept=dept, num=num).first().id

for i in Enrollment.query.filter_by(course_id=course_id).all():
    print(i)
