from app import app
from forms import CourseForm, TopicsForm
from models import Course, Topics, Discussion, Courses, Questions, Exams, Users, stud, take
from flask import Flask, render_template, request, redirect, url_for, session
from app import db

@app.route('/course', methods=['GET', 'POST'])
def course():
    result = Course.query.order_by(Course.courseId)
    return render_template('course.html', course=result)


@app.route('/add', methods=['POST', 'GET'])
def addCourse():
    form = CourseForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            course = Course(courseId = form.courseId.data, courseName= form.courseName.data , courseDesc= form.courseDesc.data)
            db.session.add(course)
            db.session.commit()
            result = Course.query.order_by(Course.courseId)
            return redirect(url_for('course', course=result, form=form))
    return render_template('addcourse.html', form=form)


@app.route('/edit/<courseId>', methods=['POST', 'GET'])
def editCourse(courseId):
    course = Course.query.filter_by(courseId=courseId).first()
    form = CourseForm()
    if form.validate_on_submit():
        course.courseId = form.courseId.data
        course.courseName = form.courseName.data
        course.courseDesc = form.courseDesc.data
        db.session.add(course)
        db.session.commit()
        result = Course.query.order_by(Course.courseId)
        return redirect(url_for('course', course=result, form=form))
    else:
        form.courseId.data = course.courseId
        form.courseName.data = course.courseName
        form.courseDesc.data = course.courseDesc
    return render_template('addcourse.html', form=form)


@app.route('/delete/<courseId>', methods=['GET', 'POST'])
def remove(courseId):
    result = Course.query.filter_by(courseId=courseId).first()
    db.session.delete(result)
    db.session.commit()
    course = Course.query.order_by(Course.courseName)
    return redirect(url_for('course', course=course))




@app.route('/')
def UserHome():
    return render_template('dashboard.html')


@app.route('/courses/<course_name>', methods=['GET', 'POST'])
def courses(course_name):
    course = Courses.query.filter_by(coursename=course_name).one()

    return render_template('course.html', course=course)


@app.route('/mycourses', methods=['GET', 'POST'])
def mycourses():
    user = session.get('user')
    user1 = Users.query.filter_by(userid=1).first()
    courses1 = user1.courses
    return render_template('mycourses.html', courses=courses1)

@app.route('/addcourseopt', methods=['POST'])
def addcourseopt():
    if request.method == 'POST':
        user = session.get('user')
        user1 = Users.query.filter_by(userid=1).first()
        coursename2 = request.form['coursename1']
        coursefind = Courses.query.filter_by(coursename=coursename2).first()
        usercourses = user1.courses
        for i in usercourses:
            if i.coursename is coursefind.coursename:
                return redirect(url_for('mycourses'))

        coursefind.students.append(user1)
        db.session.commit()
        return redirect(url_for('mycourses'))


@app.route('/removecourseopt', methods=['POST'])
def removecourseopt():
    if request.method == 'POST':
        user1 = Users.query.filter_by(userid=1).first()
        coursename1 = request.form['coursename2']
        deletethis = Courses.query.filter_by(coursename=coursename1).first()
        usercourses = user1.courses
        for i in usercourses:
            if i.coursename is deletethis.coursename:
                user1.courses.remove(deletethis)
                db.session.commit()
                return redirect(url_for('mycourses'))

        return redirect(url_for('mycourses'))


@app.route('/adminHome')
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
        examcourse = int(request.form['examcourse'])
        exam = Exams(examid=examid1, examtype=examtype, courseid=examcourse)
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


@app.route('/discussion')
def discussion():
    discussions = Discussion.query.order_by(Discussion.discussionid)
    return render_template('discussion.html', discussions=discussions)

@app.route('/add_discussion', methods=['POST', 'GET'])
def add_discussion():
    if request.method == 'POST':
        discussionid1 = int(request.form['discussionid'])
        discussionname1 = request.form['discussionname']
        discontent1 = request.form['discontent']
        topicid1 = int(request.form['topicid'])
        discussion = Discussion(discussionid=discussionid1, discussionname=discussionname1, discontent=discontent1, topicid=topicid1)
        db.session.add(discussion)
        db.session.commit()
        return redirect('discussion')
    elif request.method == 'GET':
        return render_template('add_discussion.html')
    else:
        return render_template('add_discussion.html')

@app.route('/deletediscussion/<discussionid>', methods=['GET', 'POST'])
def deletediscussion(discussionid):
    discussiondelete = Discussion.query.filter_by(discussionid=discussionid).first()
    db.session.delete(discussiondelete)
    db.session.commit()
    return redirect('discussion')

@app.route('/editdiscussion/<discussionid>', methods=['POST', 'GET'])
def editdiscussion(discussionid):
    if request.method == 'POST':
        discussion = Discussion.query.filter_by(discussionid=discussionid).first()
        discussion.discussionid = int(request.form['discussionid'])
        discussion.discussionname = request.form['discussionname']
        discussion.discontent = request.form['discontent']
        topicid = request.form['topicid']
        topic = Topics.query.filter_by(topicid=topicid).first()
        discussion.topicid = int(topic.topicid)
        db.session.commit()
        return redirect('discussion')
    else:
        discussion = Discussion.query.filter_by(discussionid=discussionid).first()
        return render_template('editdiscussion.html', discussionid=discussionid, discussion=discussion)




#Topics
@app.route('/topics', methods=['GET', 'POST'])
def topics():
    result1 = Topics.query.order_by(Topics.courseid)
    return render_template('topics.html', topics=result1)


@app.route('/addtopics', methods=['POST', 'GET'])
def addtopics():
    form = TopicsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            topics = Topics(topicname=form.topicname.data, topicdisc=form.topicdisc.data, courseid=int(form.courseid.data))
            db.session.add(topics)
            db.session.commit()
            result1 = Topics.query.order_by(Topics.courseid)
            return redirect(url_for('topics', topics=result1, form=form))
    return render_template('addtopics.html', form=form)


@app.route('/edittopics/<topicid>', methods=['POST', 'GET'])
def editrecords(topicid):
    topics = Topics.query.filter_by(topicid=topicid).first()
    form = TopicsForm()
    if form.validate_on_submit():
        topics.topicname = form.topicname.data
        topics.topicdisc = form.topicdisc.data
        topics.courseid = form.courseid.data
        db.session.add(topics)
        db.session.commit()
        result1 = Topics.query.order_by(Topics.courseid)
        return redirect(url_for('topics', topics=result1, form=form))
    else:

        form.topicname.data = topics.topicname
        form.topicdisc.data = topics.topicdisc
        form.courseid.data = topics.courseid
    return render_template('addtopics.html', form=form)


@app.route('/deletetopics/<topicid>', methods=['GET', 'POST'])
def removetopics(topicid):
    result1 = Topics.query.filter_by(topicid=topicid).first()
    db.session.delete(result1)
    db.session.commit()
    topics = Topics.query.order_by(Topics.topicname)
    return redirect(url_for('topics', topics=topics))

if __name__ == '__main__':
    app.run()