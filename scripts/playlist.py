"""Shared helpers for reading and writing the playlist CSVs in data/."""
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

PLAYLISTS = {
    # part name: (YouTube playlist id, CSV file)
    "part1": ("PLblHf1C6WdiFNFFrPb3UrHuyqMzdkNw0n", DATA / "playlist-part1.csv"),
    "part2": ("PLblHf1C6WdiEqI0RcPhlOZ2WscZEHzUah", DATA / "playlist-part2.csv"),
}

COLUMNS = ["title", "link", "channel", "added_to_playlist", "uploaded", "downloaded"]

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def read_rows(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, rows: list[dict], columns: list[str] = COLUMNS) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_all_songs() -> list[dict]:
    """All songs from every playlist part, in order."""
    return [row for _, path in PLAYLISTS.values() for row in read_rows(path)]
