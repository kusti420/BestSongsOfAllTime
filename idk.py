"""Google API."""
from googleapiclient.discovery import build
import csv


def get_links_from_playlist(link: str, developer_key: str) -> list:
    links = []
    titles = []
    channel_names = [] # name of the channel who uploaded that video
    youtube = build('youtube', 'v3', developerKey=developer_key)
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=link.split('=')[-1],
        maxResults=50
    )
    response = request.execute()
    if not response:
        pass
    else:
        try:
            while response:
                response = request.execute()
                for item in response['items']:
                    links.append(item['snippet']['resourceId']['videoId'])
                    titles.append(item['snippet']['title'])
                    try:
                        channel_names.append(item['snippet']['videoOwnerChannelTitle'])
                    except KeyError:
                        channel_names.append('removed?')
                    print(len(links))
                request = youtube.playlistItems().list_next(request, response)
        except AttributeError:
            links = [f"https://www.youtube.com/watch?v={link}" for link in links]
            links = reversed(links)
            titles = reversed(titles)
            channel_names = reversed(channel_names)
            return zip(titles, links, channel_names)


if __name__ == '__main__':
    URL = "https://www.youtube.com/playlist?list=PLblHf1C6WdiFNFFrPb3UrHuyqMzdkNw0n"
    with open("key.txt", "r") as key:
        KEY = key.read()
    playlist = get_links_from_playlist(URL, KEY)
    # print(*playlist, sep='\n')
    links_in_csv = []
    channel_names_in_csv = []
    with open("playlist.csv", "r", encoding="utf-8", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for title, link, channel_name in reader:
            links_in_csv.append(link)
        csvfile.close()
    with open("playlist.csv", "a", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for title, link, channel_name in playlist:
            if link not in links_in_csv:
                writer.writerow([title, link, channel_name])
    pass
