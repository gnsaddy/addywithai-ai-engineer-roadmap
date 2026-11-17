# split.py: split a restaurant bill between friends (tiny demo project for Episode 23)


def split_bill(total, people, tip_pct=0):
    """Return each person's share in rupees, rounded to 2 decimals."""
    if people < 1:
        raise ValueError("people must be at least 1")
    paise = round(total * (1 + tip_pct / 100) * 100)   # work in whole paise
    base, extra = divmod(paise, people)
    # the first `extra` people pay one paisa more, so the sum is exact
    return [(base + (i < extra)) / 100 for i in range(people)]
