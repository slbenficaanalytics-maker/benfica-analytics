"""
Combina os mapas de remates dos jogos do Sofascore.

Entrada:
data/sofascore/raw/2025_26/<event_id>/shotmap.json

Saída:
data/sofascore/processed/benfica_2025_26_shots.csv
"""

import json
from pathlib import Path

import pandas as pd


EVENTS_FILE = Path(
    "data/raw/sofascore_benfica_2025_26_events.csv"
)

RAW_DIR = Path(
    "data/sofascore/raw/2025_26"
)

OUTPUT_FILE = Path(
    "data/sofascore/processed/"
    "benfica_2025_26_shots.csv"
)


def is_benfica(team_name):
    return "benfica" in str(team_name).lower()


events = pd.read_csv(EVENTS_FILE)

rows = []

for _, event in events.iterrows():
    event_id = int(event["event_id"])

    shotmap_file = (
        RAW_DIR / str(event_id) / "shotmap.json"
    )

    if not shotmap_file.exists():
        print(f"Ficheiro em falta: {event_id}")
        continue

    with shotmap_file.open(
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    benfica_is_home = is_benfica(event["home_team"])

    for shot in data.get("shotmap", []):
        is_home = shot.get("isHome")

        if is_home is True:
            shooting_team = event["home_team"]
        elif is_home is False:
            shooting_team = event["away_team"]
        else:
            shooting_team = None

        if shooting_team is None:
            team_side = None
        elif is_benfica(shooting_team):
            team_side = "Benfica"
        else:
            team_side = "Opponent"

        player = shot.get("player") or {}
        coordinates = shot.get("playerCoordinates") or {}
        goalkeeper = shot.get("goalkeeper") or {}

        rows.append({
            "event_id": event_id,
            "date": event.get("date"),
            "competition": event.get("competition"),
            "round": event.get("round"),
            "venue": (
                "Home"
                if benfica_is_home
                else "Away"
            ),
            "opponent": (
                event["away_team"]
                if benfica_is_home
                else event["home_team"]
            ),
            "shooting_team": shooting_team,
            "team_side": team_side,
            "player_id": player.get("id"),
            "player": player.get("name"),
            "minute": shot.get("time"),
            "added_time": shot.get("addedTime"),
            "shot_type": shot.get("shotType"),
            "situation": shot.get("situation"),
            "body_part": shot.get("bodyPart"),
            "xg": shot.get("xg"),
            "xgot": shot.get("xgot"),
            "goal_mouth_location": shot.get(
                "goalMouthLocation"
            ),
            "x": coordinates.get("x"),
            "y": coordinates.get("y"),
            "z": coordinates.get("z"),
            "goalkeeper_id": goalkeeper.get("id"),
            "goalkeeper": goalkeeper.get("name")
        })

shots = pd.DataFrame(rows)

shots["match_minute"] = (
    shots["minute"].fillna(0)
    + shots["added_time"].fillna(0)
)

shots = shots.sort_values(
    [
        "date",
        "event_id",
        "match_minute"
    ]
)

shots.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Jogos processados:", shots["event_id"].nunique())
print("Remates guardados:", len(shots))
print(
    "Remates do Benfica:",
    (shots["team_side"] == "Benfica").sum()
)
print(
    "Remates dos adversários:",
    (shots["team_side"] == "Opponent").sum()
)
print(
    "Com xG:",
    shots["xg"].notna().sum()
)
print(
    "Com xGOT:",
    shots["xgot"].notna().sum()
)
print("Ficheiro:", OUTPUT_FILE)
