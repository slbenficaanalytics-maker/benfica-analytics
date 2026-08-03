"""
Combina alinhamentos e estatísticas individuais dos jogadores.

Entrada:
data/sofascore/raw/2025_26/<event_id>/lineups.json

Saída:
data/sofascore/processed/benfica_2025_26_player_match_stats.csv
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
    "benfica_2025_26_player_match_stats.csv"
)


def is_benfica(team_name):
    return "benfica" in str(team_name).lower()


events = pd.read_csv(EVENTS_FILE)

rows = []

for _, event in events.iterrows():
    event_id = int(event["event_id"])

    lineups_file = (
        RAW_DIR / str(event_id) / "lineups.json"
    )

    if not lineups_file.exists():
        print(f"Ficheiro em falta: {event_id}")
        continue

    with lineups_file.open(
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    for side in ["home", "away"]:
        team_name = event[f"{side}_team"]

        if not is_benfica(team_name):
            continue

        for item in data.get(side, {}).get("players", []):
            player = item.get("player") or {}
            statistics = item.get("statistics") or {}

            row = {
                "event_id": event_id,
                "date": event.get("date"),
                "competition": event.get("competition"),
                "season": event.get("season"),
                "round": event.get("round"),
                "venue": "Home" if side == "home" else "Away",
                "opponent": (
                    event["away_team"]
                    if side == "home"
                    else event["home_team"]
                ),
                "player_id": player.get("id"),
                "player": player.get("name"),
                "position": player.get("position"),
                "shirt_number": item.get("shirtNumber"),
                "starter": not item.get("substitute", False)
            }

            for key, value in statistics.items():
                row[key] = value

            rows.append(row)

players = pd.DataFrame(rows)

players = players.sort_values(
    [
        "date",
        "event_id",
        "starter",
        "player"
    ],
    ascending=[True, True, False, True]
)

players.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Jogos processados:", players["event_id"].nunique())
print("Jogadores distintos:", players["player_id"].nunique())
print("Linhas guardadas:", len(players))
print("Colunas guardadas:", len(players.columns))
print("Ficheiro:", OUTPUT_FILE)
