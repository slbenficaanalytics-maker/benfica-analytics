"""
Descarrega os dados detalhados do Sofascore para todos os jogos
listados em data/raw/sofascore_benfica_2025_26_events.csv.

Guarda os JSON originais em:
data/sofascore/raw/2025_26/<event_id>/
"""

python - <<'PY'
import json
import time
from pathlib import Path

import pandas as pd
import requests

events = pd.read_csv(
    "data/raw/sofascore_benfica_2025_26_events.csv"
)

base_dir = Path("data/sofascore/raw/2025_26")
base_dir.mkdir(parents=True, exist_ok=True)

endpoints = {
    "statistics": "statistics",
    "incidents": "incidents",
    "lineups": "lineups",
    "shotmap": "shotmap"
}

summary = []

for index, row in events.iterrows():
    event_id = int(row["event_id"])
    event_dir = base_dir / str(event_id)
    event_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "event_id": event_id,
        "date": row.get("date"),
        "competition": row.get("competition")
    }

    print(
        f"[{index + 1}/{len(events)}] "
        f"{event_id} — {row.get('home_team')} vs {row.get('away_team')}"
    )

    for name, endpoint in endpoints.items():
        url = f"https://www.sofascore.com/api/v1/event/{event_id}/{endpoint}"

        try:
            response = requests.get(url, timeout=30)

            result[f"{name}_http"] = response.status_code

            if response.status_code == 200:
                data = response.json()

                with open(
                    event_dir / f"{name}.json",
                    "w",
                    encoding="utf-8"
                ) as file:
                    json.dump(
                        data,
                        file,
                        ensure_ascii=False,
                        indent=2
                    )

                if name == "statistics":
                    result["statistics_available"] = bool(
                        data.get("statistics")
                    )
                elif name == "incidents":
                    result["incidents_count"] = len(
                        data.get("incidents", [])
                    )
                elif name == "lineups":
                    result["home_players"] = len(
                        data.get("home", {}).get("players", [])
                    )
                    result["away_players"] = len(
                        data.get("away", {}).get("players", [])
                    )
                elif name == "shotmap":
                    result["shots_count"] = len(
                        data.get("shotmap", [])
                    )
            else:
                result[f"{name}_error"] = response.text[:200]

        except Exception as error:
            result[f"{name}_http"] = None
            result[f"{name}_error"] = str(error)

        time.sleep(0.8)

    summary.append(result)

summary_df = pd.DataFrame(summary)

summary_df.to_csv(
    "data/sofascore/raw/2025_26/download_audit.csv",
    index=False
)

print("\nResumo:")
print("Jogos processados:", len(summary_df))
print(
    "Com estatísticas:",
    summary_df.get(
        "statistics_available",
        pd.Series(dtype=bool)
    ).fillna(False).sum()
)
print(
    "Com alinhamentos:",
    (
        summary_df.get(
            "home_players",
            pd.Series(dtype=float)
        ).fillna(0) > 0
    ).sum()
)
print(
    "Com incidentes:",
    (
        summary_df.get(
            "incidents_count",
            pd.Series(dtype=float)
        ).fillna(0) > 0
    ).sum()
)
print(
    "Com mapa de remates:",
    (
        summary_df.get(
            "shots_count",
            pd.Series(dtype=float)
        ).fillna(0) > 0
    ).sum()
)
PY
