"""
Acrescenta a chave interna benfica_match_id
à tabela larga de estatísticas do Sofascore.

Entradas:
- data/processed/benfica_2025_26_matches_canonical.csv
- data/sofascore/processed/benfica_2025_26_match_statistics_wide.csv

Saída:
- data/sofascore/processed/
  benfica_2025_26_match_statistics_canonical.csv
"""

from pathlib import Path

import pandas as pd


CANONICAL_FILE = Path(
    "data/processed/"
    "benfica_2025_26_matches_canonical.csv"
)

STATS_FILE = Path(
    "data/sofascore/processed/"
    "benfica_2025_26_match_statistics_wide.csv"
)

OUTPUT_FILE = Path(
    "data/sofascore/processed/"
    "benfica_2025_26_match_statistics_canonical.csv"
)


canonical = pd.read_csv(CANONICAL_FILE)
stats = pd.read_csv(STATS_FILE)

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

stats["event_id"] = pd.to_numeric(
    stats["event_id"],
    errors="coerce"
).astype("Int64")

result = stats.merge(
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

liga = result[
    result["competition"].astype(str).str.contains(
        "Liga Portugal",
        case=False,
        na=False
    )
]

print("Linhas totais:", len(result))
print("Jogos da Liga:", len(liga))
print(
    "Jogos da Liga com ID interno:",
    liga["benfica_match_id"].notna().sum()
)
print(
    "Jogos da Liga sem ID interno:",
    liga["benfica_match_id"].isna().sum()
)
print("Ficheiro:", OUTPUT_FILE)
