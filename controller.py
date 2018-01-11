from app import app, db, lm
from flask import Flask, render_template, redirect, request, url_for, json
from models import User, Course, Topic, Question, Choice, Exam, Exercise, Game, userTakesExercise, userTakesExam, userTakesGame
from flask_login import login_required, login_user, logout_user, current_user
from app import db
import random
from ast import literal_eval

################################################################()

@lm.user_loader
def getUser(name):
    return User.query.filter_by(username=name).first()

################################################################()

@app.route('/', methods=['POST', 'GET'])
def main():
    
    typinggametest = Game.query.filter_by(gamename='Typing').first()
    matchinggametest = Game.query.filter_by(gamename='Memory').first()
    machineproblemtest = Game.query.filter_by(gamename='Impossible').first()
    
    if typinggametest is None:
        typinggame = Game(gamename='Typing')
        db.session.add(typinggame)
        db.session.commit()
    
    if matchinggametest is None:
        matchinggame = Game(gamename='Memory')
        db.session.add(matchinggame)
        db.session.commit()
    
    if machineproblemtest is None:
        machineproblem = Game(gamename='Impossible')
        db.session.add(machineproblem)
        db.session.commit()
    
    check = User.query.filter_by(usertype='admin').first()
    if check is None:
        admin = User('Admin', 'wit@gmail.com', 'admin', 'adminpass')
        db.session.add(admin)
        db.session.commit()
        return render_template('landing_page.html')
    else:
        return render_template('landing_page.html')

################################################################()

@app.route('/error/<e>', methods=['POST', 'GET'])
def showError(e):
    return render_template('error.html', error=e)

################################################################()

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        if request.form['userpass'] == request.form['userpassconfirm']:
            try:
                user = User(request.form['username'], request.form['usermail'], 'member', request.form['userpass'])
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('.showDashboard', user=current_user.username))
            except Exception as e:
                return redirect(url_for('.showError', e=str(e)))
        else:
            return redirect(url_for('.showError', e = "Fail Signup"))
    else:
        return render_template('landing_page.html')

################################################################()

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['loginname']
            password = request.form['loginpass']
            user = User.query.filter_by(username=username).first()
            if user is not None and user.password == password:
                login_user(user)
                if user.usertype == 'member':
                    return redirect(url_for('.showDashboard', user=current_user.username))
                elif user.usertype == 'admin':
                    return redirect(url_for('.showadmindashboard'))
            else:
                return redirect('/')
        except Exception as e:
            return redirect(url_for('.showError', e=str(e)))
    else:
        return render_template('landing_page.html')

################################################################()

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')

################################################################()

@app.route('/<user>', methods=['POST', 'GET'])
@login_required
def showDashboard(user):
    return render_template('user_dashboard.html', user = user)

################################################################()

@app.route('/<user>/courses')
@login_required
def enrolledCourses(user):
    courses = current_user.courses
    coursesoption = Course.query.order_by().all()
    pro = [];
    count = 0.0
    for course in courses:
        ttopics = Topic.query.filter_by(courseid=course.coursename).count()
        topics = course.topics
        for topic in topics:
            exercise = userTakesExercise.query.filter_by(exer_id=topic.topicname).filter_by(user_id=current_user.username).first()
            if exercise is not None and exercise.score > 0:
                count = count + 1
        progress = (count/ttopics)*100
        pro.append(progress)
    return render_template('user_courses.html', user=user, courses=zip(courses, pro), coursesoption=coursesoption)

################################################################()

@app.route('/<user>/courses/<coursename>')
@login_required
def displayCourse(coursename, user):
    course = Course.query.filter_by(coursename=coursename).first()
    topics = Topic.query.filter_by(courseid=course.coursename).all()
    return render_template('user_showCourse.html', topics = topics, course=course, user=user)

################################################################()

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

################################################################()

@app.route('/<user>/courses/removecourse/<coursename>', methods=['POST', 'GET'])
def userRemovecourse(user, coursename):
    if request.method == 'POST':
        course = Course.query.filter_by(coursename=coursename).first()
        current_user.courses.remove(course)
        db.session.commit()
        return redirect(url_for('enrolledCourses', user=user))

################################################################()

@app.route('/<user>/courses/<coursename>/topic/<topicname>', methods=['POST', 'GET'])
def user_Topic(user, coursename, topicname):
    topic = Topic.query.filter_by(topicname=topicname).first()
    exercises = Exercise.query.filter_by(topicid=topicname).all()
    return render_template('user_Topic.html', topic=topic, coursename=coursename, exercises=exercises, user=user)

