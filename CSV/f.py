import csv
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("playlist.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    playlist = list(reader)

playlist = [line + [False] for line in playlist]

print(playlist[0])

with open("playlist2.csv", "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for line in playlist:
        writer.writerow(line)