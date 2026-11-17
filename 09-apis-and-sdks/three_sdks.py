# three_sdks.py: the same chat call through three official SDKs.
# pip install openai anthropic google-genai    (keys: see .env.example)
import os, sys

SYSTEM = "You are a friendly teacher. Use simple English."
PROMPT = "What is an API? One sentence."

def ask_openai(prompt):
    from openai import OpenAI
    client = OpenAI(max_retries=0)          # reads OPENAI_API_KEY
    r = client.responses.create(model=os.environ["OPENAI_MODEL"],
        instructions=SYSTEM, input=prompt)
    return r.output_text, r.usage.input_tokens, r.usage.output_tokens

def ask_claude(prompt):
    import anthropic
    client = anthropic.Anthropic(max_retries=0)   # reads ANTHROPIC_API_KEY
    r = client.messages.create(model=os.environ["CLAUDE_MODEL"],
        max_tokens=300, system=SYSTEM,
        messages=[{"role": "user", "content": prompt}])
    return r.content[0].text, r.usage.input_tokens, r.usage.output_tokens

def ask_gemini(prompt):
    from google import genai
    client = genai.Client()                 # reads GEMINI_API_KEY
    r = client.models.generate_content(model=os.environ["GEMINI_MODEL"],
        contents=prompt, config={"system_instruction": SYSTEM})
    u = r.usage_metadata
    return r.text, u.prompt_token_count, u.candidates_token_count

if __name__ == "__main__":
    if "--demo" in sys.argv:
        import stand_in_server
        stand_in_server.start()  # fake APIs on localhost, see the file
    for name, ask in [("openai", ask_openai), ("claude", ask_claude),
                      ("gemini", ask_gemini)]:
        text, n_in, n_out = ask(PROMPT)
        print(f"{name:<7} in={n_in:<3} out={n_out:<3} {text}")
