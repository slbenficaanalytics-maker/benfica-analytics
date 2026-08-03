"""
Cria a primeira tabela analítica por jogo da Liga Portugal 2025/26.

Entradas:
- tabela canónica dos jogos
- estatísticas canónicas do Sofascore
- estatísticas canónicas do FotMob

Saída:
- data/processed/benfica_2025_26_liga_match_analysis.csv
"""

from pathlib import Path

import pandas as pd


CANONICAL_FILE = Path(
    "data/processed/"
    "benfica_2025_26_matches_canonical.csv"
)

SOFASCORE_FILE = Path(
    "data/sofascore/processed/"
    "benfica_2025_26_match_statistics_canonical.csv"
)

FOTMOB_FILE = Path(
    "data/fotmob/processed/"
    "benfica_2025_26_liga_match_stats_canonical.csv"
)

OUTPUT_FILE = Path(
    "data/processed/"
    "benfica_2025_26_liga_match_analysis.csv"
)


canonical = pd.read_csv(CANONICAL_FILE)
sofascore = pd.read_csv(SOFASCORE_FILE)
fotmob = pd.read_csv(FOTMOB_FILE)


# Manter apenas os jogos da Liga no Sofascore
sofascore = sofascore[
    sofascore["benfica_match_id"].notna()
].copy()


def first_existing(dataframe, candidates):
    """Devolve a primeira coluna existente entre várias alternativas."""
    for column in candidates:
        if column in dataframe.columns:
            return column

    return None


sofa_columns = {
    "possession": first_existing(
        sofascore,
        [
            "benfica__match_overview__ball_possession",
            "benfica__ball_possession",
        ],
    ),
    "shots": first_existing(
        sofascore,
        [
            "benfica__match_overview__total_shots",
            "benfica__shots__total_shots",
        ],
    ),
    "shots_on_target": first_existing(
        sofascore,
        [
            "benfica__match_overview__shots_on_target",
            "benfica__shots__shots_on_target",
        ],
    ),
    "xg": first_existing(
        sofascore,
        [
            "benfica__match_overview__expected_goals",
            "benfica__expected_goals__expected_goals",
        ],
    ),
    "opponent_possession": first_existing(
        sofascore,
        [
            "opponent__match_overview__ball_possession",
            "opponent__ball_possession",
        ],
    ),
    "opponent_shots": first_existing(
        sofascore,
        [
            "opponent__match_overview__total_shots",
            "opponent__shots__total_shots",
        ],
    ),
    "opponent_shots_on_target": first_existing(
        sofascore,
        [
            "opponent__match_overview__shots_on_target",
            "opponent__shots__shots_on_target",
        ],
    ),
    "opponent_xg": first_existing(
        sofascore,
        [
            "opponent__match_overview__expected_goals",
            "opponent__expected_goals__expected_goals",
        ],
    ),
}


missing = [
    name
    for name, column in sofa_columns.items()
    if column is None
]

if missing:
    raise RuntimeError(
        "Não foram encontradas estas métricas no Sofascore: "
        + ", ".join(missing)
    )


sofa_keep = pd.DataFrame({
    "benfica_match_id": sofascore["benfica_match_id"],
    "possession": sofascore[sofa_columns["possession"]],
    "shots": sofascore[sofa_columns["shots"]],
    "shots_on_target": sofascore[
        sofa_columns["shots_on_target"]
    ],
    "xg": sofascore[sofa_columns["xg"]],
    "opponent_possession": sofascore[
        sofa_columns["opponent_possession"]
    ],
    "opponent_shots": sofascore[
        sofa_columns["opponent_shots"]
    ],
    "opponent_shots_on_target": sofascore[
        sofa_columns["opponent_shots_on_target"]
    ],
    "opponent_xg": sofascore[
        sofa_columns["opponent_xg"]
    ],
})


# Selecionar métricas complementares do FotMob quando existirem
fotmob_candidates = {
    "xg_open_play": [
        "benfica__expected_goals_xg__xg_open_play",
    ],
    "xg_set_play": [
        "benfica__expected_goals_xg__xg_set_play",
    ],
    "xg_non_penalty": [
        "benfica__expected_goals_xg__xg_non_penalty",
    ],
    "xgot": [
        "benfica__expected_goals_xg__xg_on_target_xgot",
    ],
    "opponent_xg_open_play": [
        "opponent__expected_goals_xg__xg_open_play",
    ],
    "opponent_xg_set_play": [
        "opponent__expected_goals_xg__xg_set_play",
    ],
    "opponent_xg_non_penalty": [
        "opponent__expected_goals_xg__xg_non_penalty",
    ],
    "opponent_xgot": [
        "opponent__expected_goals_xg__xg_on_target_xgot",
    ],
}


fotmob_keep = pd.DataFrame({
    "benfica_match_id": fotmob["benfica_match_id"],
})

for output_name, candidates in fotmob_candidates.items():
    column = first_existing(fotmob, candidates)

    if column is not None:
        fotmob_keep[output_name] = fotmob[column]


analysis = (
    canonical
    .merge(
        sofa_keep,
        on="benfica_match_id",
        how="left",
        validate="one_to_one",
    )
    .merge(
        fotmob_keep,
        on="benfica_match_id",
        how="left",
        validate="one_to_one",
    )
)


analysis["shot_difference"] = (
    analysis["shots"]
    - analysis["opponent_shots"]
)

analysis["shots_on_target_difference"] = (
    analysis["shots_on_target"]
    - analysis["opponent_shots_on_target"]
)

analysis["xg_difference"] = (
    analysis["xg"]
    - analysis["opponent_xg"]
)

analysis["shot_accuracy"] = (
    analysis["shots_on_target"]
    / analysis["shots"]
)

analysis["opponent_shot_accuracy"] = (
    analysis["opponent_shots_on_target"]
    / analysis["opponent_shots"]
)

analysis["xg_per_shot"] = (
    analysis["xg"]
    / analysis["shots"]
)

analysis["opponent_xg_per_shot"] = (
    analysis["opponent_xg"]
    / analysis["opponent_shots"]
)

analysis["points"] = analysis["result"].map({
    "W": 3,
    "D": 1,
    "L": 0,
})


analysis = analysis.sort_values(
    ["date", "benfica_match_id"]
)

analysis.to_csv(
    OUTPUT_FILE,
    index=False,
)

print("Jogos guardados:", len(analysis))
print(
    "Jogos com posse:",
    analysis["possession"].notna().sum()
)
print(
    "Jogos com remates:",
    analysis["shots"].notna().sum()
)
print(
    "Jogos com xG:",
    analysis["xg"].notna().sum()
)
print(
    "Jogos com decomposição FotMob:",
    analysis["xg_open_play"].notna().sum()
    if "xg_open_play" in analysis.columns
    else 0
)
print("Colunas totais:", len(analysis.columns))
print("Ficheiro:", OUTPUT_FILE)
