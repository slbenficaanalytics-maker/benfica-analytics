"""
Compara o resultado real com o desempenho sugerido pelo xG.

Regra provisória:
- diferença de xG superior a +0,25: desempenho de vitória
- entre -0,25 e +0,25: desempenho de empate
- inferior a -0,25: desempenho de derrota

Entrada:
data/processed/benfica_2025_26_liga_match_analysis.csv

Saída:
data/processed/benfica_2025_26_result_performance_gap.csv
"""

from pathlib import Path

import pandas as pd


INPUT_FILE = Path(
    "data/processed/"
    "benfica_2025_26_liga_match_analysis.csv"
)

OUTPUT_FILE = Path(
    "data/processed/"
    "benfica_2025_26_result_performance_gap.csv"
)


df = pd.read_csv(INPUT_FILE)


numeric_columns = [
    "benfica_goals",
    "opponent_goals",
    "xg",
    "opponent_xg",
    "xg_difference",
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce",
    )


def expected_result_from_xg(xg_difference):
    if pd.isna(xg_difference):
        return pd.NA

    if xg_difference > 0.25:
        return "W"

    if xg_difference < -0.25:
        return "L"

    return "D"


df["xg_result"] = df["xg_difference"].map(
    expected_result_from_xg
)


result_points = {
    "W": 3,
    "D": 1,
    "L": 0,
}

df["actual_result_points"] = df["result"].map(
    result_points
)

df["xg_result_points"] = df["xg_result"].map(
    result_points
)

df["result_performance_gap"] = (
    df["actual_result_points"]
    - df["xg_result_points"]
)


df["result_xg_class"] = df[
    "result_performance_gap"
].map({
    3: "Vitória quando o xG sugeria derrota",
    2: "Vitória quando o xG sugeria empate",
    1: "Empate quando o xG sugeria derrota",
    0: "Resultado coincidente com o desfecho do xG",
    -1: "Empate quando o xG sugeria vitória",
    -2: "Empate quando o xG sugeria vitória",
    -3: "Derrota quando o xG sugeria vitória",
})


keep_columns = [
    "benfica_match_id",
    "date",
    "opponent",
    "venue",
    "benfica_goals",
    "opponent_goals",
    "result",
    "xg",
    "opponent_xg",
    "xg_difference",
    "xg_result",
    "actual_result_points",
    "xg_result_points",
    "result_performance_gap",
    "result_xg_class",
]


result = df[keep_columns].sort_values(
    ["date", "benfica_match_id"]
)

result.to_csv(
    OUTPUT_FILE,
    index=False,
)


print("Jogos analisados:", len(result))

print("\nClassificação:")
print(
    result["result_xg_class"]
    .value_counts(dropna=False)
    .to_string()
)

print("\nMaiores divergências:")
print(
    result[
        [
            "date",
            "opponent",
            "result",
            "xg_difference",
            "xg_result",
            "result_performance_gap",
        ]
    ]
    .sort_values(
        [
            "result_performance_gap",
            "xg_difference",
        ]
    )
    .to_string(index=False)
)

print("\nFicheiro:", OUTPUT_FILE)
