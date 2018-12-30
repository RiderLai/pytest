import os

for i in range(1000):
    os.system('nslookup -qt=TXT flag-id-'+str(i)+'.flag.src.edu-info.edu.cn. TXT')