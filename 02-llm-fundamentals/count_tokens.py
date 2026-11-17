# LLM Fundamentals: count tokens and check the context window.
from dotenv import load_dotenv
from google import genai

load_dotenv()                   # reads GEMINI_API_KEY from .env
client = genai.Client()
MODEL = "gemini-flash-latest"

# 1. How big is the context window?
info = client.models.get(model=MODEL)
print("Input limit :", info.input_token_limit, "tokens")
print("Output limit:", info.output_token_limit, "tokens")

# 2. Count tokens (no answer is made, so it is quick)
texts = ["Hello", "Hello, how are you today?", "unbelievable",
         "I love learning AI engineering!"]
for text in texts:
    count = client.models.count_tokens(model=MODEL, contents=text)
    print(f"{count.total_tokens:>3} tokens  <-  {text}")

# 3. Will a very long text fit?
long_text = "Tokens are small pieces of text. " * 200_000
big = client.models.count_tokens(model=MODEL, contents=long_text)
print("Long text:", big.total_tokens, "tokens")
if big.total_tokens > info.input_token_limit:
    print("Too big for the context window! Split it into chunks.")
