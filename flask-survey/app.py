from flask import Flask, request, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret" 
debug=DebugToolbarExtension(app) 
from surveys import *

questions = satisfaction_survey.questions
responses = ["" for q in questions]
title = satisfaction_survey.title


@app.route('/')
def start_survey(): 
    """displays survey title, instructions, and start survey button"""
    instructions = satisfaction_survey.instructions
    return render_template("start_survey.html", title=title, instructions=instructions)


@app.route('/question/<int:qnum>')
def show_question(qnum):
    """displays current question, list of answer choices, selection will fire off POST request to /answer, redirect user if they have not answered previous questions"""
    question = questions[qnum].question
    choices = questions[qnum].choices
    
    if questions[-1].question == question: 
        last = True
    else: 
        last = False

    if not qnum == responses.index(""):
        previous = f'/question/{responses.index("")}'
        flash('You are trying to access an invalid question. You must answer survey questions in order.')
        return redirect(previous)
    elif not responses[-1] == "":
        flash('You have already answered all survey questions.')
        return redirect('/thanks')
    else: 
        return render_template("question.html", title=f'Survey Question {qnum+1}', question=question, choices=choices, qnum=qnum, last=last)


@app.route('/answer/<int:qnum>', methods=["POST"])
def post_answer(qnum):
    """add answer to responses list, redirect to next question"""
    answer = request.form[str(qnum)]
    responses[qnum] = answer
    if qnum == len(responses) - 1:
        next = f'/thanks'
    else:
        next = f'/question/{qnum+1}'
    return redirect(next)

@app.route('/thanks')
def thanks():
    """thank user for filling out survey"""
    return render_template('thanks.html', title=title)