"""
Extrai entradas e saídas do Benfica no Transfermarkt para 2025/26.

Saídas:
data/transfermarkt/processed/
- benfica_2025_26_arrivals.csv
- benfica_2025_26_departures.csv
"""

import re
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup


URL = (
    "https://www.transfermarkt.com/"
    "sl-benfica/transfers/verein/294/saison_id/2025"
)

BASE_URL = "https://www.transfermarkt.com"

OUTPUT_DIR = Path("data/transfermarkt/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_id(href, pattern):
    if not href:
        return None

    match = re.search(pattern, href)

    if match:
        return match.group(1)

    return None


def parse_player_cell(cell):
    link = cell.select_one(
        'a[href*="/profil/spieler/"]'
    )

    if link is None:
        return {
            "player": None,
            "player_id": None,
            "player_url": None,
            "position": None
        }

    player = link.get_text(" ", strip=True)
    href = link.get("href")

    full_text = " ".join(cell.stripped_strings)

    position = full_text.replace(player, "", 1).strip()

    return {
        "player": player,
        "player_id": extract_id(
            href,
            r"/spieler/(\d+)"
        ),
        "player_url": urljoin(BASE_URL, href),
        "position": position or None
    }


def parse_club_cell(cell):
    links = cell.select("a")

    club_link = None
    competition_link = None

    for link in links:
        href = link.get("href", "")
        text = link.get_text(" ", strip=True)

        if "/verein/" in href and text:
            club_link = link

        if (
            "/wettbewerb/" in href
            or "/transfers/wettbewerb/" in href
        ) and text:
            competition_link = link

    club = (
        club_link.get_text(" ", strip=True)
        if club_link
        else None
    )

    competition = (
        competition_link.get_text(" ", strip=True)
        if competition_link
        else None
    )

    club_href = (
        club_link.get("href")
        if club_link
        else None
    )

    competition_href = (
        competition_link.get("href")
        if competition_link
        else None
    )

    return {
        "club": club,
        "club_id": extract_id(
            club_href,
            r"/verein/(\d+)"
        ),
        "club_url": (
            urljoin(BASE_URL, club_href)
            if club_href
            else None
        ),
        "competition": competition,
        "competition_id": extract_id(
            competition_href,
            r"/wettbewerb/([^/?]+)"
        )
    }


def parse_table(table, movement):
    rows = []

    for row in table.select("tbody > tr"):
        cells = row.select(":scope > td")

        if len(cells) < 6:
            continue

        player_data = parse_player_cell(cells[1])

        if not player_data["player"]:
            continue

        club_data = parse_club_cell(cells[4])

        fee_link = cells[5].select_one("a")
        fee_href = (
            fee_link.get("href")
            if fee_link
            else None
        )

        nationality_image = cells[3].select_one("img")

        nationality = None

        if nationality_image:
            nationality = (
                nationality_image.get("title")
                or nationality_image.get("alt")
            )

        row_data = {
            "movement": movement,
            **player_data,
            "age": cells[2].get_text(
                " ",
                strip=True
            ) or None,
            "nationality": nationality,
            **club_data,
            "fee": cells[5].get_text(
                " ",
                strip=True
            ) or None,
            "transfer_id": extract_id(
                fee_href,
                r"/transfer_id/(\d+)"
            )
        }

        rows.append(row_data)

    return pd.DataFrame(rows)


response = requests.get(
    URL,
    headers={
        "User-Agent": (
            "Mozilla/5.0 "
            "(Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36"
        )
    },
    timeout=30
)

response.raise_for_status()

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

tables = soup.select("table.items")

if len(tables) < 2:
    raise RuntimeError(
        "Não foram encontradas as duas tabelas principais."
    )

arrivals = parse_table(
    tables[0],
    "Arrival"
)

departures = parse_table(
    tables[1],
    "Departure"
)

arrivals.to_csv(
    OUTPUT_DIR /
    "benfica_2025_26_arrivals.csv",
    index=False
)

departures.to_csv(
    OUTPUT_DIR /
    "benfica_2025_26_departures.csv",
    index=False
)

print("Entradas:", len(arrivals))
print("Saídas:", len(departures))

print("\nPrimeiras entradas:")
print(
    arrivals[
        [
            "player",
            "position",
            "age",
            "nationality",
            "club",
            "competition",
            "fee"
        ]
    ].head().to_string(index=False)
)

print("\nPrimeiras saídas:")
print(
    departures[
        [
            "player",
            "position",
            "age",
            "nationality",
            "club",
            "competition",
            "fee"
        ]
    ].head().to_string(index=False)
)
