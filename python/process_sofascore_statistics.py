"""
Combina as estatísticas dos jogos do Sofascore numa tabela longa.

Entrada:
data/sofascore/raw/2025_26/<event_id>/statistics.json

Saída:
data/sofascore/processed/benfica_2025_26_match_statistics_long.csv
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

OUTPUT_DIR = Path(
    "data/sofascore/processed"
)

OUTPUT_FILE = OUTPUT_DIR / (
    "benfica_2025_26_match_statistics_long.csv"
)


def is_benfica(team_name):
    """Confirma se o nome corresponde ao Benfica."""
    return "benfica" in str(team_name).lower()


events = pd.read_csv(EVENTS_FILE)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

rows = []

for _, event in events.iterrows():
    event_id = int(event["event_id"])

    statistics_file = (
        RAW_DIR / str(event_id) / "statistics.json"
    )

    if not statistics_file.exists():
        print(f"Ficheiro em falta: {event_id}")
        continue

    with statistics_file.open(
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    benfica_is_home = is_benfica(event["home_team"])

    for period in data.get("statistics", []):
        period_name = period.get("period")

        for group in period.get("groups", []):
            group_name = group.get("groupName")

            for item in group.get(
                "statisticsItems",
                []
            ):
                home_value = item.get("home")
                away_value = item.get("away")

                if benfica_is_home:
                    benfica_value = home_value
                    opponent_value = away_value
                    venue = "Home"
                    opponent = event["away_team"]
                else:
                    benfica_value = away_value
                    opponent_value = home_value
                    venue = "Away"
                    opponent = event["home_team"]

                rows.append({
                    "event_id": event_id,
                    "date": event.get("date"),
                    "competition": event.get(
                        "competition"
                    ),
                    "season": event.get("season"),
                    "round": event.get("round"),
                    "venue": venue,
                    "opponent": opponent,
                    "home_team": event.get(
                        "home_team"
                    ),
                    "away_team": event.get(
                        "away_team"
                    ),
                    "period": period_name,
                    "group": group_name,
                    "metric": item.get("name"),
                    "benfica_value": benfica_value,
                    "opponent_value": opponent_value,
                    "home_value": home_value,
                    "away_value": away_value
                })

statistics = pd.DataFrame(rows)

statistics = statistics.sort_values(
    [
        "date",
        "event_id",
        "period",
        "group",
        "metric"
    ]
)

statistics.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Jogos processados:", statistics["event_id"].nunique())
print("Métricas distintas:", statistics["metric"].nunique())
print("Linhas guardadas:", len(statistics))
print("Ficheiro:", OUTPUT_FILE)
