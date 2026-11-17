# vision.py: send an image to two vision APIs, get JSON back (Episode 22)
import base64
import json
from settings import openai_client, gemini_client, VISION, GEMINI

ASK = ('Read this receipt. Reply only with JSON: '
       '{"shop": str, "total": number, "items": int}')

def openai_vision(path, detail="low"):
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    r = openai_client().chat.completions.create(model=VISION, messages=[
        {"role": "user", "content": [
            {"type": "text", "text": ASK},
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{b64}", "detail": detail}}]}],
        response_format={"type": "json_object"})
    return json.loads(r.choices[0].message.content), r.usage.prompt_tokens

def gemini_vision(path):
    from google.genai import types
    img = types.Part.from_bytes(data=open(path, "rb").read(),
                                mime_type="image/png")
    client = gemini_client()             # keep the client open
    r = client.models.generate_content(model=GEMINI, contents=[img, ASK])
    return json.loads(r.text), r.usage_metadata.prompt_token_count

if __name__ == "__main__":
    for detail in ("low", "high"):
        data, tok = openai_vision("receipt.png", detail)
        print(f"OpenAI ({detail:4}) {tok:4} tokens ->", data)
    data, tok = gemini_vision("receipt.png")
    print(f"Gemini        {tok:4} tokens ->", data)
