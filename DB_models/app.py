from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length
from sqlalchemy import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/database'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@127.0.0.1:5432/database'

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'flaskimp'


class Enrolls(db.Model):
    __tablename__ = 'Enrolls'

    userid = db.Column(db.Integer, db.Foreignkey("user.id"), nullable=False)
    courseid = db.Column(db.Integer, db.Foreignkey("course.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    rank = db.Column(db.Integer, nullable=False)

    def __init__(self, userid, courseid, score, date, rank):
        self.userid = userid
        self.courseid = courseid
        self.score = score
        self.date = date
        self.rank = rank


class Users(db.Model):
    __tablename__ = 'Users'

    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    usertype = db.Column(db.String(30), nullable=False)
    password = db.Column(db.Integer, nullable=False)

    def __init__(self, userid, username, usertype, password):
        self.userid = userid
        self.username = username
        self.usertype = usertype
        self.password = password


class Courses(db.Model):
    __tablename__ = 'Courses'

    coursename = db.Column(db.String(50), nullable=False)
    coursedesc = db.Column(db.String(100), nullable=False)

    def __init__(self, coursename, coursedesc):
        self.coursename = coursename
        self.coursedesc = coursedesc


class Exams(db.Model):
    __tablename__ = 'Exams'

    examid = db.Column(db.Integer, primary_key=True)
    examtype = db.Column(db.String(30), nullable=False)
    courseid = db.Column(db.Integer, db.Foreignkey("course.id"), nullable=False)
    userid = db.Column(db.Integer, db.Foreignkey("user.id"), nullable=False)

    def __init__(self, examid, examtype, courseid, userid):
        self.examid = examid
        self.examtype = examtype
        self.courseid = courseid
        self.userid = userid


class Topics(db.Model):
    __tablename__ = 'Topics'

    topicid = db.Column(db.Integer, primary_key=True)
    topicname = db.Column(db.String(30), nullable=False)
    topicdisc = db.Column(db.String(100), nullable=False)
    courseid = db.Column(db.Integer, db.Foreignkey("course.id"), nullable=False)

    def __init__(self, topicid, topicname, topicdisc, courseid):
        self.topicid = topicid
        self.topicname = topicname
        self.topicdisc = topicdisc
        self.courseid = courseid

    def __repr__(self):
        return '<topicid {}>'.format(self.topicid)


class Questions(db.Model):
    __tablename__ = 'Questions'

    questionid = db.Column(db.Integer, primary_key=True)
    difficulty = db.Column(db.String(30), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    examid = db.Column(db.Integer, db.Foreignkey("exam.id"), nullable=False)

    def __init__(self, questionid, difficulty, answer, examid):
        self.questionid = questionid
        self.difficulty = difficulty
        self.answer = answer
        self.examid = examid


class Exercises(db.Model):
    __tablename__ = 'Exercises'

    exerciseid = db.Column(db.Integer, primary_key=True)
    topicid = db.Column(db.Integer, db.Foreignkey("topic.id"), nullable=False)
    questionid = db.Column(db.Integer, db.Foreignkey("question.id"), nullable=False)

    def __init__(self, exerciseid, topicid, questionid):
        self.exerciseid = exerciseid
        self.topicid = topicid
        self.questionid = questionid


class Choices(db.Model):
    __tablename__ = 'Choices'

    choicesid = db.Column(db.Integer, primary_key=True)
    questionid = db.Column(db.Integer, db.Foreignkey("question.id"), nullable=False)
    choices = db.Column(db.String(30), nullable=False)

    def __init__(self, choicesid, questionid, choices):
        self.choicesid = choicesid
        self.questionid = questionid
        self.choices = choices


class TopicsForm(Form):
    topicid = IntegerField('Topic Id', validators=[DataRequired()])
    topicname = StringField('Topic Name', validators=[DataRequired()])
    topicdisc = StringField('Topic Discussion', validators=[DataRequired()])
    courseid = IntegerField('Course Id', validators=[DataRequired()])


db.create_all()
app.debug = True


@app.route('/', methods=['GET', 'POST'])
def topics():
    result1 = Topics.query.order_by(Topics.topicname)
    return render_template('topics.html', topics=result1, form=form)


@app.route('/add', methods=['POST', 'GET'])
def addtopics():
    form = TopicsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            topics = Topics(topicname=form.topicname.data, topicdisc=form.topicdisc.data)
            db.session.add(topics)
            db.session.commit()
            result = Topics.query.order_by(Topics.topicname)
            form1 = SearchForm()
            return redirect(url_for('topics', topics=result, form=form1))
    return render_template('addtopics.html', form=form)


@app.route('/edit/<topicid>', methods=['POST', 'GET'])
def edittopics(topicid):
    topics = Topics.query.filter_by(id=topicid).first()
    form = TopicsForm()
    if form.validate_on_submit():
        topics.topicname = form.topicname.data
        topics.topicdisc = form.topicdisc.data
        db.session.add(topics)
        db.session.commit()
        result = Topics.query.order_by(Topics.topicname)
        form1 = SearchForm()
        return redirect(url_for('topics', topics=result, form=form1))
    else:

        form.topicname.data = topics.topicname
        form.topicdisc.data = topics.topicdisc
    return render_template('addtopics.html', form=form)


@app.route('/delete/<topicid>', methods=['GET', 'POST'])
def remove(topicid):
    result = Topics.query.filter_by(id=topicid).first()
    db.session.delete(result)
    db.session.commit()
    topics = Topics.query.order_by(Topics.topicname)
    form = SearchForm()
    return redirect(url_for('topics', topics=topics, form=form))


if __name__ == '__main__':
    app.run()
