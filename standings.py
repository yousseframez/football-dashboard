import requests

API_KEY = "e339f035c1504004b54b871f4e0c9c90"
url = "https://api.football-data.org/v4/competitions/PL/standings"
headers = {"X-Auth-Token": API_KEY}

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
