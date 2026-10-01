"""Append songs newly added to a YouTube playlist to its CSV in data/.

Usage:
    YOUTUBE_API_KEY=... python scripts/fetch_playlist.py [part2]

The API key can also be put in a git-ignored `key.txt` at the repo root.
Songs that are deleted or private on YouTube are skipped.
"""
import os
import sys
from datetime import datetime
from pathlib import Path

from googleapiclient.discovery import build

from playlist import DATE_FORMAT, PLAYLISTS, read_rows, write_rows

KEY_FILE = Path(__file__).resolve().parent.parent / "key.txt"


def api_key() -> str:
    if key := os.environ.get("YOUTUBE_API_KEY"):
        return key
    if KEY_FILE.exists():
        return KEY_FILE.read_text().strip()
    sys.exit("Set YOUTUBE_API_KEY or create key.txt in the repo root.")


def parse_date(value: str) -> str:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").strftime(DATE_FORMAT)


def fetch_playlist_items(youtube, playlist_id: str) -> list[dict]:
    items = []
    request = youtube.playlistItems().list(part="snippet", playlistId=playlist_id, maxResults=50)
    while request is not None:
        response = request.execute()
        items.extend(response["items"])
        request = youtube.playlistItems().list_next(request, response)
    return items


def fetch_upload_dates(youtube, video_ids: list[str]) -> dict[str, str]:
    dates = {}
    for i in range(0, len(video_ids), 50):
        response = youtube.videos().list(part="snippet", id=",".join(video_ids[i:i + 50])).execute()
        for video in response["items"]:
            dates[video["id"]] = parse_date(video["snippet"]["publishedAt"])
    return dates


def main(part: str) -> None:
    playlist_id, csv_path = PLAYLISTS[part]
    rows = read_rows(csv_path)
    known = {row["link"].split("=")[-1] for row in rows}

    youtube = build("youtube", "v3", developerKey=api_key())
    new, new_ids, unavailable = [], [], []
    for item in fetch_playlist_items(youtube, playlist_id):
        snippet = item["snippet"]
        video_id = snippet["resourceId"]["videoId"]
        if video_id in known:
            continue
        if "videoOwnerChannelTitle" not in snippet:  # deleted or private video
            unavailable.append(snippet["title"])
            continue
        new.append({
            "title": snippet["title"],
            "link": f"https://www.youtube.com/watch?v={video_id}",
            "channel": snippet["videoOwnerChannelTitle"],
            "added_to_playlist": parse_date(snippet["publishedAt"]),
            "uploaded": "unknown",
            "downloaded": "False",
        })
        new_ids.append(video_id)

    upload_dates = fetch_upload_dates(youtube, new_ids)
    for song, video_id in zip(new, new_ids):
        song["uploaded"] = upload_dates.get(video_id, "unknown")
    new.sort(key=lambda song: song["added_to_playlist"])

    write_rows(csv_path, rows + new)
    print(f"Added {len(new)} songs to {csv_path.name}.")
    if unavailable:
        print(f"Skipped {len(unavailable)} unavailable videos: {', '.join(unavailable)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "part2")
