from app import app, db, lm
from flask import Flask, render_template, redirect, request, url_for
from models import User, Course, Topic, Question, Choice, Exam
from flask_login import login_required, login_user, logout_user, current_user
from app import db

@lm.user_loader
def getUser(name):
    return User.query.filter_by(username = name).first()

@app.route('/', methods=['POST', 'GET'])
def main():
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
    return render_template('admin_users.html')

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
    return render_template('admin_coursePage.html', course=course)

@app.route('/admin/managecourses/managetopics')
@login_required
def manageTopics():
    return render_template('admin_topics.html')

@app.route('/admin/managecourses/managetopics/manageexercises')
@login_required
def manageExercises():
    return render_template('admin_exercises.html')

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
        exam = Exam(examtype=examtype, courseid=course.courseid)
        db.session.add(exam)
        db.session.commit()
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

@app.route('/admin/managequestions')
@login_required
def manageQuestions():
    return render_template('admin_questions.html')