################################################################

@app.route('/<user>/courses/<coursename>/topic/<topicname>/saveScoreExercise', methods=['POST'])
@login_required
def saveScore(user, coursename, topicname):
    #data = request.get_json()
    score = request.json['score']
    exerciseid = request.json['e']
    eid = int(exerciseid)
    exercise = Exercise.query.filter_by(exerciseid=eid).first()
    user = User.query.filter_by(username=user).first()
    exercisetaken = userTakesExercise.query.filter_by(exer_id=exercise.topicid).filter_by(user_id=user.username).first()
    if exercisetaken is None:
        result = userTakesExercise(exercise.topicid, user.username, score)
        db.session.add(result)
        db.session.commit()
    else:
        if exercisetaken.score < score:
            exercisetaken.score = score
            db.session.commit()
    return redirect(url_for('user_Topic', user = user, coursename = coursename, topicname=topicname))

################################################################

@app.route('/<user>/courses/<coursename>/topic/<topicname>/exercise/<exerciseid>', methods=['POST', 'GET'])
def user_takeExercise(user, exerciseid, coursename, topicname):
    if request.method == "POST":
        return redirect(url_for('user_takeExercise'))
    else:
        topic = Topic.query.filter_by(topicname=topicname).first()
        exercise = Exercise.query.filter_by(topicid=topic.topicname).first()
        questions = ['q']
        answers =['a']
        length = 1
        data = exercise.questions
        for d in data:
            q = d.question
            a = d.answer
            questions.append(q)
            answers.append(a)
            length = length + 1
        if exercise.gametype == 3:
            return render_template('impossible_game.html',user = user, coursename = coursename, topicname = topicname, questions = questions, answers= answers, length = length, exerciseid=exerciseid)
        elif exercise.gametype == 1:
            return render_template('typing_game.html',user = user, coursename = coursename, topicname = topicname, questions=questions, answers=answers, length = length, exerciseid=exerciseid)
        else:
            return render_template('memory_game.html', user = user, coursename = coursename, topicname = topicname, questions = questions)

################################################################()

@app.route('/<user>/exams')
@login_required
def exams(user):
    user = User.query.filter_by(username=current_user.username).first()
    exams = ()
    courses = user.courses
    for course in courses:
        exams = exams + (course.coursename,)
        examsincourse = Exam.query.filter_by(courseid=course.coursename).all()
        for exam in examsincourse:
            exams = exams + (exam,)
    print(exams)
    return render_template('user_exams.html', user=user, exams=exams, courses=courses)


################################################################

@app.route('/<user>/exams/<examid>')
def user_takeExams(user, examid):
    exam = Exam.query.filter_by(examid=examid).first()
    choices = ()
    choices2 = ()
    num = 1
    questions = exam.questions
    random.shuffle(questions)
    print(questions)
    orderquestion = ()
    innerchoices = ()
    for question in questions:
        randomchoice = ()
        choices = choices + (question.question,)
        orderquestion = orderquestion + (question.question,)
        randomchoice = randomchoice + (question.answer,)
        for choice in question.choices:
            randomchoice = randomchoice + (choice.choice,)
            innerchoices = innerchoices + (choice,)
            if len(randomchoice) == 4:
                list2 = list(randomchoice)
                random.shuffle(list2)
                tuple2 = tuple(list2)
                choices = choices + tuple2

    print(choices)
    print(innerchoices)
    if len(choices) > 100:
        list3 = list(choices)
        limit = len(choices) - 100
        for i in range(limit):
            list3.pop()
        tuple3 = tuple(list3)
        choices2 = choices2 + tuple3
        return render_template('exam.html', questions=questions, choices=choices2, exam=exam, num=num)
    print(choices2)
    return render_template('exam.html', questions=questions, choices=list(choices), exam=exam, num=num,
                           user=current_user.username, orderquestion=list(orderquestion), total=len(questions),
                           innerchoices=innerchoices)


