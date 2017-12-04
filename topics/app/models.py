from app import app, db

class Topics(db.Model):
    __tablename__ = "topics"

    topicid = db.Column(db.Integer, primary_key=True)
    topicname = db.Column(db.String(50), nullable=False)
    topicdisc = db.Column(db.String(1000), nullable=False)
    courseid = db.Column(db.Integer, db.ForeignKey(courses.courseid), nullable=False)

    def __init__(self, topicname, topicdisc, courseid):
        self.topicname = topicname
        self.topicdisc = topicdisc
        self.courseid = courseid

    def __repr__(self):
        return '<topicname {}>'.format(self.topicname)



db.create_all()
app.debug = True

