import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index("topiciq")  

def store_student_answer(student_id, answer_text):
    embedding = [0.01] * 2048
    index.upsert(vectors=[(student_id, embedding)])