################################################################()
@app.route('/<user>/exams/check_exam/<examid>/<total>', methods=['POST', 'GET'])
def check_exam(user, examid, total):
    exam = Exam.query.filter_by(examid=examid).first()
    questions = exam.questions
    ordering = request.form.getlist('ord')
    orderquestion = request.form.getlist('orderquestion')
    print(orderquestion)
    print(list(orderquestion))
    newlist11 = [x.encode('UTF8') for x in ordering]
    newlist22 = [x.encode('UTF8') for x in orderquestion]
    order = newlist11[0]
    order2 = newlist22[0]
    l = literal_eval(str(order))
    l2 = literal_eval(str(order2))
    list1 = []
    print(l)
    list22 = [x.encode('UTF8') for x in l]
    list33 = [x.encode('UTF8') for x in l2]
    print(list22)
    print(list33)
    chosen_answer = ()
    correct_answers = ()
    wrong_answers = ()
    for i in range(int(total)):
        choice_data = request.form.get('choice%d' % i)
        print(choice_data)
        if choice_data is None:
            continue
        else:
            chosen_answer = chosen_answer + (choice_data,)
            list1 = list(chosen_answer)
            print(chosen_answer)
            print(list1)

    newlist = [x.encode('UTF8') for x in list1]
    newtuple = tuple(newlist)
    for q in questions:
        print("answer:" + q.answer)
        for i in newtuple:
            print("i:" + i)
            if i == q.answer:
                correct_answers = correct_answers + (i,)
    for i in correct_answers:
        newlist.remove(i)
    listforwrong = newlist
    tuplewr = tuple(listforwrong)
    wrong_answers = wrong_answers + tuplewr
    print(questions[0])
    percentage = len(correct_answers)/int(total)
    takenexam = userTakesExam.query.filter_by(exam_id=exam.examid).filter_by(user_id=current_user.username).first()
    if takenexam is None:
        examresult = userTakesExam(exam.examid, current_user.username, percentage)
        db.session.add(examresult)
        db.session.commit()
    else:
        if takenexam.score < percentage:
            takenexam.score = percentage
            db.session.commit()
    return render_template('check_exam.html', user=current_user.username, choices=list22, exam=exam,
                           questionorder=list33, questions=questions, wrong_answers=wrong_answers,
                           correctanswers=len(correct_answers), correct_answers=correct_answers, total=total)


################################################################()

@app.route('/<user>/games')
@login_required
def games(user):
    return render_template('game.html', user = user)

################################################################()

@app.route('/<user>/profile')
@login_required
def profile(user):
    courses = current_user.courses
    exercisescores = userTakesExercise.query.filter_by(user_id=user).all()
    examscores = userTakesExam.query.filter_by(user_id=user).all()
    return render_template('user_profile.html', user = user, exercisescores = exercisescores, examscores=examscores)

################################################################

@app.route('/<user>/games/impossible')
@login_required
def impossible(user):
    return render_template('impossible_game.html', user=user, questions = game.questions)

################################################################

@app.route('/<user>/games/typing', methods=['POST'])
@login_required
def typing(user):
    return render_template('typing_game.html', user=user, questions = game.questions)

################################################################

@app.route('/<user>/games/memory')
@login_required
def memory(user):
    game = Game.query.filter_by(gamename='Memory').first()
    gameid = game.gameid
    questions = game.questions
    return render_template('memory_game.html', user=user, questions = game.questions, gameid = gameid)

################################################################

@app.route('/admin')
def showadmindashboard():
    return render_template('admin_dashboard.html')

################################################################

@app.route('/admin/manageusers', methods=['POST', 'GET'])
@login_required
def manageUsers():
    users = User.query.filter_by(usertype='member').all()
    return render_template('admin_users.html', users=users)

################################################################

@app.route('/admin/adminlist', methods=['POST', 'GET'])
@login_required
def adminList():
    users = User.query.filter_by(usertype='admin').all()
    return render_template('admin_adminlist.html', users=users)

################################################################

@app.route('/admin/adminlist/addAdmin', methods=['POST', 'GET'])
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

################################################################

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

################################################################

@app.route('/admin/adminlist/removeadmin/<username>', methods=['POST', 'GET'])
@login_required
def removeadmin(username):
    users = User.query.filter_by(usertype='admin').all()
    if request.method == 'POST':
        admin = User.query.filter_by(username=username).first()
        db.session.delete(admin)
        db.session.commit()
        return redirect(url_for(adminList, users=users))

################################################################

@app.route('/admin/managecourses')
@login_required
def managecourses():
    courses = Course.query.order_by(Course.coursename).all()
    return render_template('admin_courses.html', courses=courses)

################################################################

