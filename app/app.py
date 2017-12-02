from flask import Flask, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mysqladmin:1234@localhost/database2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

take = db.Table('taker',
                db.Column('userid', db.Integer, db.ForeignKey('Users.userid')),
                db.Column('examid', db.Integer, db.ForeignKey('Exams.examid'))
                )
stud = db.Table('stud',
                    db.Column('userid', db.Integer, db.ForeignKey('Users.userid')),
                    db.Column('courseid', db.Integer, db.ForeignKey('Courses.courseid'))
                    )

class Exams(db.Model):
    __tablename__ = 'Exams'

    examid = db.Column(db.Integer, primary_key=True)
    examtype = db.Column(db.String(30), nullable=False)
    courseid = db.Column(db.Integer, db.ForeignKey('Courses.courseid'))
    takers = db.relationship('Exams', secondary=take, backref=db.backref('take', lazy='dynamic'))

    def __init__(self, examid, examtype, courseid):
        self.examid = examid
        self.examtype = examtype
        self.courseid = courseid


class Questions(db.Model):
    __tablename__ = 'Questions'

    questionid = db.Column(db.Integer, primary_key=True)
    difficulty = db.Column(db.String(30), nullable=False)
    question = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    examid = db.Column(db.Integer, primary_key=True)

    def __init__(self, questionid, question, difficulty, answer, examid):
        self.questionid = questionid
        self.question = question
        self.difficulty = difficulty
        self.answer = answer
        self.examid = examid

class Users(db.Model):
    __tablename__ = 'Users'

    userid = db.Column(db.Integer, primary_key=True )
    username = db.Column(db.String(30), nullable=False)
    usertype = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    courses = db.relationship('Courses', secondary=stud, backref=db.backref('students', lazy='dynamic'))

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

class Discussion(db.Model):
    __tablename__ = 'Discussion'

    discussionid = db.Column(db.Integer, primary_key=True)
    discussionname = db.Column(db.String(50), nullable=False)
    discontent = db.Column(db.String(100), nullable=False)
    topicid = db.Column(db.Integer, db.ForeignKey("Topics.topicid"), nullable=False)

    def __init__(self, discussionid, discussionname, discontent, topicid):
        self.discussionid = discussionid
        self.discussionname = discussionname
        self.discontent = discontent
        self.topicid = topicid

class Topics(db.Model):
    __tablename__ = 'Topics'

    topicid = db.Column(db.Integer, primary_key=True)
    topicname = db.Column(db.String(30), nullable=False)
    topicdisc = db.Column(db.String(100), nullable=False)
    courseid = db.Column(db.Integer, db.ForeignKey("Courses.courseid"), nullable=False)

    def __init__(self, topicid, topicname, topicdisc, courseid):
        self.topicid = topicid
        self.topicname = topicname
        self.topicdisc = topicdisc
        self.courseid = courseid

    def __repr__(self):
        return '<topicid {}>'.format(self.topicid)



@app.route('/')
def UserHome():
    return render_template('dashboard.html')


@app.route('/course/<course_name>', methods=['GET', 'POST'])
def course(course_name):
    course = Courses.query.filter_by(coursename=course_name).one()

    return render_template('course.html', course=course)


@app.route('/mycourses', methods=['GET', 'POST'])
def mycourses():
    user = session.get('user')
    user1 = Users.query.filter_by(userid=1).first()
    courses1 = user1.courses
    return render_template('mycourses.html', courses=courses1)

@app.route('/addcourseopt', methods=['POST'])
def addcourseopt():
    if request.method == 'POST':
        user = session.get('user')
        user1 = Users.query.filter_by(userid=1).first()
        coursename2 = request.form['coursename1']
        coursefind = Courses.query.filter_by(coursename=coursename2).first()
        usercourses = user1.courses
        for i in usercourses:
            if i.coursename is coursefind.coursename:
                return redirect(url_for('mycourses'))

        coursefind.students.append(user1)
        db.session.commit()
        return redirect(url_for('mycourses'))


@app.route('/removecourseopt', methods=['POST'])
def removecourseopt():
    if request.method == 'POST':
        user1 = Users.query.filter_by(userid=1).first()
        coursename1 = request.form['coursename2']
        deletethis = Courses.query.filter_by(coursename=coursename1).first()
        usercourses = user1.courses
        for i in usercourses:
            if i.coursename is deletethis.coursename:
                user1.courses.remove(deletethis)
                db.session.commit()
                return redirect(url_for('mycourses'))

        return redirect(url_for('mycourses'))


@app.route('/adminHome')
def adminHome():
    return render_template('admin_dashboard.html')


@app.route('/exams')
def exams():
    exams= Exams.query.order_by(Exams.examid)
    return render_template('exams.html', exams=exams)

@app.route('/addexams', methods=['POST', 'GET'])
def addexams():
    if request.method == 'POST':
        examid1 = int(request.form['examid'])
        examtype = request.form['examtype']
        examcourse = request.form['examcourse']
        course = Courses.query.filter_by(coursename=examcourse).first()
        exam = Exams(examid=examid1, examtype=examtype, courseid=course.courseid)
        db.session.add(exam)
        db.session.commit()
        return redirect('exams')

    return render_template('addexams.html')

