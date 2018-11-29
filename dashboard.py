import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader import data as web
from datetime import datetime as dt

from course import Course, Enrollment, app

options = []
for course in Course.query.all():
    name = course.dept + " " course.num
    options.append({'label': name, 'value': str(course.id)})

app.layout = html.Div([
    html.H1('Course Enrollments'),
    dcc.Dropdown(
        id='my-dropdown',
        options=options,
        value='21276'
    ),
    dcc.Graph(id='my-graph')
])

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(course_id):
    x = []
    y = []
    seen = set()
    course_id = int(course_id)
    for e in Enrollment.query.filter_by(course_id=course_id).all():
        if e.date not in seen:
            seen.add(e.date)
            x.append(e.date)
            y.append(e.enroll)

    return {
        'data': [{
            'x': x,
            'y': y
        }]
    }

if __name__ == '__main__':
    app.run_server()