@app.route('/admin/managecourses/addcourse', methods=['POST', 'GET'])
@login_required
def addcourse():
    if request.method == 'POST':
        coursename = request.form['coursename']
        description = request.form['description']
        course = Course(coursename=coursename, coursedesc=description)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('managecourses'))
    else:
        return render_template('admin_addcourse.html')

################################################################

@app.route('/admin/managecourses/removecourse/<coursename>', methods=['POST', 'GET'])
@login_required
def removecourse(coursename):
    if request.method == 'POST':
        course = Course.query.filter_by(coursename=coursename).first()
        db.session.delete(course)
        db.session.commit()
        return redirect(url_for('managecourses'))

################################################################

@app.route('/admin/managecourses/editcourse/<coursename>', methods=['POST', 'GET'])
@login_required
def editcourse(courseid):
    if request.method == 'POST':
        course = Course.query.filter_by(coursename=coursename).first()
        course.coursename = request.form['coursename']
        course.coursedesc = request.form['coursedesc']
        db.session.commit()
        return redirect(url_for('managecourses'))
    else:
        course = Course.query.filter_by(coursename=coursename).first()
        return render_template('admin_editcourse.html', course=course)

################################################################

@app.route('/admin/<coursename>')
@login_required
def coursePage(coursename):
    course = Course.query.filter_by(coursename=coursename).first()
    exams = Exam.query.filter_by(courseid=course.coursename).all()
    topics = Topic.query.filter_by(courseid=course.coursename).all()
    return render_template('admin_coursePage.html', course=course, exams=exams, topics=topics)

################################################################

@app.route('/admin/<coursename>/managetopics')
@login_required
def manageTopics(coursename):
    course = Course.query.filter_by(coursename=coursename).first()
    topics = Topic.query.filter_by(courseid=course.coursename).all()
    return render_template('admin_topics.html', coursename=coursename, topics=topics)

################################################################

@app.route('/admin/<coursename>/managetopics/addtopic', methods=['POST', 'GET'])
@login_required
def addtopic(coursename):
    if request.method == 'POST':
        topicname = request.form['topicname']
        topicdisc = request.form['discussion']
        course = Course.query.filter_by(coursename=coursename).first()
        topic = Topic(topicname=topicname, topicdisc=topicdisc, courseid=course.coursename)
        db.session.add(topic)
        db.session.commit()
        exercise = Exercise(topicid=topicname, gametype=request.form['type'])
        db.session.add(exercise)
        db.session.commit()
        topic.exercises.append(exercise)
        db.session.commit()
        course = Course.query.filter_by(coursename=coursename).first()
        ttopics = Topic.query.filter_by(courseid=coursename).count()
        topics = course.topics
        count = 0
        for topic in topics:
            exercises = topic.exercises
            for exercise in exercises:
                scores = userTakesExercise.query.filter_by(exer_id=exercise.exerciseid).all()
                for score in scores:
                    if score is not None and score.score > 0:
                        count = count + 1
        course.progress = (count/ttopics)*100
        db.session.commit()
        return redirect(url_for('manageTopics', coursename=coursename))
    else:
        types = Game.query.all()
        return render_template('admin_addtopic.html', coursename=coursename, types = types)

################################################################

@app.route('/admin/<coursename>/managetopics/deletetopic/<topicname>', methods=['POST', 'GET'])
@login_required
def deletetopic(coursename, topicname):
    if request.method == 'POST':
        topic = Topic.query.filter_by(topicname=topicname).first()
        db.session.delete(topic)
        db.session.commit()
        return redirect(url_for('manageTopics', coursename=coursename))

################################################################

@app.route('/admin/<coursename>/managetopics/edittopic/<topicname>', methods=['POST', 'GET'])
@login_required
def edittopic(coursename, topicname):
    topic = Topic.query.filter_by(topicname=topicname).first()
    if request.method == 'POST':
        topic.topicname = request.form['topicname']
        topic.topicdisc = request.form['discussion']
        db.session.commit()
        return redirect(url_for('manageTopics', coursename=coursename))
    else:
        return render_template('admin_edittopic.html', coursename=coursename, topic=topic)

################################################################

@app.route('/admin/<coursename>/managetopics/<topicname>/manageexercises', methods=['POST', 'GET'])
@login_required
def manageExercises(coursename, topicname):
    topic = Topic.query.filter_by(topicname=topicname).first()
    if request.method == 'POST':
        exercises = topic.exercises
        for exercise in exercises:
            exercise.gametype = request.form['type']
            db.session.commit()
        return redirect(url_for('manageTopics', coursename=coursename, topicname=topicname))
    else:
        exercise = Exercise.query.filter_by(topicid=topic.topicname).first()
        game = Game.query.get(exercise.gametype)
        gametype = game.gamename
        games = Game.query.all()
        return render_template('admin_exercises.html', topicname=topicname, coursename=coursename, exercise=exercise, gametype=gametype, games=games)

