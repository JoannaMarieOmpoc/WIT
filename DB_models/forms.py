from flask_wtf import Form
from wtforms import StringField, IntegerField, ValidationError, validators
from wtforms.validators import DataRequired, Length

class TopicsForm(Form):
    topicid = IntegerField('Topic Id', validators=[DataRequired()])
    topicname = StringField('Topic Name', validators=[DataRequired()])
    topicdisc = StringField('Topic Discussion', validators=[DataRequired()])
    courseid = IntegerField('Course Id', validators=[DataRequired()])

class CourseForm(Form):
    courseid = IntegerField('Course Id', validators.DataRequired())
    courseName = StringField('Course', [validators.DataRequired(),validators.Length(min=6, max=20)])
    courseDesc = StringField('Course Description', [validators.DataRequired(),validators.Length(min=6, max=50)])

