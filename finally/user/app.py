import copy
import flask
import json
import os
import random
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from flask import Flask, session, render_template, url_for, redirect, request, flash





#impossible game
#wala pay timer


app = Flask(__name__)
app.secret_key = os.urandom(24)

questions = { "1" : { "question" : "Which city is the capital of Iran?","options": ["Dhaka","Kabul","Tehran","Istambul"], "answer" : "Tehran"},
              "2" : { "question" : "What is the human bodys biggest organ?", "options": ['The cerebrum','Epidermis','Ribs','The skin'],"answer" : "The skin"},
              "3" : { "question" : "Electric current is typically measured in what units?","options": ['joule','Ampere','Watt','Ohm'], "answer" : "Ampere" },
	      	  "4" : { "question" : "Who was known as Iron man of India?","options": ["Govind Ballabh Pant","Jawaharlal Nehru","Subhash Chandra Bose","Sardar Vallabhbhai Patel"], "answer" : "Sardar Vallabhbhai Patel" },
              "5" : {"question" : "What is the smallest planet in the Solar System?", "options": ["Mercury","Mars","Jupitar","Neptune"],"answer":"Mercury"},
              "6": {'question': "What is the name of the largest ocean on earth?", "options": ["Atlantic","Pacafic", "Indian Ocean","Meditanarian"], "answer": "Pacafic" } ,
              "7": {'question': "What country has the second largest population in the world?", "options": ["Indonasia","America", "India","China"], "answer": "India" },
              "8": {'question': "Zurich is the largest city in what country?", "options": ["France","Spain", "Scotland","Switzerland"], "answer": "Switzerland" }, 
              "9": {'question': "What is the next prime number after 7?", "options": ["13","9", "17","11"], "answer": "11"},
              "10": {'question': "At what temperature is Fahrenheit equal to Centigrade?", "options": ["0 degrees ","-40 degrees", "213 degrees","-213 degrees"], "answer": "-40 degrees"} }


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == "POST":
    if "question" in session:
	    entered_answer = request.form.get('answer', '')
	    if questions.get(session["question"],False):
		    if entered_answer == questions[session["question"]]["answer"]:
			mark = 1
			session["mark"] += mark
			session["question"] = str(int(session["question"])+1)
			alert ("Correct", "success" )
			
		    
		    else:
		      mark = 0
		
		      session["mark"] += mark

		      session["question"] = str(int(session["question"])+1)
		      alert("Oops..Wrong Answer.", "danger")
		      if session["question"] in questions:
			redirect(url_for('index'))
		      else:
			return render_template("score.html", score = session["mark"])
	    else:
		return render_template("score.html", score = session["mark"])
  
  if "question" not in session:
    session["question"] = "1"
    session["mark"] = 0

  elif session["question"] not in questions:
    return render_template("score.html")
  return render_template("quiz.html",
                         question=questions[session["question"]]["question"],
                         question_number=session["question"],
			 options=questions[session["question"]]["options"],
                         score = session["mark"]
                         )

if __name__ == '__main__':
	app.run(debug=True)











#mock exam


app = flask.Flask(__name__)
quiz_dir = 'quizzes'

quizzes = {}
for quiz in os.listdir(quiz_dir):
    print 'Loading', quiz
    quizzes[quiz] = json.loads(open(os.path.join(quiz_dir, quiz)).read())

@app.route('/')
def index():
    return flask.render_template('index.html', quiz_names=zip(quizzes.keys(), map(lambda q: q['name'], quizzes.values())))

@app.route('/quiz/<id>')
def quiz(id):
    if id not in quizzes:
        return flask.abort(404)
    quiz = copy.deepcopy(quizzes[id])
    questions = list(enumerate(quiz["questions"]))
    random.shuffle(questions)
    quiz["questions"] = map(lambda t: t[1], questions)
    ordering = map(lambda t: t[0], questions)

    return flask.render_template('quiz.html', id=id, quiz=quiz, quiz_ordering=json.dumps(ordering))

@app.route('/check_quiz/<id>', methods=['POST'])
def check_quiz(id):
    ordering = json.loads(flask.request.form['ord'])
    quiz = copy.deepcopy(quizzes[id])
    print flask.request.form
    quiz['questions'] = sorted(quiz['questions'], key=lambda q: ordering.index(quiz['questions'].index(q)))
    print quiz['questions']
    answers = dict( (int(k), quiz['questions'][int(k)]['options'][int(v)]) for k, v in flask.request.form.items() if k != 'ord' )

    print answers

    if not len(answers.keys()):
        return flask.redirect(flask.url_for('quiz', id=id))

    for k in xrange(len(ordering)):
        if k not in answers:
            answers[k] = [None, False]

    answers_list = [ answers[k] for k in sorted(answers.keys()) ]
    number_correct = len(filter(lambda t: t[1], answers_list))

    return flask.render_template('check_quiz.html', quiz=quiz, question_answer=zip(quiz['questions'], answers_list), correct=number_correct, total=len(answers_list))


if __name__ == '__main__':
    app.run(debug=True)

