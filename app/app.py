from flask import Flask, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mysqladmin:1234@localhost/examdb2'
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



@app.route('/')
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

if __name__ == '__main__':
    app.run(debug=True)