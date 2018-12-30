"""创建一个从单词到其出现情况的映射"""

import sys
import re

WORDE_RE = re.compile(r'\w+')

index = {}
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORDE_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            # 3.2
            # occurrences = index.get(word, [])
            # occurrences.append(location)
            # index[word] = occurrences

            # 3.3
            index.setdefault(word, []).append(location)

# 以字母顺序打印出结果
for word in sorted(index, key=str.upper):
    print(word, index[word])
