import random, sys
lines = open(sys.argv[1]).readlines()
for i in range(0, int(sys.argv[2])):
    sys.stdout.write(lines[random.randrange(len(lines))])
