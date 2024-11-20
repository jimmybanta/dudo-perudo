


import pytest
import random
from perudo.player.move import choose_bid, decide_call, create_bluff_hand, choose_bluff_value
from perudo.logic.legal_bids import legal_bids
from perudo.logic.hand import Hand 

@pytest.mark.parametrize("hand, options, total_dice, min_probability, palifico, blur, expected", [
    # Add test cases here
    ([1, 2, 3], legal_bids((4, 5), 20), 20, 0.5, False, 0.1, (8, 3)), 
])
def test_choose_bid(hand, options, total_dice, min_probability, palifico, blur, expected):
    random.seed(0)
    result = choose_bid(hand, options, total_dice, min_probability, palifico, blur)
    assert result == expected

@pytest.mark.parametrize("hand, bid, total_dice, min_probability, palifico, blur, expected", [
    # Add test cases here
    ([1, 2, 3], (2, 3), 10, 0.5, False, 0, False),  
])
def test_decide_call(hand, bid, total_dice, min_probability, palifico, blur, expected):
    random.seed(0)
    result = decide_call(hand, bid, total_dice, min_probability, palifico, blur)
    assert result == expected

@pytest.mark.parametrize("hand, bluff_value, bluffing_intensity, sides_per_die, expected", [
    # Add test cases here
    ([1, 2, 3], 4, 0.7, 6, Hand(size=3, values=[1, 4, 4])),  
])
def test_create_bluff_hand(hand, bluff_value, bluffing_intensity, sides_per_die, expected):
    random.seed(0)
    result = create_bluff_hand(hand, bluff_value, bluffing_intensity, sides_per_die=sides_per_die)
    assert result == expected

@pytest.mark.parametrize("round_history, palifico, sides_per_die, expected", [
    # Add test cases here
    ([('player-1', (2, 3)), ('player-2', (3, 4))], False, 6, 4),
])
def test_choose_bluff_value(round_history, palifico, sides_per_die, expected):
    random.seed(0)
    result = choose_bluff_value(round_history, palifico, sides_per_die)
    assert result == expected