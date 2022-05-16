"""Turns each folder into a separate zip file."""
from shutil import make_archive
import os

with open("pathToMusic.txt", "r") as f:
    path = f.read()
    f.close()
folders = os.listdir(path)
os.chdir(path + "/zips")
print(os.getcwd())
for folder in folders:
    files = os.listdir(os.getcwd())
    if f"{folder}.zip" not in files and folder != "zips":
        # make_archive(folder, "zip", path + folder)
        pass
    pass
