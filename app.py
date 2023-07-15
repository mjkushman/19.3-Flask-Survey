from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

RESPONSES = []

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


@app.route("/questions/<question_num>")
def show_question(question_num):
    if int(question_num) != len(RESPONSES):
        flash("Please answer this question before proceeding.",'error')
        return redirect (f'/questions/{len(RESPONSES)}')
    
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
    
    response = request.form['answer'] # type: ignore
    RESPONSES.append(response)

    if len(RESPONSES) >= len(satisfaction_survey.questions):
        return redirect('/thankyou')
    else:
        return redirect (f'/questions/{len(RESPONSES)}')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')