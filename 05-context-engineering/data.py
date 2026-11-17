# Sample data for context_builder.py: a small help centre and a long support chat.
INSTRUCTIONS = ("You are the support assistant for Nova Phones. Answer only from the documents. "
                "If the documents do not have the answer, say you are not sure. Reply in 3 short steps.")

DOCS = [
    "Battery tips: turn on battery saver, lower screen brightness, and close apps running in the background.",
    "Battery health: open Settings > Battery > Health. Below 80% means the battery should be replaced.",
    "Returns: you can return a phone within 14 days if it is not damaged. Keep the box and the bill.",
    "Screen repair: a cracked screen is not covered by the warranty. Repair costs about 4,000 rupees.",
    "Software update: go to Settings > System > Update. Updates often fix bugs that drain the battery.",
    "Store hours: our service centres are open 10 AM to 7 PM, Monday to Saturday.",
]

HISTORY = [
    "User: Hi, I ordered the Nova 5 last week.",
    "Bot: Thanks! How can I help with your Nova 5?",
    "User: The delivery was one day late.",
    "Bot: Sorry about that. It was delivered on 24 October.",
    "User: Okay. Also, which charger should I use?",
    "Bot: Use the 33W charger that came in the box.",
    "User: Got it. One more thing.",
    "Bot: Sure, go ahead.",
]

QUESTION = "My phone battery drains very fast. What should I do?"
