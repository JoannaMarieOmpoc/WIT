from app import app,db

class User(db.Model):
	__tablename__ = 'Users'
	username = db.Column(db.String(30), unique=True, primary_key=True, nullable=False)
	usermail = db.Column(db.String(50), unique=True, nullable=False)
	usertype = db.Column(db.String(10), nullable=False)
	password = db.Column(db.String(50), nullable=False)
	courses = db.relationship('Course', backref='User', secondary='Enrolled', lazy=True)

	def __init__(self, username, usermail, usertype, password):
		self.username = username
		self.usermail = usermail
		self.usertype = usertype
		self.password = password

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.username

	def __repr__(self):
		return '<User %r>' % self.username


class Course(db.Model):
    __tablename__ = 'Courses'

    courseid = db.Column(db.Integer, primary_key=True)
    coursename = db.Column(db.String(50), nullable=False)
    coursedesc = db.Column(db.Text, nullable=False)
    users = db.relationship('User', backref='Course', secondary='Enrolled', lazy=True)

    def __init__(self, coursename, coursedesc):
        self.coursename = coursename
        self.coursedesc = coursedesc

    def __repr__(self):
        return '<courseName {}>'.format(self.coursename)

class Topic(db.Model):
    __tablename__ = 'Topics'

    topicid = db.Column(db.Integer, primary_key=True)
    topicname = db.Column(db.String(30), nullable=False)
    topicdisc = db.Column(db.Text, nullable=False)
    courseid = db.Column(db.Integer, db.ForeignKey(Course.courseid), nullable=False)

    def __init__(self, topicname, topicdisc, courseid):
        self.topicname = topicname
        self.topicdisc = topicdisc
        self.courseid = courseid

    def __repr__(self):
        return '<topicid {}>'.format(self.topicid)


class Question(db.Model):
    __tablename__ = 'Questions'

    questionid = db.Column(db.Integer, primary_key=True)
    difficulty = db.Column(db.String(30), nullable=False)
    question = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    examid = db.Column(db.Integer, db.ForeignKey('Exams.examid'), nullable=False)

    def __init__(self, question, difficulty, answer, examid):
        self.question = question
        self.difficulty = difficulty
        self.answer = answer
        self.examid = examid

class Choice(db.Model):
	__tablename__ = 'Choices'

	choiceid = db.Column(db.Integer, primary_key=True)
	choice = db.Column(db.String(100), nullable=False)
	question = db.Column(db.Integer, db.ForeignKey('Questions.questionid'))

	def __init__(self, choice, question):
		self.choice = choice
		self.question = question

class Exam(db.Model):
    __tablename__ = 'Exams'

    examid = db.Column(db.Integer, primary_key=True)
    examtype = db.Column(db.String(30), nullable=False)
    courseid = db.Column(db.Integer, db.ForeignKey('Courses.courseid'), nullable=False)

    def __init__(self, examtype, courseid):
        self.examtype = examtype
        self.courseid = courseid

class Exercise(db.Model):
	__tablename__ = 'Exercises'

	exerciseid = db.Column(db.Integer, primary_key=True)
	questions = db.relationship('Question', backref='Exercises', lazy=True)

class Enroll(db.Model):
	__tablename__ = 'Enrolled'

	user = db.Column(db.ForeignKey('Users.username'), primary_key=True)
	course = db.Column(db.ForeignKey('Courses.courseid'), primary_key=True)
	#enroll_date = db.Column('date', db.DateTime, default=datetime.utcnow)

	user = db.relationship('User', backref='Enrolled')
	course = db.relationship('Course', backref='Enrolled')

db.create_all()
app.debug = True
