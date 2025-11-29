import os
# NOTE: The official Gemini / Google Generative AI Python client library name and usage
# may change. Replace the sample code below with the exact code from the official quickstart:
# https://cloud.google.com/generative-ai/docs/ (search 'Python quickstart' for the right import)
try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
except Exception:
    genai = None

def ask_gemini(prompt: str, model: str = "gemini-1.0"):
    if not genai:
        raise RuntimeError("Gemini client not configured. Install and configure official SDK per docs.")
    # Example / pseudo-call - replace with exact call from current SDK version
    resp = genai.generate_text(model=model, prompt=prompt, max_output_tokens=512)
    # adapt based on the actual response structure of the SDK
    return getattr(resp, 'text', str(resp))
