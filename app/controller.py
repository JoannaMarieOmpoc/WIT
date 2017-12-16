from app import app, db, lm
from flask import Flask, render_template, redirect, request, url_for
from models import User, Course, Topic, Question, Choice, Exam, Exercise, Game
from flask_login import login_required, login_user, logout_user, current_user
from app import db
from  sqlalchemy.sql.expression import func, select

@lm.user_loader
def getUser(name):
    return User.query.filter_by(username = name).first()

@app.route('/', methods=['POST', 'GET'])
def main():
    admintest = User.query.filter_by(username='admin').first()
    if admintest is None:
        admin = User(username='admin', usermail='admin@gmail.com', usertype='admin', password='adminpass')
        db.session.add(admin)
        db.session.commit()
    return render_template('landing_page.html')

@app.route('/error/<e>', methods=['POST', 'GET'])
def showError(e):
    return render_template('error.html', error=e)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        if request.form['inputPassword'] == request.form['inputPasswordConfirm']:
            try:
                user = User(request.form['inputName'], request.form['inputEmail'], 'member', request.form['inputPassword'])
                db.session.add(user)
                db.session.commit()
                login_user(user)

                if user.usertype == 'member':
                    return redirect(url_for('.showDashboard', user = user.username))
                elif user.usertype == 'admin':
                    return redirect(url_for('.showAdminDashboard', admin = user.username))
            except Exception as e:
                return redirect(url_for('.showError', e = str(e)))
        else:
            return redirect('/')
    else:
        return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['inputName']
            password = request.form['inputPassword']
            user = User.query.filter_by(username=username).filter_by(password=password).first()
            if user is not None:
                login_user(user)
                return redirect(url_for('.showDashboard', user = user.username))
            else:
                return redirect('/login')
        except Exception as e:
            return redirect(url_for('.showError', e = str(e)))
    else:
        return render_template('login.html')

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/<user>', methods=['POST', 'GET'])
@login_required
def showDashboard(user):
    return render_template('user_dashboard.html', user = user)

@app.route('/<user>/courses')
@login_required
def enrolledCourses(user):
    courses = current_user.courses
    coursesoption = Course.query.order_by().all()
    return render_template('user_courses.html', user=user, courses=courses, coursesoption=coursesoption)

@app.route('/<user>/courses/<coursename>')
@login_required
def displayCourse(coursename, user):
    course = Course.query.filter_by(coursename=coursename).first()
    topics = Topic.query.filter_by(courseid=course.courseid).all()
    return render_template('user_showCourse.html', topics = topics, course=course, user=user)

@app.route('/<user>/courses/addcourse', methods=['POST'])
def userAddcourse(user):
    if request.method == 'POST':
        coursename2 = request.form.get('coursename1')
        coursefind = Course.query.filter_by(coursename=coursename2).first()
        usercourses = current_user.courses
        for i in usercourses:
            if i.coursename is coursefind.coursename:
                return redirect(url_for('enrolledCourses', user=user))

        current_user.courses.append(coursefind)
        db.session.commit()
        return redirect(url_for('enrolledCourses', user=user))

@app.route('/<user>/courses/removecourse/<coursename>', methods=['POST', 'GET'])
def userRemovecourse(user, coursename):
    if request.method == 'POST':
        course = Course.query.filter_by(coursename=coursename).first()
        current_user.courses.remove(course)
        db.session.commit()
        return redirect(url_for('enrolledCourses', user=user))

@app.route('/<user>/courses/<coursename>/topic/<topicid>', methods=['POST', 'GET'])
def user_Topic(user, coursename, topicid):
    topic = Topic.query.filter_by(topicid=topicid).first()
    exercises = Exercise.query.filter_by(topicid=topicid).all()
    return render_template('user_Topic.html', topic=topic, coursename=coursename, exercises=exercises, user=user)

@app.route('/<user>/courses/<coursename>/topic/<topicname>/exercise/<exerciseid>', methods=['POST', 'GET'])
def user_takeExercise(user, coursename, topicname, exerciseid):
    topic = Topic.query.filter_by(topicname=topicname).first()
    exercise1 = Exercise.query.filter_by(exerciseid=exerciseid).first()
    questionss = exercise1.questions.select.order_by(func.rand())
    return render_template('user_exercise.html', topic=topic, exercise=exercise1, questions=questionss)


