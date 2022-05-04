import csv
from collections import namedtuple

FILE = "playlist.csv"

def get_delimiter():
    global delimiter
    with open (FILE, "r") as f:
        delimiter = f.readline()
    if not delimiter:
        return
    for c in delimiter:
        if c.isalpha():
            delimiter = delimiter.replace(c, "")
    delimiter = list(set(delimiter))
    delimiter.remove("\n"); delimiter.remove(" ")
    delimiter = delimiter[0]
    return delimiter[0]

def get_playlist():
    playlist = namedtuple("playlist", ["titles", "links", "channel_names"])
    titles = []
    links = []
    channel_names = []
    reader = csv.reader(open(FILE, "r", encoding="utf-8", newline=""), delimiter=delimiter)
    for row in reader:
        titles.append(row[0])
        links.append(row[1])
        channel_names.append(row[2])
    return playlist(titles, links, channel_names)

def fix(playlist):
    for i in range(len(playlist.titles)):
        playlist.titles[i] = playlist.titles[i].replace(str(delimiter), "")
        playlist.titles[i] = playlist.titles[i].strip(); 
        playlist.titles[i] = playlist.titles[i].replace('"', "")
        playlist.titles[i] = playlist.titles[i].replace("'", "")
    
    writer = csv.writer(open(FILE, "w", encoding="utf-8", newline=""), delimiter=delimiter)
    for i in range(len(playlist.titles)):
        writer.writerow([playlist.titles[i], playlist.links[i], playlist.channel_names[i]])


if __name__ == "__main__":
    get_delimiter()
    # print(delimiter)
    fix(get_playlist())
    pass
