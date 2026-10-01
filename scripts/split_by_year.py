"""Regenerate data/by-year/<year>.csv, grouping songs by YouTube upload year.

Usage:
    python scripts/split_by_year.py
"""
from collections import defaultdict

from playlist import DATA, read_all_songs, write_rows

OUT = DATA / "by-year"


def main() -> None:
    by_year = defaultdict(list)
    for song in read_all_songs():
        year = song["uploaded"][:4]
        if year.isdigit():
            by_year[year].append(song)

    for old in OUT.glob("*.csv"):
        old.unlink()
    for year, songs in sorted(by_year.items()):
        write_rows(OUT / f"{year}.csv", songs)
        print(f"{year}: {len(songs)} songs")


if __name__ == "__main__":
    main()
