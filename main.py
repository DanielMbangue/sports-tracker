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
    visitor = game.get("visitor_team",{}).get("full_name","Unknown")
    home = game.get("home_team", {}).get("full_name", "Unknown")
    v_Score = game.get("visitor_team_score")
    h_Score = game.get("home_team_score")
    return f"{date}: {visitor} {v_Score} @ {home} {h_Score}"

def game_winner(game):
    visitor = game.get("visitor_team", {}).get("full_name", "Unknown")
    home = game.get("home_team", {}).get("full_name", "Unknown")
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
       visitor = game.get("visitor_team", {}).get("full_name", "Unknown")
       home = game.get("home_team", {}).get("full_name", "Unknown")
       winner = game_winner(game)
       if team_name != visitor and team_name != home:
           continue
       if team_name == winner:
           wins += 1
       else:
           losses += 1 
    return (wins, losses)

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