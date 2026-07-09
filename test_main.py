from main import format_players

def test_format_players_basic():
    fake_player = {
        "first_name": "Stephen",
        "last_name": "Curry",
        "team": { "full_name": "Golden State Warriors"}
    }
    result = format_players(fake_player)
    assert result == "Stephen Curry - Golden State Warriors"

def test_format_players_different_player():
    fake_player = {
        "first_name": "Lebron",
        "last_name": "James",
        "team": {"full_name": "Los Angeles Lakers"}
    }
    result = format_players(fake_player)
    assert result == "Lebron James - Los Angeles Lakers"

def test_format_players_missing_team():
    fake_player = {
        "first_name": "Ghost",
        "last_name": "Player",
    }
    result = format_players(fake_player)
    assert result == "Ghost Player - Unknown"