@app.route('/editexam/<examid>', methods=['POST', 'GET'])
def editexam(examid):
    if request.method == 'POST':
        exam = Exams.query.filter_by(examid=examid).first()
        exam.examid = int(request.form['examid'])
        exam.examtype = request.form['examtype']
        examupdated = request.form['examcourse']
        examcourseid = Courses.query.filter_by(coursename=examupdated).first()
        exam.courseid = int(examcourseid.courseid)
        db.session.commit()
        return redirect('exams')
    else:
        exam = Exams.query.filter_by(examid=examid).first()
        course = Courses.query.filter_by(courseid=exam.courseid).first()
    return render_template('editexam.html', exam=exam, course=course)

@app.route('/deleteexam/<examid>', methods=['GET', 'POST'])
def deleteexam(examid):
    examdelete = Exams.query.filter_by(examid=examid).first()
    db.session.delete(examdelete)
    db.session.commit()
    return redirect('exams')

@app.route('/examquestions/<examid>', methods=['POST', 'GET'])
def examquestions(examid):
    if request.method == 'POST':
            exam = Exams.query.filter_by(examid=examid).first()
            questions = Questions.query.filter_by(examid=examid).all()

            return render_template('examquestions.html', exam=exam, questions=questions)
    else:
        exam = Exams.query.filter_by(examid=examid).first()
        questions = Questions.query.filter_by(examid=examid).all()
        return render_template('examquestions.html', exam=exam, questions=questions)

@app.route('/addexamquestions/<examid>', methods=['POST','GET'])
def addexamquestions(examid):
    if request.method == 'POST':
        exam = Exams.query.filter_by(examid=examid).first()
        questionid = int(request.form['questionid'])
        question = request.form['question']
        answer = request.form['answer']
        difficulty = request.form['difficulty']
        exam_id = int(exam.examid)
        questionnew = Questions(questionid=questionid,question=question, answer=answer, difficulty=difficulty, examid=exam_id)
        db.session.add(questionnew)
        db.session.commit()
        questions = Questions.query.filter_by(examid=examid).all()
        return render_template('examquestions.html', examid = examid, exam=exam, questions=questions)
    else:
        exam = Exams.query.filter_by(examid=examid).first()
        return render_template('addexamquestions.html', exam=exam)

@app.route('/deleteexamquestion/<examid>/<questionid>', methods=['POST', 'GET'])
def deleteexamquestion(examid, questionid):
    exam = Exams.query.filter_by(examid=examid).first()
    question = Questions.query.filter_by(questionid=questionid).first()
    db.session.delete(question)
    db.session.commit()
    questions = Questions.query.filter_by(examid=examid).all()
    return render_template('examquestions.html', examid = examid, exam=exam, questions=questions)

@app.route('/editexamquestion/<examid>/<questionid>', methods=['POST', 'GET'])
def editexamquestion(examid, questionid):
    if request.method == 'POST':
        exam = Exams.query.filter_by(examid=examid).first()
        question = Questions.query.filter_by(questionid=questionid).first()
        question.questionid = int(request.form['questionid'])
        question.question = request.form['question']
        question.answer = request.form['answer']
        question.difficulty = request.form['difficulty']
        db.session.commit()
        questions = Questions.query.filter_by(examid=examid).all()
        return render_template('examquestions.html', examid=examid, exam=exam, questions=questions)
    else:
        exam = Exams.query.filter_by(examid=examid).first()
        question = Questions.query.filter_by(questionid=questionid).first()
        return render_template('editexamquestion.html', examid=examid, exam=exam, question=question)


@app.route('/discussion')
def discussion():
    discussions = Discussion.query.order_by(Discussion.discussionid)
    return render_template('discussion.html', discussions=discussions)

@app.route('/add_discussion', methods=['POST', 'GET'])
def add_discussion():
    if request.method == 'POST':
        discussionid1 = int(request.form['discussionid'])
        discussionname1 = request.form['discussionname']
        discontent1 = request.form['discontent']
        topicid1 = int(request.form['topicid'])
        topic = Topics.query.filter_by(topicid=topicid1).first()
        discussion = Discussion(discussionid=discussionid1, discussionname=discussionname1, discontent=discontent1, topicid=topic.topicid)
        db.session.add(discussion)
        db.session.commit()
        return redirect('discussion')
    elif request.method == 'GET':
        return render_template('add_discussion.html')
    else:
        return render_template('add_discussion.html')

@app.route('/deletediscussion/<discussionid>', methods=['GET', 'POST'])
def deletediscussion(discussionid):
    discussiondelete = Discussion.query.filter_by(discussionid=discussionid).first()
    db.session.delete(discussiondelete)
    db.session.commit()
    return redirect('discussion')

@app.route('/editdiscussion/<discussionid>', methods=['POST', 'GET'])
def editdiscussion(discussionid):
    if request.method == 'POST':
        discussion = Discussion.query.filter_by(discussionid=discussionid).first()
        discussion.discussionid = int(request.form['discussionid'])
        discussion.discussionname = request.form['discussionname']
        discussion.discontent = request.form['discontent']
        topicid = request.form['topicid']
        topic = Topics.query.filter_by(topicid=topicid).first()
        discussion.topicid = int(topic.topicid)
        db.session.commit()
        return redirect('discussion')
    else:
        discussion = Discussion.query.filter_by(discussionid=discussionid).first()
        return render_template('editdiscussion.html', discussionid=discussionid, discussion=discussion)

if __name__ == '__main__':
    app.run(debug=True)