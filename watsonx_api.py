import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
MODEL_ID = os.getenv("WATSONX_MODEL_ID")

def get_iam_token():
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": API_KEY
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]

def generate_quiz(topic):
    token = get_iam_token()

    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "model_id": MODEL_ID,
        "input": f"Generate 5 unique multiple choice questions on the topic '{topic}'. Each question must be different in content and meaning. Include 4 options labeled A, B, C, D. End each with 'Answer: [A/B/C/D]'. Avoid repetition across questions. Return only plain text.",
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 500
        },
        "project_id": PROJECT_ID
    }

    response = requests.post(url, headers=headers, json=data)
    print("RESPONSE JSON:", response.json())  
    try:
        result = response.json().get("results", [{}])[0].get("generated_text")
        return result if result else "No quiz generated"
    except Exception as e:
        return f"Error in response: {str(e)}"
    
def get_watsonx_access_token():
    api_key = os.getenv("WATSONX_API_KEY")
    url = "https://iam.cloud.ibm.com/identity/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "apikey": api_key,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]   
 
def generate_from_watsonx(prompt):
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    headers = {
        "Authorization": f"Bearer {get_watsonx_access_token()}",
        "Content-Type": "application/json"
    }

    payload = {
        "model_id": "ibm/granite-13b-instruct-v2",
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 300
        },
        "project_id": os.getenv("WATSONX_PROJECT_ID")  
    }

    response = requests.post(url, headers=headers, json=payload)
    response_json = response.json()

    # 🛡️ Handle errors safely
    if 'results' in response_json and len(response_json['results']) > 0:
        return response_json['results'][0]['generated_text'].strip()
    elif 'errors' in response_json:
        print(" Watsonx Error:", response_json['errors'])
        return "Sorry, I couldn't generate an explanation. Please try again."
    else:
        print(" Unexpected Watsonx Response:", response_json)
        return "Unexpected response from AI service."
   
def generate_explanation(topic):
    prompt = (
        f"Explain the term '{topic}' in 3-5 simple paragraphs for a high school student. "
        "Avoid using complex jargon. Focus on clear, concise explanation."
    )
    return generate_from_watsonx(prompt)