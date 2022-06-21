"""Turns each folder into a separate zip file."""
from shutil import make_archive
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("pathToMusic.txt", "r") as f:
    path = f.read()
    f.close()
folders = os.listdir(path)
os.chdir(path + "/zips")
print(os.getcwd())
for folder in folders:
    files = os.listdir(os.getcwd())
    if f"{folder}.zip" not in files and folder != "zips":
        print(f"Creating {folder}.zip")
        make_archive(folder, "zip", path + folder)
        pass
    pass
