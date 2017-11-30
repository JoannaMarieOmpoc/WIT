from app import app
from forms import CourseForm
from models import Course
from flask import Flask, render_template, request, redirect, url_for
from app import db

@app.route('/', methods=['GET', 'POST'])
def course():
    result = Course.query.order_by(Course.courseId)
    return render_template('topics.html', course=result)


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
    return render_template('addtopics.html', form=form)


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
    return render_template('addtopics.html', form=form)


@app.route('/delete/<courseId>', methods=['GET', 'POST'])
def remove(courseId):
    result = Course.query.filter_by(courseId=courseId).first()
    db.session.delete(result)
    db.session.commit()
    course = Course.query.order_by(Course.courseName)
    return redirect(url_for('course', course=course))


if __name__ == '__main__':
    app.run()