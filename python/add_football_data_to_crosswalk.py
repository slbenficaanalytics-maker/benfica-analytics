"""
Acrescenta ao cruzamento Sofascore/FotMob os jogos
do Football-Data.co.uk da Liga Portugal 2025/26.

Entrada:
data/processed/benfica_2025_26_match_id_crosswalk.csv
data/football_data_co_uk/raw/portugal_2025_26.csv

Saída:
data/processed/benfica_2025_26_match_id_crosswalk_extended.csv
"""

import re
import unicodedata
from pathlib import Path

import pandas as pd


CROSSWALK_FILE = Path(
    "data/processed/benfica_2025_26_match_id_crosswalk.csv"
)

FOOTBALL_DATA_FILE = Path(
    "data/football_data_co_uk/raw/portugal_2025_26.csv"
)

OUTPUT_FILE = Path(
    "data/processed/"
    "benfica_2025_26_match_id_crosswalk_extended.csv"
)


def normalise_team(value):
    value = str(value).lower().strip()

    replacements = {
        "est amadora": "estrela amadora",
        "estrela amadora": "estrela amadora",
        "estrela": "estrela amadora",
        "avs": "avs futebol sad",
        "avs futebol sad": "avs futebol sad",
        "avs - futebol sad": "avs futebol sad",
        "porto": "fc porto",
        "fc porto": "fc porto",
        "sp lisbon": "sporting cp",
        "sporting": "sporting cp",
        "sporting cp": "sporting cp",
        "sporting clube de portugal": "sporting cp",
        "sp lisbon": "sporting cp",
        "sporting clube de portugal": "sporting cp",
        "sp braga": "braga",
        "sporting clube de braga": "braga",
        "est amadora": "estrela amadora",
        "cf estrela da amadora": "estrela amadora",
        "guimaraes": "vitoria guimaraes",
        "vitoria guimaraes": "vitoria guimaraes",
        "famalicao": "famalicao",
        "fc famalicao": "famalicao",
        "nacional": "nacional",
        "cd nacional": "nacional",
        "estoril": "estoril",
        "gd estoril praia": "estoril",
        "casa pia": "casa pia",
        "casa pia ac": "casa pia",
        "alverca": "alverca",
        "fc alverca": "alverca",
        "arouca": "arouca",
        "fc arouca": "arouca",
        "benfica": "benfica",
        "sport lisboa e benfica": "benfica",
    }

    value = replacements.get(value, value)

    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", "", value)

    return value


crosswalk = pd.read_csv(CROSSWALK_FILE)
football_data = pd.read_csv(FOOTBALL_DATA_FILE)

football_data["date"] = pd.to_datetime(
    football_data["Date"],
    dayfirst=True,
    errors="coerce"
).dt.strftime("%Y-%m-%d")

football_data["home_key"] = football_data["HomeTeam"].map(
    normalise_team
)

football_data["away_key"] = football_data["AwayTeam"].map(
    normalise_team
)

benfica_key = normalise_team("Benfica")

benfica = football_data[
    (football_data["home_key"] == benfica_key)
    | (football_data["away_key"] == benfica_key)
].copy()

benfica["venue"] = benfica["home_key"].map(
    lambda value: "Home" if value == benfica_key else "Away"
)

benfica["opponent_key"] = benfica.apply(
    lambda row: (
        row["away_key"]
        if row["venue"] == "Home"
        else row["home_key"]
    ),
    axis=1
)

benfica["football_data_row_id"] = benfica.index

keep_columns = [
    "football_data_row_id",
    "date",
    "venue",
    "opponent_key",
    "HomeTeam",
    "AwayTeam",
    "FTHG",
    "FTAG",
    "FTR",
    "HTHG",
    "HTAG",
    "HTR",
]

for column in [
    "AvgH",
    "AvgD",
    "AvgA",
    "MaxH",
    "MaxD",
    "MaxA",
]:
    if column in benfica.columns:
        keep_columns.append(column)

extended = crosswalk.merge(
    benfica[keep_columns],
    on=[
        "date",
        "venue",
        "opponent_key",
    ],
    how="left",
    validate="one_to_one"
)

extended["benfica_match_id"] = (
    "SLB_"
    + extended["date"].astype(str).str.replace("-", "", regex=False)
    + "_"
    + extended["venue"].astype(str).str.upper().str[0]
    + "_"
    + extended["opponent_key"].astype(str).str.upper()
)

if not extended["benfica_match_id"].is_unique:
    duplicates = extended[
        extended["benfica_match_id"].duplicated(
            keep=False
        )
    ]

    raise RuntimeError(
        "Existem chaves internas duplicadas:\n"
        + duplicates[
            [
                "date",
                "venue",
                "opponent_key",
                "benfica_match_id"
            ]
        ].to_string(index=False)
    )

extended.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Jogos no cruzamento:", len(extended))
print(
    "Com Football-Data:",
    extended["football_data_row_id"].notna().sum()
)
print(
    "Sem Football-Data:",
    extended["football_data_row_id"].isna().sum()
)
print(
    "IDs Football-Data únicos:",
    extended["football_data_row_id"].nunique()
)

print(
    "IDs internos únicos:",
    extended["benfica_match_id"].nunique()
)

print("Ficheiro:", OUTPUT_FILE)
