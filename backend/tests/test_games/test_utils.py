import pytest
import yaml
from games.utils import load_yaml, format_message_history, format_bid
import logging

logger = logging.getLogger(__name__)

# Mock data for testing
mock_yaml_content = """
player: John Doe
dice_per_player: 5
sides_per_die: 6
table:
  - John Doe
  - AI Player 1
  - AI Player 2
history: []
"""

@pytest.fixture
def mock_yaml_file(tmp_path):
    file_path = tmp_path / "mock.yaml"
    file_path.write_text(mock_yaml_content)
    return file_path

def test_load_yaml(mock_yaml_file):
    result = load_yaml(mock_yaml_file)
    expected = {
        "player": "John Doe",
        "dice_per_player": 5,
        "sides_per_die": 6,
        "table": ["John Doe", "AI Player 1", "AI Player 2"],
        "history": []
    }
    assert result == expected

def test_format_message_history():
    message_history = [
        {"writer": "John", "text": "Hello!"},
        {"writer": "AI", "text": "Hi there!"},
        {"writer": "John", "text": "How are you?"},
    ]
    result = format_message_history(message_history)
    expected = "[John]: Hello!\n[AI]: Hi there!\n[John]: How are you?\n"
    assert result == expected

def test_format_message_history_with_error():
    message_history = [
        {"writer": "John", "text": "Hello!"},
        {"writer": "AI"},  # Missing "text" key
        {"writer": "John", "text": "How are you?"},
    ]
    result = format_message_history(message_history)
    expected = "[John]: Hello!\n[John]: How are you?\n"
    assert result == expected

@pytest.mark.parametrize("quantity, value, singular, palifico, expected", [
    (2, 3, False, False, "2 threes"),
    (1, 1, True, True, "1 one"),
    (3, 5, False, True, "3 fives"),
    (1, 2, True, False, "1 two"),
    (4, 6, False, False, "4 sixes"),
    (1, 1, True, False, "1 jessie"),
])
def test_format_bid(quantity, value, singular, palifico, expected):
    result = format_bid(quantity, value, singular=singular, palifico=palifico)
    assert result == expected