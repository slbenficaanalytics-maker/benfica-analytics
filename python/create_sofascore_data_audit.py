from pathlib import Path

import pandas as pd


PROCESSED_DIR = Path("data/sofascore/processed")

events = pd.read_csv(
    "data/raw/sofascore_benfica_2025_26_events.csv"
)

match_stats = pd.read_csv(
    PROCESSED_DIR /
    "benfica_2025_26_match_statistics_wide.csv"
)

incidents = pd.read_csv(
    PROCESSED_DIR /
    "benfica_2025_26_incidents.csv"
)

players = pd.read_csv(
    PROCESSED_DIR /
    "benfica_2025_26_player_match_stats.csv"
)

shots = pd.read_csv(
    PROCESSED_DIR /
    "benfica_2025_26_shots.csv"
)

shot_coverage = (
    shots.groupby("event_id")
    .agg(
        total_shots=("event_id", "size"),
        shots_with_xg=("xg", "count")
    )
    .reset_index()
)

shot_coverage["shots_without_xg"] = (
    shot_coverage["total_shots"]
    - shot_coverage["shots_with_xg"]
)

audit = pd.DataFrame({
    "item": [
        "Jogos oficiais",
        "Jogos com estatísticas",
        "Jogos com incidentes",
        "Jogos com alinhamentos",
        "Jogos com mapas de remates",
        "Jogadores distintos",
        "Registos jogador-jogo",
        "Incidentes",
        "Remates",
        "Remates do Benfica",
        "Remates dos adversários",
        "Jogos totalmente sem xG por remate",
        "Jogos com cobertura parcial de xG",
        "Remates isolados sem xG"
    ],
    "value": [
        events["event_id"].nunique(),
        match_stats["event_id"].nunique(),
        incidents["event_id"].nunique(),
        players["event_id"].nunique(),
        shots["event_id"].nunique(),
        players["player_id"].nunique(),
        len(players),
        len(incidents),
        len(shots),
        (shots["team_side"] == "Benfica").sum(),
        (shots["team_side"] == "Opponent").sum(),
        (
            shot_coverage["shots_with_xg"] == 0
        ).sum(),
        (
            (shot_coverage["shots_with_xg"] > 0)
            & (shot_coverage["shots_without_xg"] > 0)
        ).sum(),
        shot_coverage.loc[
            shot_coverage["shots_with_xg"] > 0,
            "shots_without_xg"
        ].sum()
    ]
})

output_file = (
    PROCESSED_DIR /
    "benfica_2025_26_data_audit.csv"
)

audit.to_csv(output_file, index=False)

print(audit.to_string(index=False))
print("\nFicheiro:", output_file)
