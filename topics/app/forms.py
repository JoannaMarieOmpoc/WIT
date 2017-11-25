from wtforms import Form, StringField, IntegerField, ValidationError, SubmitField, validators

class TopicsForm(Form):
    topicname = StringField('Topic Name', [validators.length(min=1, max=60)])
    topicdisc = StringField('Topic Discussion', [validators.length(min=1, max=100)])
    courseid = StringField('Course Id', [validators.length(min=1, max=60)])
    submit = SubmitField("Submit")