from google import genai

from environment import GEMINI_API_KEY

print(GEMINI_API_KEY)

client = genai.Client(api_key=GEMINI_API_KEY)

def call_gemini(prompt: str) -> dict:
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt)
    return {
        "text": response.text,
        "metadata": {
            "model": "gemini-pro",
            "tokens": len(prompt.split()),
        }
    }
