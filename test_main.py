from main import format_players
from main import format_games

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

def test_format_games_basic():
    fake = {
        "date": "1946-11-01",
        "visitor_team": {"full_name": "New York Knicks"},
        "home_team": {"full_name": "Toronto Huskies"},
        "visitor_team_score": 24,
        "home_team_score": 18,
    }
    assert format_games(fake) == "1946-11-01: New York Knicks 24 @ Toronto Huskies 18"

def test_format_games_missing_team():
    fake = {
        "date": "2020-01-01",
        "visitor_team": {"full_name": "Lakers"},
        "home_team": {},
        "visitor_team_score": 100,
        "home_team_score": 98,
    }
    assert format_games(fake) == "2020-01-01: Lakers 100 @ Unknown 98"