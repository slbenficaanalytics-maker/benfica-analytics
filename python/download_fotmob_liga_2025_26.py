"""
Descarrega os detalhes completos dos 34 jogos do Benfica
na Liga Portugal 2025/26 através do FotMob.

Entrada:
data/raw/fotmob_benfica_2025_26_liga_matches.csv

Saída:
data/fotmob/raw/2025_26_liga/<match_id>.json
"""

import json
import time
from pathlib import Path

import pandas as pd
import requests


MATCHES_FILE = Path(
    "data/raw/fotmob_benfica_2025_26_liga_matches.csv"
)

OUTPUT_DIR = Path(
    "data/fotmob/raw/2025_26_liga"
)

AUDIT_FILE = OUTPUT_DIR / "download_audit.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

matches = pd.read_csv(MATCHES_FILE)

rows = []

for index, match in matches.iterrows():
    match_id = int(match["match_id"])

    url = (
        "https://www.fotmob.com/api/data/matchDetails"
        f"?matchId={match_id}&ccode3=PRT_MA"
    )

    print(
        f"[{index + 1}/{len(matches)}] "
        f"{match_id} — "
        f"{match['home_team']} vs {match['away_team']}"
    )

    result = {
        "match_id": match_id,
        "date": match.get("date"),
        "home_team": match.get("home_team"),
        "away_team": match.get("away_team")
    }

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            },
            timeout=30
        )

        result["http_status"] = response.status_code

        if response.status_code == 200:
            data = response.json()

            output_file = OUTPUT_DIR / f"{match_id}.json"

            with output_file.open(
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

            content = data.get("content", {})

            result["has_stats"] = bool(
                content.get("stats")
            )
            result["has_player_stats"] = bool(
                content.get("playerStats")
            )
            result["has_shotmap"] = bool(
                content.get("shotmap")
            )
            result["has_lineup"] = bool(
                content.get("lineup")
            )
            result["has_momentum"] = bool(
                content.get("momentum")
            )
            result["has_attacking_zones"] = bool(
                content.get("attackingZones")
            )
        else:
            result["error"] = response.text[:200]

    except Exception as error:
        result["http_status"] = None
        result["error"] = str(error)

    rows.append(result)

    time.sleep(0.8)

audit = pd.DataFrame(rows)

audit.to_csv(
    AUDIT_FILE,
    index=False
)

print("\nResumo:")
print("Jogos processados:", len(audit))
print(
    "Com estatísticas:",
    audit["has_stats"].fillna(False).sum()
)
print(
    "Com estatísticas de jogadores:",
    audit["has_player_stats"].fillna(False).sum()
)
print(
    "Com mapa de remates:",
    audit["has_shotmap"].fillna(False).sum()
)
print(
    "Com alinhamentos:",
    audit["has_lineup"].fillna(False).sum()
)
print(
    "Com momentum:",
    audit["has_momentum"].fillna(False).sum()
)
print(
    "Com zonas de ataque:",
    audit["has_attacking_zones"].fillna(False).sum()
)
