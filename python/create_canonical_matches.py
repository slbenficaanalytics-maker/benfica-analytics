"""
Cria a tabela principal dos jogos do Benfica na Liga Portugal 2025/26.

Fonte:
data/processed/benfica_2025_26_match_id_crosswalk_extended.csv

Saída:
data/processed/benfica_2025_26_matches_canonical.csv
"""

from pathlib import Path

import pandas as pd


INPUT_FILE = Path(
    "data/processed/"
    "benfica_2025_26_match_id_crosswalk_extended.csv"
)

OUTPUT_FILE = Path(
    "data/processed/"
    "benfica_2025_26_matches_canonical.csv"
)


df = pd.read_csv(INPUT_FILE)

canonical = pd.DataFrame({
    "benfica_match_id": df["benfica_match_id"],
    "date": df["date"],
    "season": "2025/26",
    "competition": "Liga Portugal",
    "venue": df["venue"],
    "opponent_key": df["opponent_key"],

    "opponent": df[
        "opponent_sofascore"
    ].fillna(
        df["opponent_fotmob"]
    ),

    "home_team": df[
        "home_team_sofascore"
    ].fillna(
        df["home_team_fotmob"]
    ),

    "away_team": df[
        "away_team_sofascore"
    ].fillna(
        df["away_team_fotmob"]
    ),

    "round": df[
        "round_sofascore"
    ].fillna(
        df["round_fotmob"]
    ),

    "home_goals": df["FTHG"],
    "away_goals": df["FTAG"],
    "result_home": df["FTR"],

    "sofascore_event_id": df[
        "sofascore_event_id"
    ],

    "fotmob_match_id": df[
        "fotmob_match_id"
    ],

    "football_data_row_id": df[
        "football_data_row_id"
    ]
})

canonical["benfica_goals"] = canonical.apply(
    lambda row: (
        row["home_goals"]
        if row["venue"] == "Home"
        else row["away_goals"]
    ),
    axis=1
)

canonical["opponent_goals"] = canonical.apply(
    lambda row: (
        row["away_goals"]
        if row["venue"] == "Home"
        else row["home_goals"]
    ),
    axis=1
)

canonical["result"] = canonical.apply(
    lambda row: (
        "W"
        if row["benfica_goals"] > row["opponent_goals"]
        else "D"
        if row["benfica_goals"] == row["opponent_goals"]
        else "L"
    ),
    axis=1
)

canonical = canonical.sort_values(
    ["date", "benfica_match_id"]
)

if not canonical["benfica_match_id"].is_unique:
    raise RuntimeError(
        "Existem benfica_match_id duplicados."
    )

canonical.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Jogos guardados:", len(canonical))
print(
    "IDs internos únicos:",
    canonical["benfica_match_id"].nunique()
)
print(
    "IDs Sofascore presentes:",
    canonical["sofascore_event_id"].notna().sum()
)
print(
    "IDs FotMob presentes:",
    canonical["fotmob_match_id"].notna().sum()
)
print(
    "Linhas Football-Data presentes:",
    canonical["football_data_row_id"].notna().sum()
)
print("Ficheiro:", OUTPUT_FILE)
