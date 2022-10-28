import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
with open("pathToMusic.txt", "r") as f:
    path = f.read()
    f.close()
folders = os.listdir(path)
os.chdir(path)

folders_to_ignore = [
    "part1",
    "part2",
    "part3",
    "part5",
]

folders_with_lossy_files = set()
for folder in folders:
    if folder != "zips" and folder not in folders_to_ignore:
        files_in_folder = os.listdir(path + "/" + folder)
        for file in files_in_folder:
            if file.endswith(".mp3") or file.endswith(".m4a"):
                folders_with_lossy_files.add(folder)
folders_with_lossy_files = [f"part{part_nr}" for part_nr in sorted([int(folder[folder.index("part")+4:]) for folder in folders_with_lossy_files])]
print(*folders_with_lossy_files, sep='\n')
