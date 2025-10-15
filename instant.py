import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from google import genai

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def instant():
    try:
        # Check if API key exists
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "<html><body><h1>Error: GEMINI_API_KEY not found</h1></body></html>"
        
        # Initialize client
        client = genai.Client(api_key=api_key)
        
        prompt = """
You are on a website that has just been deployed to production for the first time!
Please reply with an enthusiastic announcement to welcome visitors to the site, explaining that it is live on production for the first time!
"""

        # Make API call - use 'contents' instead of 'input'
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        # Check if response has text
        if not hasattr(resp, 'text') or not resp.text:
            return "<html><body><h1>Error: No text in response</h1><p>Response: " + str(resp) + "</p></body></html>"
        
        reply_html = resp.text.replace("\n", "<br/>")
        return f"<html><head><title>Live in an Instant!</title></head><body><p>{reply_html}</p></body></html>"
        
    except Exception as e:
        return f"<html><body><h1>Error occurred:</h1><p>{str(e)}</p><p>Type: {type(e).__name__}</p></body></html>"