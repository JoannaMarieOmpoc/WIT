from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf import Form
from wtforms import StringField, PasswordField, validators


class SignInForm(Form):
    uname = StringField('Username', [validators.DataRequired(), validators.Length(min=5, max=30)])


class CourseForm(Form):
    courseId = StringField('Course Id', validators=[DataRequired()])
    courseName = StringField('Course Name', validators=[DataRequired()])
    courseDesc = StringField('Course Description', validators=[DataRequired()])

class TopicsForm(Form):
    topicname = StringField('Topic', validators=[DataRequired()])
    topicdisc = StringField('Discussion', validators=[DataRequired()])
    courseid = StringField('Course Id', validators=[DataRequired()])
