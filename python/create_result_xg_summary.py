"""
Cria uma tabela curta para apresentar no site os jogos em que
o resultado real divergiu do desfecho sugerido pelo xG.

Entrada:
data/processed/benfica_2025_26_result_performance_gap.csv

Saída:
data/processed/benfica_2025_26_result_xg_summary.csv
"""

from pathlib import Path

import pandas as pd


INPUT_FILE = Path(
    "data/processed/"
    "benfica_2025_26_result_performance_gap.csv"
)

OUTPUT_FILE = Path(
    "data/processed/"
    "benfica_2025_26_result_xg_summary.csv"
)


df = pd.read_csv(INPUT_FILE)

summary = df[
    df["result_performance_gap"] != 0
].copy()

summary["date"] = pd.to_datetime(
    summary["date"],
    errors="coerce"
).dt.strftime("%d/%m/%Y")

summary["venue_pt"] = summary["venue"].map({
    "Home": "Casa",
    "Away": "Fora",
})

summary["score"] = (
    summary["benfica_goals"]
    .astype("Int64")
    .astype(str)
    + "–"
    + summary["opponent_goals"]
    .astype("Int64")
    .astype(str)
)

summary["xg_score"] = (
    summary["xg"].round(2).astype(str)
    + "–"
    + summary["opponent_xg"].round(2).astype(str)
)

summary = summary[
    [
        "date",
        "opponent",
        "venue_pt",
        "score",
        "xg_score",
        "xg_difference",
        "result_xg_class",
        "result_performance_gap",
    ]
].rename(
    columns={
        "date": "data",
        "opponent": "adversario",
        "venue_pt": "local",
        "score": "resultado",
        "xg_score": "xg",
        "xg_difference": "diferenca_xg",
        "result_xg_class": "classificacao",
        "result_performance_gap": "desvio_pontos",
    }
)

summary = summary.sort_values(
    [
        "desvio_pontos",
        "diferenca_xg",
    ],
    ascending=[
        True,
        False,
    ],
)

summary.to_csv(
    OUTPUT_FILE,
    index=False,
)

print("Jogos divergentes:", len(summary))

print("\nPor classificação:")
print(
    summary["classificacao"]
    .value_counts()
    .to_string()
)

print("\nFicheiro:", OUTPUT_FILE)
