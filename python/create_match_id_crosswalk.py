"""
Cria uma tabela de correspondência entre os jogos do Sofascore
e do FotMob na Liga Portugal 2025/26.

Saída:
data/processed/benfica_2025_26_match_id_crosswalk.csv
"""

import re
import unicodedata
from pathlib import Path

import pandas as pd


SOFASCORE_FILE = Path(
    "data/raw/sofascore_benfica_2025_26_events.csv"
)

FOTMOB_FILE = Path(
    "data/raw/fotmob_benfica_2025_26_liga_matches.csv"
)

OUTPUT_DIR = Path("data/processed")

OUTPUT_FILE = OUTPUT_DIR / (
    "benfica_2025_26_match_id_crosswalk.csv"
)


def normalise_team(value):
    """Normaliza nomes diferentes usados pelas fontes."""
    value = str(value).lower().strip()

    replacements = {
        "cf estrela amadora": "estrela amadora",
        "estrela da amadora": "estrela amadora",
        "fc alverca": "alverca",
        "fc arouca": "arouca",
        "vitória sc": "vitoria guimaraes",
        "vitoria de guimaraes": "vitoria guimaraes",
        "casa pia ac": "casa pia",
        "cd nacional": "nacional",
        "sporting braga": "braga",
        "estoril praia": "estoril",
    }

    value = replacements.get(value, value)

    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", "", value)

    return value


sofascore = pd.read_csv(SOFASCORE_FILE)

sofascore = sofascore[
    sofascore["competition"].astype(str).str.contains(
        "Liga Portugal",
        case=False,
        na=False
    )
].copy()

fotmob = pd.read_csv(FOTMOB_FILE)

# Criar local e adversário no ficheiro FotMob
fotmob["benfica_is_home"] = (
    fotmob["home_team"]
    .astype(str)
    .str.contains(
        "Benfica",
        case=False,
        na=False
    )
)

fotmob["venue"] = fotmob["benfica_is_home"].map({
    True: "Home",
    False: "Away"
})

fotmob["opponent"] = fotmob.apply(
    lambda row: (
        row["away_team"]
        if row["benfica_is_home"]
        else row["home_team"]
    ),
    axis=1
)

# Criar local e adversário no ficheiro Sofascore
sofascore["benfica_is_home"] = (
    sofascore["home_team"]
    .astype(str)
    .str.contains(
        "Benfica",
        case=False,
        na=False
    )
)

sofascore["venue"] = sofascore["benfica_is_home"].map({
    True: "Home",
    False: "Away"
})

sofascore["opponent"] = sofascore.apply(
    lambda row: (
        row["away_team"]
        if row["benfica_is_home"]
        else row["home_team"]
    ),
    axis=1
)

print("Colunas Sofascore:")
print(list(sofascore.columns))

print("\nColunas FotMob:")
print(list(fotmob.columns))

for dataframe in [sofascore, fotmob]:
    dataframe["date"] = pd.to_datetime(
        dataframe["date"],
        errors="coerce",
        utc=True
    ).dt.strftime("%Y-%m-%d")

    dataframe["opponent_key"] = dataframe["opponent"].map(
        normalise_team
    )


crosswalk = sofascore[
    [
        "event_id",
        "date",
        "round",
        "venue",
        "opponent",
        "opponent_key",
        "home_team",
        "away_team"
    ]
].merge(
    fotmob[
        [
            "match_id",
            "date",
            "round",
            "venue",
            "opponent",
            "opponent_key",
            "home_team",
            "away_team"
        ]
    ],
    on=[
        "date",
        "venue",
        "opponent_key"
    ],
    how="outer",
    suffixes=("_sofascore", "_fotmob"),
    indicator=True
)


crosswalk = crosswalk.rename(
    columns={
        "event_id": "sofascore_event_id",
        "match_id": "fotmob_match_id"
    }
)

crosswalk["match_key"] = (
    crosswalk["date"].astype(str)
    + "__"
    + crosswalk["venue"].astype(str).str.lower()
    + "__"
    + crosswalk["opponent_key"]
)

crosswalk = crosswalk.sort_values(
    ["date", "match_key"]
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

crosswalk.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Linhas:", len(crosswalk))
print(
    "Correspondências completas:",
    (crosswalk["_merge"] == "both").sum()
)
print(
    "Apenas Sofascore:",
    (crosswalk["_merge"] == "left_only").sum()
)
print(
    "Apenas FotMob:",
    (crosswalk["_merge"] == "right_only").sum()
)
print("Chaves únicas:", crosswalk["match_key"].nunique())
print("Ficheiro:", OUTPUT_FILE)
