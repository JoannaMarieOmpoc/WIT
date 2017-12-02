from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf import Form


class TopicsForm(Form):
    topicname = StringField('Topic', validators=[DataRequired()])
    topicdisc = StringField('Discussion', validators=[DataRequired()])
    courseid = StringField('Course Id', validators=[DataRequired()])
