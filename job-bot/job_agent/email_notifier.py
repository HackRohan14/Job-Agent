import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_email_update(job_title, company, job_link):
    msg = MIMEText(f"[APPLIED] Applied to {job_title} at {company}\nLink: {job_link}")
    msg["Subject"] = f"Job Applied: {job_title} - {company}"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_USER, msg.as_string())