################################################################

@app.route('/admin/<coursename>/managetopics/<topicname>/manageexercises/<exerciseid>/deleteexercise',
           methods=['POST', 'GET'])
@login_required
def deleteExercise(coursename, topicname, exerciseid):
    exercise = Exercise.query.filter_by(exerciseid=exerciseid).first()
    db.session.delete(exercise)
    db.session.commit()
    return redirect(url_for('manageExercises', topicname=topicname, coursename=coursename))

################################################################

@app.route('/admin/<coursename>/managetopics/<topicname>/manageexercises/<exerciseid>', methods=['POST', 'GET'])
@login_required
def exercisePage(coursename, topicname, exerciseid):
    exercise = Exercise.query.filter_by(exerciseid=exerciseid).first()
    questions = exercise.questions
    return render_template('admin_addexercise.html', topicname=topicname, coursename=coursename, exercise=exercise,
                       questions=questions)

################################################################

@app.route('/admin/<coursename>/managetopics/<topicname>/manageexercises/<exerciseid>/manageexercisequestion',
           methods=['POST', 'GET'])
@login_required
def manageExerciseQuestion(coursename, topicname, exerciseid):
    exercise = Exercise.query.filter_by(exerciseid=exerciseid).first()
    if request.method == 'POST':
        question = Question.query.get(request.form['action'])
        exercise.questions.remove(question)
        db.session.commit()
        return redirect(url_for('exercisePage', topicname=topicname, coursename=coursename, exerciseid=exerciseid))
    else:
        return render_template('admin_manageexercisequestions.html', topicname=topicname, coursename=coursename,
                       exerciseid=exerciseid)

################################################################

@app.route('/admin/<coursename>/managetopics/<topicname>/manageexercises/<exerciseid>/manageexercisequestion/addquestion', methods=['POST', 'GET'])
@login_required
def addExerciseQuestion(coursename, topicname, exerciseid):
    exercise = Exercise.query.filter_by(exerciseid=exerciseid).first()
    if request.method == 'POST':
        question = Question.query.get(request.form['action'])
        exercise.questions.append(question)
        db.session.commit()
        return redirect(url_for('exercisePage', topicname=topicname, coursename=coursename, exerciseid=exerciseid))
    else:
        questions = Question.query.filter_by(topic_id=topicname).all()
        return render_template('admin_addexercisequestion.html', topicname=topicname, coursename=coursename,
                       exerciseid=exerciseid, questions=questions)

################################################################

@app.route('/admin/<coursename>/manageexams', methods=['POST', 'GET'])
@login_required
def manageExams(coursename):
    course = Course.query.filter_by(coursename=coursename).first()
    exams = Exam.query.filter_by(courseid=course.coursename).all()
    return render_template('admin_exam.html', exams=exams, coursename=coursename)

################################################################

@app.route('/admin/<coursename>/manageexams/addexam', methods=['POST', 'GET'])
@login_required
def addexam(coursename):
    if request.method == 'POST':
        examtype = request.form.get("examtype")
        course = Course.query.filter_by(coursename=coursename).first()
        examtest = Exam.query.filter_by(courseid=course.coursename, examtype=examtype).first()
        if examtest is None:
            exam = Exam(examtype=examtype, courseid=course.coursename)
            db.session.add(exam)
            db.session.commit()
            course.exams.append(exam)
            return redirect(url_for('manageExamQuestions', examid=exam.examid, coursename=coursename))
        else:
            return redirect(url_for('manageExams', coursename=coursename))
    else:
        return redirect(url_for('manageExams', coursename=coursename))

################################################################

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

################################################################

@app.route('/admin/<coursename>/manageexams/<examid>/managequestions', methods=['POST', 'GET'])
@login_required
def manageExamQuestions(coursename, examid):
    exam = Exam.query.filter_by(examid=examid).first()
    listofquestions = ()
    if request.method == "POST":
        delete1 = Question.query.get(request.form['action'])
        exam.questions.remove(delete1)
        db.session.commit()
        questions = Question.query.all()
        examquestions = exam.questions
        for examquestion in examquestions:
            questions.remove(examquestion)
        print(listofquestions)

        return redirect(url_for('addExamQuestions', coursename=coursename, examid=examid, questions=questions,
                                examquestions=examquestions))
    else:
        exam = Exam.query.filter_by(examid=examid).first()
        questions = exam.questions
        topics = Topic.query.all()
        return render_template('admin_examquestion.html', exam=exam, coursename=coursename, questions=questions,
                               topics=topics)


