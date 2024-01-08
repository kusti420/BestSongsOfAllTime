import os
path = "K:\MEGAsync\Music\LosslessBest\sorted"

files = os.listdir(path)
files = [int(f.split(".")[0]) for f in files if f.split(".")[0].isdigit()]
# print(files)

not_in_list = []
for i in range(1, max(files)):
    if i not in files:
        not_in_list.append(i)
print(not_in_list)