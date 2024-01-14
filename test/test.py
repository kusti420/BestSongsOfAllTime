"""shift back if some songs removed from playlist"""
import os
# path = "K:\MEGAsync\Music\LosslessBest\Lossless"
# path = "K:\MEGAsync\Music\LosslessBest\Lossy"
def shift_back(path):
    files = os.listdir(path)
    if "desktop.ini" in files:
        files.remove("desktop.ini")

    # print(files)

    for file in files:
        index, file = int(file.split(".")[0]), file[len(str(int(file.split(".")[0]))) + 1:]
        # print(index, file)
        if index >= 4765 and index <= 5000:
            try:
                os.rename(f"{path}\{index}.{file}", f"{path}\{index - 1}.{file}")
                print(index)
            except:
                pass

shift_back(path = "K:\MEGAsync\Music\LosslessBest\Lossless")
shift_back(path = "K:\MEGAsync\Music\LosslessBest\Lossy")