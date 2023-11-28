from flask import Flask, render_template, request, redirect, url_for, session
from typing import Final
import json
import random
import os

app = Flask(__name__)
app.secret_key = 'Thiss iss my ssecret key.'

correct_STR: Final = 'correct'
correct_message_STR: Final = 'Correct!'
error_STR: Final = 'error'
feedback_STR: Final = 'feedback'
feedback_class_STR: Final = 'feedback_class'
got_question_STR: Final = 'got_question'
quantity_STR: Final = 'og_quantity'
quiz_html_STR: Final = 'quiz.html'
selected_file_STR: Final = 'selected_file'
success_STR: Final = 'success'
remaining_questions_STR: Final = 'remaining_questions'


# Routes and logic here
@app.route('/')
def index():
    # List only JSON files in the current directory
    files = [f for f in os.listdir('./') if f.endswith('.json')]
    print(files)
    return render_template('index.html', files=files)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # If coming from the index page with a file selected
        if 'selected_file' in request.form:
            session.clear()
            selected_file = request.form['selected_file']
            questions_data = load_questions(selected_file)
            question_ids = [question['id'] for question in questions_data]
            session[remaining_questions_STR] = question_ids
            session[selected_file_STR] = selected_file
            session['sum_questions'] = len(questions_data)
            shuffle_questions()
        
        # If submitting an answer
        elif 'answer' in request.form:
            current_question = session['current_question']
            selected_answers = request.form.getlist('answer')
            correct_answers = current_question[correct_STR]
            if set(selected_answers) == set(correct_answers):
                # Correct answer, remove from remaining questions
                pull_new_question()
                session[got_question_STR] = 'Correct!'
                session[feedback_class_STR] = success_STR
            else:
                # Incorrect answer, reset the board!
                errMsg = f"The correct answer was:"
                shuffle_questions()
                session[feedback_STR] = errMsg
                session[feedback_class_STR] = error_STR
                session[got_question_STR] = 'Incorrect.'
                session['correct_options'] = current_question[correct_STR]
        # If requesting the next question, clear feedback
        elif 'next' in request.form:
            session.pop(feedback_STR, None)
            session.pop(feedback_class_STR, None)
            # Check if there are no more questions left
            if len(session[remaining_questions_STR]) == 0:
                # Quiz completed, redirect to a completion page or back to quiz selection
                session.pop(remaining_questions_STR, None)
                session.pop(selected_file_STR, None)
                
    # If there are questions remaining, display the next question
    if remaining_questions_STR in session and session[remaining_questions_STR]:
        current_question = session['current_question']
        random.shuffle(current_question['options']) # Shuffle the options every time so that I have to memorize the answer, not the order
        num_select = len(current_question[correct_STR])
        quiz_title = session[selected_file_STR].rsplit('.', 1)[0] # Extract title from filename
        session['questions_left'] = len(session[remaining_questions_STR])

        return render_template('quiz.html', question=current_question,
                                            quiz_title=quiz_title,
                                            num_select=num_select)
    # No questions remaining, or not started, redirect to index
    else:
        session.pop('current_question', None)
        session.pop('current_quesstion_id', None)
        session.pop(remaining_questions_STR, None)
        session.pop(selected_file_STR, None)
        session.pop(feedback_STR, None)
        session.pop(feedback_STR, None)
        return redirect(url_for('index'))

def load_questions(filename):
    with open(filename, 'r') as file:
        questions = json.load(file)

    for question in questions:
        question['is_multiple_choice'] = len(question[correct_STR]) > 1

    return questions

def load_question():
    session['current_question_id'] = session[remaining_questions_STR][0]
    questions = load_questions(session[selected_file_STR])
    session['current_question'] = [x for x in questions if x['id'] == session['current_question_id']][0]

def pull_new_question():
    session[remaining_questions_STR].pop(0)
    if len(session[remaining_questions_STR]):
        load_question()

def shuffle_questions():
    random.shuffle(session[remaining_questions_STR])
    load_question()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True) # Accessible in the local network