import csv
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# open playlist.csv
# reverse the playlist.csv file itself
# save the reversed playlist.csv file

with open("playlist.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    playlist = list(reader)
    playlist.reverse()
    # save the reversed playlist.csv file
with open("playlist.csv", "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for title, link in playlist:
        writer.writerow([title, link])