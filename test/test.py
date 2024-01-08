import os
files = os.listdir("K:\MEGAsync\Music\LosslessBest\sorted")
files.remove("desktop.ini")
print(files)

for file in files:
    index, file = int(file.split(".")[0]), file[len(str(int(file.split(".")[0]))) + 1:]
    # print(index, file)
    if index >= 4654 and index <= 4698:
        os.rename(f"K:\MEGAsync\Music\LosslessBest\sorted\{index}.{file}", f"K:\MEGAsync\Music\LosslessBest\sorted\{index - 1}.{file}")
        print(index)