# LLM Fundamentals: see the tokens a real request uses.
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()
MODEL = "gemini-flash-latest"

limit = client.models.get(model=MODEL).input_token_limit
response = client.models.generate_content(
    model=MODEL,
    contents="Explain a context window in one short sentence.",
)
print(response.text)

usage = response.usage_metadata
print("Input tokens :", usage.prompt_token_count)
print("Output tokens:", usage.candidates_token_count)
print("Total tokens :", usage.total_token_count)
print(f"Window used  : {usage.prompt_token_count / limit:.4%}")
