"""
Cria uma tabela larga, com uma linha por jogo e uma coluna por métrica.

Entrada:
data/sofascore/processed/benfica_2025_26_match_statistics_long.csv

Saída:
data/sofascore/processed/benfica_2025_26_match_statistics_wide.csv
"""

import re
import unicodedata
from pathlib import Path

import pandas as pd


INPUT_FILE = Path(
    "data/sofascore/processed/"
    "benfica_2025_26_match_statistics_long.csv"
)

OUTPUT_FILE = Path(
    "data/sofascore/processed/"
    "benfica_2025_26_match_statistics_wide.csv"
)


def clean_name(value):
    value = unicodedata.normalize("NFKD", str(value))
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


df = pd.read_csv(INPUT_FILE)

df = df[df["period"] == "ALL"].copy()

df["metric_name"] = (
    df["group"].map(clean_name)
    + "__"
    + df["metric"].map(clean_name)
)

identifiers = [
    "event_id",
    "date",
    "competition",
    "season",
    "round",
    "venue",
    "opponent",
    "home_team",
    "away_team"
]

benfica = (
    df.pivot_table(
        index=identifiers,
        columns="metric_name",
        values="benfica_value",
        aggfunc="first"
    )
    .add_prefix("benfica__")
    .reset_index()
)

opponent = (
    df.pivot_table(
        index=identifiers,
        columns="metric_name",
        values="opponent_value",
        aggfunc="first"
    )
    .add_prefix("opponent__")
    .reset_index()
)

wide = benfica.merge(
    opponent,
    on=identifiers,
    how="outer"
)

wide.columns.name = None

wide = wide.sort_values(
    ["date", "event_id"]
)

wide.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Jogos guardados:", len(wide))
print("Colunas guardadas:", len(wide.columns))
print("Ficheiro:", OUTPUT_FILE)
