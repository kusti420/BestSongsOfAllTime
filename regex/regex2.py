import re
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

beginning_rx = [
    r"\d_\d\d?\W?-\W",
    r"\d_\d\d?\W?_",
]

end_rx = [
    r"_FLAC",
    r"\W\WFLAC\W",
]

# replace matched part with ""


for filename in os.listdir():
    for rx in beginning_rx:
        if re.search(rx, filename):
            print(filename)
            os.rename(filename, re.sub(rx, "", filename))

for filename in os.listdir():
    for rx in end_rx:
        if re.search(rx, filename):
            print(filename)
            os.rename(filename, re.sub(rx, "", filename))
