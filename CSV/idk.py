"""Google API."""
# https://developers.google.com/youtube/v3/quickstart/python
from googleapiclient.discovery import build
import csv
import delimiter_fix
import os
import datetime
os.chdir(os.path.dirname(os.path.realpath(__file__)))
# TODO: make it so that the amount of requests is reduced. stuff in the csv file should not be requested again

def get_playlist_data(link: str, developer_key: str) -> list:
    """Get data about a youtube playlist using the Google API."""
    links = []
    titles = []
    channel_names = []
    date_added_to_playlist = []
    date_added_to_youtube = []
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
                    date_added_to_playlist.append(str(datetime.datetime.strptime(item['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")))
                    # print(f"date added to playlist: {datetime.datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')}")
                    # get the video id and use it to get the date the video was uploaded to youtube
                    # https://stackoverflow.com/questions/28218698/how-to-get-the-date-a-youtube-video-was-uploaded
                    try:
                        id = item['snippet']['resourceId']['videoId']
                        request2 = youtube.videos().list(
                            part='snippet',
                            id=id
                        )
                        response2 = request2.execute()
                        # print(f"date uploaded to youtube: {datetime.datetime.strptime(response2['items'][0]['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')}")
                        date_added_to_youtube.append(str(datetime.datetime.strptime(response2['items'][0]['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")))
                    except:
                        date_added_to_youtube.append('no clue')

                    try:
                        channel_names.append(item['snippet']['videoOwnerChannelTitle'])
                    except KeyError:
                        channel_names.append('removed?')
                    print(len(links))
                request = youtube.playlistItems().list_next(request, response)
        except AttributeError:
            links = [f"https://www.youtube.com/watch?v={link}" for link in links]
            links.reverse()
            titles.reverse()
            date_added_to_playlist.reverse()
            date_added_to_youtube.reverse()
            channel_names.reverse()
            return [titles, links, channel_names, date_added_to_playlist, date_added_to_youtube]


if __name__ == '__main__':
    URL = "https://www.youtube.com/playlist?list=PLblHf1C6WdiFNFFrPb3UrHuyqMzdkNw0n"
    with open("key.txt", "r") as key:
        KEY = key.read()
        key.close()
    playlist = get_playlist_data(URL, KEY)

    # print(*playlist, sep='\n')
    links_in_csv = []
    links_in_removed_songs = []
    channel_names_in_csv = []
    titles, links, channel_names, dates_added_to_playlist, dates_added_to_youtube = playlist
    # print(dates_added_to_playlist)
    with open("playlist.csv", "r", encoding="utf-8", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for title, link, channel_name, date_added_to_playlist, date_added_to_youtube in reader:
            links_in_csv.append(link)
        csvfile.close()

    with open("removedSongs.csv", "r", encoding="utf-8", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for title, link, channel_name, date_added_to_playlist in reader:
            links_in_removed_songs.append(link)
        csvfile.close()

    with open("playlist.csv", "a", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in range(len(links)):
            if links[i] not in links_in_csv:
                if channel_names[i] != 'removed?':
                    writer.writerow([titles[i], links[i], channel_names[i], "no clue", "no clue"])
                else:
                    with open("removedSongs.csv", "a", encoding="utf-8", newline="") as csvfile2:
                        writer2 = csv.writer(csvfile2, delimiter=',')
                        if links[i] not in links_in_removed_songs:
                            try:
                                writer2.writerow([titles[i], links[i], channel_names[i], dates_added_to_playlist[i]])
                            except:
                                # print(titles[i], links[i], channel_names[i], i)
                                pass
            elif links[i] in links_in_csv:
                try:
                    writer.writerow([titles[i], links[i], channel_names[i], dates_added_to_playlist[i], dates_added_to_youtube[i]])
                except:
                    # print(titles[i], links[i], channel_names[i], i)
                    pass

    # delimiter_fix.get_delimiter(); delimiter_fix.fix(delimiter_fix.get_playlist())
    pass