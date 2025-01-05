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

# ignore numbers 0-456
for i in range(0, 549):
    if i in not_in_list:
        not_in_list.remove(i)

# remove digits 3801 - 5000
for i in range(3700, 5000):
    try:
        if i in not_in_list:
            not_in_list.remove(i)
    except:
        break

# single values to ignore
ignore = [806]
for i in ignore:
    if i in not_in_list:
        not_in_list.remove(i)
# print(not_in_list)
# print in a way where all elements are equal length making a perfect grid
# print("\n".join(["\t".join([str(i) for i in not_in_list[j:j+10]]) for j in range(0, len(not_in_list), 10)]))

def print_numbers_grid(numbers):
    # Create a set of the numbers for quick lookup
    numbers_set = set(numbers)

    # Iterate over the range of numbers 0 to 5000
    for start in range(0, 5001, 10):  # Step by tens to find the start of each line
        line = []

        # For each line, populate numbers or whitespace
        for i in range(start, start + 10):
            if i in numbers_set:
                line.append(str(i).rjust(4))  # Adjust ljust width for equal spacing
            else:
                line.append("-" * 4)

        # Join the line and print
        # if line is empty, don't print
        # print(" ".join(line))
        if line == ['----', '----', '----', '----', '----', '----', '----', '----', '----', '----']:
            continue
        # print()
        print("  ".join(line))
        # exit()

# Example usage
# numbers = [601, 602, 604, 605, 606, 607, 609]
print_numbers_grid(not_in_list)
