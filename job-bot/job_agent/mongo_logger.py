import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["job_bot_db"]
collection = db["applied_jobs"]

def log_job(job_title, company, link):
    collection.insert_one({
        "job_title": job_title,
        "company": company,
        "link": link
    })
