_time = []
cpu = []
with open('run100_1000.txt') as fp:
    i = 0
    while True:
        line = fp.readline()
        i += 1
        if line:
            if i % 9 == 8:
                cpu.append(line.split()[5])
            elif i % 9 == 1:
                _time.append(line.split()[2])
        else:
            break


for i in range(len(cpu)):
    print(_time[i] + ',' + str(int(cpu[i])/1000))
