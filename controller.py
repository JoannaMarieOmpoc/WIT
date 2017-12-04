from app import app, db, lm
from flask import render_template, redirect, request, url_for
from model import User, Course, Topic, Question, Choice, Exam, Exercise
from flask_login import login_required, login_user, logout_user, current_user

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
					return redirect(url_for('.showAdminDashboard'))
			except Exception as e:
				return redirect(url_for('.showError', e = str(e)))
		else:
			#flash('Failed Password Confirmation!')
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
			print user
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

@app.route('/<user>/myCourses')
@login_required
def enrolledCourses(user):
	return render_template('user_courses.html', user = user)

@app.route('/<user>/about')
@login_required
def about(user):
	return render_template('about.html', user = user)

@app.route('/<user>/games')
@login_required
def games(user):
	return render_template('user_games.html', user = user)

@app.route('/<user>/profile')
@login_required
def profile(user):
	return render_template('user_profile.html', user = user)

@app.route('/admin')
@login_required
def showAdminDashboard():
	return return_template('admin_dashboard.html')

@app.route('/admin/manageusers', methods=['POST', 'GET'])
@login_required
def manageUsers():
	return render_template('admin_users.html')

@app.route('/admin/managecourses')
@login_required
def manageCourses():
	return render_template('admin_courses.html')

@app.route('/admin/managecourses/managetopics')
@login_required
def manageTopics():
	return render_template('admin_topics.html')

@app.route('/admin/managecourses/managetopics/manageexercises')
@login_required
def manageTopics():
	return render_template('admin_exercises.html')

@app.route('/admin/managecourses/manageexams')
@login_required
def manageExams():
	return render_template('admin_exams.html')

@app.route('/admin/managequestions')
@login_required
def manageQuestions():
	return render_template('admin_questions.html')



