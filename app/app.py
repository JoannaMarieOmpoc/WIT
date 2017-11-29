from flask import Flask, render_template, json, request,redirect,session,jsonify
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'super secret key'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'secret'
app.config['MYSQL_DATABASE_DB'] = 'user'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


# table for database
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


@app.route('/')
def main():
    return render_template('landing_page.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('landing_page.html')

@app.route('/logging')
def logging():
    return render_template('landing_page2.html')

@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        return render_template('dashboard.html')
    else:
        return render_template('landing_page2.html')

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('dashboard.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/profile')
def profile():
	return render_template('profile.html')
    

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        

        
        # connect to mysql

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()

        


        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                return render_template('userHome.html')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
            

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return render_template('dashboard.html')
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

if __name__ == "__main__":
    app.run(port=5000)
