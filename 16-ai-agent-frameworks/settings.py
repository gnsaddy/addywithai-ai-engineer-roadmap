# settings.py: one place for the model settings and the two demo questions.
# Any OpenAI-compatible API works: Ollama on your laptop, or a hosted one.
import os, sys

BASE_URL = os.getenv("BASE_URL", "http://localhost:11434/v1")
MODEL = os.getenv("CHAT_MODEL", "llama3.2")
API_KEY = os.getenv("API_KEY", "none")

if "--demo" in sys.argv:            # no model needed: start the stand-in
    from stand_in_server import start
    BASE_URL = start()

SYSTEM = ("You help with travel expenses. Think step by step. Use a tool "
          "when you need a policy fact or maths. Never guess numbers. "
          "When you are done, give a short final answer.")

QUESTIONS = [
    "I stay 3 nights in Tokyo, with 3 days of meals. What is my max budget?",
    "When must I submit my expense claim?",
]
