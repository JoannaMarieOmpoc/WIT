from flask import render_template, request, redirect, url_for
from forms import CourseForm, TopicsForm
from app import Topics
import app
from app import db


@app.route('/', methods=['GET', 'POST'])
def topics():
    result1 = Topics.query.order_by(Topics.topicname)
    return render_template('topics.html', topics=result1, form=form)


@app.route('/add', methods=['POST', 'GET'])
def addtopics():
    form = TopicsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            topics = Topics(topicname=form.topicname.data, topicdisc=form.topicdisc.data)
            db.session.add(topics)
            db.session.commit()
            result = Topics.query.order_by(Topics.topicname)
            form1 = SearchForm()
            return redirect(url_for('topics', topics=result, form=form1))
    return render_template('addtopics.html', form=form)


@app.route('/edit/<topicid>', methods=['POST', 'GET'])
def edittopics(topicid):
    topics = Topics.query.filter_by(id=topicid).first()
    form = TopicsForm()
    if form.validate_on_submit():
        topics.topicname = form.topicname.data
        topics.topicdisc = form.topicdisc.data
        db.session.add(topics)
        db.session.commit()
        result = Topics.query.order_by(Topics.topicname)
        form1 = SearchForm()
        return redirect(url_for('topics', topics=result, form=form1))
    else:

        form.topicname.data = topics.topicname
        form.topicdisc.data = topics.topicdisc
    return render_template('addtopics.html', form=form)


@app.route('/delete/<topicid>', methods=['GET', 'POST'])
def remove(topicid):
    result = Topics.query.filter_by(id=topicid).first()
    db.session.delete(result)
    db.session.commit()
    topics = Topics.query.order_by(Topics.topicname)
    form = SearchForm()
    return redirect(url_for('topics', topics=topics, form=form))


if __name__ == '__main__':
    app.run()