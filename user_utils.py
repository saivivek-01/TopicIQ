import json
import os

USER_DB = 'users.json'
QUIZ_LOG = 'quiz_log.json'

if not os.path.exists(USER_DB):
    with open(USER_DB, 'w') as f:
        json.dump({}, f)

if not os.path.exists(QUIZ_LOG):
    with open(QUIZ_LOG, 'w') as f:
        json.dump([], f)

def save_user_info(email, name, role):
    with open(USER_DB, 'r+') as f:
        data = json.load(f)
        data[email] = {'name': name, 'role': role, 'level': 'beginner'}
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

def get_user_level(email):
    with open(USER_DB) as f:
        return json.load(f).get(email, {}).get('level', 'beginner')

def set_user_level(email, level):
    with open(USER_DB, 'r+') as f:
        data = json.load(f)
        if email in data:
            data[email]['level'] = level
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()

def store_quiz_metadata(email, topic, score=None):
    with open(QUIZ_LOG, 'r+') as f:
        logs = json.load(f)
        logs.append({'email': email, 'topic': topic, 'score': score})
        f.seek(0)
        json.dump(logs, f, indent=2)
        f.truncate()

'''def get_all_quiz_data():
    with open(QUIZ_LOG) as f:
        return json.load(f)'''
    
from collections import Counter
import json

QUIZ_LOG = "quiz_log.json"  

def get_topic_rankings():
    try:
        with open(QUIZ_LOG, "r") as f:
            quiz_data = json.load(f)
    except FileNotFoundError:
        return []

    topic_counter = Counter()

    for item in quiz_data:
        topic = item.get("topic", "Unknown")
        topic_counter[topic] += 1

    return sorted(topic_counter.items(), key=lambda x: x[1], reverse=True)