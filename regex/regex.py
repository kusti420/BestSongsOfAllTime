"""Renames files in a directory based on a regex."""
import re, os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open("pathToMusic.txt", "r") as f:
    path = f.read()
    f.close()
folders = os.listdir(path)
folders.remove("zips")
a = r"\d_\d\d?\W?-\W"
b = r"\d_\d\d?\W?_"
c = r"\d\d? - "
d = r"\d\d-"
e = r"\d_"

f = r"_FLAC"
g = r"\W\WFLAC\W"

def fix(filename):
    filename = filename.replace('"', "")
    filename = filename.replace("'", "")
    filename = filename.replace("–", "-")
    filename = filename.replace("—", "-")
    filename = filename.replace(",", '')
    filename = filename.replace("“", '')
    filename = filename.replace("”", '')
    filename = filename.replace("‘", '')
    filename = filename.replace("’", '')
    filename = filename.replace("「", '[')
    filename = filename.replace("」", ']')
    filename = filename.replace("『", '[')
    filename = filename.replace("』", ']')
    filename = filename.replace("（", '(')
    filename = filename.replace("）", ')')
    filename = filename.replace("［", '[')
    filename = filename.replace("］", ']')
    filename = filename.replace("｛", '{')
    filename = filename.replace("｝", '}')
    filename = filename.replace("／", '/')
    filename = filename.replace("＼", '\\')
    filename = filename.replace("．", '.')
    filename = filename.replace("，", ',')
    filename = filename.replace("：", ':')
    filename = filename.replace("；", ';')
    filename = filename.replace("？", '?')
    filename = filename.replace("！", '!')
    filename = filename.replace("＠", '@')
    filename = filename.replace("＃", '#')
    filename = filename.replace("＄", '$')
    filename = filename.replace("％", '%')
    filename = filename.replace("＆", '&')
    filename = filename.replace("＊", '*')
    filename = filename.replace("→", "-")
    filename = filename.replace("✕", '')
    filename = filename.replace("✓", '')
    filename = filename.replace("♫", '')
    filename = filename.replace("♪", '')
    filename = filename.replace("♩", '')
    filename = filename.replace("♬", '')
    filename = filename.replace("♭", '')
    filename = filename.replace("♮", '')
    filename = filename.replace("♯", '')
    filename = filename.replace("◉", '')
    filename = filename.replace("♛", '')
    filename = filename.replace("♥", '')
    filename = filename.replace("​", '')
    return filename

for folder in folders:
    pattern_a = {}
    pattern_b = {}
    pattern_c = {}
    pattern_d = {}
    pattern_e = {}
    
    pattern_f = {}
    pattern_g = {}
    files = os.listdir(path + folder)
    for file in files:
        os.rename(path + folder + '/' + file, path + folder + '/' + fix(file))
        if re.search(rf"{a}(.*)", file) != None:
            pattern_a[file] = re.search(rf"{a}(.*)", file).group(1)
        elif re.search(rf"{b}(.*)", file) != None:
            pattern_b[file] = re.search(rf"{b}(.*)", file).group(1)
        elif re.search(rf"{c}(.*)", file) != None:
            pattern_c[file] = re.search(rf"{c}(.*)", file).group(1)
        elif re.search(rf"{d}(.*)", file) != None:
            pattern_d[file] = re.search(rf"{d}(.*)", file).group(1)
        elif re.search(rf"{e}(.*)", file) != None:
            pattern_e[file] = re.search(rf"{e}(.*)", file).group(1)
    [os.rename(path + folder + "/" + k, path + folder + "/" + v) for k, v in pattern_a.items()]
    [os.rename(path + folder + "/" + k, path + folder + "/" + v) for k, v in pattern_b.items()]
    [os.rename(path + folder + "/" + k, path + folder + "/" + v) for k, v in pattern_c.items()]
    [os.rename(path + folder + "/" + k, path + folder + "/" + v) for k, v in pattern_d.items()]
    [os.rename(path + folder + "/" + k, path + folder + "/" + v) for k, v in pattern_e.items()]
    files = os.listdir(path + folder)
    for file in files:
        if re.search(rf"(.*){f}(.*)", file) != None:
            pattern_c[file] = re.search(rf"(.*){e}(.*)", file).group(1) + re.search(rf"(.*){e}(.*)", file).group(2)
        elif re.search(rf"(.*){g}(.*)", file) != None:
            pattern_d[file] = re.search(rf"(.*){f}(.*)", file).group(1) + re.search(rf"(.*){f}(.*)", file).group(2)
    [os.rename(path + folder + "/" + k, path + folder + "/" + v) for k, v in pattern_f.items()]
    [os.rename(path + folder + "/" + k, path + folder + "/" + v) for k, v in pattern_g.items()]
