from perudo.logic.dice import Die, D6
import pytest
from collections import Counter
import math


# Fixture for a standard die
@pytest.fixture
def standard_die():
    return Die(6)

# Fixture for a die with a specific value
@pytest.fixture
def specific_value_die():
    return Die(6, 3)

# Fixture for a D6 instance
@pytest.fixture
def d6_die():
    return D6()

class TestDie:
    def test_die_creation_with_valid_sides(self, standard_die):
        assert standard_die.sides == 6

    def test_die_creation_with_explicit_value(self, specific_value_die):
        assert specific_value_die.value == 3

    def test_die_creation_without_value(self, standard_die):
        assert 1 <= standard_die.value <= 6

    def test_d6_creation(self, d6_die):
        assert d6_die.sides == 6 and 1 <= d6_die.value <= 6

    # 2. Equality and Comparison tests
    def test_dice_equality(self):
        die1 = Die(6, 4)
        die2 = Die(6, 4)
        assert die1 == die2

    def test_dice_inequality(self):
        die1 = Die(6, 3)
        die2 = Die(6, 5)
        assert die1 != die2

    def test_less_than(self):
        die1 = Die(6, 3)
        die2 = Die(6, 5)
        assert die1 < die2

    def test_less_than_or_equal(self):
        die1 = Die(6, 3)
        die2 = Die(6, 3)
        die3 = Die(6, 4)
        assert die1 <= die2 and die1 <= die3

    def test_greater_than(self):
        die1 = Die(6, 5)
        die2 = Die(6, 3)
        assert die1 > die2

    def test_greater_than_or_equal(self):
        die1 = Die(6, 5)
        die2 = Die(6, 5)
        die3 = Die(6, 4)
        assert die1 >= die2 and die1 >= die3

    # 3. Randomness tests
    def test_random_die_value_in_range(self, standard_die):
        assert 1 <= standard_die.value <= 6

    def test_random_value_distribution(self):
        num_dice = 10000
        sides = 6
        tolerance = 0.1  # 10% tolerance

        # Instantiate dice and collect values
        values = [Die(sides).value for _ in range(num_dice)]

        # Count the frequency of each value
        frequency = Counter(values)
        
        # Expected count for each value
        expected_count = num_dice / sides

        # Check if each value's frequency is within the tolerance range
        for value in range(1, sides + 1):
            assert math.isclose(frequency[value], expected_count, rel_tol=tolerance), \
                f"Value {value} frequency {frequency[value] / num_dice} out of expected range"

