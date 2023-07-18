from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecurepassword"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)  # instantiates toolbar

quiz_title = satisfaction_survey.title
instructions = satisfaction_survey.instructions


@app.route("/")
def show_home():
    return render_template(
        "index.html", quiz_title=quiz_title, instructions=instructions
    )

@app.route('/survey-start', methods=['POST'])
def start_survey():
    session['RESPONSES'] =[]
    return redirect (f"/questions/{len(session['RESPONSES'])}")


@app.route("/questions/<question_num>")
def show_question(question_num):
    if int(question_num) != len(session['RESPONSES']):
        flash("Please answer this question before proceeding.",'error')
        return redirect (f"/questions/{len(session['RESPONSES'])}")
    
    current_question = satisfaction_survey.questions[int(question_num)]
    question_text = current_question.question #gets the specific question text
    answer_options = current_question.choices #gets the answer options for this question
    
    
    return render_template(
        "question.html",
        question_num=question_num,
        quiz_title=quiz_title,
        question_text=question_text,
        answer_options=answer_options
    )

@app.route('/answer', methods=['POST'])
def record_answer():
    responses = session['RESPONSES'] #load the stored responses
    response = request.form['answer'] #Get the latest response from the form. type: ignore
    responses.append(response) # add the latest response to the list of responses
    session['RESPONSES'] = responses #update the stored responses with the new list

    if len(session['RESPONSES']) >= len(satisfaction_survey.questions):
        return redirect('/thankyou')
    else:
        return redirect (f"/questions/{len(session['RESPONSES'])}")

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

