# testset.py: one small search task, used to compare embedding models fairly.
# 8 help-desk notes + 6 test questions, each with the note that SHOULD come back.

DOCS = [
    "Reset your password from the login page",          # 0
    "My laptop battery dies too fast",                   # 1
    "Refunds take 5 to 7 days to reach your bank",       # 2
    "Error E42 means the printer is out of paper",       # 3
    "Change the app language in settings",               # 4
    "Our office is closed on public holidays",           # 5
    "The phone app crashes when I upload a photo",       # 6
    "Cancel your plan any time from the billing page",   # 7
]

TESTS = [  # (question, index of the right note)
    ("I forgot my login",            0),
    ("my computer power runs out",   1),
    ("when do I get my money back",  2),
    ("what does E42 mean",           3),
    ("stop my subscription",         7),
    ("app closes on picture upload", 6),
]
