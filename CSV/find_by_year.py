import os
import csv
import datetime

os.chdir(os.path.dirname(os.path.realpath(__file__)))

def get_songs_by_year(year: int) -> list:
    """Return a list of songs from a given year."""
    songs = []
    with open('playlist.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            date = row[4]
            try:
                date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                if date.year == year:
                    songs.append(row)
            except ValueError:
                pass
    return songs

# print(get_songs_by_year(2009))

# for i in range(2004, 2011, 1):
#     with open(f'{i}.csv', 'w', encoding='utf-8', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerows(get_songs_by_year(i))

def find_songs_where_upload_date_is_the_same_as_date_when_it_was_added_to_the_playlist():
    # date has to be the same but not the time on that date
    songs = []
    with open('playlist.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            date_added_to_playlist = row[3]
            date_added_to_youtube = row[4]
            try:
                date_added_to_playlist = datetime.datetime.strptime(date_added_to_playlist, "%Y-%m-%d %H:%M:%S")
                date_added_to_youtube = datetime.datetime.strptime(date_added_to_youtube, "%Y-%m-%d %H:%M:%S")
                # print(date_added_to_playlist, date_added_to_youtube)
                if date_added_to_playlist.date() == date_added_to_youtube.date():
                    songs.append(row)
            except ValueError:
                pass
    # sort songs based on date added to youtube
    songs.sort(key=lambda x: datetime.datetime.strptime(x[4], "%Y-%m-%d %H:%M:%S"))
    return songs

# print(find_songs_where_upload_date_is_the_same_as_date_when_it_was_added_to_the_playlist())

# with open('songs_where_upload_date_is_the_same_as_date_when_it_was_added_to_the_playlist.csv', 'w', encoding='utf-8', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerows(find_songs_where_upload_date_is_the_same_as_date_when_it_was_added_to_the_playlist())