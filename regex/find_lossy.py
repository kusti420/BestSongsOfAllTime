import os
with open("pathToMusic.txt", "r") as f:
    path = f.read()
    f.close()
folders = os.listdir(path)
os.chdir(path)

folders_with_lossy_files = set()
for folder in folders:
    if folder != "zips":
        files_in_folder = os.listdir(path + "/" + folder)
        for file in files_in_folder:
            if file.endswith(".mp3") or file.endswith(".m4a"):
                folders_with_lossy_files.add(folder)
folders_with_lossy_files = [f"part{part_nr}" for part_nr in sorted([int(folder[folder.index("t")+1:]) for folder in folders_with_lossy_files])]
print(*folders_with_lossy_files, sep='\n')
