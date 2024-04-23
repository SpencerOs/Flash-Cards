from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from markdown import markdown
from pprint import pprint
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

@app.route('/get_attempts_data', methods=['GET'])
def get_attempts_data():
    # Retrieve the filename from the request parameters
    filename = request.args.get('filename')

    # Constructs the path to the JSON file
    file_path = os.path.join(app.root_path, filename)

    # Initialize an empty list for attempts
    attempts = []
    questions_count = 0

    # Safely load the JSON file
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                attempts = data.get('attempts', []) # Get attempts, default to empty list
                questions = data.get('questions', []) # Get questions
                questions_count = len(questions)
        except json.JSONDecodeError:
            # Handle the cases where the JSON file is not properly formatted
            print(f"Error reading JSON file: {filename}")

    # Send back the attempts data
    return jsonify(attempts=attempts, questionsCount = questions_count)

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
            session['questions_answered'] = 0
            shuffle_questions()
        
        # If submitting an answer
        elif 'answer' in request.form:
            current_question = session['current_question']
            selected_answers = request.form.getlist('answer')
            correct_answers = [opt['text'] for opt in current_question['options'] if opt['isCorrect']]
            session['questions_answered'] += 1
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
        num_select = sum(1 for option in current_question['options'] if option['isCorrect'])
        quiz_title = session[selected_file_STR].rsplit('.', 1)[0] # Extract title from filename
        session['questions_left'] = len(session[remaining_questions_STR])
        return render_template('quiz.html', question=current_question,
                                            quiz_title=quiz_title,
                                            num_select=num_select)
    # No questions remaining, or not started, redirect to index
    else:
        append_attempt()
        session.pop('current_question', None)
        session.pop('current_quesstion_id', None)
        session.pop('questions_answered', None)
        session.pop(remaining_questions_STR, None)
        session.pop(selected_file_STR, None)
        session.pop(feedback_STR, None)
        session.pop(feedback_STR, None)
        return redirect(url_for('index'))
    
def append_attempt():
    with open(session[selected_file_STR], 'r') as file:
        data = json.load(file)
    
    data['attempts'].append(session['questions_answered'])

    with open(session[selected_file_STR], 'w') as file:
        json.dump(data, file, indent=4)

def load_questions(filename):
    with open(filename, 'r') as file:
        questions = json.load(file)['questions']

    for question in questions:
        question['has_matrix'] = 'matrix' in question

    return questions

def load_question():
    session['current_question_id'] = session[remaining_questions_STR][0]
    # We have to pull the questions from the file...
    questions = load_questions(session[selected_file_STR])
    # then we pull the question with the matching id and we're good to go!
    session['current_question'] = [x for x in questions if x['id'] == session['current_question_id']][0]
    session['current_question']['text'] = markdown(session['current_question']['text'], extensions=['fenced_code'])
    for option in session['current_question']['options']:
        option['text'] = markdown(option['text'], extensions=['fenced_code'])
    

def pull_new_question():
    session[remaining_questions_STR].pop(0)
    if len(session[remaining_questions_STR]):
        load_question()

def shuffle_questions():
    random.shuffle(session[remaining_questions_STR])
    load_question()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True) # Accessible in the local network