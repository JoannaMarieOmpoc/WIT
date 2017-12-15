from app import app, db, lm
from flask import Flask, render_template, redirect, request, url_for
from models import User, Course, Topic, Question, Choice, Exam, Exercise
from flask_login import login_required, login_user, logout_user, current_user
from app import db

@lm.user_loader
def getUser(name):
    return User.query.filter_by(username = name).first()

@app.route('/', methods=['POST', 'GET'])
def main():
    '''
    admin = User(username='admin', usermail='admin@gmail.com', usertype='admin', password='adminpass')
    db.session.add(admin)
    db.session.commit()
    '''
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
def enrolledCourses():
    courses = current_user.courses
    return render_template('user_courses.html', courses = courses)

@app.route('/<user>/courses)/<course>')
@login_required
def displayCourse(course):
    topics = Topic.query.filter_by(courseid=course).all()
    return render_template('user_showCourse.html', topics = topics)

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

@app.route('/admin/adminlist/removeadmin/<username>', methods=['POST', 'GET'])
@login_required
def removeadmin(username):
    users = User.query.filter_by(usertype='admin').all()
    if request.method == 'POST':
        admin = User.query.filter_by(username=username).first()
        db.session.add(admin)
        db.session.commit()
    return redirect(url_for(adminList, users=users))


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



@app.route('/admin/managequestions')
@login_required
def manageQuestions():
    return render_template('admin_questions.html')



