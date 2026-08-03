"""
Acrescenta a chave interna benfica_match_id
à tabela de estatísticas do FotMob.

Entradas:
- data/processed/benfica_2025_26_matches_canonical.csv
- data/fotmob/processed/benfica_2025_26_liga_match_stats.csv

Saída:
- data/fotmob/processed/
  benfica_2025_26_liga_match_stats_canonical.csv
"""

from pathlib import Path

import pandas as pd


CANONICAL_FILE = Path(
    "data/processed/"
    "benfica_2025_26_matches_canonical.csv"
)

STATS_FILE = Path(
    "data/fotmob/processed/"
    "benfica_2025_26_liga_match_stats.csv"
)

OUTPUT_FILE = Path(
    "data/fotmob/processed/"
    "benfica_2025_26_liga_match_stats_canonical.csv"
)


canonical = pd.read_csv(CANONICAL_FILE)
stats = pd.read_csv(STATS_FILE)

id_map = canonical[
    [
        "benfica_match_id",
        "fotmob_match_id"
    ]
].copy()

id_map["fotmob_match_id"] = pd.to_numeric(
    id_map["fotmob_match_id"],
    errors="coerce"
).astype("Int64")

stats["match_id"] = pd.to_numeric(
    stats["match_id"],
    errors="coerce"
).astype("Int64")

result = stats.merge(
    id_map,
    left_on="match_id",
    right_on="fotmob_match_id",
    how="left",
    validate="one_to_one"
)

first_columns = [
    "benfica_match_id",
    "match_id"
]

remaining_columns = [
    column
    for column in result.columns
    if column not in first_columns
    and column != "fotmob_match_id"
]

result = result[
    first_columns + remaining_columns
]

result.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Linhas totais:", len(result))
print(
    "Com ID interno:",
    result["benfica_match_id"].notna().sum()
)
print(
    "Sem ID interno:",
    result["benfica_match_id"].isna().sum()
)
print(
    "IDs internos únicos:",
    result["benfica_match_id"].nunique()
)
print("Ficheiro:", OUTPUT_FILE)
