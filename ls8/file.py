import sys

if len(sys.argv) != 2:
    print("usage: file.py filename")
    sys.exit(1)

filename = sys.argv[1]

with open(filename) as f:
    for line in f:

        common_split = line.split("#")

        num = common_split[0].strip()

        if num == ' ':
            continue

        val = int(num)
