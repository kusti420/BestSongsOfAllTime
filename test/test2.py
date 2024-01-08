import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.chdir("..")
os.chdir("CSV")
# print(os.getcwd())
import csv
with open("playlist.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    playlist = list(reader)
    f.close()
playlist = [lst[0] for lst in playlist]
print(playlist)
