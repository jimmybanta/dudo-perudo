import pytest
from games.models import Game, Character

@pytest.mark.django_db
def test_create_game():
    game = Game.objects.create(
        player="John Doe",
        dice_per_player=5,
        sides_per_die=6,
        table=["John Doe", "AI Player 1", "AI Player 2"],
        history=[]
    )
    assert game.player == "John Doe"
    assert game.dice_per_player == 5
    assert game.sides_per_die == 6
    assert game.table == ["John Doe", "AI Player 1", "AI Player 2"]
    assert game.history == []

@pytest.mark.django_db
def test_create_character():
    character = Character.objects.create(
        name="Warrior",
        description="A brave warrior with unmatched strength."
    )
    assert character.name == "Warrior"
    assert character.description == "A brave warrior with unmatched strength."

@pytest.mark.django_db
def test_character_str():
    character = Character.objects.create(
        name="Warrior",
        description="A brave warrior with unmatched strength."
    )
    assert str(character) == "Warrior"