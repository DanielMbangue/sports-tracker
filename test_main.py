from main import format_players
from main import format_games
from main import game_winner
from main import margin
from main import is_blowout
from main import largest_margin
from main import team_record

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

def test_game_winner_visitor():
    game = {
        "visitor_team": {"full_name": "Knicks"},
        "home_team": {"full_name": "Huskies"},
        "visitor_team_score": 24,
        "home_team_score": 18
    }
    assert game_winner(game) == "Knicks"

def test_game_winner_home():
    game = {
        "visitor_team": {"full_name": "Knicks"},
        "home_team": {"full_name": "Huskies"},
        "visitor_team_score": 10,
        "home_team_score": 25
    }
    assert game_winner(game) == "Huskies"

def test_game_margin():
    game = {
        "visitor_team": {"full_name": "Knicks"},
        "home_team": {"full_name": "Huskies"},
        "visitor_team_score": 24,
        "home_team_score": 18
    }
    assert margin(game) == 6

def test_game_is_blowout():
    game = {
        "visitor_team_score": 18,
        "home_team_score": 50
    }
    assert is_blowout(game) == True

def test_is_blowout_just_under():
    game = {"visitor_team_score": 18, "home_team_score": 37}  
    assert not is_blowout(game)

def test_is_blowout_exactly_at_threshold():
    game = {"visitor_team_score": 18, "home_team_score": 38}
    assert is_blowout(game)

def test_is_blowout_just_over():
    game = {"visitor_team_score": 18, "home_team_score": 39}
    assert is_blowout(game)

def test_largest_margin():
    games = [
        {"visitor_team_score": 100, "home_team_score": 98}, 
        {"visitor_team_score": 100, "home_team_score": 70},
        {"visitor_team_score": 100, "home_team_score": 95},
    ]
    assert largest_margin(games) == games[1]

def test_largest_margin_empty():
    assert largest_margin([]) is None

def test_team_record():
    games = [
        {"visitor_team": {"full_name": "Knicks"}, "home_team": {"full_name": "Celtics"},
         "visitor_team_score": 100, "home_team_score": 90},    # Knicks win (away)
        {"visitor_team": {"full_name": "Celtics"}, "home_team": {"full_name": "Knicks"},
         "visitor_team_score": 80, "home_team_score": 95},     # Knicks win (home)
        {"visitor_team": {"full_name": "Knicks"}, "home_team": {"full_name": "Bulls"},
         "visitor_team_score": 70, "home_team_score": 88},     # Knicks lose
        {"visitor_team": {"full_name": "Lakers"}, "home_team": {"full_name": "Heat"},
         "visitor_team_score": 100, "home_team_score": 99},    # no Knicks — must be skipped
    ]
    assert team_record(games, "Knicks") == (2, 1)