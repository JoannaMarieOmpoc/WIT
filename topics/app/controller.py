from app import app
from forms import TopicsForm
from models import Topics
from flask import Flask, render_template, request, redirect, url_for
from app import db


@app.route('/', methods=['GET', 'POST'])
def topics():
    result1 = Topics.query.order_by(Topics.courseid)
    return render_template('topics.html', topics=result1)


@app.route('/add', methods=['POST', 'GET'])
def addtopics():
    form = TopicsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            topics = Topics(topicname=form.topicname.data, topicdisc=form.topicdisc.data, courseid=form.courseid.data)
            db.session.add(topics)
            db.session.commit()
            result = Topics.query.order_by(Topics.courseid)
            return redirect(url_for('topics', topics=result, form=form))
    return render_template('addtopics.html', form=form)


@app.route('/edit/<topicid>', methods=['POST', 'GET'])
def editrecords(topicid):
    topics = Topics.query.filter_by(topicid=topicid).first()
    form = TopicsForm()
    if form.validate_on_submit():
        topics.topicname = form.topicname.data
        topics.topicdisc = form.topicdisc.data
        topics.courseid = form.courseid.data
        db.session.add(topics)
        db.session.commit()
        result = Topics.query.order_by(Topics.courseid)
        return redirect(url_for('topics', topics=result, form=form))
    else:

        form.topicname.data = topics.topicname
        form.topicdisc.data = topics.topicdisc
        form.courseid.data = topics.courseid
    return render_template('addtopics.html', form=form)


@app.route('/delete/<topicid>', methods=['GET', 'POST'])
def remove(topicid):
    result = Topics.query.filter_by(topicid=topicid).first()
    db.session.delete(result)
    db.session.commit()
    topics = Topics.query.order_by(Topics.topicname)
    return redirect(url_for('topics', topics=topics))


if __name__ == '__main__':
    app.run()