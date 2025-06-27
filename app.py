from flask import Flask, render_template, request, redirect, session, url_for
from watsonx_api import generate_quiz, generate_explanation
from pinecone_utils import store_student_answer
from user_utils import store_quiz_metadata
from user_utils import get_topic_rankings
from user_utils import save_user_info, get_user_level, set_user_level
import os
import re
import google_auth_oauthlib.flow
import googleapiclient.discovery
import google.oauth2.credentials

app = Flask(__name__)
app.secret_key = 'super_secret_key'

'''@app.route('/')
def index():
    return render_template('index.html')'''
@app.route('/')
def index():
    if 'email' in session:
        if session.get('role') == 'student':
            return redirect(url_for('student_dashboard'))
        elif session.get('role') == 'educator':
            return redirect(url_for('educator_dashboard'))
    return render_template('index.html')

@app.route('/quiz', methods=['POST'])
def quiz():
    topic = request.form['user_input']
    student_id = session.get('email', 'guest_user')
    level = get_user_level(student_id)
    prompt = f"Generate a {level} level multiple choice quiz on the topic: {topic}."
    quiz = generate_quiz(prompt)
    store_student_answer(student_id, quiz)
    store_quiz_metadata(student_id, topic, score=None)  
    return render_template('quiz.html', quiz=quiz)

@app.route('/diagnostic', methods=['GET'])
def diagnostic_topic():
    origin = request.args.get('from', '/')
    return render_template('diagnostic_form.html', origin=origin)

@app.route('/run-diagnostic', methods=['POST'])
def run_diagnostic_quiz():
    topic = request.form['topic']
    student_id = session.get('email', 'guest_user')
    origin = request.form.get('origin', '/')

    prompt = (
        f"Create a 5-question multiple-choice diagnostic test on the topic '{topic}'.\n"
        "Each question must include 4 options labeled A, B, C, D, and end with 'Answer: [A/B/C/D]'."
    )

    raw_quiz = generate_quiz(prompt)
    questions = parse_mcq_questions(raw_quiz)
    
    session['diagnostic_answers'] = [q['answer'] for q in questions]
    session['diagnostic_topic'] = topic
    session['diagnostic_origin'] = origin

    return render_template('diagnostic_quiz_form.html', questions=questions, topic=topic)

@app.route('/submit-diagnostic', methods=['POST'])
def submit_diagnostic():
    student_id = session.get('email', 'guest_user')
    topic = session.get('diagnostic_topic', 'Unknown Topic')
    correct_answers = session.get('diagnostic_answers', [])
    origin = session.pop('diagnostic_origin', '/')

    correct_answers = session.get('diagnostic_answers', [])
    total = len(correct_answers)
    correct = 0

    for i in range(total):
        user_ans = request.form.get(f'q{i}')
        if user_ans == correct_answers[i]:
            correct += 1

    if total == 0:
        error_msg = "Diagnostic quiz was not generated properly. Please try a more academic topic (e.g., Algebra, Biology)."
        return render_template("error.html", error_message=error_msg)

    score_percent = (correct / total) * 100
    if score_percent >= 80:
        level = 'advanced'
    elif score_percent >= 50:
        level = 'intermediate'
    else:
        level = 'beginner'

    set_user_level(student_id, level)
    return render_template('diagnostic_result.html', score=score_percent, level=level.title(), topic=topic, origin=origin)


import re

import re
from difflib import SequenceMatcher

def is_similar(q1, q2, threshold=0.85):
    """Return True if q1 and q2 are semantically similar above threshold."""
    return SequenceMatcher(None, q1.lower(), q2.lower()).ratio() > threshold

def parse_mcq_questions(text):
    questions = []
    seen_questions = []

    current = {}
    option_pattern = re.compile(r"^[A-D][\).]?\s+(.*)")
    lines = text.strip().splitlines()

    for line in lines:
        line = line.strip()

       
        if re.match(r"^\d+\.", line):
            if 'question' in current:
                
                if len(current.get('options', [])) == 4 and 'answer' in current:
                    question_text = current['question']
                    if not any(is_similar(question_text, q['text']) for q in questions):
                        questions.append({
                            'text': question_text,
                            'options': current['options'],
                            'answer': current['answer']
                        })
                current = {}

            current['question'] = line

        elif option_pattern.match(line):
            if 'options' not in current:
                current['options'] = []
            current['options'].append(option_pattern.match(line).group(1).strip())

        elif line.lower().startswith("answer:"):
            current['answer'] = line.split(":")[-1].strip().upper()


    if 'question' in current and len(current.get('options', [])) == 4 and 'answer' in current:
        question_text = current['question']
        if not any(is_similar(question_text, q['text']) for q in questions):
            questions.append({
                'text': question_text,
                'options': current['options'],
                'answer': current['answer']
            })

    return questions

@app.route('/login')
def login():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/classroom.courses.readonly',
                'https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email',
                'openid'],
        redirect_uri='https://topiciq.begetter.me/callback'
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)

@app.route('/callback')
def callback():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json',
        scopes=[
            'https://www.googleapis.com/auth/classroom.courses.readonly',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email',
            'openid'
        ],
        redirect_uri='https://topiciq.begetter.me/callback'
    )
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    from googleapiclient.discovery import build
    service = build('oauth2', 'v2', credentials=credentials)
    user_info = service.userinfo().get().execute()

    session['email'] = user_info.get('email')
    session['name'] = user_info.get('name')
    session['role'] = 'student'

    return redirect(url_for('student_dashboard'))

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

@app.route('/student-dashboard')
def student_dashboard():
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    service = googleapiclient.discovery.build('classroom', 'v1', credentials=credentials)
    courses = service.courses().list().execute().get('courses', [])
    return render_template('student_dashboard.html', name=session['name'], courses=courses)

@app.route('/get-info', methods=['POST'])
def get_info():
    word = request.form.get('concept', '')
    if not word:
        return redirect(url_for('student_dashboard'))

    info = generate_explanation(word)

    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    service = googleapiclient.discovery.build('classroom', 'v1', credentials=credentials)
    courses = service.courses().list().execute().get('courses', [])

    return render_template('student_dashboard.html', name=session.get('name', 'Student'), courses=courses, info=info)

from user_utils import get_topic_rankings

@app.route("/educator-dashboard")
def educator_dashboard():
    rankings = get_topic_rankings()
    return render_template("educator_dashboard.html", rankings=rankings)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", error_message="Internal server error or OAuth failure."), 500

@app.route('/login-success')
def login_success():
    return render_template("login_success.html", name=session.get("name", "User"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
