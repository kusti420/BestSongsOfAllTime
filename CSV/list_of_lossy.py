import os
import csv

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# find all lossy files and write them to a file

with open("../regex/pathToMusic.txt", "r", encoding="utf-8") as f:
    path = f.read().strip()

# find all lossy files (mp3, m4a, ogg)

files = []
for root, _, filenames in os.walk(path):
    for filename in filenames:
        if filename.endswith(".mp3") or filename.endswith(".m4a") or filename.endswith(".ogg"):
            files.append(os.path.join(root, filename))

# only keep the path after K:\MEGAsync\Music\LosslessBestSongsOfAllTime
files = [file.split("LosslessBestSongsOfAllTime\\")[1] for file in files]

# sort based on part number

print(files[200].split("part")[1].split("\\")[0])
# files.sort(key=lambda x: int(x.split("\\")[-2].split("part")[1]))
files.sort(key=lambda x: int(x.split("part")[1].split("\\")[0]))


# print(*files, sep="\n")

with open("list_of_lossy.csv", "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["path"])
    writer.writerows([[file] for file in files])

files = [file.split("\\")[1] for file in files]
files = [file.split(".")[0] for file in files]
print(*files, sep="\n")

