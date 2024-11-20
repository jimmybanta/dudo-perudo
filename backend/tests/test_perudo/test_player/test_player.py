
import pytest
import random
from perudo.player.player import Player, HumanPlayer, AIPlayer, AIRandomPlayer, AISmartPlayer

@pytest.fixture
def player():
    return Player(name="Player1", num_dice=5, sides_per_die=6, ai=False)

@pytest.fixture
def human_player():
    return HumanPlayer(name="Human", num_dice=5, sides_per_die=6)

@pytest.fixture
def ai_player():
    return AIPlayer(name="AI", num_dice=5, sides_per_die=6)

@pytest.fixture
def ai_random_player():
    return AIRandomPlayer(name="AI", num_dice=5, sides_per_die=6)

@pytest.fixture
def ai_smart_player():
    return AISmartPlayer(name="AI", num_dice=5, sides_per_die=6)

def test_player_initialization(player):
    assert player.name == "Player1"
    assert player.num_dice == 5
    assert player.sides_per_die == 6
    assert player.ai == False
    assert player.hand == None

def test_player_roll(player):
    player.roll(values=[1, 2, 3, 4, 5])
    assert [die.value for die in player.hand] == [1, 2, 3, 4, 5]

def test_player_lose_die(player):
    player.lose_die()
    assert player.num_dice == 4

def test_player_one_left(player):
    player.num_dice = 1
    assert player.one_left == True

def test_human_player_initialization(human_player):
    assert human_player.name == "Human"
    assert human_player.num_dice == 5
    assert human_player.sides_per_die == 6
    assert human_player.ai == False

def test_ai_player_initialization(ai_player):
    assert ai_player.name == "AI"
    assert ai_player.num_dice == 5
    assert ai_player.sides_per_die == 6
    assert ai_player.ai == True

def test_ai_random_player_initialization(ai_random_player):
    assert ai_random_player.name == "AI"
    assert ai_random_player.num_dice == 5
    assert ai_random_player.sides_per_die == 6
    assert ai_random_player.ai == True

def test_ai_smart_player_initialization(ai_smart_player):
    assert ai_smart_player.name == "AI"
    assert ai_smart_player.num_dice == 5
    assert ai_smart_player.sides_per_die == 6
    assert ai_smart_player.ai == True


def test_ai_smart_player_starting_bid(ai_smart_player):

    random.seed(0)

    hand = [1, 1, 2, 2, 5]
    total_dice = 30
    palifico = False

    bid, delay = ai_smart_player.starting_bid(hand, total_dice, palifico=palifico)

    assert bid == (12, 2)
    assert delay == 930

def test_ai_smart_player_move(ai_smart_player):

    random.seed(0)

    hand = [1, 1, 2, 2, 5]
    total_dice = 30
    palifico = False
    round_history = [['adam-2', [10, 2]]]

    move, delay = ai_smart_player.move(hand, round_history, [], total_dice, palifico=palifico)

    assert move == (11, 6)
    assert delay == 930

def test_ai_smart_player_move_call(ai_smart_player):

    random.seed(0)

    hand = [1, 1, 2, 2, 5]
    total_dice = 30
    palifico = False
    round_history = [['adam-2', [20, 2]]]

    move, delay = ai_smart_player.move(hand, round_history, [], total_dice, palifico=palifico)

    assert move == 'call'
    assert delay == 1276