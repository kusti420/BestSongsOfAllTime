"""Renames files in a directory based on a regex."""
import re, os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("pathToMusic.txt", "r") as f:
    path = f.read()
    f.close()
folders = os.listdir(path)
a, b, c, d = r"\d_\d\d?\W?-\W", r"\d_\d\d?\W?_", r"_FLAC", r"\W\WFLAC\W"
for folder in folders:
    pattern_a, pattern_b, pattern_c, pattern_d = {}, {}, {}, {}
    files = os.listdir(path + folder)
    for file in files:
        if re.search(rf"{a}(.*)", file) != None:
            pattern_a[file] = re.search(rf"{a}(.*)", file).group(1)
        elif re.search(rf"{b}(.*)", file) != None:
            pattern_b[file] = re.search(rf"{b}(.*)", file).group(1)
    [os.rename(path + folder + "/" + k, path + folder + "/" + v) for k, v in pattern_a.items()]
    [os.rename(path + folder + "/" + k, path + folder + "/" + v) for k, v in pattern_b.items()]
    files = os.listdir(path + folder)
    for file in files:
        if re.search(rf"(.*){c}(.*)", file) != None:
            pattern_c[file] = re.search(rf"(.*){c}(.*)", file).group(1) + re.search(rf"(.*){c}(.*)", file).group(2)
        elif re.search(rf"(.*){d}(.*)", file) != None:
            pattern_d[file] = re.search(rf"(.*){d}(.*)", file).group(1) + re.search(rf"(.*){d}(.*)", file).group(2)
    [os.rename(path + folder + "/" + k, path + folder + "/" + v) for k, v in pattern_c.items()]
    [os.rename(path + folder + "/" + k, path + folder + "/" + v) for k, v in pattern_d.items()]
