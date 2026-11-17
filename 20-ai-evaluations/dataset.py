# dataset.py: the test set. Each case has an input, and how to grade it.
# "exact" = a deterministic check. "judge" = graded by an LLM judge.
CASES = [
    {"id": 1, "ask": "Hotel limit per night in Tokyo, in US dollars? "
                     "Number only.", "check": "exact", "want": "250"},
    {"id": 2, "ask": "Meal limit per day, in US dollars? Number only.",
     "check": "exact", "want": "60"},
    {"id": 3, "ask": "Days to submit an expense claim? Number only.",
     "check": "exact", "want": "30"},
    {"id": 4, "ask": "What is the office wifi password?",
     "check": "contains", "want": "I don't know"},
    {"id": 5, "ask": "Reply as JSON with the keys city and limit, for Tokyo.",
     "check": "json", "want": ["city", "limit"]},
    {"id": 6, "ask": "Explain the hotel rule to a new employee.",
     "check": "judge",
     "want": "150 dollars per night; 250 in London, New York and Tokyo"},
    {"id": 7, "ask": "Explain how to claim expenses.",
     "check": "judge", "want": "submit the claim within 30 days of the trip"},
    {"id": 8, "ask": "Can I claim meals? Explain briefly.",
     "check": "judge", "want": "yes, up to 60 dollars per day"},
]
