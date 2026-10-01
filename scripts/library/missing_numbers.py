"""Print a grid of playlist numbers that have no downloaded file yet.

Files in the library folders are named `<number>.<title>.<ext>`, where the
number is the song's position in the playlist.

Usage:
    python scripts/library/missing_numbers.py LOSSLESS_DIR LOSSY_DIR
"""
import os
import sys

# Numbers that are known to be missing on purpose.
IGNORED_RANGES = [range(0, 549), range(3700, 5000)]
IGNORED_NUMBERS = {806}


def numbers_in(folder: str) -> set[int]:
    return {int(name.split(".")[0]) for name in os.listdir(folder) if name.split(".")[0].isdigit()}


def is_ignored(number: int) -> bool:
    return number in IGNORED_NUMBERS or any(number in r for r in IGNORED_RANGES)


def print_grid(numbers: set[int], width: int = 10) -> None:
    for start in range(0, max(numbers, default=0) + 1, width):
        row = [str(i).rjust(4) if i in numbers else "----" for i in range(start, start + width)]
        if any(cell != "----" for cell in row):
            print("  ".join(row))


def main(folders: list[str]) -> None:
    have = set().union(*(numbers_in(folder) for folder in folders))
    missing = {i for i in range(1, max(have)) if i not in have and not is_ignored(i)}
    print_grid(missing)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
