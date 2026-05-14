import requests

API_KEY = "e339f035c1504004b54b871f4e0c9c90"
url = "https://api.football-data.org/v4/competitions/PL/scorers"

headers = {
    "X-Auth-Token": API_KEY
}

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
