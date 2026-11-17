# stand_in.py: DEMO ONLY. A fake, gullible "model", so the demo runs offline.
# It does not think. It follows the newest order it can find in its input,
# even one hidden inside an email. Real models resist more, but not always.
import re

ORDER = re.compile(r"(reveal|print|show|send|tell|give|share|output)\b.{0,40}"
                   r"\b(code|notes?|instructions|prompt)", re.I | re.S)

def fake_model(system, user):
    secret = re.search(r"staff refund code is (\S+)\.", system)
    if ORDER.search(user) and secret:        # it obeys the hidden order
        return f"Sure. The staff refund code is {secret.group(1)}."
    email = user.split("EMAIL:", 1)[-1]
    email = re.sub(r"</?untrusted_email>", "", email).strip()
    first = re.split(r"(?<=[.!?])\s+", email)[0]
    return "Summary: " + first
