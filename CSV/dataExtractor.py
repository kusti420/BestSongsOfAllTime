"""Google API."""
# https://developers.google.com/youtube/v3/quickstart/python
from googleapiclient.discovery import build
import csv
import os
import datetime
from types import SimpleNamespace
os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("key.txt", "r") as key:
    KEY = key.read()
    key.close()

def get_playlist_data(link: str, developer_key: str = KEY) -> list:
    # must get links, titles, channel names, date added to playlist, date added to youtube
    lst = []
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
                    outputItem = SimpleNamespace()
                    outputItem.link = item['snippet']['resourceId']['videoId']
                    outputItem.title = item['snippet']['title']
                    outputItem.date_added_to_playlist = str(datetime.datetime.strptime(item['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"))
                    try:
                        outputItem.channel_name = item['snippet']['videoOwnerChannelTitle']
                    except KeyError:
                        outputItem.channel_name = 'removed?'
                    outputItem.date_added_to_youtube = None
                    lst.append(outputItem)
                    print(len(lst))
                request = youtube.playlistItems().list_next(request, response)
        except AttributeError:
            return lst[::-1]

def get_date_added_to_youtube(outputItem: SimpleNamespace, developer_key: str = KEY):
    try:
        youtube = build('youtube', 'v3', developerKey=developer_key)
        request = youtube.videos().list(
            part='snippet',
            id=outputItem.link
        )
        response = request.execute()
        outputItem.date_added_to_youtube = str(datetime.datetime.strptime(response['items'][0]['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"))
    except IndexError:
        outputItem.date_added_to_youtube = 'no clue'
    return outputItem

if __name__ == '__main__':
    URL = "https://www.youtube.com/playlist?list=PLblHf1C6WdiFNFFrPb3UrHuyqMzdkNw0n"
    with open("playlist.csv", "r", encoding="utf-8", newline="") as csvfile:
        pl_csv = []
        reader = csv.reader(csvfile, delimiter=',')
        try:
            while(line:=reader.__next__()):
                pl_csv.append(SimpleNamespace(title=line[0], link=line[1], channel_name=line[2], date_added_to_playlist=line[3], date_added_to_youtube=line[4]))
        except StopIteration:
            csvfile.close()

    print(pl_csv[7].title)

    removed_songs = [item for item in pl_csv if item.channel_name == 'removed?']

    master_playlist = get_playlist_data(URL)
    playlist = [item for item in master_playlist if item.link not in [itm.link.split("=")[-1] for itm in pl_csv]]

    # TODO: make this part run multithreaded with parallellism
    # for i, item in enumerate(playlist):
    #     # print(item.date_added_to_youtube)
    #     if not item.date_added_to_youtube:
    #         playlist[i] = get_date_added_to_youtube(item)
    #         print(i)

    import concurrent.futures

    def process_item(item):
        if not item.date_added_to_youtube:
            return get_date_added_to_youtube(item)
        return item

    # playlist = [...]  # Your playlist data

    # Create a thread pool executor with a maximum of 5 threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit each item from the playlist to the executor
        future_to_item = {executor.submit(process_item, item): item for item in playlist}

        # Process the results as they complete
        for future in concurrent.futures.as_completed(future_to_item):
            item = future_to_item[future]
            try:
                result = future.result()
            except Exception as e:
                print(f"An error occurred while processing {item}: {e}")
            else:
                if result is not None:
                    # Update the playlist with the processed item
                    index = playlist.index(item)
                    print(index)
                    playlist[index] = result

    print(playlist, len(playlist))

    with open("playlist.csv", "a", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for item in playlist:
            if item.channel_name != 'removed?':
                writer.writerow([item.title, f"https://www.youtube.com/watch?v={item.link}", item.channel_name, item.date_added_to_playlist, item.date_added_to_youtube])
            else:
                removed_songs.append(item)
        csvfile.close()
    print(removed_songs)