@app.route('/<user>/exams')
@login_required
def exams(user):
    return render_template('user_exams.html', user = user)

@app.route('/<user>/games')
@login_required
def games(user):
    return render_template('user_games.html', user = user)

@app.route('/<user>/profile')
@login_required
def profile(user):
    return render_template('user_profile.html', user = user)

@app.route('/admin')
def showadmindashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/manageusers', methods=['POST', 'GET'])
@login_required
def manageUsers():
    users = User.query.filter_by(usertype='member').all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/adminlist', methods=['POST', 'GET'])
@login_required
def adminList():
    users = User.query.filter_by(usertype='admin').all()
    return render_template('admin_adminlist.html', users=users)

@app.route('/admin/adminlist/addAdmin', methods=['POST','GET'])
@login_required
def addAdmin():
    users = User.query.filter_by(usertype='admin').all()
    if request.method == 'POST':
        username = request.form['username']
        usermail = request.form['usermail']
        password = request.form['password']
        admin = User(username=username, usermail=usermail, usertype='admin', password=password)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('adminList', users=users))
    else:
        return render_template('admin_addadmin.html')

@app.route('/admin/adminlist/editadmin/<username>', methods=['POST', 'GET'])
@login_required
def editAdmin(username):
    admin = User.query.filter_by(username=username).first()
    users = User.query.filter_by(usertype='admin').all()
    if request.method == 'POST':
        admin.username = request.form['username']
        admin.usermail = request.form['usermail']
        admin.password = request.form['password']
        db.session.commit()
        return redirect(url_for('adminList', users=users))
    else:
        return render_template('admin_editadmin.html', user=admin)

@app.route('/admin/managecourses')
@login_required
def managecourses():
    courses = Course.query.order_by(Course.courseid).all()
    return render_template('admin_courses.html', courses=courses)

@app.route('/admin/managecourses/addcourse', methods=['POST','GET'])
@login_required
def addcourse():
    if request.method =='POST':
        coursename = request.form['coursename']
        description = request.form['description']
        course = Course(coursename=coursename, coursedesc=description)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('managecourses'))
    else:
        return render_template('admin_addcourse.html')

@app.route('/admin/managecourses/removecourse/<courseid>', methods=['POST','GET'])
@login_required
def removecourse(courseid):
    if request.method =='POST':
        course = Course.query.filter_by(courseid=courseid).first()
        db.session.delete(course)
        db.session.commit()
        return redirect(url_for('managecourses'))

@app.route('/admin/managecourses/editcourse/<courseid>', methods=['POST', 'GET'])
@login_required
def editcourse(courseid):
    if request.method =='POST':
        course = Course.query.filter_by(courseid=courseid).first()
        course.coursename = request.form['coursename']
        course.coursedesc = request.form['coursedesc']
        db.session.commit()
        return redirect(url_for('managecourses'))
    else:
        course = Course.query.filter_by(courseid=courseid).first()
        return render_template('admin_editcourse.html', course=course)

@app.route('/admin/<coursename>')
@login_required
def coursePage(coursename):
    course = Course.query.filter_by(coursename=coursename).first()
    exams = Exam.query.filter_by(courseid = course.courseid).all()
    topics = Topic.query.filter_by(courseid=course.courseid).all()

    return render_template('admin_coursePage.html', course=course, exams=exams, topics=topics)

@app.route('/admin/<coursename>/managetopics')
@login_required
def manageTopics(coursename):
    course = Course.query.filter_by(coursename=coursename).first()
    topics = Topic.query.filter_by(courseid = course.courseid).all()
    return render_template('admin_topics.html', coursename=coursename, topics=topics)

@app.route('/admin/<coursename>/managetopics/addtopic', methods=['POST', 'GET'])
@login_required
def addtopic(coursename):
    if request.method == 'POST':
        topicname = request.form['topicname']
        topicdisc = request.form['discussion']
        course = Course.query.filter_by(coursename=coursename).first()
        topic = Topic(topicname=topicname, topicdisc=topicdisc, courseid=course.courseid)
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('manageTopics', coursename=coursename))
    else:
        return render_template('admin_addtopic.html', coursename=coursename)

@app.route('/admin/<coursename>/managetopics/deletetopic/<topicid>', methods=['POST', 'GET'])
@login_required
def deletetopic(coursename, topicid):
    if request.method == 'POST':
        topic = Topic.query.filter_by(topicid=topicid).first()
        db.session.delete(topic)
        db.session.commit()
    return redirect(url_for('manageTopics', coursename=coursename))