################################################################

@app.route('/admin/<coursename>/manageexams/<examid>/managequestions/addquestions', methods=['POST', 'GET'])
@login_required
def addExamQuestions(coursename, examid):
    exam = Exam.query.filter_by(examid=examid).first()
    listofquestions = ()
    if request.method == 'POST':
        question = Question.query.get(request.form['action'])
        exam.questions.append(question)
        db.session.commit()
        questions = Question.query.all()
        examquestions = exam.questions
        for examquestion in examquestions:
             questions.remove(examquestion)
        return redirect(url_for('addExamQuestions', coursename=coursename, examid=examid, questions=questions,
                                examquestions=examquestions))
    else:
        questions = Question.query.all()
        examquestions = exam.questions
        for examquestion in examquestions:
            questions.remove(examquestion)
        return render_template('admin_addexamquestions.html', coursename=coursename,
                               examid=examid, questions=questions, examquestions=examquestions)


################################################################

@app.route('/admin/managequestions', methods=['POST', 'GET'])
@login_required
def manageQuestions():
    if request.method == "POST":
        qid = request.form['action']
        delete = Question.query.filter_by(questionid=qid).first()
        db.session.delete(delete)
        db.session.commit()
        return redirect(url_for('manageQuestions'))
    else:
        questions = Question.query.all()
        return render_template('admin_questions.html', questions = questions)

################################################################()

@app.route('/admin/games')
@login_required
def adminGames():
    return render_template('admin_games.html')

################################################################

@app.route('/admin/games/impossiblegame', methods=['POST', 'GET'])
@login_required
def manageImpossible():
    game = Game.query.filter_by(gamename='Impossible')
    if request.method == 'POST':
        question = Question.query.get(request.form['remove'])
        game.questions.remove(question)
        db.session.commit()
        return redirect(url_for('adminGames'))
    else:
        questions = game.questions
        return render_template('admin_impossible.html', questions = questions)

################################################################

@app.route('/admin/games/impossiblegame/addquestion', methods=['POST' , 'GET'])
@login_required
def addImpossibleQuestion():
    game = Game.query.filter_by(gamename='typingGame').first()
    if request.method == 'POST':
        question = Question.query.get(request.form['add'])
        return redirect(url_for('manageImposible'))
    else:
        questions = Question.query.all()
        return render_template('admin_impossiblequestion.html', questions = questions)

################################################################

@app.route('/admin/games/typinggame', methods=['POST', 'GET'])
@login_required
def manageTyping():
    game = Game.query.filter_by(gamename='Typing').first()
    if request.method == 'POST':
        question = Question.query.get(request.form['remove'])
        game.questions.remove(question)
        db.session.commit()
        return redirect(url_for('adminGames'))
    else:
        questions = game.questions
        return render_template('admin_typing.html', questions = questions)

################################################################

@app.route('/admin/games/typinggame/addquestion', methods=['POST' , 'GET'])
@login_required
def addTypingQuestion():
    game = Game.query.filter_by(gamename='typingGame').first()
    if request.method == 'POST':
        question = Question.query.get(request.form['select'])
        return redirect(url_for('admintypinggame'))
    else:
        questions = Question.query.all()
        return render_template('admin_typingquestion.html')

################################################################

@app.route('/admin/addquestions', methods=['POST', 'GET'])
@login_required
def addquestions():
    if request.method == "POST":
        question = Question(request.form['question'], request.form['topic'], request.form['difficulty'], request.form['answer'])
        db.session.add(question)
        db.session.commit()
        choice1 = Choice(request.form['choice1'], question.questionid)
        choice2 = Choice(request.form['choice2'], question.questionid)
        choice3 = Choice(request.form['choice3'], question.questionid)
        question.choices.append(choice1)
        question.choices.append(choice2)
        question.choices.append(choice3)
        db.session.commit()
        questions = Question.query.all()
        return redirect(url_for('manageQuestions'))
    else:
        topics = Topic.query.all()
        return render_template('admin_addquestions.html', topics=topics)

################################################################