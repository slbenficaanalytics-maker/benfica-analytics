"""
Audita a tabela analítica da Liga Portugal 2025/26.

Verifica:
- IDs duplicados
- campos essenciais em falta
- resultados incoerentes
- valores estatísticos impossíveis
"""

from pathlib import Path

import pandas as pd


INPUT_FILE = Path(
    "data/processed/"
    "benfica_2025_26_liga_match_analysis.csv"
)


df = pd.read_csv(INPUT_FILE)

numeric_columns = [
    "benfica_goals",
    "opponent_goals",
    "possession",
    "opponent_possession",
    "shots",
    "shots_on_target",
    "opponent_shots",
    "opponent_shots_on_target",
    "xg",
    "opponent_xg",
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False),
        errors="coerce",
    )

errors = []


# 1. Chave interna
duplicate_ids = df[
    df["benfica_match_id"].duplicated(keep=False)
]

if len(duplicate_ids) > 0:
    errors.append(
        f"IDs internos duplicados: {len(duplicate_ids)} linhas"
    )


# 2. Campos essenciais
essential_columns = [
    "benfica_match_id",
    "date",
    "opponent",
    "venue",
    "benfica_goals",
    "opponent_goals",
    "result",
    "possession",
    "shots",
    "shots_on_target",
    "xg",
    "opponent_shots",
    "opponent_shots_on_target",
    "opponent_xg",
]

missing_essential = df[
    essential_columns
].isna().sum()

for column, count in missing_essential.items():
    if count > 0:
        errors.append(
            f"{column}: {count} valores em falta"
        )


# 3. Resultado coerente com os golos
expected_result = df.apply(
    lambda row: (
        "W"
        if row["benfica_goals"] > row["opponent_goals"]
        else "D"
        if row["benfica_goals"] == row["opponent_goals"]
        else "L"
    ),
    axis=1,
)

result_mismatch = df[
    df["result"] != expected_result
]

if len(result_mismatch) > 0:
    errors.append(
        f"Resultados incoerentes: {len(result_mismatch)}"
    )


# 4. Limites estatísticos básicos
checks = {
    "possession_below_zero": df["possession"] < 0,
    "possession_above_100": df["possession"] > 100,
    "opponent_possession_below_zero":
        df["opponent_possession"] < 0,
    "opponent_possession_above_100":
        df["opponent_possession"] > 100,
    "shots_below_zero": df["shots"] < 0,
    "opponent_shots_below_zero":
        df["opponent_shots"] < 0,
    "shots_on_target_above_shots":
        df["shots_on_target"] > df["shots"],
    "opponent_sot_above_shots":
        df["opponent_shots_on_target"]
        > df["opponent_shots"],
    "xg_below_zero": df["xg"] < 0,
    "opponent_xg_below_zero":
        df["opponent_xg"] < 0,
}

for name, condition in checks.items():
    count = int(condition.fillna(False).sum())

    if count > 0:
        errors.append(
            f"{name}: {count} jogos"
        )


# 5. Soma aproximada da posse
possession_total = (
    df["possession"]
    + df["opponent_possession"]
)

possession_mismatch = df[
    (possession_total < 99)
    | (possession_total > 101)
]

if len(possession_mismatch) > 0:
    errors.append(
        "Soma da posse fora de 99–101%: "
        f"{len(possession_mismatch)} jogos"
    )


print("Jogos auditados:", len(df))
print(
    "IDs internos únicos:",
    df["benfica_match_id"].nunique()
)
print(
    "Datas distintas:",
    df["date"].nunique()
)
print(
    "Adversários distintos:",
    df["opponent_key"].nunique()
)

print("\nResultados:")
print(
    df["result"]
    .value_counts()
    .reindex(["W", "D", "L"], fill_value=0)
    .to_string()
)

print("\nAuditoria:")

if errors:
    for error in errors:
        print("-", error)

    raise SystemExit(
        "\nA auditoria encontrou problemas."
    )

print("Nenhum problema encontrado.")
