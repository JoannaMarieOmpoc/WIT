from app import app
from forms import TopicsForm
from models import Topics
from flask import Flask, render_template, request, redirect, url_for
from app import db


@app.route('/', methods=['GET', 'POST'])
def topics():
    result1 = Topics.query.order_by(Topics.courseid)
    return render_template('topics.html', topics=result1)


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