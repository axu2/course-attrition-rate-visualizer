from flask import Flask, jsonify
from course import Course, Enrollment, app

@app.route("/<dept>/<num>")
def api(dept, num):
    course_id = Course.query.filter_by(dept=dept, num=num).first().id
    ret = []
    seen = set()
    for e in Enrollment.query.filter_by(course_id=course_id).all():
        date = "-".join(map(str, (e.date.year, e.date.month, e.date.day)))
        if date not in seen:
            seen.add(date)
            ret.append((date, e.enroll))
            
    return jsonify(ret)

if __name__ == "__main__":
    app.run(debug=True)
