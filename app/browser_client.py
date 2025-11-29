from playwright.async_api import async_playwright
import re

async def fetch_rendered_page_and_links(url: str, timeout_ms: int = 60000):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, timeout=timeout_ms)
        await page.wait_for_load_state("networkidle")
        content = await page.content()

        # Find pdf links on the page (simple heuristic)
        pdf_links = await page.eval_on_selector_all("a[href$='.pdf']", "els => els.map(e=>e.href)")
        pdf_url = pdf_links[0] if pdf_links else None

        # Try to find a submit URL (form action or links containing 'submit')
        submit_url = None
        form_actions = await page.eval_on_selector_all("form[action]", "els => els.map(e=>e.action)")
        if form_actions:
            submit_url = form_actions[0]
        else:
            anchors = await page.eval_on_selector_all("a", "els => els.map(e=>e.href)")
            for a in anchors:
                if a and ('submit' in a or 'answer' in a):
                    submit_url = a
                    break

        await browser.close()
        return {"html": content, "pdf_url": pdf_url, "submit_url": submit_url}
