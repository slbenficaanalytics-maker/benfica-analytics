"""
Acrescenta benfica_match_id às estatísticas jogador-jogo
do Sofascore.

Entradas:
- data/processed/benfica_2025_26_matches_canonical.csv
- data/sofascore/processed/benfica_2025_26_player_match_stats.csv

Saída:
- data/sofascore/processed/
  benfica_2025_26_player_match_stats_canonical.csv
"""

from pathlib import Path

import pandas as pd


CANONICAL_FILE = Path(
    "data/processed/"
    "benfica_2025_26_matches_canonical.csv"
)

PLAYERS_FILE = Path(
    "data/sofascore/processed/"
    "benfica_2025_26_player_match_stats.csv"
)

OUTPUT_FILE = Path(
    "data/sofascore/processed/"
    "benfica_2025_26_player_match_stats_canonical.csv"
)


canonical = pd.read_csv(CANONICAL_FILE)
players = pd.read_csv(PLAYERS_FILE)

id_map = canonical[
    [
        "benfica_match_id",
        "sofascore_event_id"
    ]
].copy()

id_map["sofascore_event_id"] = pd.to_numeric(
    id_map["sofascore_event_id"],
    errors="coerce"
).astype("Int64")

players["event_id"] = pd.to_numeric(
    players["event_id"],
    errors="coerce"
).astype("Int64")

result = players.merge(
    id_map,
    left_on="event_id",
    right_on="sofascore_event_id",
    how="left",
    validate="many_to_one"
)

first_columns = [
    "benfica_match_id",
    "event_id"
]

remaining_columns = [
    column
    for column in result.columns
    if column not in first_columns
    and column != "sofascore_event_id"
]

result = result[
    first_columns + remaining_columns
]

result.to_csv(
    OUTPUT_FILE,
    index=False
)

liga_ids = set(
    canonical["sofascore_event_id"]
    .dropna()
    .astype("Int64")
)

liga = result[
    result["event_id"].isin(liga_ids)
]

print("Registos totais:", len(result))
print("Registos da Liga:", len(liga))
print(
    "Registos da Liga com ID interno:",
    liga["benfica_match_id"].notna().sum()
)
print(
    "Registos da Liga sem ID interno:",
    liga["benfica_match_id"].isna().sum()
)
print(
    "Jogos da Liga representados:",
    liga["benfica_match_id"].nunique()
)
print(
    "Jogadores distintos na Liga:",
    liga["player"].nunique()
)
print("Ficheiro:", OUTPUT_FILE)
