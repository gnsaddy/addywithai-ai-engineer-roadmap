# test_split.py: the rules the code must follow. The AI tool runs these after every change.
import pytest
from split import split_bill


def test_even_split():
    assert split_bill(900, 3) == [300.0, 300.0, 300.0]


def test_tip_is_added():
    assert sum(split_bill(1000, 4, tip_pct=10)) == 1100.0


def test_shares_add_up_to_the_bill():
    shares = split_bill(1000, 3)
    assert round(sum(shares), 2) == 1000.0     # nobody pays a paisa too little


def test_needs_people():
    with pytest.raises(ValueError):
        split_bill(500, 0)
