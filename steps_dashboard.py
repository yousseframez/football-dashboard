import requests
import pandas as pd
API_KEY = "e339f035c1504004b54b871f4e0c9c90"
headers = {"X-Auth-Token": API_KEY}
def get_standings():

    url = "https://api.football-data.org/v4/competitions/PL/standings"
    response = requests.get(url, headers=headers)
    data = response.json()
    #print(data)

    table = data["standings"][0]["table"]
    print("-------------------------PL--------------------------")
    for team in table:
        position = team["position"]
        name = team["team"]["shortName"]
        points = team["points"]
        played = team["playedGames"]
        won = team["won"]
        draw = team["draw"]
        lost = team["lost"]
        print(f"{position:2}. {name:15} - {points}pts - {played} games - {won:2} wins - {draw:2} draws - {lost:2} loses")
    print("-------------------------PL--------------------------")

def get_scorers():

    url = "https://api.football-data.org/v4/competitions/PL/scorers"
    response = requests.get(url, headers=headers)
    data = response.json()

    scorers = data["scorers"]

    print("---------------------- PL Top Scorers ----------------------")

    for i, player in enumerate(scorers, start=1):
        name = player["player"]["name"]
        team = player["team"]["name"]
        goals = player["goals"]
        matches = player["playedMatches"]

        print(f"{i:2}. {name:25} | {team:26} | {goals} goals | {matches} matches")

    print("----------------------------------------------------------------")
def analyze_standings():
    url = "https://api.football-data.org/v4/competitions/PL/standings"
    response = requests.get(url, headers=headers)
    data = response.json()
    table = data["standings"][0]["table"]

    rows = []
    for team in table:
        rows.append({
            "team": team["team"]["shortName"],
            "points": team["points"],
            "played": team["playedGames"],
            "won": team["won"],
            "draw": team["draw"],
            "lost": team["lost"],
            "goals_for": team["goalsFor"],
            "goals_against": team["goalsAgainst"]
        })

    df = pd.DataFrame(rows)
    df["goal_difference"] = df["goals_for"] - df["goals_against"]
    df["points_per_game"] = (df["points"] / df["played"]).round(2)    
    print("\n--- Best Attack ---")
    print(df[["team", "goals_for"]].sort_values("goals_for", ascending=False).head(5).to_string(index=False))

    print("\n--- Best Defense ---")
    print(df[["team", "goals_against"]].sort_values("goals_against").head(5).to_string(index=False))

    print("\n--- Most Draws ---")
    print(df[["team", "draw"]].sort_values("draw", ascending=False).head(5).to_string(index=False))
    print("\n--- Best Goal Difference ---")
    print(df[["team", "goals_for", "goals_against", "goal_difference"]].sort_values("goal_difference", ascending=False).head(5).to_string(index=False))

    print("\n--- Most Efficient Teams (points per game) ---")
    print(df[["team", "points_per_game", "played"]].sort_values("points_per_game", ascending=False).head(5).to_string(index=False))
analyze_standings()
get_standings()
get_scorers()
