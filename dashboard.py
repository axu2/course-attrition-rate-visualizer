import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt

from course import Course, Enrollment, Session

app = dash.Dash()
server = app.server

session = Session()

options = []
for course in session.query(Course).all():
    name = course.dept + " " + course.num
    options.append({'label': name, 'value': course.id})

app.layout = html.Div([
    html.H1('Course Enrollments'),
    dcc.Dropdown(
        id='my-dropdown',
        options=options,
        value=21276
    ),
    dcc.Graph(id='my-graph')
])

@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(course_id):
    x = []
    y = []
    seen = set()
    for e in session.query(Enrollment).filter_by(course_id=course_id).all():
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