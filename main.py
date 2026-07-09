import requests
import os
import json
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
        print(f"Request Failed: {response.status_code} , {response.text}")
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

def main():
    players = fetch_players("Curry")
    if players:
        for player in players:
            print(format_players(player))
        save_players(players, "players.json")

if __name__ == "__main__":
    main()