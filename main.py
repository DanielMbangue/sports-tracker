import requests
import os
import json
import argparse
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def fetch_players(search_term):
    key = os.environ.get("BALLDONTLIE_KEY")
    url = "https://api.balldontlie.io/v1/players"
    headers = {"Authorization": key}
    params = {"search": search_term}
    response = requests.get(url, headers=headers,params=params)

    if response.status_code == 200:
        data = response.json()
        players = data['data']
        return players
    else:
        logging.error(f"Request Failed: {response.status_code} , {response.text}")
        return None
    
def fetch_games():
    key = os.environ.get("BALLDONTLIE_KEY")
    url = "https://api.balldontlie.io/v1/games"
    headers = {"Authorization": key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        games = data['data']
        return games
    else:
        logging.error(f"Request Failed: {response.status_code} , {response.text}")
        return None
    

def save_players(players, filename):
    with open(filename, "w") as f:
            json.dump(players, f, indent=2)


def format_players(player):
    first = player.get("first_name","")
    last = player.get("last_name","")
    team = player.get("team", {})
    team_name = team.get("full_name", 'Unknown')
    return f"{first} {last} - {team_name}"

def format_games(game):
    date = game.get("date","Unknown")
    visitor, home = team_names(game)
    v_Score = game.get("visitor_team_score")
    h_Score = game.get("home_team_score")
    return f"{date}: {visitor} {v_Score} @ {home} {h_Score}"

def game_winner(game):
    visitor, home = team_names(game)
    v_score = game.get("visitor_team_score")
    h_score = game.get("home_team_score")
    if v_score > h_score:
        return visitor
    if h_score > v_score:
        return home
    else:
        return "Tie game"

def margin(game):
    v_score = game.get("visitor_team_score")
    h_score = game.get("home_team_score")
    finalScr = v_score - h_score
    if finalScr < 0:
        finalScr = finalScr * -1
    return finalScr

def is_blowout(game, threshold=20):
    return margin(game) >= threshold

def largest_margin(games):
    if not games:
        return None
    bestGame = games[0]
    for game in games:
        if margin(game) > margin(bestGame):
            bestGame = game
    return bestGame

def team_record(games ,team_name):
    wins = 0
    losses = 0
    for game in games:
       visitor, home = team_names(game)
       winner = game_winner(game)
       if team_name != visitor and team_name != home:
           continue
       if team_name == winner:
           wins += 1
       else:
           losses += 1 
    return (wins, losses)

def team_names(game):
    visitor = game.get("visitor_team", {}).get("full_name", "Unknown")
    home = game.get("home_team", {}).get("full_name", "Unknown")
    return visitor, home

def count_wins(games, team_name):
    wins, losses = team_record(games, team_name)
    return wins

def highest_scorer(games):
    max_score = 0
    if not games:
            return "No game data was pulled"
    for game in games:
        v_score = game.get("visitor_team_score")
        h_score = game.get("home_team_score")
        
        if v_score > max_score:
            max_score = v_score
        if h_score > max_score:
            max_score = h_score
    return max_score

def count_high_scoring_games(games, threshold):
    count = 0
    if not games:
        return 0
    for game in games:
        v_Score = game.get("visitor_team_score", 0)
        h_Score = game.get("home_team_score", 0)
        if v_Score + h_Score > threshold:
            count += 1
    return count

def main():
    parser = argparse.ArgumentParser(description="Fetch NBA data")
    parser.add_argument("--search", default="Curry", help="Player name to search")
    parser.add_argument("--output", default="players.json", help="Output file")
    args = parser.parse_args()
    logging.info(f"Fetching Players for search: {args.search}")

    players = fetch_players(args.search)
    if players:
        for player in players:
            print(format_players(player))
        save_players(players, args.output)

if __name__ == "__main__":
    main()