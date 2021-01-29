import sys


x = sys.argv[2]
for i in range(10):
    i = i + 11
sys.stdout.writelines(x)
