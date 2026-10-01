"""Renumber library files down by one after a song is removed from the playlist.

Every `<number>.<title>.<ext>` file with number >= FROM becomes `<number-1>.<title>.<ext>`.

Usage:
    python scripts/library/shift_numbers.py FROM DIR [DIR ...]
"""
import os
import sys


def shift_back(folder: str, start: int) -> None:
    # Ascending order so each target name has already been freed up.
    files = sorted(
        (int(name.split(".", 1)[0]), name.split(".", 1)[1])
        for name in os.listdir(folder)
        if name.split(".", 1)[0].isdigit()
    )
    for number, rest in files:
        if number >= start:
            os.rename(os.path.join(folder, f"{number}.{rest}"), os.path.join(folder, f"{number - 1}.{rest}"))
            print(f"{number} -> {number - 1}: {rest}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    for folder in sys.argv[2:]:
        shift_back(folder, int(sys.argv[1]))
