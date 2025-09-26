import schedule
import time
import json
from job_agent.email_notifier import send_email_update
from job_agent.mongo_logger import log_job
from job_agent.answer_generator import generate_answer
from playwright.sync_api import sync_playwright

with open("resume.json", "r", encoding="utf-8") as f:
    RESUME_JSON = json.load(f)

RESUME_TEXT = json.dumps(RESUME_JSON)

with open("config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

def search_and_apply(resume_text):
    print("[INFO] Running job search...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.linkedin.com/jobs/search/?keywords=software%20engineer&f_TPR=r3600")
        jobs = page.query_selector_all(".job-card-container")

        for job in jobs:
            title = job.query_selector("h3").inner_text()
            company = job.query_selector("h4").inner_text()
            link = job.query_selector("a").get_attribute("href")

            try:
                posted_text = job.query_selector(".job-search-card__listdate").inner_text()
                if "seconds" not in posted_text.lower() and "minute" not in posted_text.lower():
                    continue
            except:
                continue

            if "fresher" not in title.lower() and CONFIG["experience_level"].lower() not in title.lower():
                continue

            print(f"[INFO] Applying to {title} at {company}")

            job.click()
            page.fill("input[name='name']", RESUME_JSON["name"])
            page.fill("input[name='email']", RESUME_JSON["contact"]["email"])
            page.set_input_files("input[type='file']", "resume.pdf")

            questions = page.query_selector_all(".application-question")
            for q in questions:
                question_text = q.inner_text()
                if "salary" in question_text.lower():
                    answer = CONFIG["expected_salary"]
                elif "availability" in question_text.lower():
                    answer = CONFIG["availability"]
                else:
                    answer = generate_answer(question_text)
                q.fill(answer)

            buttons = page.query_selector_all("button")
            for b in buttons:
                if b.inner_text().lower() in ["submit", "apply", "done"]:
                    b.click()
                    break

            send_email_update(title, company, link)
            log_job(title, company, link)

        browser.close()

schedule.every(30).minutes.do(search_and_apply, RESUME_TEXT)

print("[INFO] Job Agent started! Checking every 30 minutes...")
while True:
    schedule.run_pending()
    time.sleep(10)
