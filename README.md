# Best Songs Of All Time

My YouTube "best songs of all time" playlists, tracked as CSV.

## Layout

```
data/
  playlist-part1.csv    songs in playlist part 1
  playlist-part2.csv    songs in playlist part 2 (the one still growing)
  by-year/<year>.csv    every song grouped by YouTube upload year (generated)
  removed-songs.csv     songs that got deleted or made private on YouTube
  outside-sources.csv   songs from outside YouTube (SoundCloud etc.)
scripts/
  fetch_playlist.py     append newly added songs from YouTube to a playlist CSV
  split_by_year.py      regenerate data/by-year/
  library/              helpers for the local music folder
```

Playlist CSV columns: `title, link, channel, added_to_playlist, uploaded, downloaded`.
`downloaded` is `True`, `False` or `Lossy`.

## Updating

```sh
pip install -r requirements.txt
export YOUTUBE_API_KEY=...          # or put the key in key.txt (git-ignored)
python scripts/fetch_playlist.py    # defaults to part2
python scripts/split_by_year.py
```

## Local music library

The downloaded songs live in two folders (`Lossless` and `Lossy`), with files
named `<playlist number>.<title>.<ext>`.

```sh
# which playlist numbers don't have a file yet
python scripts/library/missing_numbers.py "K:\MEGAsync\Music\LosslessBest\Lossless" "K:\MEGAsync\Music\LosslessBest\Lossy"

# a song was removed from the playlist at position 515: shift everything after it down by one
python scripts/library/shift_numbers.py 516 "K:\MEGAsync\Music\LosslessBest\Lossless" "K:\MEGAsync\Music\LosslessBest\Lossy"
```
