# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""Read local rainfall data and create two rainfall visualisations."""

import calendar
import csv
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

FILE = "daily_HKO_RF_ALL.csv"
BAR_PICTURE = "plot.png"
CALENDAR_PICTURE = "rainfall-calendar.png"
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


def read_year(path: Path, year_to_plot: int) -> tuple[list[date], list[float]]:
    """Read numeric daily rainfall values for one year from the local CSV."""
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
        if observation_date.year == year_to_plot:
            dates.append(observation_date)
            values.append(rainfall)

    if not values:
        raise ValueError(f"No usable rainfall data found for {year_to_plot}.")

    print(f"{DATA.name}: {len(table)} data rows")
    print(
        f"{len(values)} usable values plotted for {year_to_plot}; "
        f"{skipped_missing} missing values, {skipped_trace} trace values, "
        f"and {skipped_invalid} invalid rows skipped"
    )
    return dates, values


def save_bar_chart(dates: list[date], values: list[float]) -> None:
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
    fig.savefig(OUT / BAR_PICTURE, dpi=150)
    plt.close(fig)
    print(f"Saved out/{BAR_PICTURE}")


def save_calendar(dates: list[date], values: list[float]) -> None:
    """Save a calendar where darker blue means more rainfall."""
    rainfall_by_date = dict(zip(dates, values))
    top_three = set(sorted(rainfall_by_date, key=rainfall_by_date.get, reverse=True)[:3])
    maximum = max(values)
    norm = Normalize(vmin=0, vmax=maximum or 1)
    cmap = plt.get_cmap("Blues")

    fig, axes = plt.subplots(3, 4, figsize=(16, 11), constrained_layout=True)
    fig.suptitle(
        f"Hong Kong Observatory daily rainfall calendar, {PLOT_YEAR}\n"
        "Darker blue means more rainfall (millimetres, mm)",
        fontsize=18,
    )

    for month, ax in enumerate(axes.flat, start=1):
        ax.set_title(calendar.month_name[month], fontsize=13, pad=12)
        ax.set_xlim(0, 7)
        ax.set_ylim(6, 0)
        ax.set_xticks(range(7), ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        ax.set_yticks([])
        ax.tick_params(axis="x", labelsize=8, length=0)
        ax.set_aspect("equal")
        first_weekday, days_in_month = calendar.monthrange(PLOT_YEAR, month)

        for day in range(1, days_in_month + 1):
            column = (first_weekday + day - 1) % 7
            row = (first_weekday + day - 1) // 7
            current_date = date(PLOT_YEAR, month, day)
            rainfall = rainfall_by_date.get(current_date)
            face_color = "#f4f4f4" if rainfall is None else cmap(norm(rainfall))
            rectangle = plt.Rectangle(
                (column + 0.04, row + 0.04),
                0.92,
                0.92,
                facecolor=face_color,
                edgecolor="white",
                linewidth=1,
            )
            ax.add_patch(rectangle)
            label_color = "white" if rainfall is not None and rainfall > maximum * 0.35 else "#17324d"
            ax.text(
                column + 0.12,
                row + 0.25,
                str(day),
                ha="left",
                va="center",
                fontsize=8,
                color=label_color,
            )
            if current_date in top_three:
                ax.text(
                    column + 0.78,
                    row + 0.24,
                    "★",
                    ha="center",
                    va="center",
                    fontsize=11,
                    color="#d32f2f",
                )

        ax.spines[:].set_visible(False)

    colorbar = fig.colorbar(
        ScalarMappable(norm=norm, cmap=cmap),
        ax=axes,
        fraction=0.025,
        pad=0.02,
    )
    colorbar.set_label("Daily rainfall (mm)")
    fig.text(
        0.5,
        0.02,
        "★ Top three rainfall days",
        ha="center",
        color="#d32f2f",
        fontsize=11,
    )
    fig.savefig(OUT / CALENDAR_PICTURE, dpi=150)
    plt.close(fig)
    print(f"Saved out/{CALENDAR_PICTURE}")


def main() -> None:
    dates, values = read_year(DATA, PLOT_YEAR)
    OUT.mkdir(exist_ok=True)
    save_bar_chart(dates, values)
    save_calendar(dates, values)


if __name__ == "__main__":
    main()
