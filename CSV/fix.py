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
        last_part += 1
    elif len(lines[i].split(",")) == 2:
        lines[i] = lines[i][:-2]+",False"+lines[i][-2:]

for i in range(len(lines)):
    if i - 45 == last_index:
        lines = lines[:i] + [f"{last_part}-{last_part + 1},{last_part}-{last_part + 1},{last_part}-{last_part + 1}\r\n"] + lines[i:]
        last_index = i + 1
        last_part += 1

with open("downloaded_playlist.csv", "w", encoding="utf-8", newline="") as f:
    f.writelines(lines)