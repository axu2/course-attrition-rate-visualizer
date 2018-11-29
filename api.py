from flask import Flask, jsonify
from course import Course, Enrollment, app


@app.route("/dept/<dept>")
def dept(dept):
    ret = []
    for c in Course.query.filter_by(dept=dept).all():
        ret.append({
            'label' : c.dept + " " + c.num + ": " + c.title,
            'value' : c.id
        })
    return jsonify(ret)


@app.route("/enroll/<int:course_id>")
def enroll(course_id):
    x = []
    y = []
    seen = set()
    for e in Enrollment.query.filter_by(course_id=course_id).all():
        if e.date not in seen:
            seen.add(e.date)
            x.append(e.date)
            y.append(e.enroll)
            
    return jsonify({'x': x, 'y': y})


@app.route("/enroll/<dept>/<num>")
def enroll2(dept, num):
    course_id = Course.query.filter_by(dept=dept, num=num).first().id
    return enroll(course_id)


if __name__ == "__main__":
    app.run(debug=True)
