import pytest
from perudo.logic.calculate_probs import calculate_prob


@pytest.mark.parametrize("bid, total_dice, palifico, sides_per_die, expected", [
    ((2, 3), 5, False, 6, 0.5390946502057613),  # Replace with the actual expected value
    ((2, 1), 5, True, 6, 0.1962448559670782),   # Replace with the actual expected value
    ((10, 4), 30, False, 6, 0.5682556444214808),    # Replace with the actual expected value
    ((10, 4), 30, True, 6, 0.01970628376896778),    # Replace with the actual expected value
    ((10, 2), 10, False, 6, .000016935087808430286) # Replace with the actual expected value
])

def test_calculate_prob(bid, total_dice, palifico, sides_per_die, expected):
    result = calculate_prob(bid, total_dice, palifico, sides_per_die)
    assert pytest.approx(result, 0.00001) == expected
