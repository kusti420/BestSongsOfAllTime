from ast import pattern
import re
import os

with open("pathToMusic.txt", "r") as f:
    path = f.read()
    f.close()
folders = os.listdir(path)

a = r"\d_\d\d?\W?-\W"  # beginning of the file name
b = r"\d_\d\d?\W?_"  # beginning of the file name
c = r"_FLAC"  # end of the filename + file extension
d = r"\W\WFLAC\W"  # end of the filename + file extension
pattern_a, pattern_b, pattern_c, pattern_d = {}, {}, {}, {}

for folder in folders[-1:]:
    files = os.listdir(path + folder)
    for file in files:
        if re.search(rf"{a}(.*)", file) != None:
            pattern_a[file] = re.search(rf"{a}(.*)", file).group(1)
            
        if re.search(rf"{b}(.*)", file) != None:
            pattern_b[file] = re.search(rf"{b}(.*)", file).group(1)
    [os.rename(path + folder + "/" + k, path + folder + "/" + v) for k, v in pattern_a.items()]
    [os.rename(path + folder + "/" + k, path + folder + "/" + v) for k, v in pattern_b.items()]

for file in files:
    files = os.listdir(path + folder)
    for file in files:
        if re.search(rf"(.*){c}(.*)", file) != None:
            pattern_c[file] = re.search(rf"(.*){c}(.*)", file).group(1)
            
        if re.search(rf"(.*){d}(.*)", file) != None:
            pattern_d[file] = re.search(rf"(.*){d}(.*)", file).group(1)
    [os.rename(path + folder + "/" + k, path + folder + "/" + v) for k, v in pattern_c.items()]
    [os.rename(path + folder + "/" + k, path + folder + "/" + v) for k, v in pattern_d.items()]

if __name__ == "__main__":
    pass