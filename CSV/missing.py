import os
path = "K:\MEGAsync\Music\LosslessBest\Lossless"
path2 = "K:\MEGAsync\Music\LosslessBest\Lossy"

files = os.listdir(path)
files = [int(f.split(".")[0]) for f in files if f.split(".")[0].isdigit()]
# print(files)

files2 = os.listdir(path2)
files2 = [int(f.split(".")[0]) for f in files2 if f.split(".")[0].isdigit()]

not_in_list = []
for i in range(1, max(files)):
    if i not in files:
        if i not in files2:
            not_in_list.append(i)

print(not_in_list)