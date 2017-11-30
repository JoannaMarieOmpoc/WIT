from app import app,db

class Course(db.Model):
    __tablename__ = "course"

    courseId = db.Column(db.Integer, primary_key=True)
    courseName = db.Column(db.String(50), nullable=False)
    courseDesc = db.Column(db.String(500), nullable=False)

    def __init__(self, courseId, courseName, courseDesc):
        self.courseId = courseId
        self.courseName = courseName
        self.courseDesc = courseDesc

    def __repr__(self):
        return '<courseName {}>'.format(self.courseName)


db.create_all()
app.debug = True