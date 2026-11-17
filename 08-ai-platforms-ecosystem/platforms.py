# platforms.py: one chat() function, many AI platforms.
# Every platform below speaks the OpenAI-compatible chat API,
# so switching platform = a new base URL, key and model name.
import json, os, time, urllib.request  # standard library only

PLATFORMS = {  # name: (base URL, env var that holds the key)
    "ollama":     ("http://localhost:11434/v1", None),
    "lmstudio":   ("http://localhost:1234/v1", None),
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
    "together":   ("https://api.together.xyz/v1", "TOGETHER_API_KEY"),
    "groq":       ("https://api.groq.com/openai/v1", "GROQ_API_KEY"),
    "fireworks":  ("https://api.fireworks.ai/inference/v1", "FIREWORKS_API_KEY"),
}

def chat(platform, model, prompt, timeout=60):
    base_url, key_var = PLATFORMS[platform]
    key = os.environ.get(key_var, "") if key_var else "local"
    body = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request(base_url + "/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + key})
    start = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.load(r)
    text = data["choices"][0]["message"]["content"]
    return text, data["usage"]["completion_tokens"], time.time() - start