@app.route('/admin/<coursename>/managetopics/edittopic/<topicid>', methods=['POST','GET'])
@login_required
def edittopic(coursename, topicid):
    topic = Topic.query.filter_by(topicid=topicid).first()
    if request.method == 'POST':
        topic.topicname = request.form['topicname']
        topic.topicdisc = request.form['discussion']
        db.session.commit()
        return redirect(url_for('manageTopics', coursename=coursename))
    else:
        return render_template('admin_edittopic.html', coursename=coursename, topic=topic)

@app.route('/admin/<coursename>/managetopics/<topicname>/manageexercises')
@login_required
def manageExercises(coursename, topicname):
    topic = Topic.query.filter_by(topicname=topicname).first()
    exercises = Exercise.query.filter_by(topicid=topic.topicid).all()
    return render_template('admin_exercises.html', topic=topic, coursename=coursename, exercises=exercises)

@app.route('/admin/<coursename>/managetopics/<topicname>/manageexercises/addexercise', methods=['POST','GET'])
@login_required
def addExercise(coursename, topicname):
    topic = Topic.query.filter_by(topicname=topicname).first()
    if request.method == 'POST':
        exercise = Exercise(topicid=topic.topicid)
        db.session.add(exercise)
        db.session.commit()
        questions = exercise.questions
        return redirect(url_for('exercisePage',topicname=topicname, coursename=coursename,
                                exerciseid=exercise.exerciseid, questions=questions))

@app.route('/admin/<coursename>/managetopics/<topicname>/manageexercises/<exerciseid>/deleteexercise', methods=['POST', 'GET'])
@login_required
def deleteExercise(coursename, topicname, exerciseid):
    exercise = Exercise.query.filter_by(exerciseid=exerciseid).first()
    db.session.delete(exercise)
    db.session.commit()
    return redirect(url_for('manageExercises', topicname=topicname, coursename=coursename))

@app.route('/admin/<coursename>/managetopics/<topicname>/manageexercises/<exerciseid>', methods=['POST','GET'])
@login_required
def exercisePage(coursename, topicname, exerciseid):
    exercise = Exercise.query.filter_by(exerciseid=exerciseid).first()
    questions=exercise.questions
    return render_template('admin_addexercise.html', topicname=topicname, coursename=coursename, exercise=exercise,
                           questions=questions)

@app.route('/admin/<coursename>/managetopics/<topicname>/manageexercises/<exerciseid>/addexercisequestion', methods=['POST','GET'])
@login_required
def addExerciseQuestion(coursename, topicname, exerciseid):
    exercise = Exercise.query.filter_by(exerciseid=exerciseid).first()
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        difficulty = request.form.get('difficulty')
        questionnew = Question(question=question, answer=answer, difficulty=difficulty)
        db.session.add(questionnew)
        db.session.commit()
        choice1 = Choice(choice=request.form['choice1'], question=questionnew.questionid)
        db.session.add(choice1)
        questionnew.choices.append(choice1)
        choice2 = Choice(choice=request.form['choice2'], question=questionnew.questionid)
        db.session.add(choice2)
        questionnew.choices.append(choice2)
        choice3 = Choice(choice=request.form['choice3'], question=questionnew.questionid)
        db.session.add(choice3)
        questionnew.choices.append(choice3)
        exercise.questions.append(questionnew)
        db.session.commit()
        questions = exercise.questions
        return redirect(url_for('exercisePage', topicname=topicname, coursename=coursename, exerciseid=exerciseid,
                           questions=questions))
    return render_template('admin_addexercisequestion.html', topicname=topicname, coursename=coursename,
                            exerciseid=exerciseid)

