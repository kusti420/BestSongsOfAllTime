from shutil import make_archive
import shutil
from zipfile import ZipFile
import os


with open("pathToMusic.txt", "r") as f:
    path = f.read()
    f.close()
folders = os.listdir(path)
os.chdir(path + "/zips")
print(os.getcwd())
for folder in folders:
    files = os.listdir(os.getcwd())
    # print(folder + ".zip" in files)
    if f"{folder}.zip" not in files and folder != "zips":
        make_archive(folder, "zip", path + folder)
        pass
    pass
