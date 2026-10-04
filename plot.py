# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""Read local rainfall data and create a daily bar chart."""

import csv
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt

FILE = "daily_HKO_RF_ALL.csv"
PICTURE = "rainfall.png"
PLOT_YEAR = 2025

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"


def rows(path: Path) -> list[list[str]]:
    """Return data rows from the raw CSV, skipping headings and notes."""
    kept = []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.reader(handle):
            if len(row) >= 5 and row[0].isdigit():
                kept.append(row[:5])
    return kept


def main() -> None:
    table = rows(DATA)
    dates: list[date] = []
    values: list[float] = []
    skipped_missing = 0
    skipped_trace = 0
    skipped_invalid = 0

    for year, month, day, value, completeness in table:
        if value == "***":
            skipped_missing += 1
            continue
        if value == "Trace":
            skipped_trace += 1
            continue
        try:
            observation_date = date(int(year), int(month), int(day))
            rainfall = float(value)
        except ValueError:
            skipped_invalid += 1
            continue
        if observation_date.year == PLOT_YEAR:
            dates.append(observation_date)
            values.append(rainfall)

    if not values:
        raise ValueError(f"No usable rainfall data found for {PLOT_YEAR}.")

    print(f"{DATA.name}: {len(table)} data rows")
    print(
        f"{len(values)} usable values plotted for {PLOT_YEAR}; "
        f"{skipped_missing} missing values, {skipped_trace} trace values, "
        f"and {skipped_invalid} invalid rows skipped"
    )

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(
        dates,
        values,
        width=1.0,
        color="#1976d2",
        edgecolor="#0d47a1",
        linewidth=0.2,
    )
    ax.set_xlabel("date")
    ax.set_ylabel("daily rainfall (mm)")
    ax.set_title(f"Daily rainfall at Hong Kong Observatory, {PLOT_YEAR}")
    fig.autofmt_xdate()
    fig.tight_layout()

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=150)
    print(f"Saved out/{PICTURE}")


if __name__ == "__main__":
    main()
