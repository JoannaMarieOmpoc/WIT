from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import TopicsForm
from sqlalchemy import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0143@localhost/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'flaskimp'


class Enrolls(db.Model):
    __tablename__ = 'Enrolls'

    userid = db.Column(db.Integer, primary_key=True)
    courseid = db.Column(db.Integer, primary_key=True)
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

    courseid = db.Column(db.Integer, primary_key=True)
    coursename = db.Column(db.String(50), nullable=False)
    coursedesc = db.Column(db.String(100), nullable=False)

    def __init__(self, courseid, coursename, coursedesc):
        self.courseid = courseid
        self.coursename = coursename
        self.coursedesc = coursedesc


class Exams(db.Model):
    __tablename__ = 'Exams'

    examid = db.Column(db.Integer, primary_key=True)
    examtype = db.Column(db.String(30), nullable=False)
    courseid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, primary_key=True)

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
    courseid = db.Column(db.Integer)

    def __init__(self, topicname, topicdisc, courseid):
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
    examid = db.Column(db.Integer, primary_key=True)

    def __init__(self, questionid, difficulty, answer, examid):
        self.questionid = questionid
        self.difficulty = difficulty
        self.answer = answer
        self.examid = examid


class Exercises(db.Model):
    __tablename__ = 'Exercises'

    exerciseid = db.Column(db.Integer, primary_key=True)
    topicid = db.Column(db.Integer, primary_key=True)
    questionid = db.Column(db.Integer, primary_key=True)

    def __init__(self, exerciseid, topicid, questionid):
        self.exerciseid = exerciseid
        self.topicid = topicid
        self.questionid = questionid


class Choices(db.Model):
    __tablename__ = 'Choices'

    choicesid = db.Column(db.Integer, primary_key=True)
    questionid = db.Column(db.Integer, primary_key=True)
    choices = db.Column(db.String(30), nullable=False)

    def __init__(self, choicesid, questionid, choices):
        self.choicesid = choicesid
        self.questionid = questionid
        self.choices = choices


app.debug = True


@app.route('/', methods=['GET', 'POST'])
def topics():
    db.create_all()
    result1 = Topics.query.order_by(Topics.topicname)
    return render_template('topics.html', topics=result1, )


@app.route('/add', methods=['POST', 'GET'])
def addtopics():
    form = TopicsForm(request.form)
    if request.method == 'POST':
        if form.validate():
            topics = Topics(topicname=form.topicname.data, topicdisc=form.topicdisc.data, courseid=form.courseid.data)
            db.session.add(topics)
            db.session.commit()
            return redirect(url_for('topics'))
        else:
            return render_template('addtopics.html', form=form)
    else:
        return render_template('addtopics.html', form=form)


@app.route('/delete', methods=['GET', 'POST'])
def deletetopics():
    topics = Topics.query.order_by(Topics.topicname)
    if request.method == 'POST':
        Store = request.form['storage']
        result = Topics.query.filter_by(topicname=Store).first()
        db.session.delete(result)
        db.session.commit()
        topics = Topics.query.order_by(Topics.topicname)
        return redirect(url_for('topics', topics=topics))
    else:
        return redirect(url_for('topics', topics=topics))


@app.route('/update', methods=['POST', 'GET'])
def updatetopics():
    form = TopicsForm()
    if request.method == 'POST':
        if form.validate():
            topics.topicname = form.topicname.data
            topics.topicdisc = form.topicdisc.data
            db.session.add(topics)
            db.session.commit()
            result = Topics.query.order_by(Topics.topicname)
            return redirect(url_for('topics.html', topics=result))
        else:
            return render_template('updatetopics.html', form=form)
    else:
        return render_template('topics.html', form=form)


if __name__ == '__main__':
    app.run()
