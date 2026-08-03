"""
Compara Sofascore e FotMob nos 34 jogos da Liga Portugal 2025/26.

Compara:
- posse
- remates
- remates enquadrados
- xG

Saída:
data/comparisons/sofascore_vs_fotmob_2025_26_liga.csv
"""

import re
from pathlib import Path

import pandas as pd


SOFASCORE_FILE = Path(
    "data/sofascore/processed/"
    "benfica_2025_26_match_statistics_wide.csv"
)

FOTMOB_FILE = Path(
    "data/fotmob/processed/"
    "benfica_2025_26_liga_match_stats.csv"
)

OUTPUT_DIR = Path("data/comparisons")

OUTPUT_FILE = OUTPUT_DIR / (
    "sofascore_vs_fotmob_2025_26_liga.csv"
)


def normalise_team(value):
    value = str(value).lower()

    replacements = {
        "cf estrela amadora": "estrela amadora",
        "estrela da amadora": "estrela amadora",
        "fc alverca": "alverca",
        "fc arouca": "arouca",
        "vitória sc": "vitoria guimaraes",
        "vitoria de guimaraes": "vitoria guimaraes",
        "casa pia ac": "casa pia",
        "cd nacional": "nacional",
        "famalicão": "famalicao",
        "sporting braga": "braga",
        "estoril praia": "estoril"
    }

    value = replacements.get(value, value)

    value = (
        value.replace("á", "a")
             .replace("à", "a")
             .replace("â", "a")
             .replace("ã", "a")
             .replace("é", "e")
             .replace("ê", "e")
             .replace("í", "i")
             .replace("ó", "o")
             .replace("ô", "o")
             .replace("õ", "o")
             .replace("ú", "u")
             .replace("ç", "c")
    )

    value = re.sub(r"[^a-z0-9]+", "", value)

    return value


def first_existing_column(df, candidates):
    for column in candidates:
        if column in df.columns:
            return column

    return None


def numeric_part(series):
    return pd.to_numeric(
        series.astype(str).str.extract(
            r"(-?\d+(?:\.\d+)?)"
        )[0],
        errors="coerce"
    )


sofa = pd.read_csv(SOFASCORE_FILE)
fotmob = pd.read_csv(FOTMOB_FILE)

sofa = sofa[
    sofa["competition"].astype(str).str.contains(
        "Liga Portugal",
        case=False,
        na=False
    )
].copy()

sofa["date"] = pd.to_datetime(
    sofa["date"],
    errors="coerce"
).dt.strftime("%Y-%m-%d")

fotmob["date"] = pd.to_datetime(
    fotmob["date"],
    errors="coerce"
).dt.strftime("%Y-%m-%d")

sofa["opponent_key"] = sofa["opponent"].map(
    normalise_team
)

fotmob["opponent_key"] = fotmob["opponent"].map(
    normalise_team
)

sofa_columns = {
    "possession": first_existing_column(
        sofa,
        [
            "benfica__match_overview__ball_possession"
        ]
    ),
    "shots": first_existing_column(
        sofa,
        [
            "benfica__match_overview__total_shots",
            "benfica__shots__total_shots"
        ]
    ),
    "shots_on_target": first_existing_column(
        sofa,
        [
            "benfica__shots__shots_on_target"
        ]
    ),
    "xg": first_existing_column(
        sofa,
        [
            "benfica__match_overview__expected_goals"
        ]
    )
}

fotmob_columns = {
    "possession": first_existing_column(
        fotmob,
        [
            "benfica__top_stats__ball_possession"
        ]
    ),
    "shots": first_existing_column(
        fotmob,
        [
            "benfica__top_stats__total_shots",
            "benfica__shots__total_shots"
        ]
    ),
    "shots_on_target": first_existing_column(
        fotmob,
        [
            "benfica__top_stats__shots_on_target",
            "benfica__shots__shots_on_target"
        ]
    ),
    "xg": first_existing_column(
        fotmob,
        [
            "benfica__top_stats__expected_goals_xg",
            "benfica__expected_goals_xg__expected_goals_xg"
        ]
    )
}

print("Colunas Sofascore:", sofa_columns)
print("Colunas FotMob:", fotmob_columns)

for metric, column in sofa_columns.items():
    if column:
        sofa[f"sofascore_{metric}"] = numeric_part(
            sofa[column]
        )

for metric, column in fotmob_columns.items():
    if column:
        fotmob[f"fotmob_{metric}"] = numeric_part(
            fotmob[column]
        )

sofa_keep = [
    "event_id",
    "date",
    "opponent",
    "opponent_key",
    "venue"
] + [
    f"sofascore_{metric}"
    for metric, column in sofa_columns.items()
    if column
]

fotmob_keep = [
    "match_id",
    "date",
    "opponent",
    "opponent_key",
    "venue"
] + [
    f"fotmob_{metric}"
    for metric, column in fotmob_columns.items()
    if column
]

comparison = sofa[sofa_keep].merge(
    fotmob[fotmob_keep],
    on=["date", "opponent_key", "venue"],
    how="inner",
    suffixes=("_sofa", "_fotmob")
)

for metric in [
    "possession",
    "shots",
    "shots_on_target",
    "xg"
]:
    sofa_metric = f"sofascore_{metric}"
    fotmob_metric = f"fotmob_{metric}"

    if (
        sofa_metric in comparison.columns
        and fotmob_metric in comparison.columns
    ):
        comparison[f"difference_{metric}"] = (
            comparison[sofa_metric]
            - comparison[fotmob_metric]
        )

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

comparison.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nJogos comparados:", len(comparison))

for metric in [
    "possession",
    "shots",
    "shots_on_target",
    "xg"
]:
    difference = f"difference_{metric}"

    if difference in comparison.columns:
        available = comparison[difference].notna()

        print(f"\n{metric}:")
        print(
            "Casos comparáveis:",
            available.sum()
        )
        print(
            "Diferença média absoluta:",
            comparison.loc[
                available,
                difference
            ].abs().mean().round(3)
        )
        print(
            "Máxima diferença absoluta:",
            comparison.loc[
                available,
                difference
            ].abs().max()
        )

print("\nFicheiro:", OUTPUT_FILE)
