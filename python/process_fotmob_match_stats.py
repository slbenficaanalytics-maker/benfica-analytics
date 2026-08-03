"""
Extrai do FotMob as principais estatísticas dos 34 jogos da Liga Portugal 2025/26.

Entrada:
data/fotmob/raw/2025_26_liga/<match_id>.json

Saída:
data/fotmob/processed/benfica_2025_26_liga_match_stats.csv
"""

import json
import re
import unicodedata
from pathlib import Path

import pandas as pd


MATCHES_FILE = Path(
    "data/raw/fotmob_benfica_2025_26_liga_matches.csv"
)

RAW_DIR = Path(
    "data/fotmob/raw/2025_26_liga"
)

OUTPUT_DIR = Path(
    "data/fotmob/processed"
)

OUTPUT_FILE = OUTPUT_DIR / (
    "benfica_2025_26_liga_match_stats.csv"
)


def is_benfica(name):
    return "benfica" in str(name).lower()


def clean_name(value):
    value = unicodedata.normalize("NFKD", str(value))
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


matches = pd.read_csv(MATCHES_FILE)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

rows = []

for _, match in matches.iterrows():
    match_id = int(match["match_id"])

    input_file = RAW_DIR / f"{match_id}.json"

    if not input_file.exists():
        print(f"Ficheiro em falta: {match_id}")
        continue

    with input_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    periods = (
        data.get("content", {})
            .get("stats", {})
            .get("Periods", {})
    )

    all_period = periods.get("All", {})

    stats_groups = (
        all_period.get("stats")
        or all_period.get("Stats")
        or []
    )

    home_team = match["home_team"]
    away_team = match["away_team"]

    benfica_is_home = is_benfica(home_team)

    row = {
        "match_id": match_id,
        "date": match.get("date"),
        "round": match.get("round"),
        "home_team": home_team,
        "away_team": away_team,
        "venue": "Home" if benfica_is_home else "Away",
        "opponent": away_team if benfica_is_home else home_team
    }

    for group in stats_groups:
        group_name = clean_name(group.get("title"))

        for item in group.get("stats", []):
            metric = clean_name(item.get("title"))
            values = item.get("stats")

            if not isinstance(values, list) or len(values) < 2:
                continue

            home_value = values[0]
            away_value = values[1]

            metric_name = f"{group_name}__{metric}"

            if benfica_is_home:
                row[f"benfica__{metric_name}"] = home_value
                row[f"opponent__{metric_name}"] = away_value
            else:
                row[f"benfica__{metric_name}"] = away_value
                row[f"opponent__{metric_name}"] = home_value

    rows.append(row)

df = pd.DataFrame(rows)

df = df.sort_values(["date", "match_id"])

df.to_csv(OUTPUT_FILE, index=False)

print("Jogos processados:", len(df))
print("Colunas guardadas:", len(df.columns))
print("Ficheiro:", OUTPUT_FILE)
