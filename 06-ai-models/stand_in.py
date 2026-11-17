# stand_in.py: two fake models for the --demo run (no download, no API key).
# Canned answers and a small fixed delay, so you can see the score card work.
import time

def fake(answers, delay):
    def ask(question):
        time.sleep(delay)
        return answers.get(question, "I am not sure.")
    return ask

SMALL = {"What is the capital of France?": "Paris.",
         "What is 12 * 12?": "12 * 12 = 124.",
         "Which planet is called the red planet?": "Mars.",
         "What is H2O usually called?": "Water.",
         "Which gas do plants take in for photosynthesis?": "Oxygen."}
BIG = {"What is the capital of France?": "The capital of France is Paris.",
       "What is 12 * 12?": "12 * 12 = 144.",
       "Which planet is called the red planet?": "Mars is the red planet.",
       "What is H2O usually called?": "H2O is water.",
       "Which gas do plants take in for photosynthesis?":
           "Plants take in carbon dioxide and release oxygen."}

MODELS = {"local": (fake(SMALL, 0.30), 0.0),
          "hosted": (fake(BIG, 0.80), 1.0)}
