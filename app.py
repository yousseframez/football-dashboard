import streamlit as st
import requests
import pandas as pd

API_KEY = "e339f035c1504004b54b871f4e0c9c90"
headers = {"X-Auth-Token": API_KEY}

LEAGUES = {
    "Premier League": "PL",
    "Champions League": "CL",
    "La Liga": "PD",
    "Bundesliga": "BL1",
    "Serie A": "SA",
    "Ligue 1": "FL1",
    "Eredivisie": "DED"
}
selected_league = st.selectbox("Pick a league", list(LEAGUES.keys()))
league = LEAGUES[selected_league]
st.title("League Dashboard")

# fetch
url = f"https://api.football-data.org/v4/competitions/{league}/standings"
response = requests.get(url, headers=headers)
data = response.json()
table = data["standings"][0]["table"]


rows = []
for team in table:
    rows.append({
        "Crest": team["team"]["crest"],
        "Team": team["team"]["shortName"],
        "Points": team["points"],
        "Played": team["playedGames"],
        "Won": team["won"],
        "Draw": team["draw"],
        "Lost": team["lost"],
        "GF": team["goalsFor"],
        "GA": team["goalsAgainst"],
    })

df = pd.DataFrame(rows)
df["GD"] = df["GF"] - df["GA"]
df["PPG"] = (df["Points"] / df["Played"]).round(2)

# best attack and defense
col1, col2 = st.columns(2)

with col1:
    st.subheader("Best Attack")
    st.dataframe(df[["Team", "GF"]].sort_values("GF", ascending=False).head(5), hide_index=True)

with col2:
    st.subheader("Best Defense")
    st.dataframe(df[["Team", "GA"]].sort_values("GA").head(5), hide_index=True)

# top scorers
st.subheader("Top Scorers")
scorers_url = f"https://api.football-data.org/v4/competitions/{league}/scorers"
scorers_data = requests.get(scorers_url, headers=headers).json()

scorer_rows = []
for i, player in enumerate(scorers_data["scorers"], start=1):
    scorer_rows.append({
        "Rank": i,
        "Player": player["player"]["name"],
        "Team": player["team"]["name"],
        "Goals": player["goals"],
        "Matches": player["playedMatches"]
    })

scorers_df = pd.DataFrame(scorer_rows)
st.dataframe(scorers_df, hide_index=True)
df.insert(0, "Pos", range(1, len(df) + 1))
st.subheader("Standings")
st.dataframe(
    df,
    column_config={
        "Crest": st.column_config.ImageColumn("Crest", width="small")
    },
    hide_index=True
)

#stats
st.subheader("Stats")

col1, col2, col3 = st.columns(3)

with col1:
    most_wins = df.loc[df["Won"].idxmax(), "Team"]
    st.metric("Most Wins", most_wins, df["Won"].max())

with col2:
    most_draws = df.loc[df["Draw"].idxmax(), "Team"]
    st.metric("Biggest Draw Merchants", most_draws, df["Draw"].max())

with col3:
    most_losses = df.loc[df["Lost"].idxmax(), "Team"]
    st.metric("Most Losses", most_losses, df["Lost"].max(), delta_color="inverse")

col4, col5, col6 = st.columns(3)

with col4:
    best_gd = df.loc[df["GD"].idxmax(), "Team"]
    st.metric("Best Goal Difference", best_gd, df["GD"].max())

with col5:
    worst_gd = df.loc[df["GD"].idxmin(), "Team"]
    st.metric("Worst Goal Difference", worst_gd, df["GD"].min())

with col6:
    best_ppg = df.loc[df["PPG"].idxmax(), "Team"]
    st.metric("Most Efficient Team", best_ppg, df["PPG"].max())
