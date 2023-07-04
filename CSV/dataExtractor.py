"""Google API."""
# https://developers.google.com/youtube/v3/quickstart/python
from googleapiclient.discovery import build
import csv
import os
import datetime
from types import SimpleNamespace
import concurrent.futures

os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("key.txt", "r") as key:
    KEY = key.read()
    key.close()

def get_data_about_a_specific_page(link: str, developer_key: str = KEY, pageToken = None):
    data = []
    youtube = build('youtube', 'v3', developerKey=developer_key)
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=link.split('=')[-1],
        maxResults=50,
        pageToken=pageToken,
    )
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
        data.append(outputItem)
    return data

def run_get_data_about_a_specific_page_in_parallel(link:str, page_tokens:dict, developer_key: str = KEY):

    # must keep track of the index of the page token to make sure the output of
    # this function is in the correct order
    output = {}
    def get_data(link, pageToken):
        return get_data_about_a_specific_page(link, developer_key, pageToken)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_pageToken = {executor.submit(get_data, link, pageToken): pageToken for pageToken in page_tokens}
        for future in concurrent.futures.as_completed(future_to_pageToken):
            pageToken = future_to_pageToken[future]
            try:
                result = future.result()
            except Exception as e:
                print(f"An error occurred while getting data about a specific page: {e}")
            else:
                # page_tokens[page_tokens.index(pageToken)] = result
                output[page_tokens[pageToken]] = result
    return output




def get_playlist_data(link: str, developer_key: str = KEY, pageToken = None) -> list:
    lst = []
    # pagetokens = []
    youtube = build('youtube', 'v3', developerKey=developer_key)
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=link.split('=')[-1],
        maxResults=50,
        pageToken=pageToken,
        # pageToken="EAAaB1BUOkNMQWk",
    )
    response = request.execute()
    # print nextpageToken
    # nextpageToken = response['nextPageToken']
    # pagetokens.append(nextpageToken)
    # print(nextpageToken)
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
                # try:
                #     nextpageToken = response['nextPageToken']
                #     pagetokens.append(nextpageToken)
                #     print(nextpageToken)
                # except KeyError:
                #     pass
        except AttributeError:
            return lst[::-1]

def get_date_added_to_youtube(outputItem: SimpleNamespace, developer_key: str = KEY):
    if outputItem.channel_name != 'removed?':
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

def get_page_tokens(link: str, developer_key: str = KEY, pageToken = None):
    pagetokens = []
    youtube = build('youtube', 'v3', developerKey=developer_key)
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=link.split('=')[-1],
        maxResults=50,
        pageToken=pageToken,
    )
    response = request.execute()
    nextpageToken = response['nextPageToken']
    # pagetokens.append(nextpageToken)
    print(nextpageToken)
    if not response:
        pass
    else:
        try:
            while response:
                response = request.execute()
                request = youtube.playlistItems().list_next(request, response)
                try:
                    nextpageToken = response['nextPageToken']
                    pagetokens.append(nextpageToken)
                    print(nextpageToken)
                except KeyError:
                    pass
        except AttributeError:
            return pagetokens

def run_date_added_to_youtube_in_parallel(playlist: list):
    def process_item(item):
        if not item.date_added_to_youtube:
            return get_date_added_to_youtube(item)
        return item

    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
        future_to_item = {executor.submit(process_item, item): item for item in playlist}

        for future in concurrent.futures.as_completed(future_to_item):
            item = future_to_item[future]
            try:
                result = future.result()
            except Exception as e:
                print(f"An error occurred while processing {item}: {e}")
            else:
                if result is not None:
                    index = playlist.index(item)
                    print(index, result)
                    playlist[index] = result
    return playlist


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

    try:
        with open("pagetokens.txt", "r") as tokens:
            pagetokens = tokens.read().split("\n")
            pagetokens = [None] + pagetokens
            tokens.close()
    except FileNotFoundError:
        # pagetokens = [None]
        pagetokens = get_page_tokens(URL, developer_key=KEY)
        with open("pagetokens.txt", "w", encoding="utf-8") as tokens:
            for token in get_page_tokens(URL, pageToken=None):
                tokens.write(token + "\n")

    print(pagetokens)
    # exit()

    pagetokens = {token: index for index, token in enumerate(pagetokens)}
    print(pagetokens)
    removed_songs = [item for item in pl_csv if item.channel_name == 'removed?']

    print(get_data_about_a_specific_page(URL, pageToken=None))
    # exit()

    # master_playlist = get_playlist_data(URL)
    master_playlist = run_get_data_about_a_specific_page_in_parallel(URL, pagetokens)

    # print(master_playlist.keys())
    pl = []
    print(sorted(master_playlist.keys()))
    # for key in sorted(master_playlist.keys()):
    #     pl.extend(master_playlist[key])
    master_playlist = [master_playlist[key] for key in sorted(master_playlist.keys())]
    # take master playlist and turn it into a list. use the indecies from the pagetokens to get the correct order of the playlist
    temp = []
    for lst in master_playlist:
        temp.extend(lst)
    master_playlist = temp[::-1]

    print(master_playlist, len(master_playlist))
    # print(len(master_playlist))
    # exit()
    playlist = [item for item in master_playlist if item.link not in [itm.link.split("=")[-1] for itm in pl_csv]]

    playlist = run_date_added_to_youtube_in_parallel(playlist)


    # print(playlist, len(playlist))

    with open("playlist.csv", "a", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for item in playlist:
            if item.channel_name != 'removed?':
                writer.writerow([item.title, f"https://www.youtube.com/watch?v={item.link}", item.channel_name, item.date_added_to_playlist, item.date_added_to_youtube])
            else:
                removed_songs.append(item)
        csvfile.close()
    # print(removed_songs)

    # print(get_page_tokens(URL))


    pass