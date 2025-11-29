# LLM Quiz Solver - Starter

This is a starter project for the "LLM Analysis Quiz" task (uses Playwright + FastAPI + optional Gemini calls).

## Quick start (local)

1. Create and activate virtualenv:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   playwright install
   ```

2. Copy `.env.example` to `.env` and fill values:
   ```
   cp .env.example .env
   # edit .env and add GEMINI_API_KEY and MY_SECRET
   ```

3. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Test:
   Use an HTTP client (curl/Postman) to POST JSON to `http://localhost:8000/solve`
   Example:
   ```json
   {
     "email": "you@example.com",
     "secret": "mysecret",
     "url": "https://tds.s-anand.net/..."
   }
   ```

## Notes
- Replace the Gemini client usage with the official client from Google Generative AI docs.
- Do not commit `.env` to git. Add it to `.gitignore`.
