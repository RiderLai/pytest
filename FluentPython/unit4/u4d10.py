# open('test.txt', 'w', encoding='utf_8').write('4')
f1 = open('test.txt', 'r').read()
f2 = open('test.txt', 'r', encoding='cp1252')
print(f1)
print(f2)

import os

print(os.stat('test.txt').st_size)
