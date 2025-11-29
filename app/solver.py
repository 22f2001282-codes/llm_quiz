import asyncio
import requests
import os
from app.browser_client import fetch_rendered_page_and_links
from app.pdf_utils import download_and_sum_pdf_value_column

async def handle_quiz(task):
    url = task["url"]
    email = task["email"]
    secret = task["secret"]

    # 1) Open page & extract rendered HTML + any file links/submit URL
    page_data = await fetch_rendered_page_and_links(url)
    if not page_data:
        return {"error": "could not fetch page data"}

    # 2) If there's a PDF, process it (example: sum 'value' column on page 2)
    answer = None
    if page_data.get("pdf_url"):
        try:
            answer = download_and_sum_pdf_value_column(page_data["pdf_url"])
        except Exception as e:
            answer = {"error_parsing_pdf": str(e)}

    # 3) Prepare submit payload
    submit_json = {
        "email": email,
        "secret": secret,
        "url": url,
        "answer": answer
    }

    # 4) If submit_url present, send answer (best-effort)
    submit_url = page_data.get("submit_url")
    if submit_url:
        try:
            r = requests.post(submit_url, json=submit_json, timeout=20)
            return {"submitted": True, "status_code": r.status_code, "response": r.text}
        except Exception as e:
            return {"submitted": False, "error": str(e), "payload": submit_json}
    else:
        return {"submitted": False, "reason": "no submit_url found", "payload": submit_json}
