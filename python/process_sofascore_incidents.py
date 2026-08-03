"""
Combina os incidentes dos jogos do Sofascore numa tabela única.

Entrada:
data/sofascore/raw/2025_26/<event_id>/incidents.json

Saída:
data/sofascore/processed/benfica_2025_26_incidents.csv
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
    "benfica_2025_26_incidents.csv"
)


def is_benfica(team_name):
    return "benfica" in str(team_name).lower()


events = pd.read_csv(EVENTS_FILE)

rows = []

for _, event in events.iterrows():
    event_id = int(event["event_id"])

    incidents_file = (
        RAW_DIR / str(event_id) / "incidents.json"
    )

    if not incidents_file.exists():
        print(f"Ficheiro em falta: {event_id}")
        continue

    with incidents_file.open(
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    benfica_is_home = is_benfica(event["home_team"])

    for incident in data.get("incidents", []):
        is_home = incident.get("isHome")

        if is_home is True:
            incident_team = event["home_team"]
        elif is_home is False:
            incident_team = event["away_team"]
        else:
            incident_team = None

        if incident_team is None:
            team_side = None
        elif is_benfica(incident_team):
            team_side = "Benfica"
        else:
            team_side = "Opponent"

        player = incident.get("player") or {}
        player_in = incident.get("playerIn") or {}
        player_out = incident.get("playerOut") or {}
        assist = incident.get("assist1") or {}

        rows.append({
            "event_id": event_id,
            "date": event.get("date"),
            "competition": event.get("competition"),
            "round": event.get("round"),
            "home_team": event.get("home_team"),
            "away_team": event.get("away_team"),
            "incident_type": incident.get(
                "incidentType"
            ),
            "incident_class": incident.get(
                "incidentClass"
            ),
            "time": incident.get("time"),
            "added_time": incident.get(
                "addedTime"
            ),
            "period": (
    "1ST"
    if incident.get("time") is not None
    and incident.get("time") <= 45
    else "2ND"
    if incident.get("time") is not None
    and incident.get("time") <= 90
    else "ET1"
    if incident.get("time") is not None
    and incident.get("time") <= 105
    else "ET2"
    if incident.get("time") is not None
    else None
),
            "is_home": is_home,
            "incident_team": incident_team,
            "team_side": team_side,
            "player_id": player.get("id"),
            "player": player.get("name"),
            "assist_id": assist.get("id"),
            "assist": assist.get("name"),
            "player_in_id": player_in.get("id"),
            "player_in": player_in.get("name"),
            "player_out_id": player_out.get("id"),
            "player_out": player_out.get("name"),
            "home_score": incident.get(
                "homeScore"
            ),
            "away_score": incident.get(
                "awayScore"
            ),
            "from_penalty": incident.get(
                "fromPenalty"
            ),
            "rescinded": incident.get(
                "rescinded"
            )
        })

incidents = pd.DataFrame(rows)

incidents["match_minute"] = (
    incidents["time"].fillna(0)
    + incidents["added_time"].fillna(0)
)

incidents = incidents.sort_values(
    [
        "date",
        "event_id",
        "match_minute"
    ]
)

incidents.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    "Jogos processados:",
    incidents["event_id"].nunique()
)

print(
    "Incidentes guardados:",
    len(incidents)
)

print("\nTipos de incidente:")
print(
    incidents["incident_type"]
    .value_counts(dropna=False)
    .to_string()
)

print("\nFicheiro:", OUTPUT_FILE)
