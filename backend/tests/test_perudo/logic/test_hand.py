import pytest
from perudo.logic.hand import Hand
from perudo.logic.dice import Die

# Fixture for a standard hand
@pytest.fixture
def standard_hand():
    return Hand()

# Fixture for a hand with specific values
@pytest.fixture
def specific_value_hand():
    return Hand(size=5, values=[1, 2, 3, 4, 5])

class TestHand:
    def test_hand_creation_with_default_values(self, standard_hand):
        assert len(standard_hand) == 5
        assert all(isinstance(die, Die) for die in standard_hand)

    def test_hand_creation_with_specific_values(self, specific_value_hand):
        assert len(specific_value_hand) == 5
        assert all(isinstance(die, Die) for die in specific_value_hand)
        assert [die.value for die in specific_value_hand] == [1, 2, 3, 4, 5]

    def test_hand_creation_with_incorrect_values(self):
        with pytest.raises(ValueError):
            Hand(size=5, values=[1, 2, 3])

    def test_hand_str_representation(self, specific_value_hand):
        assert str(specific_value_hand) == '[1, 2, 3, 4, 5]'

    def test_hand_count_normal(self, specific_value_hand):
        assert specific_value_hand.count(1) == 1  # 1 jessie
        assert specific_value_hand.count(2) == 2  # 1 from the specific value and 1 from the jessie
        assert specific_value_hand.count(3) == 2  # 1 from the specific value and 1 from the jessie
        assert specific_value_hand.count(4) == 2  # 1 from the specific value and 1 from the jessie
        assert specific_value_hand.count(5) == 2  # 1 from the specific value and 1 from the jessie
        assert specific_value_hand.count(6) == 1  # 1 from the jessies

    def test_hand_count_palifico(self, specific_value_hand):
        assert specific_value_hand.count(1, palifico=True) == 1
        assert specific_value_hand.count(2, palifico=True) == 1
        assert specific_value_hand.count(3, palifico=True) == 1
        assert specific_value_hand.count(4, palifico=True) == 1
        assert specific_value_hand.count(5, palifico=True) == 1
        assert specific_value_hand.count(6, palifico=True) == 0