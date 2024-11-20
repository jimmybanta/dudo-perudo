
import pytest
from perudo.logic.score import score

@pytest.mark.parametrize(
    "bid, all_dice, palifico, expected",
    [
        ((3, 3), [1, 2, 3, 3, 4, 5], False, (True, (3, 3))),
        ((3, 3), [1, 2, 3, 4, 5, 6], False, (False, (2, 3))),
        ((3, 1), [1, 2, 3, 4, 5, 6], False, (False, (1, 1))),
        ((2, 1), [1, 1, 3, 4, 5, 6], False, (True, (2, 1))),

        ((2, 3), [1, 2, 3, 3, 4, 5], True, (True, (2, 3))),
        ((3, 3), [1, 2, 3, 4, 5, 6], True, (False, (1, 3))),
        ((2, 1), [1, 1, 3, 4, 5, 6], True, (True, (2, 1))),
    ],
)
def test_score(bid, all_dice, palifico, expected):
    assert score(bid, all_dice, palifico) == expected