# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

"""Download the official Hong Kong Observatory rainfall CSV once."""

from pathlib import Path

import requests

URL = "https://data.weather.gov.hk/weatherAPI/cis/csvfile/HKO/ALL/daily_HKO_RF_ALL.csv"
FILE = "daily_HKO_RF_ALL.csv"
HERE = Path(__file__).parent
DATA = HERE / "data"


def fetch(url: str, path: Path) -> Path:
    """Save the server's original response, unless it is already saved."""
    if path.exists():
        print(f"data/{path.name} is already here; no download needed.")
        return path

    DATA.mkdir(exist_ok=True)
    print(f"Downloading {url}")
    response = requests.get(
        url, timeout=60, headers={"User-Agent": "SD5913 PolyU student"}
    )
    response.raise_for_status()
    path.write_bytes(response.content)
    print(f"Saved data/{path.name}")
    return path


if __name__ == "__main__":
    fetch(URL, DATA / FILE)
