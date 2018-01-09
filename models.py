from app import app, db

enroll = db.Table('Enrolled',
                    db.Column('username', db.ForeignKey('Users.username')),
                    db.Column('coursename', db.String(50), db.ForeignKey('Courses.coursename'))
                  )

questionHasChoices = db.Table('questionHasChoices',
                      db.Column('questionid', db.ForeignKey('Questions.questionid')),
                      db.Column('choiceid', db.ForeignKey('Choices.choiceid'))
                      )
examHasQuestions = db.Table('examHasQuestions',
                            db.Column('examid', db.ForeignKey('Exams.examid'), primary_key=True),
                            db.Column('questionid', db.ForeignKey('Questions.questionid'), primary_key=True)
                            )
exerciseHasQuestions = db.Table('exerciseHasQuestions',
                                db.Column('exerciseid', db.ForeignKey('Exercises.exerciseid'), primary_key=True),
                                db.Column('questionid', db.ForeignKey('Questions.questionid'), primary_key=True)
                                )

gameHasQuestions = db.Table('gameHasQuestions',
                            db.Column('gameid', db.ForeignKey('Games.gameid'), primary_key=True),
                            db.Column('questionid', db.ForeignKey('Questions.questionid'), primary_key=True)
                            )

class User(db.Model):
    __tablename__ = 'Users'

    username = db.Column(db.String(30), unique=True, primary_key=True, nullable=False)
    usermail = db.Column(db.String(50), unique=True, nullable=False)
    usertype = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    courses = db.relationship('Course', secondary=enroll, backref=db.backref('students', lazy='dynamic'))

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

    coursename = db.Column(db.String(50), unique=True, nullable=False, primary_key=True)
    coursedesc = db.Column(db.Text, nullable=False)
    progress = db.Column(db.Integer, nullable=True)
    topics = db.relationship('Topic', cascade='all, delete', backref='course')
    exams = db.relationship('Exam', cascade='all, delete', backref='course')

    def __init__(self, coursename, coursedesc):
        self.coursename = coursename
        self.coursedesc = coursedesc

    def __repr__(self):
        return '<courseName {}>'.format(self.coursename)


class Topic(db.Model):
    __tablename__ = 'Topics'

    topicname = db.Column(db.String(30), unique=True, nullable=False, primary_key=True)
    topicdisc = db.Column(db.Text, nullable=False)
    courseid = db.Column(db.String(50), db.ForeignKey('Courses.coursename'), nullable=False)
    exercises = db.relationship('Exercise', cascade='all, delete', backref='topic')

    def __init__(self, topicname, topicdisc, courseid):
        self.topicname = topicname
        self.topicdisc = topicdisc
        self.courseid = courseid

    def __repr__(self):
        return '<topicid {}>'.format(self.topicid)

class Game(db.Model):
    __tablename__ = 'Games'

    gameid = db.Column(db.Integer, primary_key=True)
    gamename = db.Column(db.String(30), unique=True)
    questions = db.relationship('Question', secondary=gameHasQuestions, backref=db.backref('game', lazy='dynamic'))

    def __init__(self, gamename):
        self.gamename = gamename


class Question(db.Model):
    __tablename__ = 'Questions'

    questionid = db.Column(db.Integer, primary_key=True)
    difficulty = db.Column(db.String(30), nullable=False)
    question = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    topic_id = db.Column(db.String(30), db.ForeignKey(Topic.topicname), nullable=False)
    choices = db.relationship('Choice', secondary=questionHasChoices, cascade='all, delete', backref=db.backref('questions', lazy='dynamic'))

    def __init__(self, question, topic_id, difficulty, answer):
        self.question = question
        self.topic_id = topic_id
        self.difficulty = difficulty
        self.answer = answer


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
    courseid = db.Column(db.String(50), db.ForeignKey('Courses.coursename'), nullable=False)
    questions = db.relationship('Question', secondary=examHasQuestions, backref=db.backref('exam', lazy='dynamic'))

    def __init__(self, examtype, courseid):
        self.examtype = examtype
        self.courseid = courseid



class Exercise(db.Model):
    __tablename__ = 'Exercises'

    exerciseid = db.Column(db.Integer, primary_key=True)
    topicid = db.Column(db.String(30), db.ForeignKey(Topic.topicname), unique=True)
    gametype = db.Column(db.Integer, db.ForeignKey(Game.gameid))
    questions = db.relationship('Question', secondary=exerciseHasQuestions, backref=db.backref('exercise', lazy='dynamic'))

    def __init__(self, topicid, gametype):
        self.topicid = topicid
        self.gametype = gametype

class userTakesExercise(db.Model):
    __tablename__ = 'ExerciseResult'

    exerresultid = db.Column(db.Integer, primary_key=True)
    exer_id = db.Column(db.Integer, db.ForeignKey(Exercise.exerciseid))
    user_id = db.Column(db.String(30), db.ForeignKey(User.username))
    score = db.Column(db.Integer)

    def __init__(self, exer_id, user_id, score):
        self.exer_id = exer_id
        self.user_id = user_id
        self.score = score

class userTakesExam(db.Model):
    __tablename__ = 'ExamResult'

    examresultid = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey(Exam.examid))
    user_id = db.Column(db.String(30), db.ForeignKey(User.username))
    score = db.Column(db.Integer)

    def __init__(self, exam_id, user_id, score):
        self.exam_id = exam_id
        self.user_id = user_id
        self.score = score

class userTakesGame(db.Model):
    __tablename__ = 'GameResult'

    gameresultid = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.gameid), nullable=False)
    user_id = db.Column(db.String(30), db.ForeignKey(User.username))
    highscore = db.Column(db.Integer)

    def __init__(self, game_id, user_id, highscore):
        self.game_id = game_id
        self.user_id = user_id
        self.highscore = highscore



db.create_all()
app.debug = True
