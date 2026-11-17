# Prompt templates: one tested prompt, many inputs. Stdlib only.
from string import Template

SYSTEM = ("You are a support agent for BookNest, an online bookshop. "
          "Reply in simple English, in 2 short sentences.")

EXAMPLES = [  # few-shot: show the style you want
    ("Where is my order 1042?", "Let me check order 1042 for you."),
    ("Can I return a book?", "Yes, within 30 days. Keep the receipt."),
]

USER = Template('''Customer message:
"""$message"""
If you are not sure, say so. Never invent order details.''')

def build_messages(message):
    msgs = [{"role": "system", "content": SYSTEM}]
    for q, a in EXAMPLES:
        msgs.append({"role": "user", "content": q})
        msgs.append({"role": "assistant", "content": a})
    user_text = USER.substitute(message=message)    # fill the slot
    msgs.append({"role": "user", "content": user_text})
    return msgs

for text in ["My book came torn.", "Do you sell e-books?"]:
    msgs = build_messages(text)
    print(f"{len(msgs)} messages. Roles: {[m['role'] for m in msgs]}")
    print(msgs[-1]["content"], end="\n\n")
