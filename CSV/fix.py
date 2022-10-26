import os, re
os.chdir(os.path.dirname(os.path.realpath(__file__)))


with open("downloaded_playlist.csv", "r", encoding="utf-8", newline="") as f:
    lines = f.readlines()

# remove all empty lines
lines = [line for line in lines if line.strip() != ""]
# if line only consists of only one \d+-\d+ then turn it into match,match,match
last_index = 0
last_part = 0
for i in range(len(lines)):
    if re.match(r"\d+-\d+", lines[i]) and not re.match(r"\d+-\d+,\d+-\d+,\d+-\d+", lines[i]) and len(lines[i]) < 15:
        lines[i] = lines[i][:-2]+","+lines[i][:-2]+","+lines[i]
    elif re.match(r"\d+-\d+,\d+-\d+,\d+-\d+", lines[i]):
        last_index = i + 1
        last_part = int(lines[i].split(",")[0].split("-")[1])
    elif len(lines[i].split(",")) == 2:
        lines[i] = lines[i][:-2]+",False"+lines[i][-2:]
special_case = False
for i in range(len(lines)):
    try:
        # print(any([re.match(r"\d+-\d+,\d+-\d+,\d+-\d+", lines[j]) for j in range(i, i+20)]))
        if i - 45 >= last_index and any([re.match(r"\d+-\d+,\d+-\d+,\d+-\d+", lines[j]) for j in range(i, i+20)]):
            special_case = True
    except IndexError:
        break
    if i - 45 >= last_index and not special_case:
        lines = lines[:i] + [f"{last_part}-{last_part + 1},{last_part}-{last_part + 1},{last_part}-{last_part + 1}\r\n"] + lines[i:]
        last_index = i + 1
        last_part += 1
    if i - 45 >= last_index and special_case:
        if re.match(r"\d+-\d+,\d+-\d+,\d+-\d+", lines[i]):
            special_case = False

with open("downloaded_playlist.csv", "w", encoding="utf-8", newline="") as f:
    f.writelines(lines)