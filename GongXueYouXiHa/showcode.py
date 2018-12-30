from time import sleep
import sys
import code

with open('code.py') as file:
    lines = file.readlines()
    for line in lines:
        print(">>>", end='')
        for word in line:
            print(word, end='')
            sys.stdout.flush()
            sleep(0.2)

for s in ">>> hello_gongxue()":
    print(s, end='')
    sys.stdout.flush()
    sleep(0.2)

code.hello_gongxue()
