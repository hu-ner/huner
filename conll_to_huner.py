import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input")
args = parser.parse_args()

f = open(args.input, 'r')

last = False
for line in f:
    line = line.strip()
    if 'DOCSTART' in line:
        continue
    if not line:
        if not last:
            print()
            last = True
    else:
        print(line.split()[-3] + " ", end="")
        last = False

