from app import app,db

class Course(db.Model):
    __tablename__ = "course"

    courseId = db.Column(db.Integer, primary_key=True)
    courseName = db.Column(db.String(50), nullable=False)
    courseDesc = db.Column(db.String(500), nullable=False)

    def __init__(self, courseId, courseName, courseDesc):
        self.courseId = courseId
        self.courseName = courseName
        self.courseDesc = courseDesc

    def __repr__(self):
        return '<courseName {}>'.format(self.courseName)

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
    courseid = db.Column(db.Integer, nullable=False)
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
    discontent = db.Column(db.String(1000), nullable=False)
    topicid = db.Column(db.Integer, nullable=False)

    def __init__(self, discussionid, discussionname, discontent, topicid):
        self.discussionid = discussionid
        self.discussionname = discussionname
        self.discontent = discontent
        self.topicid = topicid

class Topics(db.Model):
    __tablename__ = 'Topics'

    topicid = db.Column(db.Integer, primary_key=True)
    topicname = db.Column(db.String(30), nullable=False)
    topicdisc = db.Column(db.String(1000), nullable=False)
    courseid = db.Column(db.Integer, nullable=False)

    def __init__(self, topicname, topicdisc, courseid):
        self.topicname = topicname
        self.topicdisc = topicdisc
        self.courseid = courseid

    def __repr__(self):
        return '<topicid {}>'.format(self.topicid)

db.create_all()
app.debug = True