@app.route('/admin/<coursename>/managetopics/<topicname>/manageexercises/<exerciseid>/addexercisequestion/<questionid>/editquestion', methods=['POST','GET'])
@login_required
def editExerciseQuestion(coursename, topicname, exerciseid, questionid):
    question = Question.query.filter_by(questionid=questionid).first()
    achoices = Choice.query.filter_by(question=questionid).all()
    exercise = Exercise.query.filter_by(exerciseid=exerciseid).first()
    choices = question.choices

    if request.method == 'POST':
        achoices[0].choice = request.form['choices1']
        achoices[1].choice = request.form['choices2']
        achoices[2].choice = request.form['choices3']
        question.question = request.form['question']
        question.answer = request.form['answer']
        question.difficulty = request.form.get('difficulty')
        db.session.commit()
        questions = exercise.questions
        return redirect(url_for('exercisePage', coursename=coursename, exerciseid=exerciseid, topicname=topicname,
                                questions=questions))
    else:
        return render_template('admin_editexercisequestion.html', coursename=coursename, exerciseid=exerciseid, question=question,
                               choices=choices, topicname=topicname)

@app.route('/admin/<coursename>/managetopics/<topicname>/manageexercises/<exerciseid>/addexercisequestion/<questionid>/deletequestion', methods=['POST','GET'])
@login_required
def deleteExerciseQuestion(coursename, topicname, exerciseid, questionid):
    question = Question.query.filter_by(questionid=questionid).first()
    choices1 = question.choices
    choices2 = Choice.query.filter_by(question=questionid).all()
    for i in choices1:
        question.choices.remove(i)
        db.session.commit()
    for j in choices2:
        db.session.delete(j)
        db.session.commit()

    db.session.delete(question)
    db.session.commit()
    exercise = Exercise.query.filter_by(exerciseid=exerciseid).first()
    questions = exercise.questions
    return redirect(url_for('exercisePage', coursename=coursename, exerciseid=exerciseid, topicname=topicname, questions=questions))

@app.route('/admin/<coursename>/manageexams', methods=['POST', 'GET'])
@login_required
def manageExams(coursename):
    course = Course.query.filter_by(coursename=coursename).first()
    exams = Exam.query.filter_by(courseid=course.courseid).all()
    return render_template('admin_exam.html', exams=exams, coursename=coursename)

@app.route('/admin/<coursename>/manageexams/addexam', methods=['POST', 'GET'])
@login_required
def addexam(coursename):
    if request.method == 'POST':
        examtype = request.form.get("examtype")
        course = Course.query.filter_by(coursename=coursename).first()
        examtest = Exam.query.filter_by(courseid=course.courseid, examtype=examtype).first()
        if examtest is None:
            exam = Exam(examtype=examtype, courseid=course.courseid)
            db.session.add(exam)
            db.session.commit()
            return redirect(url_for('manageExamQuestions', examid=exam.examid, coursename=coursename))
        else:
            return redirect(url_for('manageExams', coursename=coursename))
    else:
        return redirect(url_for('manageExams', coursename=coursename))
@app.route('/admin/<coursename>/manageexams/deleteexam/<examid>', methods=['POST', 'GET'])
@login_required
def deleteexam(coursename, examid):
    if request.method == 'POST':
        exam = Exam.query.filter_by(examid=examid).first()
        db.session.delete(exam)
        db.session.commit()
        return redirect(url_for('manageExams', coursename=coursename))
    else:
        return redirect(url_for('manageExams', coursename=coursename))

@app.route('/admin/<coursename>/manageexams/<examid>/managequestions', methods=['POST','GET'])
@login_required
def manageExamQuestions(coursename, examid):
    exam = Exam.query.filter_by(examid=examid).first()
    questions = exam.questions

    return render_template('admin_examquestion.html', exam=exam, coursename=coursename, questions=questions)

@app.route('/admin/<coursename>/manageexams/<examid>/addquestion', methods=['POST','GET'])
@login_required
def addExamQuestion(coursename, examid):
    exam = Exam.query.filter_by(examid=examid).first()
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        difficulty = request.form.get('difficulty')
        questionnew = Question(question=question, answer=answer, difficulty=difficulty)
        db.session.add(questionnew)
        db.session.commit()
        choice1 = Choice(choice=request.form['choice1'], question=questionnew.questionid)
        db.session.add(choice1)
        questionnew.choices.append(choice1)
        choice2 = Choice(choice=request.form['choice2'], question=questionnew.questionid)
        db.session.add(choice2)
        questionnew.choices.append(choice2)
        choice3 = Choice(choice=request.form['choice3'], question=questionnew.questionid)
        db.session.add(choice3)
        questionnew.choices.append(choice3)
        exam.questions.append(questionnew)
        db.session.commit()
        return redirect(url_for('manageExamQuestions', coursename=coursename, examid=exam.examid))
    return render_template('admin_addexamquestion.html', coursename=coursename, exam=exam)

