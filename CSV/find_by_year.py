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

print(get_songs_by_year(2009))

# save output of get_songs_by_year() to a csv file based on the year, e.g. 2009.csv

for i in range(2004, 2011, 1):
    with open(f'{i}.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(get_songs_by_year(i))