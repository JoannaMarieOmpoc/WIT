from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, IntegerField, validators, ValidationError
from wtforms.validators import DataRequired, Length
from sqlalchemy import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/mydbs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'wit'


class Topics(db.Model):
    __tablename__ = "topics"

    topicid = db.Column(db.Integer, primary_key=True)
    topicname = db.Column(db.String(50), nullable=False)
    topicdisc = db.Column(db.String(500), nullable=False)
    courseid = db.Column(db.String(30), nullable=False)

    def __init__(self, topicname, topicdisc, courseid):
        self.topicname = topicname
        self.topicdisc = topicdisc
        self.courseid = courseid

    def __repr__(self):
        return '<topicname {}>'.format(self.topicname)


class TopicsForm(Form):
    topicname = StringField('Topic', validators=[DataRequired()])
    topicdisc = StringField('Discussion', validators=[DataRequired()])
    courseid = StringField('Course Id', validators=[DataRequired()])


db.create_all()
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def topics():
    result1 = Topics.query.order_by(Topics.courseid)
    return render_template('topics.html', topics=result1)


@app.route('/add', methods=['POST', 'GET'])
def addtopics():
    form = TopicsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            topics = Topics(topicname=form.topicname.data, topicdisc=form.topicdisc.data, courseid=form.courseid.data)
            db.session.add(topics)
            db.session.commit()
            result = Topics.query.order_by(Topics.courseid)
            return redirect(url_for('topics', topics=result, form=form))
    return render_template('addtopics.html', form=form)


@app.route('/edit/<topicid>', methods=['POST', 'GET'])
def editrecords(topicid):
    topics = Topics.query.filter_by(topicid=topicid).first()
    form = TopicsForm()
    if form.validate_on_submit():
        topics.topicname = form.topicname.data
        topics.topicdisc = form.topicdisc.data
        topics.courseid = form.courseid.data
        db.session.add(topics)
        db.session.commit()
        result = Topics.query.order_by(Topics.courseid)
        return redirect(url_for('topics', topics=result, form=form))
    else:

        form.topicname.data = topics.topicname
        form.topicdisc.data = topics.topicdisc
        form.courseid.data = topics.courseid
    return render_template('addtopics.html', form=form)


@app.route('/delete/<topicid>', methods=['GET', 'POST'])
def remove(topicid):
    result = Topics.query.filter_by(topicid=topicid).first()
    db.session.delete(result)
    db.session.commit()
    topics = Topics.query.order_by(Topics.topicname)
    return redirect(url_for('topics', topics=topics))


if __name__ == '__main__':
    app.run()