@app.route('/admin/<coursename>/manageexams/<examid>/managequestions/<questionid>/editquestion', methods=['POST','GET'])
@login_required
def editExamQuestion(coursename, examid, questionid):
    question = Question.query.filter_by(questionid=questionid).first()
    achoices = Choice.query.filter_by(question=questionid).all()
    exam = Exam.query.filter_by(examid=examid).first()
    choices = question.choices

    if request.method == 'POST':
        achoices[0].choice = request.form['choices1']
        achoices[1].choice = request.form['choices2']
        achoices[2].choice = request.form['choices3']
        question.question = request.form['question']
        question.answer = request.form['answer']
        question.difficulty = request.form.get('difficulty')
        db.session.commit()
        questions = exam.questions
        return redirect(url_for('manageExamQuestions', coursename=coursename, examid=examid, questions=questions))
    else:
        return render_template('admin_editexamquestion.html', coursename=coursename, exam=exam, question=question, choices=choices)



@app.route('/admin/<coursename>/manageexams/<examid>/managequestions/<questionid>/deletequestion', methods=['POST','GET'])
@login_required
def deleteExamQuestion(coursename, examid, questionid):
    question= Question.query.filter_by(questionid=questionid).first()
    choices1 = question.choices
    choices2 = Choice.query.filter_by(question=questionid).all()
    for i in choices1:
        question.choices.remove(i)
        db.session.commit()
    for j in choices2:
        db.session.delete(j)
        db.session.commit()

    db.session.delete(question)
    db.session.commit()
    exam = Exam.query.filter_by(examid=examid).first()
    questions = exam.questions
    return redirect(url_for('manageExamQuestions', coursename=coursename, examid=examid, questions=questions))

@app.route('/admin/games')
@login_required
def adminGames():
    typinggametest = Game.query.filter_by(gamename='typingGame').first()
    matchinggametest = Game.query.filter_by(gamename='matchingGame').first()
    machineproblemtest = Game.query.filter_by(gamename='machineProblem').first()
    if typinggametest is None:
        typinggame = Game(gamename='typingGame')
        db.session.add(typinggame)
        db.session.commit()
    if matchinggametest is None:
        matchinggame = Game(gamename='matchingGame')
        db.session.add(matchinggame)
        db.session.commit()
    if machineproblemtest is None:
        machineproblem = Game(gamename='machineProblem')
        db.session.add(machineproblem)
        db.session.commit()

    return render_template('admin_games.html')

@app.route('/admin/games/typinggame')
@login_required
def admintypinggame():
    typinggame = Game.query.filter_by(gamename='typingGame').first()
    questions = typinggame.questions
    return render_template('admin_typinggame.html', typinggame=typinggame, questions=questions)

@app.route('/admin/games/typinggame/addquestion', methods=['POST' , 'GET'])
@login_required
def addTypingQuestion():
    typinggame = Game.query.filter_by(gamename='typingGame').first()
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        difficulty = request.form.get("difficulty")
        newquestion = Question(question=question, answer=answer, difficulty=difficulty)
        db.session.add(newquestion)
        typinggame.questions.append(newquestion)
        db.session.commit()
        return redirect(url_for('admintypinggame'))
    return render_template('admin_typinggamequestion.html')

@app.route('/admin/games/typinggame/editquestion/<questionid>', methods=['POST', 'GET'])
@login_required
def editTypingQuestion(questionid):
    typinggame = Game.query.filter_by(gamename='typingGame').first()
    question = Question.query.filter_by(questionid=questionid).first()
    if request.method == 'POST':
        question.question = request.form['question']
        question.answer = request.form['answer']
        question.difficulty = request.form.get("difficulty")
        db.session.commit()
        return redirect(url_for('admintypinggame'))
    else:
        return render_template('admin_edittypinggamequestion.html', question=question)

@app.route('/admin/games/typinggame/deletequestion/<questionid>', methods=['POST', 'GET'])
@login_required
def deleteTypingQuestion(questionid):
    typinggame = Game.query.filter_by(gamename='typingGame').first()
    question = Question.query.filter_by(questionid=questionid).first()
    typinggame.questions.remove(question)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('admintypinggame'))



@app.route('/admin/managequestions')
@login_required
def manageQuestions():
    return render_template('admin_questions.html')



